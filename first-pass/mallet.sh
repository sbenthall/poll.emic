

#import data
mallet-2.0.6/bin/mallet import-file --input sample-data/tweets.txt --output twitter-topic-input.mallet --keep-sequence --remove-stopwords

#build topic model
mallet-2.0.6/bin/mallet train-topics --input twitter-topic-input.mallet --inferencer-filename inferencer.mallet --num-topics 10 --output-state topic-state.gz --optimize-interval 150

#test topic model by infering topics on data set
mallet-2.0.6/bin/mallet infer-topics --input twitter-topic-input.mallet --inferencer inferencer.mallet --output-doc-topics inferred-topics.1
