'''
Crawls images for args and creates a csv label file
prepares data for automl
author: Christian Roncal 2/16/2019
'''
from icrawler.builtin import GoogleImageCrawler
import pandas as pd
import subprocess
import os
import shutil

from config import *

def ensure_dir(dirname):
    if(not os.path.isdir(dirname)):
        os.mkdir('./'+dirname)

def mk_classdirs():
    for c in CLASSES_COUNT.keys():
       ensure_dir(c) #maybe use format strings 

#makes datasets and crawls images
def crawl():
    mk_classdirs()

    for imgclass, count in CLASSES_COUNT.items():
        google_crawler = GoogleImageCrawler(storage={'root_dir': imgclass})
        google_crawler.crawl(keyword=imgclass, max_num=count)

# uploads to gcloud storage
def upload_gs():
    for label in CLASSES_COUNT:
        dir_name = '/'+label
        print('executing: ', 'gsutil -m cp -r ' + label + " " + GCS_BASE + DSET_NAME)
        os.system('gsutil -m cp -r ' + label + " " + GCS_BASE  + DSET_NAME)

'''
uploads dset to GCS_BASE, creates uploads csv
'''
def make_csv():
    data_dirs = next(os.walk('.'))[1] # class directories
    img_files = [os.listdir(f) for f in data_dirs]
    data_dict = dict(zip(data_dirs, img_files)) # {label: img.jpg}
    data_array = []

    for label in data_dict.keys():
        gcs_folder = label

        for fname in data_dict[label]:
            
            if label == 'junk_food' or label == 'chips_junk_food':
                label = 'food'
            elif(label == 'tables' or label == 'chairs' or label == 'floor' or label == 'carpeted_floor' or label == 'lecture_hall'):
                label = 'other'

            #fname = label+fname if label == 'junk_food' or label == 'chips_junk_food' else fname
            label = 'food' if label == 'junk_food' or label == 'chips_junk_food' else label
            data_array.append((GCS_BASE + DSET_NAME + gcs_folder + "/" + fname, label))

    df = pd.DataFrame(data_array)
    df.to_csv(CSV_FNAME, index=False, header=False)

    print("uploading: ", 'gsutil -m cp -r ' + CSV_FNAME + " " + GCS_BASE  + DSET_NAME)
    os.system('gsutil cp ' + CSV_FNAME + " " + GCS_BASE + DSET_NAME)

if __name__ == "__main__":
    crawl()
    upload_gs()
    make_csv()
    print("csv link: ", GCS_BASE + DSET_NAME + CSV_FNAME)

    if DELETE_AFTER:
        for k in CLASSES_COUNT.keys():
            shutil.rmtree('./'+k)
        os.remove('./'+CSV_FNAME)

