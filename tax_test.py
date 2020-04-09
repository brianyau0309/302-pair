# Unit Test for tax.py
# To Run this Unit Test, run "python tax_text.py"
# TaxCalc(self income, spouse income)
import unittest
from tax import TaxCalc

class TestTax(unittest.TestCase):
    '''
    TestCase:
      Test Case 1   : Testing MPF Calulation
      Test Case 2-4 : Testing Tax Bracket and Remain Balance
      Test Case 5   : Testing Standard Rate
      Test Case 6-n : Testing Normal Case
    '''
    def test_case_1(self):
        # Testing MPF which is 5% of income when income greater than or equal to 7100 every month
        # Maximum is 1500 per month and 180000 per year
        # Husband: 7099*12=85188, Wife: 7100*12=85200
        Calc = TaxCalc(85188, 85200)
        self.assertEqual(Calc.MPF(), [0, 4260], 'Error: MPF Miscalculated')
        Calc = TaxCalc(1000000, 360000)
        self.assertEqual(Calc.MPF(), [18000, 18000], 'Error: MPF Miscalculated')

    def test_case_2(self):
        # Testing Tax Bracket and Remain Balance
        # Husband: 50000, Wife: 100000
        Calc = TaxCalc(50000, 100000)
        self.assertEqual(Calc.MPF(), [0, 5000], 'Error: MPF Miscalculated')
        self.assertEqual(Calc.NetIncome(), [50000, 95000], 'Error: Net Income Miscalculated')
        self.assertEqual(Calc.Separate(), [0, 0], 'Error: Separate Taxation Miscalculated')
        self.assertEqual(Calc.Joint(), 0, 'Error: Joint Assessment Miscalculated')

    def test_case_3(self):
        # Testing Tax Bracket and Remain Balance
        # Husband: 150000, Wife: 200000
        Calc = TaxCalc(150000, 200000)
        self.assertEqual(Calc.MPF(), [7500, 10000], 'Error: MPF Miscalculated')
        self.assertEqual(Calc.NetIncome(), [142500, 190000], 'Error: Net Income Miscalculated')
        self.assertEqual(Calc.Separate(), [210, 1480], 'Error: Separate Taxation Miscalculated')
        self.assertEqual(Calc.Joint(), 2110, 'Error: Joint Assessment Miscalculated')

    def test_case_4(self):
        # Testing Tax Bracket and Remain Balance
        # Husband: 250000, Wife: 300000
        Calc = TaxCalc(250000, 300000)
        self.assertEqual(Calc.MPF(), [12500, 15000], 'Error: MPF Miscalculated')
        self.assertEqual(Calc.NetIncome(), [237500, 285000], 'Error: Net Income Miscalculated')
        self.assertEqual(Calc.Separate(), [4550, 9420], 'Error: Separate Taxation Miscalculated')
        self.assertEqual(Calc.Joint(), 25945, 'Error: Joint Assessment Miscalculated')

    def test_case_5(self):
        # Testing Standard Rate which is over 15% of Net Chargeable Income
        # Husband: 5000000, Wife: 8000000
        # Using Standard Rate   : 747300, 1197300
        Calc = TaxCalc(5000000, 8000000)
        self.assertEqual(Calc.Separate(), [747300, 1197300], 'Error: Standard Rate Miscalculated')

    def test_case_6(self):
        # Normal Case
        # Husband: 300000, Wife: 0
        Calc = TaxCalc(300000, 0)
        self.assertEqual(Calc.MPF(), [15000, 0], 'Error: MPF Miscalculated')
        self.assertEqual(Calc.NetIncome(), [285000, 0], 'Error: Net Income Miscalculated')
        self.assertEqual(Calc.Separate(), [9420, 0], 'Error: Separate Taxation Miscalculated')
        self.assertEqual(Calc.Joint(), 420, 'Error: Joint Assessment Miscalculated')

    def test_case_7(self):
        # Normal Case
        # Husband: 540000, Wife: 120000
        Calc = TaxCalc(540000, 120000)
        self.assertEqual(Calc.MPF(), [18000, 6000], 'Error: MPF Miscalculated')
        self.assertEqual(Calc.NetIncome(), [522000, 114000], 'Error: Net Income Miscalculated')
        self.assertEqual(Calc.Separate(), [48300, 0], 'Error: Separate Taxation Miscalculated')
        self.assertEqual(Calc.Joint(), 45240, 'Error: Joint Assessment Miscalculated')

if __name__ == '__main__':
    unittest.main()
