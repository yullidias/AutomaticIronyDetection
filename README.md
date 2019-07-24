# Automatic irony detection
Detecção de ironia em Tweets da lingua portuguesa

## Folder organization
  Data: any necessary data necessary
  
  Source: Pyhton and Jupyter Notebook files

  SVM: folds, model and prediction
  
    * The files training.json, test.json and validation.json contains the id of de tweets selected for partition
    * The file predict.xlsx contains the result of prediction of fold, using de test model
    * python.object is the object of the svm model
    * vectorizer.object is the object generate for axis
    * The logs files contains the metrics of model
