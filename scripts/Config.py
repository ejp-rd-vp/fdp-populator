import os
import glob

print("Files from the parent dir : " + str(glob.glob("../*")))

FDP_URL = os.environ['FDP_URL']
FDP_USERNAME = os.environ['FDP_USERNAME']
FDP_PASSWORD = os.environ['FDP_PASSWORD']
FDP_PERSISTENT_URL = os.environ['FDP_PERSISTENT_URL']
INPUT_FILE = "../catalogs.csv"