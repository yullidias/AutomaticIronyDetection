# -*- coding: utf-8 -*-
import src.utils.constants as cns
from src.my_cross_validation import CrossValidation
from src.utils.files import write_json
from src.utils.files import write_obj
from src.utils.files import read_excel
from src.utils.files import remove_extension
from src.generate_vocabulary import get_features
from src.analysis.plots import plot_confusion_matrix

import os
import glob
import numpy as np
import shutil
from sklearn import svm
from sklearn.metrics import classification_report, confusion_matrix


def get_score(report):
    return report['macro avg']['f1-score']


def get_reports(clf, label, predicted):
    report = classification_report(label, predicted, output_dict=True)
    cm = confusion_matrix(label, predicted)
    score = get_score(report)
    return report, cm, score


def log_results(path, partition, size_partition, fold, clf, score, c,
                report, confusion_matrix):
    values = {
        "fit_status": "error" if clf.fit_status_ else "OK",
        "partition": partition,
        "size_partition": size_partition,
        "fold": fold,
        "score": score,
        "c": c,
        "report": report,
        "confusion_matriz": confusion_matrix.tolist(),
        "parameters": clf.get_params(),
        "suport_vectors_shape": clf.support_vectors_.shape,
        "suport_vectors_for_class": clf.n_support_.tolist(),
        "suport_vectors_indices": clf.support_.tolist()
    }

    directory = path + str(fold) + '/' + partition + '/'
    write_json(directory + f"c{c}.json", values)

    values["clf"] = clf  # Object clf is not JSON serializable
    write_obj(directory + f"c{c}_clf.obj", clf)

    return values


def get_best(best, result):
    if best is None:
        return result
    if result["score"] > best["score"]:
        return result
    return best


def parse_to_int(array):
    return list(map(int, array))


def save_fold(out_dir, train, validation, test):
    fold = {
        "train": parse_to_int(train),
        "validation": parse_to_int(validation),
        "test": parse_to_int(test)
    }
    write_json(out_dir + "folds.json", fold)


def get_SVC(kernel, c):
    if cns.USE_CLASS_WEIGHT_BALANCED:
        return svm.SVC(kernel=kernel, C=c, class_weight='balanced')
    return svm.SVC(kernel=kernel, C=c)


def svm_cv(X, y, root_dir, n_splits=cns.N_SPLITS, kernel='linear'):
    y = np.asarray(y)

    C = [2**x for x in range(-5, 17, 2)]

    cv = CrossValidation(n_splits=n_splits, n_samples=X.shape[0])
    for n, (train, validation, test) in enumerate(cv.split_train_val_test()):
        save_fold(root_dir, train, validation, test)
        best_clf = None
        for c in C:
            clf = get_SVC(kernel, c)
            clf.fit(X[train], y[train])
            pred_train = clf.predict(X[train])
            report, c_matriz, score = get_reports(clf, pred_train, y[train])

            log_results(root_dir, "train", X[train].shape, n, clf,
                        score, c, report, c_matriz)

            pred_val = clf.predict(X[validation])
            report, c_matriz, score = get_reports(clf, pred_val, y[validation])

            result = log_results(root_dir, "val", X[validation].shape,
                                 n, clf, score, c, report, c_matriz)

            best_clf = get_best(best_clf, result)

        pred_test = clf.predict(X[test])
        report, c_matriz, score = get_reports(best_clf["clf"],
                                              pred_test, y[test])
        log_results(root_dir, "test", X[test].shape, best_clf["fold"],
                    best_clf["clf"], score, best_clf["c"], report, c_matriz)
        plot_confusion_matrix(best_clf["clf"], X[test], y[test],
                              root_dir + str(n) + '/test/')


def run(path_data, root_dir):
    dataset_name = remove_extension(os.path.basename(path_data), '.xlsx')
    target = root_dir + dataset_name + "/"
    print(f"--- [START] SVM dataset {dataset_name} ...")
    df = read_excel(path_data)

    print(f"BOW-NGRAM {dataset_name} ...")
    svm_cv(get_features(df['text'], True), df['label'], target + "bow_ngram/")

    print(f"BOW {dataset_name} ...")
    svm_cv(get_features(df['text'], False), df['label'], target + "bow/")
    print(f"--- [END] SVM dataset {dataset_name} ...")


def run_all_datasets(root_dir=cns.ROOT_SVM):
    if os.path.exists(root_dir):
        shutil.rmtree(root_dir)

    for path in glob.glob(cns.PATH_TRAIN_DIR + '*.xlsx'):
        run(path, root_dir)


if __name__ == "__main__":
    dataset = read_excel(cns.PATH_TEMP_DIR + "poquer.xlsx", suffle=True)
    features = get_features(dataset['text'], False)

    # run("Teste", cns.PATH_TEMP_DIR + "poquer.xlsx", cns.PATH_TEMP_DIR + "TestSVC/")
    svm_cv(features, dataset['label'], cns.PATH_TEMP_DIR + "TestSVC/")
