import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from string import punctuation
from nltk.corpus import stopwords
from sqlalchemy import create_engine, text
from .config import FSTR_DB_LOGIN, FSTR_DB_PASS, FSTR_DB_HOST, FSTR_DB_PORT, FSTR_DB_NAME
# from typing import Generator
# import psycopg2


def get_clear_tokens(text) -> str:
    tokens = nltk.tokenize.word_tokenize(text.lower())
    wnl = nltk.stem.WordNetLemmatizer()
    tokens_ = (wnl.lemmatize(token) for token in tokens if check_conditions(wnl.lemmatize(token)))
    return " ".join(tokens_)


def check_conditions(lemmatized_token: str) -> bool:
    words_to_avoid = set(stopwords.words("russian") + stopwords.words("english") + list(punctuation))
    bool_ = all((lemmatized_token not in words_to_avoid, nltk.pos_tag([lemmatized_token])[0][1] == "NN"))
    return bool_


def vectorize(tokens: pd.DataFrame, names: np.array) -> pd.DataFrame:
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')
    vectorizer = TfidfVectorizer(input='content',
                                 use_idf=True,
                                 lowercase=True,
                                 analyzer='word',
                                 ngram_range=(1, 1),
                                 stop_words=None,
                                 vocabulary=None)
    tfidf_matrix = vectorizer.fit_transform(tokens)
    terms = vectorizer.get_feature_names_out()
    matrix = pd.DataFrame(tfidf_matrix.toarray(),
                          columns=terms,
                          index=names)
    print("DF with vectorized 'tokenized_text' created", "OK")
    return matrix


def write_to_db(df: pd.DataFrame, engine):
    for idx in df.index:
        with engine.connect() as cur:
            res_ = df.loc[idx, :].reset_index().sort_values(by=[idx, 'index'], ascending=False)
            res = " ".join(res_["index"].iloc[:20].values)
            params = ({"ml_key_words": res, "id": idx})
            cur.execute(text(f"""
            UPDATE article
            SET ml_key_words = :ml_key_words
            WHERE :id = article.id 
            RETURNING article.id, :id"""), params)
            cur.commit()
    print("Words written to DB", "OK")


def main():
    engine = create_engine(
        f'postgresql+psycopg2://{FSTR_DB_LOGIN}:{FSTR_DB_PASS}@{FSTR_DB_HOST}:{FSTR_DB_PORT}/{FSTR_DB_NAME}')
    print("DB engine created", "OK")
    df = pd.read_sql_query("""SELECT id, full_text FROM article WHERE ml_key_words IS NULL""", con=engine)
    print("DB data loaded", "OK")
    df["tokenized_text"] = df["full_text"].apply(get_clear_tokens)
    print("DF column 'tokenized_text' created", "OK")
    mtrx = vectorize(df["tokenized_text"].values, names=df["id"].values)
    write_to_db(mtrx, engine=engine)


if __name__ == "__main__":
    main()
