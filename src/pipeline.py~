import src.utils.constants as cns
import src.utils.files as f
import src.dataset.generate_datasets_tweet as d_tweet
import src.generate_vocabulary as vocab
import src.generate_data as data
import src.dataset.generate_datasets_user as user
import src.svm as my_svm
import src.analysis.analysis as analysis
import src.generate_error_map as gem

if __name__ == '__main__':
    DESCRIPTION = "Executando o pipeline"

    f.create_if_not_exists(cns.PATH_ANALYSIS_VOCABULARY)
    f.create_if_not_exists(cns.PATH_ANALYSIS_SVM)

    gem.generate_error_map()
    # d_tweet.generate_datasets()

    # d_tweet.generate_preprocess()
    vocab.generate_vocabs(DESCRIPTION, cns.TOKENIZE_DEFAULT)

    data.generate_train_data()
    my_svm.run_all_datasets()

    analysis.svm()
    analysis.dataset()
