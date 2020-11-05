
SEED = 17


IRONIC_LABEL = 1
NOT_IRONIC_LABEL = 0
UNLABEL = -1
DONT_KNOW_LABLE = 2

HOME_REPOSITORY = '/home/yulli/Desktop/Github/AutomaticIronyDetectionOnTwitter/'
SRC = HOME_REPOSITORY + 'src/'

HOME = '/home/yulli/Desktop/Github/AutomaticIronyDetectionData/'
ROOT_DATA = HOME + 'data/'
ROOT_COLLECT = ROOT_DATA + 'collect/'
ROOT_COLLECT_TWEETS = ROOT_COLLECT + 'tweets/'
ROOT_COLLECT_USERS = ROOT_COLLECT + 'users/'
ROOT_REPLY_IRONICS = 'RespostasIronicos/'
ROOT_REPLY_RESPONSES = 'Responses/'
ROOT_PREPROCESS_SAMPLE = 'Preprocess/'

PATH_IRONICOS = ROOT_COLLECT_TWEETS + 'ironics/'
PATH_STOPWORDS = ROOT_COLLECT_TWEETS + 'stopWords/'
PATH_UNLABELED = ROOT_DATA + 'unlabeledSample/'
PATH_LABELED = PATH_UNLABELED + 'labledSheets/'
PATH_TEMP_DIR = ROOT_DATA + 'temp/'
PATH_TOKENS = ROOT_DATA + 'tokens.json'
PATH_DATASETS = ROOT_DATA + 'datasets/'
PATH_TRAIN_DIR = ROOT_DATA + 'train_datasets/'
PATH_FILTER_DIR = ROOT_DATA + 'filter_datasets/'
PATH_ANALYSIS = ROOT_DATA + 'analysis/'

LOG_USER_COLLECT = ROOT_COLLECT_USERS + 'logUserColect.txt'


# bases
FILE_SAMPLE = 'sample.txt'
PREPROCESS_SAMPLE = PATH_STOPWORDS + 'preprocess-sample.txt'
UNLABLED_SAMPLE = PATH_STOPWORDS + FILE_SAMPLE
B_M_IRONIC = PATH_STOPWORDS + 'manual_ironic.txt'
B_M_NOT_IRONIC = PATH_STOPWORDS + 'manual_not_ironic.txt'


# Datasets
D_PREPROCESS = PATH_DATASETS + 'preprocess.xlsx'
D_IRONIA = PATH_DATASETS + '#ironia.xlsx'
D_SQN = PATH_DATASETS + '#sqn.xlsx'
D_SOQUENAO = PATH_DATASETS + '#soquenao.xlsx'
D_HASHTAG = PATH_DATASETS + "ironicHashtags.xlsx"
D_UNLABLED = PATH_DATASETS + 'unlabled.xlsx'
D_M_IRONIC = PATH_DATASETS + "manually_ironic.xlsx"
D_IRONIC = PATH_DATASETS + "ironic.xlsx"
D_NOT_IRONIC = PATH_DATASETS + "manually_not_ironic.xlsx"


# PARAMETERS
REMOVE_STOP_WORDS = False
USE_STEMMING = False
BALANCED_DATASET = False
USE_CLASS_WEIGHT_BALANCED = True


# Vocabulary
PATH_ANALYSIS_VOCABULARY = PATH_ANALYSIS + "vocabulary/"
V_BOW_NGRAM = PATH_ANALYSIS_VOCABULARY + "bow_ngram.obj"
V_BOW = PATH_ANALYSIS_VOCABULARY + "bow.obj"
PATH_PLOT = PATH_ANALYSIS_VOCABULARY + "plots/"

TOKENIZE_TEXT = "text"
TOKENIZE_PUNCTUANTION = "punctuation"
TOKENIZE_DEFAULT = "default"


# SVM
ROOT_SVM = ROOT_DATA + "svm/"
PATH_PREDICT_DIR = ROOT_DATA + 'predict/'
N_SPLITS = 10


# Analisys
PATH_ANALYSIS_SVM = PATH_ANALYSIS + 'svm/'
PATH_RESULT_FOLDS = PATH_ANALYSIS_SVM + 'result-partition-test.xlsx'
FOLDS_FIG = PATH_ANALYSIS + 'macrof1-cv.svg'