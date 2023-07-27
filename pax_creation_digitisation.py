# This Script is for Creating Multi-Representation PAX files from the Digitistion files produced by Townsweb, for ingest into Preservica.
# This was so that the OCR's produced by Townsweb were represented in the Archive.

# The scirpt is 'hardcoded' for a Structure that resembles:
# ---Top-Level/
# ------PDF/
# ------Tiff

# This is possibly a basis for a more advanced system of creating PAX's for Ingest 
# Hard coded Elements: root_path, logic for selecting Preservation (In a Folder PDF or Tiff) -- how to make this Dynamic? 


import os
import shutil
import zipfile
from time import sleep
import argparse

parser = argparse.ArgumentParser(description="PAX Generator for Preservica Uploads - Specifically for Digitisation")
parser.add_argument("-i","--input",required=True, nargs='?',default=os.getcwd())
parser.add_argument("-o","--output",required=False, nargs='?')
parser.add_argument("-f","--filter",required=False,nargs="+")
args = parser.parse_args()

root_path = args.input
if not args.output: 
    dest_root = args.input
else: dest_root = args.output

filterlist = args.filter

if not os.path.exists(dest_root):
    os.makedirs(dest_root)

def file_detect(dir):
    with os.scandir(dir) as scan:
        file_flag = False
        for f in scan:
            if os.path.isfile(f): file_flag = True
            else: file_flag = False
    return file_flag

def structure_create_dir(dir, flag):
    basename = os.path.basename(dir)
    if flag == "Access": representation = "Representation_Access"
    elif flag == "Pres": representation = "Representation_Preservation"
    dest_path = os.path.join(dest_root,"PAX",basename,representation)
    if not os.path.exists(dest_path): os.makedirs(dest_path)
    for file in os.listdir(dir):
        file = os.path.join(dir,file)
        shutil.copy2(file,dest_path)
        shutil.make_archive(dest_path,'zip',file)

def create_pax_folder(dest_root):
    if os.path.exists(os.path.join(dest_root,"PAX")):
        pass
    else: os.makedirs(os.path.join(dest_root,"PAX"))

def structure_create_zip(dir, flag):
    dir_basename = os.path.basename(dir)
    if flag == "Access": representation = "Representation_Access"
    elif flag == "Pres": representation = "Representation_Preservation"
    for file in os.listdir(dir):
        file_path = os.path.join(dir,file)
        file_basename = os.path.splitext(file)[0]        
        if rep_flag == "Access":
            dest_zip = os.path.join(dest_root,"PAX",file_basename + '.pax.zip')
        else:
            dest_zip = os.path.join(dest_root,"PAX", dir_basename + '.pax.zip') 
        file_zip = representation + "/" + file
        if os.path.exists(dest_zip):
            zip_mode = 'a'
        else: 
            zip_mode = 'w'
        zip = zipfile.ZipFile(dest_zip,zip_mode)
        print(f'Zipping File: {file_path} to PAX: {dest_zip}')
        try: 
            zip.write(file_path, file_zip)
            zip.close()
        except Exception as e: print(e)

def dir_loop(dir):
    file_flag = file_detect(dir)
    if not file_flag:
        print('No files')
    else:
        if filterlist:
            print(f'Filtering enabled: filtering for {filterlist}')
            if filterlist in dir:
                print('Filtered Match')
                structure_create_zip(dir,rep_flag)
            else: 'Print override set passing'
        else:
            print(f'Filtering disabled: processing all')
            structure_create_zip(dir,rep_flag)
    for d in os.listdir(dir):
        npath = os.path.join(dir,d)
        if os.path.isdir(npath):
            dir_loop(npath)
        if os.path.isfile(npath):
            pass
            #print(os.pardir(npath))

if __name__ == "__main__":
    # file = r"D:\HD039 Townsweb\Leverhulme Batch 4\PAX\GB1752.LBC-213-1.pax.zip"
    # info = zipfile.ZipFile(file)
    # with zipfile.ZipFile(file,mode='r') as archive:
    #     archive.printdir()
    os.chdir(root_path)
    create_pax_folder(dest_root)
    for dir in os.listdir(root_path):
        print(f'Processing {dir}')
        if "Tiff" in dir:
            rep_flag = "Pres"
            dir = os.path.join(root_path,dir)
            dir_loop(dir)
        elif "PDF" in dir:
            rep_flag = "Access"
            dir = os.path.join(root_path,dir)
            dir_loop(dir)