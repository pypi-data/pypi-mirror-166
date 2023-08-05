import sys
import os
import shutil
import subprocess
import glob 
import re
import json

from importlib import resources
from pdbtools import pdb_mkensemble
from nerrds.functions import check_quiet_print

natsort = lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\\d+)', s)] # used throughout to loop through files in natural order


def refine(home_dir, job_id, pdb, cpu, tleap, sander, sander_MPI, cpptraj, quiet=False):

    wd = home_dir+'/'+job_id+'/refined/'+os.path.splitext(os.path.basename(pdb))[0] # make dir to run refinement in
    os.makedirs(wd,exist_ok=True)

    with resources.path("nerrds.scripts.AMBER", "leap.in") as f:
        leap_script = f
    with resources.path("nerrds.scripts.AMBER", "min.in") as f:
        min_script = f
    with resources.path("nerrds.scripts.AMBER", "min_solv.in") as f:
        min_solv_script = f
    with resources.path("nerrds.scripts.AMBER", "extract_pdb.cpptraj") as f:
        cpptraj_script = f

    shutil.copyfile(leap_script, wd+"/leap.in") # copy various refinement scripts into wd
    shutil.copyfile(min_script, wd+"/min.in")  
    shutil.copyfile(min_solv_script, wd+"/min_solv.in")
    shutil.copyfile(pdb, wd+'/prot_for_min.tmp') # pdb is renamed to generic name referred to in refinement scripts, will be renamed after

    os.chdir(wd)

    out = open("prot_for_min.pdb","w")
    for line in open("prot_for_min.tmp","r"):
        if "OT" not in line:
            out.write(line)
    out.close()
    os.remove("prot_for_min.tmp")

    run_tleap = subprocess.run([tleap, "-f", "leap.in"],stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))

    if int(cpu)==1:  
        check_quiet_print(quiet,home_dir+'/'+job_id,"refining "+pdb+" with 1 cpu using sander")
        run_amber = subprocess.run([sander, "-i", "min_solv.in", "-o", "min_solv.out", "-p", "prot_solv.parm7", "-c", "prot_solv.rst7", "-r", "prot_min_solv.rst7", "-x", "prot_min_solv.nc", "-ref", "prot_solv.rst7", "-O"],stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
        run_amber = subprocess.run([sander, "-i", "min.in", "-o", "min.out", "-p", "prot_solv.parm7", "-c", "prot_min_solv.rst7", "-r", "prot_min.rst7", "-x", "prot_min.nc", "-O"],stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
    elif int(cpu) > 1:
        check_quiet_print(quiet,home_dir+'/'+job_id,"refining "+pdb+" with "+str(cpu)+" cpus using sander.MPI")
        run_amber = subprocess.run(["mpirun", "-np", str(cpu), sander_MPI, "-i", "min_solv.in", "-o", "min_solv.out", "-p", "prot_solv.parm7", "-c", "prot_solv.rst7", "-r", "prot_min_solv.rst7", "-x", "prot_min_solv.nc", "-ref", "prot_solv.rst7", "-O"],stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
        run_amber = subprocess.run(["mpirun", "-np", str(cpu), sander_MPI, "-i", "min.in", "-o", "min.out", "-p", "prot_solv.parm7", "-c", "prot_min_solv.rst7", "-r", "prot_min.rst7", "-x", "prot_min.nc", "-O"],stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))

    if os.path.exists("prot_min.nc"):
        run_cpptraj = subprocess.run([cpptraj, "-i", cpptraj_script],stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
        if os.path.exists("prot_min.pdb"): # sometimes cpptraj fails
            shutil.copyfile('prot_min.pdb',wd.split('/')[-1]+'_refined.pdb')
            os.remove('prot_min.pdb') 

    
    # remove traj - way too much space
    to_remove = glob.glob("*.nc")
    for t in to_remove:
        os.remove(t)
    to_remove = glob.glob("*.parm7")
    for t in to_remove:
        os.remove(t)
    to_remove = glob.glob("*.rst7")
    for t in to_remove:
        os.remove(t)
    to_remove = glob.glob("*.in")
    for t in to_remove:
        os.remove(t)

    os.remove("prot_for_min.pdb")
    os.chdir(home_dir)


def combine(home_dir, job_id, pdb_id,quiet=False):
    os.chdir(home_dir)

    # remove traj data for failures

    to_remove = glob.glob(home_dir+'/'+job_id+'/refined/anm*/*.nc')
    for t in to_remove:
        os.remove(t)
    to_remove = glob.glob(home_dir+'/'+job_id+'/refined/anm*/*.parm7')
    for t in to_remove:
        os.remove(t)
    to_remove = glob.glob(home_dir+'/'+job_id+'/refined/anm*/*.rst7')
    for t in to_remove:
        os.remove(t)
    to_remove = glob.glob(home_dir+'/'+job_id+'/refined/anm*/*.in')
    for t in to_remove:
        os.remove(t)


    mkensemble_string = []
    refined_pdbs = 0
    for pdb in sorted(glob.glob(home_dir+'/'+job_id+"/refined/anm_"+pdb_id+"_*/anm_"+pdb_id+"_*_refined.pdb"),key=natsort):
        fail=0
        for i in open(pdb,'r').readlines():  # remove the structures which blew up i.e. have coords with "***"
            if "*" in i:
                fail=1
        if fail == 0:
            mkensemble_string.append(pdb)
            refined_pdbs +=1

    new_pdb = pdb_mkensemble.run(mkensemble_string)

    out = open(home_dir+"/"+job_id+"/refined/anm_"+pdb_id+"_refined.tmp",'w')
    for line in enumerate(new_pdb):
        out.write(line[1])
    out.close()

    # rename HIE, HID to HIS, Amber uses HIE and HID which is not recognised by ANSURR
    out = open(home_dir+"/"+job_id+"/refined/anm_"+pdb_id+"_refined.pdb",'w')   
    for line in open(home_dir+"/"+job_id+"/refined/anm_"+pdb_id+"_refined.tmp",'r'):
        out.write(line.replace('HIE','HIS').replace('HID','HIS'))
    out.close()

    os.remove(home_dir+"/"+job_id+"/refined/anm_"+pdb_id+"_refined.tmp")

    # read REMARKs in combined file to generate dictionary which links model number to the name of the PDB

    model_link = {}
    for line in open(home_dir+"/"+job_id+"/refined/anm_"+pdb_id+"_refined.pdb",'r'):
        line = line.split()
        if line[0] == 'REMARK':
            model_link[str(line[2])] = line[4]
            
    with open(home_dir+"/"+job_id+"/refined/model_link.json", "w") as outfile:
        json.dump(model_link, outfile)


    # check refinement success
    if refined_pdbs > 0:
        check_quiet_print(quiet,home_dir+'/'+job_id,"sucessfully refined "+str(refined_pdbs)+" models")
    else:
        check_quiet_print(quiet,home_dir+'/'+job_id,"ERROR failed to refine any models, quitting")
        sys.exit(0)





if __name__ == "__main__":
    import sys
    mode = sys.argv[1] # why do I do this to myself?

    if mode == 'refine':
        home_dir = sys.argv[2]
        job_id = sys.argv[3]
        pdb = sys.argv[4]
        cpu = sys.argv[5]
        tleap = sys.argv[6]
        sander = sys.argv[7]
        sander_MPI = sys.argv[8]
        cpptraj = sys.argv[9]
        refine(home_dir, job_id, pdb, cpu, tleap, sander, sander_MPI, cpptraj)
    elif mode == 'combine':
        home_dir = sys.argv[2]
        job_id = sys.argv[3]
        pdb_id = sys.argv[4]
        combine(home_dir, job_id, pdb_id)
