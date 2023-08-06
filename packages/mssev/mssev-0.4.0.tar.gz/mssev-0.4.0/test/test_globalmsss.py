import unittest
import numpy as np
import pandas as pd

from mssev import global_msss


class TestGlobalMSSS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = pd.read_csv('test/mssev.csv')

    def test_original(self):
        original_msss = global_msss(self.data, ref='original')
        self.assertTrue(np.allclose(original_msss, self.data.oGMSSS,
                                    equal_nan=True))

    @unittest.expectedFailure
    def test_updated(self):
        updated_msss = global_msss(self.data, ref='updated')
        self.assertTrue(np.allclose(updated_msss, self.data.uGMSSS,
                                    equal_nan=True))
