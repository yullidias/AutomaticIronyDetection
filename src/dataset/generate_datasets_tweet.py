import src.utils.constants as cns
from src.utils.files import get_paths
from src.utils.files import to_excel
from src.utils.effects import progress_bar
from src.collect.tweet import Tweet
from src.preprocess import preprocess
import src.dataset.manually_labeled_bases as d_manual

import pandas as pd
import argparse
import glob
from datetime import datetime


def generate(collect_list_files, target_file, label,
             add_original_tweet=False, is_temp=True):
    dataset_df = pd.DataFrame(columns=["id", "text", "user_id",
                                       "reply_to_status", "reply_to_user",
                                       "retweet_count", "favorite_count",
                                       "language", "label"])
    for collect_list_file in collect_list_files:
        paths = get_paths(collect_list_file)
        progress_bar(0, len(paths))
        for count, path in enumerate(paths):
            tweet = Tweet(path)
            if not tweet.is_retweet():
                words = preprocess(tweet.get_text(), out_tokens=True)
                if len(words) > 0:
                    columns = {
                         "id": tweet.id(),
                         "text": ' '.join(words),
                         "user_id": tweet.user_id(),
                         "reply_to_status": tweet.reply_to_status(),
                         "reply_to_user": tweet.reply_to_user(),
                         "retweet_count": tweet.retweet_count(),
                         "favorite_count": tweet.favorite_count(),
                         "language": tweet.language()
                         }

                    if label is not None:
                        columns["label"] = label
                    if add_original_tweet:
                        columns["tweet"] = tweet.get_text()

                    dataset_df = dataset_df.append(columns, ignore_index=True)
                else:
                    print(f"Tweet {path} has {len(words)} words after "
                          "preprocess. Ignored.")
            progress_bar(count + 1, len(paths))
    if is_temp:
        target_file = target_file.split('.')[0]
        target_file += '_' + datetime.now().strftime("%Y%m%d-%H%M%S")

    if not target_file.endswith('.xlsx'):
        target_file += '.xlsx'

    to_excel(target_file, dataset_df)


def generate_datasets():
    print("Generate #ironia ...")
    ironia = glob.glob(cns.PATH_IRONICOS + '#ironia-[1-9]coleta.txt')
    generate(ironia, cns.D_IRONIA, cns.IRONIC_LABEL, is_temp=False)

    print("Generate #soquenao ...")
    soquenao = glob.glob(cns.PATH_IRONICOS + '#soquenao-[1-9]coleta.txt')
    generate(soquenao, cns.D_SOQUENAO, cns.IRONIC_LABEL, is_temp=False)

    print("Generate #sqn ...")
    sqn = [cns.PATH_IRONICOS + '#sqn.txt']
    generate(sqn, cns.D_SQN,  cns.IRONIC_LABEL, is_temp=False)

    bases_hashtags = ironia + soquenao + sqn

    print("Generate all hashtags ...")
    generate(bases_hashtags, cns.D_HASHTAG, cns.IRONIC_LABEL, is_temp=False)

    print("Generate manually ironic ...")
    manually_ironic = [cns.B_M_IRONIC]
    generate(manually_ironic, cns.D_M_IRONIC, cns.IRONIC_LABEL, is_temp=False)

    print("Generate ironic ...")
    generate(bases_hashtags + manually_ironic, cns.D_IRONIC, cns.IRONIC_LABEL,
             is_temp=False)

    print("Generate not ironic ...")
    generate([cns.B_M_NOT_IRONIC], cns.D_NOT_IRONIC, cns.NOT_IRONIC_LABEL,
             is_temp=False)


def generate_preprocess():
    print("Generate preprocess ...")
    generate([cns.PREPROCESS_SAMPLE], cns.D_PREPROCESS, None,
             add_original_tweet=True, is_temp=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create datasets.")
    parser.add_argument('-v', '--valid_datasets', action='store_true',
                        help="Generate real datasets")
    parser.add_argument('-p', '--preprocess', action='store_true',
                        help="Generate preprocess dataset")
    args = parser.parse_args()

    if not args.valid_datasets:
        print("Generate porquer dataset ...")
        generate([cns.ROOT_COLLECT_TWEETS + "randomWords/poquer/poquer.txt"],
                 cns.PATH_TEMP_DIR + 'poquer', cns.IRONIC_LABEL)
    else:
        d_manual.generate_manually_bases()
        generate_datasets()

    if args.preprocess:
        generate_preprocess()
    print("DONE!")
