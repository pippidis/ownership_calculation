from oc import Company2
from oc import Owner

from pprint import pprint


c1 = Company2('Skeii', "Johannes' idea", n_stocks=50000)
c1.add_owners_presentage({'Johannes':30, 'Sara':30}, expansion=False)
c1.add_owners_presentage({'Random 1':5, 'Random 2':5}, expansion=False)
c1.add_owners_presentage({'Random 3':2, 'Random 4':2}, expansion=False)
c1.add_owner_presentage('StartupLab', 12, expansion=False)
c1.add_owners({'Johannes':1000, 'Sara':2000, 'Random 1':600, 'Random 2':900, 'Random 3':80, 'Random 4':1500}) # Payout for work
c1.remove_owner('StartupLab')
c1.add_owner_presentage('Investor 1', 20)
c1.add_owners({'Johannes':500, 'Sara':1500, 'Random 1':200, 'Random 2':100, 'Random 3':300, 'Random 4':1000}) # Payout for work
c1.add_owner_presentage('Investor 2',20)
print(c1)
pprint(c1.history)
df = c1.history_dataframe()
df.to_excel('Scenario 1.xlsx')