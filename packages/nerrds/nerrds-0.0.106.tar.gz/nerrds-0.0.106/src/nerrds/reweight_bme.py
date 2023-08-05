import sys
import os
import glob
import shutil
import json
import numpy as np
import re

from importlib import resources
from pdbtools import pdb_mkensemble
from nerrds.functions import check_quiet_print

with resources.path("nerrds.scripts.BME","BME.py") as f:
    BME_path = os.path.dirname(f)
sys.path.insert(1, BME_path)
import BME

natsort = lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\\d+)', s)] # used throughout to loop through files in natural order

def reweight_ensemble(home_dir,job_id,pdb_id,shifts_id,quiet=False):

    check_quiet_print(quiet,home_dir+'/'+job_id,"determining ensemble using BME")

    bme_dir = home_dir+"/"+job_id+"/bme/"
    os.makedirs(bme_dir,exist_ok=True)
    os.chdir(bme_dir)

    # collate ansurr output into data files for BME
    data = glob.glob(home_dir+"/"+job_id+"/ansurr/anm_"+pdb_id+"_refined_"+shifts_id+"/ANSURR_output/out/*.out")

    calc = []
    exp = []
    labels = []
    n=0
    for i in sorted(data,key=natsort):
        calc_tmp = []
        for line in open(i,'r'):
            if 'nan' not in line:
                line = line.split()
                if n==0:
                    exp.append([float(line[2]),0.05])
                    labels.append(line[0])   # do we need labels? probably yes because includes residue IDs actually used 
                    calc_tmp.append(float(line[3]))
                else:
                    calc_tmp.append(float(line[3]))
                    
        calc.append(calc_tmp)        
        n=1

    calc = np.array(calc)
    exp = np.array(exp)  

    out = open(bme_dir+"exp.txt",'w')
    # BME wants to know what kind of the data is being used so it knows how to average the data. JCOUPLINGS is just a simple mean - fine for comparing per residue flexibility
    out.write("# DATA=JCOUPLINGS\n")  
    i=0
    for e in exp:
        i+=1
        out.write(str(i)+' '+str(e[0])+' '+str(e[1])+'\n')
    out.close()

    j=0
    out = open(bme_dir+"calc.txt",'w')
    for e in calc:
        j+=1
        out.write(str(j)+' ')
        for i in e:
            out.write(str(i)+' ')
        out.write('\n')
    out.close()

    # define input file names
    exp_file = bme_dir+"exp.txt"
    calc_file = bme_dir+"calc.txt"

    # initialize. A name must be specified 
    rew = BME.Reweight("reweight_ANM")

    # load the experimental and calculated datasets
    rew.load(exp_file,calc_file)

    # 5-fold cross validation for 20 theta values
    thetas = np.geomspace(1,10000,20) # will this hold for everything?
    opt_theta = rew.theta_scan(thetas=thetas,nfold=5)

    # initialize. A name must be specified 
    rew = BME.Reweight("reweight_ANM_opt")

    # load the experimental and calculated datasets
    rew.load(exp_file,calc_file)

    # fit the data 
    chi2_before, chi2_after, phi = rew.fit(theta=opt_theta)

    # get weights
    weights = rew.get_weights()

    # copy chosen, named accoring to weight, and combined into a single file
    ensemble_dir = home_dir+"/"+job_id+"/ensemble/"
    os.makedirs(ensemble_dir,exist_ok=True)

    selected_models = [] # used later for plotting PCA
    selected_weights = [] # used later for plotting PCA

    with open(home_dir+"/"+job_id+"/refined/model_link.json") as json_file:
        model_link = json.load(json_file)

    mkensemble_string = []
    chosen_ensemble = {}
    for i in enumerate(weights):
        if i[1] > 0.01:   # have a cut off - need to have at least 1% weight
            #print(i[0]+1,round(i[1],2),model_link[str(i[0]+1)])
            chosen_ensemble[str(i[0]+1)] = {"weight":str(round(i[1],2)),"pdb":model_link[str(i[0]+1)]}
            shutil.copyfile(home_dir+"/"+job_id+"/refined/"+model_link[str(i[0]+1)].split('_refined.pdb')[0]+"/"+model_link[str(i[0]+1)],ensemble_dir+os.path.splitext(model_link[str(i[0]+1)])[0]+'_'+str(int(100*round(i[1],2)))+'.pdb')
            mkensemble_string.append(ensemble_dir+os.path.splitext(model_link[str(i[0]+1)])[0]+'_'+str(int(100*round(i[1],2)))+'.pdb')
            selected_models.append(i[0]+1)
            selected_weights.append(round(i[1],2))
            
    new_pdb = pdb_mkensemble.run(mkensemble_string)

    out = open(ensemble_dir+pdb_id+'_ensemble.pdb','w')
    for line in enumerate(new_pdb):
        out.write(line[1])
    out.close()

    if len(chosen_ensemble) > 0:
        check_quiet_print(quiet,home_dir+'/'+job_id,"determined an ensemble consisting of "+str(len(chosen_ensemble))+" models with the following weights:")
        max_pdb_name = []
        for i in chosen_ensemble:
            for pdb in chosen_ensemble[i]:
                max_pdb_name.append(int(len(pdb)))

        max_pdb_name ='{:>'+str(max(max_pdb_name))+'}'
        max_model_name = '{:>'+str(max([len(i) for i in chosen_ensemble]))+'}'

        for model in chosen_ensemble:
            check_quiet_print(quiet,home_dir+'/'+job_id," -> model "+model+" "+chosen_ensemble[model]["pdb"]+" "+chosen_ensemble[model]["weight"])
        check_quiet_print(quiet,home_dir+'/'+job_id,"the ensemble has been saved here: "+ensemble_dir+pdb_id+'_ensemble.pdb')
    else:
        check_quiet_print(quiet,home_dir+'/'+job_id,"BME failed to determine an ensemble, quitting")
        sys.exit(0)
        

if __name__ == "__main__":
    import sys,os,glob
    home_dir = sys.argv[1]
    job_id = sys.argv[2]
    pdb_id = sys.argv[3]
    shifts_id = sys.argv[4]
    reweight_ensemble(home_dir,job_id,pdb_id,shifts_id)
    
    # clean up after dag job
    delete_dag = glob.glob(home_dir+"/"+job_id+".dag*")
    for f in delete_dag:
        os.remove(f)
    delete_scripts = glob.glob(home_dir+"/"+job_id+"/*.py")
    for f in delete_scripts:
        os.remove(f)
    delete_jobs = glob.glob(home_dir+"/"+job_id+"*.sh")
    for f in delete_jobs:
        os.remove(f)
    delete_jobs = glob.glob(home_dir+"/"+job_id+"*.sub")
    for f in delete_jobs:
        os.remove(f)