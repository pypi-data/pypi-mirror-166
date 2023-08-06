import unittest
import numpy as np
import pandas as pd

from mssev import irreversible_ds

import matplotlib.pyplot as plt


class TestGlobalMSSS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = pd.read_csv('test/assessments.csv', parse_dates=['date'])

        cls.data.set_index('date')[['edss', 'iedss_6M']].plot()
        plt.show()

    @unittest.skip
    def test_without_stability_period(self):
        iedss = irreversible_ds(self.data)
        self.assertTrue(np.allclose(iedss, self.data.iedss, equal_nan=True))

    def test_with_stability_period(self):
        iedss = irreversible_ds(self.data, min_period=np.timedelta64(6, 'M'))
        self.assertTrue(np.allclose(iedss, self.data.iedss_6M, equal_nan=True))
