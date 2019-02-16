'''
Config file for crawler
'''
DSET_NAME = 'Xcharity.ai/' #format: /name/
CLASSES_COUNT = {"clothes": 150, "food": 100, "junk_food" : 50, "chips_junk_food" : 50,
"bottled_water" : 150} # class:count 
GCS_BASE = "gs://glossy-motif-231903-vcm/"
CSV_FNAME = "labels.csv"
