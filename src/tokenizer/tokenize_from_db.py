from typing import Generator
import psycopg2
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from string import punctuation
from nltk.corpus import stopwords
from sqlalchemy import create_engine, text
from config import FSTR_DB_LOGIN, FSTR_DB_PASS, FSTR_DB_HOST, FSTR_DB_PORT, FSTR_DB_NAME


def get_clear_tokens(text) -> str:
    tokens = nltk.tokenize.word_tokenize(text.lower())
    wnl = nltk.stem.WordNetLemmatizer()
    tokens_ = (wnl.lemmatize(token) for token in tokens if check_conditions(wnl.lemmatize(token)))
    return " ".join(tokens_)


def check_conditions(lemmatized_token: str) -> bool:
    words_to_avoid = set(stopwords.words("russian") + stopwords.words("english") + list(punctuation))
    bool_ = all([lemmatized_token not in words_to_avoid,
                nltk.pos_tag([lemmatized_token])[0][1] == "NN"])
    return bool_


def vectorize(tokens: pd.DataFrame) -> pd.DataFrame:
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt')
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
                          index=list(range(1, tokens.shape[0] + 1)))
    return matrix


def write_to_db(df: pd.DataFrame, engine):
    with engine.connect() as cur:
        for idx in df.index:
            res_ = df.loc[idx, :].reset_index().sort_values(by=[idx, 'index'], ascending=False)
            res = " ".join(res_["index"].iloc[:20].values)
            params = ({"ml_key_words": res, "id": idx})
            cur.execute(text(f"""
            UPDATE article
            SET ml_key_words = :ml_key_words
            WHERE id = :id"""), params)
            cur.commit()


def main():
    engine = create_engine(
        f'postgresql+psycopg2://{FSTR_DB_LOGIN}:{FSTR_DB_PASS}@{FSTR_DB_HOST}:{FSTR_DB_PORT}/{FSTR_DB_NAME}')
    df = pd.read_sql_query("""SELECT id, full_text FROM article""", index_col="id", con=engine)
    df["tokenized_text"] = df["full_text"].apply(get_clear_tokens)
    m = vectorize(df["tokenized_text"].values)
    write_to_db(m, engine=engine)


if __name__ == "__main__":
    main()
