import os, sys
import zipfile
from tqdm.autonotebook import trange, tqdm

import argparse

def get_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--folder', '-f', dest='folder',
                    help='the folder where the files to unzip are')

    return parser

def unzipper(folder, file_to_unzip):
        
    # properly define the folder to store the unzipped stuff
    # take the extension of file out
    out_folder_file=file_to_unzip.split('.')[0]
    # take the 'summaries' text out
    out_folder_file=out_folder_file.split('_')[:-1]
    # get two indices for the number at the beginning of the string
    ordering=str(int(out_folder_file[0])).zfill(2)
    # rebuilt the string without the first number
    out_folder_file='_'.join(out_folder_file[1:])
    # replace blanks with underscores
    out_folder_file=out_folder_file.replace(' ', '_')
    # add the number
    out_folder_file=ordering+'_'+out_folder_file
    
    # final folder name
    fifo_name=folder+out_folder_file
    
    # create the folder
    if not os.path.exists(fifo_name):
        os.makedirs(fifo_name)
    else:
        counter=0
        new_name=fifo_name+'_'+str(counter)
        while os.path.exists(fifo_name):
            counter+=1
            new_name=fifo_name+'_'+str(counter)
            
        fifo_name=new_name
        

    # unzip all files in the folder
    with zipfile.ZipFile(folder+file_to_unzip, 'r') as zip_ref:
        zip_ref.extractall(fifo_name)
        
    # delete the zip file
    os.remove(folder+file_to_unzip)
    
    
def main():
    # unzip all zip files
    
    parser = get_parser()
    args = parser.parse_args()
    folder=args.folder
    
    files=[file for file in os.listdir(folder) if file.endswith('.zip')]
    
    files.sort()
    
    for file in tqdm(files):
        unzipper(folder, file)
        
    
        
if __name__ == "__main__":
    main()    