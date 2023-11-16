import os
from typing import Generator, Any
import re
import json
import nltk
from nltk.corpus import stopwords
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from pprint import pprint

# nltk.download('averaged_perceptron_tagger')
words_to_avoid = set(stopwords.words("russian") + list(punctuation))


def get_clear_tokens(text) -> str:
    tokens = nltk.tokenize.word_tokenize(text.lower())
    wnl = nltk.stem.WordNetLemmatizer()
    tokens_ = (wnl.lemmatize(token) for token in tokens if check_conditions(wnl.lemmatize(token)))
    return " ".join(tokens_)


def check_conditions(lemmatized_token: str) -> bool:
    bool_ = all([lemmatized_token not in words_to_avoid,
                nltk.pos_tag([lemmatized_token])[0][1] == "NN"])
    return bool_


def vectorize(tokens: Generator, names: list) -> pd.DataFrame:
    vectorizer = TfidfVectorizer(input='content',
                                 use_idf=True,
                                 lowercase=True,
                                 analyzer='word',
                                 ngram_range=(1, 2),
                                 stop_words=None,
                                 vocabulary=None)
    tfidf_matrix = vectorizer.fit_transform(tokens)
    terms = vectorizer.get_feature_names_out()
    matrix = pd.DataFrame(tfidf_matrix.toarray(),
                          columns=terms,
                          index=names)
    return matrix


def write_keywords(df: pd.DataFrame, names: list):
    for name in names:
        with open(f"key_words/key_words_{name[:50]}.txt", "a") as f:
            # print(name, ":")
            res_ = df.loc[name, :].reset_index().sort_values(by=[name, 'index'], ascending=False)
            res = res_["index"].iloc[:20].values
            # print(" ".join(res), end='\n\n')
            print(" ".join(res), file=f, flush=True)


if __name__ == "__main__":
    with open("../../parse_news/fontanka.json", "r") as f:
        data = json.load(f)
        titles = [news.get('title') for news in data]
        full_texts = [news.get('full_text') for news in data]
        lemmatized_tokens = (get_clear_tokens(text) for text in full_texts)
        df = vectorize(lemmatized_tokens, titles)
        write_keywords(df, titles)
