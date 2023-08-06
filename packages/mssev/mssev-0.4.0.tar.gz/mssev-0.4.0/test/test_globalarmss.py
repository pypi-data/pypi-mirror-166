import numpy as np
import pandas as pd
import unittest

from mssev import global_armss


class TestGlobalARMSS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = pd.read_csv('test/mssev.csv')

    def test_original(self):
        original_armss = global_armss(self.data, ref='original')
        self.assertTrue(np.allclose(original_armss, self.data.gARMSS))
