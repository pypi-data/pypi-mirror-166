# NLP Classification Python Package For Profile Category and NER

## Functionality of the Package

Performs Classification using Regex for social media user's profile categorization and NER tasks
1. If profile:
    * Categories: Politician, Information Vehicule, Health Professional, Science, Education Professional, Artist, Organization and Journalist;
2. NER: 
    * Vaccines, Products, Drugs, Diseases, Symptoms, Science, Part of the body; returns a dataframe that has information of the entity id, name and it's occurence frequency on the input text.


## The package takes the following parameters as input:

1. Profile: 
    * Text containing informations about the user's biography or channel description in the context of communication reaseach porpuses
2. NER: 
    * Text

## Usage

´pip install nlpclassifier´

### Example

´´´
from nlpclassifier_profilener import NLPClassifier

#instatiate the classifier
tpc = TwitterProfileClassifier('profile')
#preprocess the text. Its's important to lowercase and remove accents
yt['channelDesc'] = yt['channelDesc'].apply(lambda x: pipeline.preprocess(x, lower = True)).apply(lambda x: pipeline.strip_accents(x))
#classify channelCategory
yt['channelCategory'] = yt['channelDesc'].apply(lambda x: tpc.classifier(str(x)))

yt['channelCategory'].value_counts()

´´´ 
### Note
The package is currently in a very elementary stage and work is in progress.
In case of error, feel free to contact me.