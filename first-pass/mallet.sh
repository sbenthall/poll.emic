

#import data
mallet-2.0.6/bin/mallet import-file --input sample-data/tweets.txt --output twitter-topic-input.mallet --keep-sequence --remove-stopwords

#build topic model
mallet-2.0.6/bin/mallet train-topics --input twitter-topic-input.mallet --num-topics 100 --output-state topic-state.gz --optimize-interval 100
