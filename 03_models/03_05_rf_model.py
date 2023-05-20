import pickle
import argparse
from joblib import load

import pandas as pd


parser = argparse.ArgumentParser(description='model_input')

parser.add_argument(
    '--input',
    type=str,
    required=True,
    help='Model input'
)

args = parser.parse_args()

data = {'text' : [args.input]}

df = pd.DataFrame(data=data)

phrases = []

with open('..\data\suspicious_phrases.txt') as f:
    for line in f.readlines():
        phrases.append(line.strip())

df['is_suspicious'] = df['text'].apply(lambda x : 1 if any([phrase in x for phrase in phrases]) else 0)

print(df)

tfidf = pickle.load(open("..\\03_models\TFIDF_serialized.pickle", 'rb'))
data = pd.DataFrame(tfidf.transform(df['text']).todense(), columns = tfidf.get_feature_names_out()).astype('float32')
data


clf = load('..\\03_models\\random_forest_model.joblib')

X = data
X['is_suspicious'] = df['is_suspicious']

pred = clf.predict(X)
print(pred)