import os
import sys

PROJECT_PATH = os.getcwd() #run test from top folder.
SOURCE_PATH = os.path.join(
    PROJECT_PATH, "src"
)
sys.path.append(SOURCE_PATH)

#Since we have test dir parallel to src, just add it as syspath.