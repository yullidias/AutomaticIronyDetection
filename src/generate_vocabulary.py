# -*- coding: utf-8 -*-
import src.utils.constants as cns
from src.utils.files import write_obj
from src.utils.files import read_obj
from src.preprocess import tokenize_text
from src.preprocess import remove_irrelevant_punctuation

import pandas as pd
import argparse
from sklearn.feature_extraction.text import CountVectorizer
from datetime import datetime


def get_feature_names(bow_ngram):
    if bow_ngram:
        vectorizer = read_obj(cns.V_BOW_NGRAM)
    else:
        vectorizer = read_obj(cns.V_BOW)
    return vectorizer.get_feature_names()


def get_features(raw_documents, bow_ngram):
    if bow_ngram:
        vectorizer = read_obj(cns.V_BOW_NGRAM)
    else:
        vectorizer = read_obj(cns.V_BOW)
    return vectorizer.transform(raw_documents)


def log_len(log_filename, bow_ngram, vectorizer, desc):
    with open(log_filename, "a") as f:
        repr_str = "[BOW+Ngram]" if bow_ngram else "[BOW]"
        msg = f"N features: {len(vectorizer.vocabulary_)} {repr_str}"
        print(msg)
        f.write(f"{datetime.now().isoformat()} - {desc} - {msg}  \n")


def generate(bow_ngram, target_vocab, description, tokenizer,
             path_vocab=cns.D_PREPROCESS,
             log_filename=cns.PATH_ANALYSIS_VOCABULARY+'len_vocab.txt'):
    print("Generate vocabulary ...")
    vocab_df = pd.read_excel(path_vocab, index_col=0)
    vectorizer = CountVectorizer(lowercase=False,
                                 tokenizer=tokenizer,
                                 ngram_range=(1, 3) if bow_ngram else (1, 1))
    vectorizer.fit(vocab_df["text"])
    log_len(log_filename, bow_ngram, vectorizer, description)
    write_obj(target_vocab, vectorizer)
    return vectorizer


def generate_vocabs(description, tokenizer):
    if tokenizer == cns.TOKENIZE_TEXT:
        choosed_tokenize = tokenize_text
    elif tokenizer == cns.TOKENIZE_PUNCTUANTION:
        choosed_tokenize = remove_irrelevant_punctuation
    else:
        choosed_tokenize = None

    generate(True, cns.V_BOW_NGRAM, description, choosed_tokenize)
    generate(False, cns.V_BOW, description, choosed_tokenize)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create datasets.")
    parser.add_argument('-v', '--valid_sample', action='store_true',
                        help="Generate real datasets")
    args = parser.parse_args()

    if args.valid_sample:
        generate_vocabs("Generate vocabulary")
    else:
        generate(path_vocab=cns.PATH_TEMP_DIR + "poquer.xlsx",
                 bow_ngram=False,
                 description="TESTE",
                 tokenizer=None,
                 target_vocab=cns.PATH_TEMP_DIR + "test_vocab",
                 log_filename=cns.PATH_TEMP_DIR + "log_len_vocab.txt")
