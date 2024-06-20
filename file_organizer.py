import os, sys, shutil

import argparse


def main():
    
    parser = get_parser()
    args = parser.parse_args()
    folder=args.folder
    
    
    
    # if present, delete __MACOSX
    shutil.rmtree(folder+'/'+subfolder+'/__MACOSX', ignore_errors=True)
    
    files=os.listdir(folder+'/'+subfolder)
    for file in files:
        new_name=name_changer(file)
        os.rename(folder+'/'+subfolder+'/'+file, folder+'/'+subfolder+'/'+new_name)
        
    
    
    
def get_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--folder', '-f', dest='folder',
                    help='the folder to be organized are')
    return parser    

def name_changer(file_name):
    # get the words divided by underscores
    aux=file_name.split('_')
    # get the year from the word made by digit
    year=[a for a in aux if a.isdigit()]
    if len(year)>0:
        year=year[0]
        # it may happen that there are just two entries in the year input
        if len(year)==2:
            year='20'+year
        new_name='_'.join([a for a in aux if not a.isdigit()])
    else:
        # the year may be hidden in a year+char word
        hidden_year=[]
        new_entries=[]
        for a in aux:
            hy=[_ for _ in a if _.isdigit()]
            if len(hy)>0:
                hy=''.join(hy)
                hidden_year.append(hy)
                # the part of the name that does not contain an integer
                other_part=[_ for _ in a if not _.isdigit()]
                other_part=''.join(other_part)
                new_entries.append(other_part)
            else:
                new_entries.append(a)
        if len(hidden_year)==1:
            year=hidden_year[0]
            if len(year)==2:
                year='20'+year
            new_name='_'.join(new_entries)
        else:
            return 1
    
    return year+'_'+new_name

if __name__ == "__main__":
    main()   
        