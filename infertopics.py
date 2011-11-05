import os
from settings import *

MALLET = "mallet-2.0.6/bin/mallet "

def import_file():
    cmd = MALLET + "import-file "
    cmd += "--input %s " % (DUMP_FILE)
    cmd += "--output %s " % (MALLET_INPUT_FILE)
    cmd += "--keep-sequence --remove-stopwords"
    os.system(cmd)

def train_topics():
    cmd = MALLET + "train-topics "
    cmd += "--input %s " % (MALLET_INPUT_FILE)
    cmd += "--inferencer-filename %s " % (INFERENCER_FILE)
    cmd += "--num-topics %d " % (NUM_TOPICS)
    cmd += "--output-state %s " % (OUTPUT_STATE)
    cmd += "--optimize-interval %d " % (OPTIMIZE_INTERVAL)
    os.system(cmd)

def infer_topics():
    cmd = MALLET + "infer-topics "
    cmd += "--input %s " % (MALLET_INPUT_FILE)
    cmd += "--inferencer %s " % (INFERENCER_FILE)
    cmd += "--output-doc-topics %s " % (INFERRED_FILE)



import_file()
train_topics()
infer_topics()
