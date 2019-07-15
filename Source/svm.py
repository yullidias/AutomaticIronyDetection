import pandas as pd
import pickle

PREDICT_FILE = 'predict.xlsx'
PYTHON_OBJECT_FILE = 'python.object'
VECTORIZER_OBJECT_FILE = 'vectorizer.object'
VALIDATION_FILE = 'logValidation.txt'
TEST_LOG_FILE = 'logTest.txt'
PREDICTION_LOG = 'logPrediction.txt'
TRAINING_IDS_FILE = 'training.json'
VALIDATION_IDS_FILE = 'validation.json'
TEST_IDS_FILE = 'test.json'

def getBaseDF(dataPathList):
    base = pd.DataFrame()
    for path in dataPathList:
        base = base.append(pd.read_excel(path, index_col=0), ignore_index=True)
    base['text'] = base['text'].values.astype('U')
    base['rotulo'] = base['rotulo'].values.astype(int)
    base = base.sample(frac=1, replace=True, random_state=17) #use the same random_state for reproducibility
    return base

def toExcel(df, path):
    writer = pd.ExcelWriter(path, engine='xlsxwriter',options={'strings_to_urls': False})
    df.to_excel(writer)
    writer.close()

def getFeatures(vectorizerVocabulary, dataset):
    features = vectorizerVocabulary.transform(dataset['text'])
    return features

def savePrediction(baseDF, prediction, rootTarget):
    predictDF = baseDF[['id', 'rotulo']]
    predictDF['id'] = predictDF['id'].values.astype('U')
    predictDF['predict'] = prediction
    toExcel(predictDF, rootTarget + PREDICT_FILE)

def writeObjectInFile(filename, obj):
     with open(filename, 'wb') as objectFile:
            pickle.dump(obj, objectFile)

def readObjectInFile(filename):
     with open(filename, 'rb') as objectFile:
        return pickle.load(objectFile)
