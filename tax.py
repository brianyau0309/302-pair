import subprocess as sp
''' Tax Calculator for 2020-2021 '''
MPF_floor, MPF_percent, MPF_max = 7100, 0.05, 18000
basic_allowance, married_allowance = 132000, 264000
tax_stage = 50000
tax_bracket, remaining_balance, standard_rate = [0.02, 0.06, 0.1, 0.14], 0.17, 0.15

class TaxCalc():
    def __init__(self, income: float, spouse_income: float = 0):
        self.income, self.spouse_income = income, spouse_income
        if self.income < 0 or self.spouse_income < 0:
            raise Exception("Error: The income must greater than or equal 0.")

    def MPF(self):
        # MPF Maximum contribution per YEAR is 1500 x 12 = 18000
        MPF = min(self.income*MPF_percent, MPF_max) if self.income/12 >= MPF_floor else 0
        spouse_MPF = min(self.spouse_income*MPF_percent, MPF_max) if self.spouse_income/12 >= MPF_floor else 0
        return [MPF, spouse_MPF]

    def NetIncome(self):
        # Net Income(NI) = Total Income - Deductions(MPF)
        MPF = self.MPF()
        NET, spouse_NET = self.income - MPF[0], self.spouse_income - MPF[1]
        return [NET, spouse_NET]

    def Tax(self, NCI: float, t = None):
        allowance = married_allowance if t else basic_allowance
        tax, tax_standard = 0, (NCI+allowance)*standard_rate
        for charge_rate in tax_bracket: # Calc Tax by Tax Bracket
            if NCI <= tax_stage:
                tax += NCI*charge_rate
                NCI = 0
                break
            else:
                tax += tax_stage*charge_rate
                NCI -= tax_stage
        tax += NCI*remaining_balance
        return min(tax, tax_standard)

    def Separate(self):
        # Separate Assessment, Income(NCI) = Total Income - Deductions(MPF) - Allowances
        NCI = [i - basic_allowance if i > basic_allowance else 0 for i in self.NetIncome()]
        return [self.Tax(i) for i in NCI]

    def Joint(self):
        # Joint Assessment, Net Chargeable Income(NCI) = Total Income - Deductions(MPF) - Allowances
        Joint_NI = sum(self.NetIncome())
        Joint_NCI = Joint_NI - married_allowance if Joint_NI > married_allowance else 0
        return self.Tax(Joint_NCI, 'join')

def main():
    sp.call('cls', shell=True)
    print('\n Tax Calculator\n Input Income (Exclude cents)\n')
    income, spouse_income = input(' Self Income \n > '), input(' Spouse Income (Press Enter if Single) \n > ')
    try:
      income, spouse_income, married = float(income), 0 if spouse_income == "" else float(spouse_income), False if spouse_income == "" else True
      Calc = TaxCalc(income, spouse_income)
    except:
        print('\n Error: Invalid Value, please input int or float and non-negative number\n')
        return

    MPF, NI, Separate, Joint = Calc.MPF(), Calc.NetIncome(), Calc.Separate(), Calc.Joint()
    shortbar, bar = ' '+'-'*51, ' '+'-'*70, 
    shortrow, row = ' | {:<22}| {:<10.1f}              |', ' | {:<22}| {:<10.1f}  {:<10.1f}  | {:<16.1f} |'

    print('\n' + bar if married else shortbar)
    print(' | Result(Exclude Cents) | Separate Assessment     |'+(' Joint Assessment |' if married else ''))
    print(' | HK$                   | Self       '+('Spouse       | Joint            |' if married else ' '*13+'|'))
    print(bar if married else shortbar)

    if married:
      print(row.format('Income', income, spouse_income, income+spouse_income))
      print(row.format('MPF', MPF[0], MPF[1], sum(MPF)))
      print(row.format('NetIncome', NI[0], NI[1], sum(NI)))
      print(row.format('Allowance', basic_allowance if income != 0 else 0, basic_allowance if spouse_income != 0 else 0, married_allowance if income+spouse_income != 0 else 0))
      print(row.format('Net Chargeable Income', max(NI[0]-basic_allowance, float(0)), max(NI[1]-basic_allowance,float(0)), max(sum(NI)-married_allowance,float(0))))
      print(row.format('Tax Payable', Separate[0], Separate[1], Joint))
    else:
      print(shortrow.format('Income', income))
      print(shortrow.format('MPF', MPF[0]))
      print(shortrow.format('NetIncome', NI[0]))
      print(shortrow.format('Allowance', basic_allowance if spouse_income != 0 else 0))
      print(shortrow.format('Net Chargeable Income', max(NI[0]-basic_allowance, float(0))))
      print(shortrow.format('Tax Payable', Separate[0]))

    print(bar if married else shortbar + '\n')
    print('\n Joint Assessment' if sum(Separate) > Joint and married else ' Separate Assessment', 'are recommanded.\n')

if __name__ == '__main__':
    main()
