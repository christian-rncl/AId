'''
Config file for crawler
'''
DSET_NAME = 'Xcharity.ai/' #format: /name/
CLASSES_COUNT = {"clothes": 200, "food": 100, "junk_food" : 50, "chips_junk_food" : 50,
"bottled_water" : 200, "tables" : 50, "chairs" : 50, "floor": 50, "carpeted_floor" : 50, "lecture_hall" : 50} # class:count 
GCS_BASE = "gs://glossy-motif-231903-vcm/"
CSV_FNAME = "labels.csv"
DELETE_AFTER = True