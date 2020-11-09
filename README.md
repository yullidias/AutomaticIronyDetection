# Automatic irony detection
Neste repositório estão os códigos referência citados nos trabalhos abaixo, onde foi realizado uma detecção de ironia em Tweets da lingua portuguesa. 

* Yulli Dias Tavares Alves, Ana Luiza Sanches, Daniel H. Dalip, and Ismael S. Silva. 2019. Automatic identification of irony: a case study on Twitter. In Proceedings of the 25th Brazillian Symposium on Multimedia and the Web (WebMedia ’19). Association for Computing Machinery, New York, NY, USA, 253–256. DOI:https://doi.org/10.1145/3323503.3360627

* Yulli Alves and Daniel Dalip. 2020. Automatic identification of irony: a case studyon Twitter. Thesis (Bachelor of Computer Engineering), CEFET-MG (Centro Federal de Educação Tecnológica de Minas Gerais), Belo Horizonte, Brazil

## Folder organization
  Data: any necessary data necessary
  
  Source: Pyhton and Jupyter Notebook files

  SVM: folds, model and prediction
  
    * The files training.json, test.json and validation.json contains the id of de tweets selected for partition
    * The file predict.xlsx contains the result of prediction of fold, using de test model
    * python.object is the object of the svm model
    * vectorizer.object is the object generate for axis
    * The logs files contains the metrics of model
