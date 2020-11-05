# -*- coding: utf-8 -*-
from src.my_cross_validation import CrossValidation

import unittest


class TestCrossValidation(unittest.TestCase):
    def assert_train_val_test(self, cv, e_train, e_val, e_test):
        for count, (train, val, test) in enumerate(cv.split_train_val_test()):
            self.assertListEqual(train, e_train[count])
            self.assertListEqual(val, e_val[count])
            self.assertListEqual(test, e_test[count])

    def test_split_train_val_test(self):
        # 5 folds 10 classes
        cv10 = CrossValidation(5, 10)
        e_train = [[0, 1, 2, 3, 4, 5], [2, 3, 4, 5, 6, 7], [4, 5, 6, 7, 8, 9],
                   [0, 1, 6, 7, 8, 9], [0, 1, 2, 3, 8, 9]]
        e_val = [[6, 7], [8, 9], [0, 1], [2, 3], [4, 5]]
        e_test = [[8, 9], [0, 1], [2, 3], [4, 5], [6, 7]]
        self.assert_train_val_test(cv10, e_train, e_val, e_test)

        # 5 folds 8 classes
        cv8 = CrossValidation(5, 8)
        e_train = [[0, 1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [4, 5, 6, 7],
                   [0, 1, 6, 7], [0, 1, 2, 3, 7]]
        e_val = [[6], [7], [0, 1], [2, 3], [4, 5]]
        e_test = [[7], [0, 1], [2, 3], [4, 5], [6]]
        self.assert_train_val_test(cv8, e_train, e_val, e_test)


if __name__ == "__main__":
    unittest.main()
