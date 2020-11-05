# -*- coding: utf-8 -*-

import unittest

from src.utils.files import get_filename
from src.utils.files import remove_extension


class TestFiles(unittest.TestCase):

    def test_get_filename(self):
        self.assertEqual(get_filename('text', '.json'), "text.json")
        self.assertEqual(get_filename('text.json', '.json'), "text.json")
        self.assertEqual(get_filename('text.txt', '.json'),
                         "text.txt.json")

    def test_remove_extension(self):
        self.assertEqual(remove_extension('teste.xlsx', '.xlsx'), 'teste')
        self.assertEqual(remove_extension('teste', '.xlsx'), 'teste')
        self.assertEqual(remove_extension('abc/teste.xlsx', '.xlsx'),
                         'abc/teste')
        self.assertEqual(remove_extension('abc/teste', '.xlsx'), 'abc/teste')


if __name__ == '__main__':
    unittest.main()
