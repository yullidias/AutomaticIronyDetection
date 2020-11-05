import src.utils.constants as cns
from src.utils.files import write_list

import pandas as pd
import glob
import os


def read_sheets():
    manually_labeled_df = pd.DataFrame()
    for sheet in glob.glob(cns.PATH_LABELED + '*'):
        manually_labeled_df = manually_labeled_df.append(
                pd.read_excel(sheet, index_col=0), ignore_index=True)
    return manually_labeled_df


def rename_columns(dataset):
    return dataset.rename(columns={
            "pathOriginal": "path_ask",
            "tweet 'Pergunta'": "reply_response_tweet",
            "pathTweet": "id",
            "tweet a ser avaliado": "tweet",
            "rotulo": "label"
            })


def parser_label(label):
    if label == "Irônico":
        return cns.IRONIC_LABEL
    elif label == "Não irônico":
        return cns.NOT_IRONIC_LABEL
    else:
        return cns.DONT_KNOW_LABLE


def update_label(df, col):
    df[col] = df[col].apply(parser_label)


def path_to_id(df, col):
    df[col] = df[col].apply(lambda x: os.path.basename(x)
                            .split('.json')[0])


def get_by_label(df, label):
    return df[df["label"] == label]


def generate_manually_bases():
    labled_df = read_sheets()
    path_to_id(labled_df, "pathTweet")
    labled_df = rename_columns(labled_df)
    labled_df = labled_df[["id", "label"]]
    update_label(labled_df, "label")

    print("Generate base manually labeled as ironic ...")
    write_list(cns.B_M_IRONIC,
               get_by_label(labled_df, cns.IRONIC_LABEL)["id"].to_list())
    print("Generate base manually labeled as not ironic ...")
    write_list(cns.B_M_NOT_IRONIC,
               get_by_label(labled_df, cns.NOT_IRONIC_LABEL)["id"].to_list())

    return labled_df


if __name__ == "__main__":
    generate_manually_bases()
