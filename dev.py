from company_ownership import Company

from pprint import pprint


c1 = Company('Some Name', "Johannes' idea", n_stocks=50000)
c1.add_owners_presentage({'Johannes':30, 'Sara':30}, expansion=False)
c1.add_owners_presentage({'Random 1':5, 'Random 2':5}, expansion=False)
c1.add_owners_presentage({'Random 3':2, 'Random 4':2}, expansion=False)
c1.add_owner_percentage('StartupLab', 12, expansion=False)
c1.add_owners({'Johannes':1000, 'Sara':2000, 'Random 1':600, 'Random 2':900, 'Random 3':80, 'Random 4':1500}) # Payout for work
c1.remove_owner('StartupLab')
c1.add_owner_percentage('Investor 1', 20)
c1.add_owners({'Johannes':500, 'Sara':1500, 'Random 1':200, 'Random 2':100, 'Random 3':300, 'Random 4':1000}) # Payout for work
c1.add_owner_percentage('Investor 2',20)
print(c1)
c1.transfer_stocks('Johannes', 'Sara', 15206)
print(c1)
#pprint(c1.history)
df = c1.history_dataframe()
df.to_excel('Scenario 1.xlsx', index=False)


# Main scenario
c = Company('Verres', "Idea", n_stocks=10_000_000)
c.add_owners_presentage({'Johannes':30, 'Sara':30}, expansion=False, external_desription='Johannes and Sara initial ownership')
c.add_owners_presentage({'Frontend 1':3, 'Backend 1':3, 'Crime 1':2, 'Sales 1':2, 'Stock Option Pool':20}, expansion=False, external_desription='Recruting intital staff and making stock option pool') 

# Paying out intital stock options - Just before starting with accelerator
c.transfer_stocks('Stock Option Pool', 'Johannes', n_stocks=1500, external_desription='Johannes worked a lot on the POC')
c.transfer_stocks('Stock Option Pool', 'Sara', n_stocks=2500, external_desription='Sara worked on the application and buisniss plan')
c.transfer_stocks('Stock Option Pool', 'Backend 1', n_stocks=1500, external_desription='Made the backend database up and running')
c.transfer_stocks('Stock Option Pool', 'Frontend 1', n_stocks=1900, external_desription='Made the initial fronend for the platform')
c.transfer_stocks('Stock Option Pool', 'Crime 1', n_stocks=500, external_desription='Collected 300 cases')
c.transfer_stocks('Stock Option Pool', 'Sales 1', n_stocks=50, external_desription='Worked on a strategy, but not that much')

# Adding inn Startuplab with 13% ownership by expansion
c.add_owner_percentage('Startup Lab', 13, expansion=True, external_description='Startup Lab entered into the company with a 13 % wonership for 1.7 MNOK')

# Paying out stock options two times for work
c.transfer_stocks('Stock Option Pool', 'Johannes', n_stocks=500, external_desription='Johannes had to focus on his Phd')
c.transfer_stocks('Stock Option Pool', 'Sara', n_stocks=1900, external_desription='Sara worked a lot')
c.transfer_stocks('Stock Option Pool', 'Backend 1', n_stocks=1800, external_desription='Continued developing the backend')
c.transfer_stocks('Stock Option Pool', 'Frontend 1', n_stocks=2200, external_desription='Added more features to the frontend')
c.transfer_stocks('Stock Option Pool', 'Crime 1', n_stocks=700, external_desription='Added more cases')
c.transfer_stocks('Stock Option Pool', 'Sales 1', n_stocks=200, external_desription='Started the sales prosess')

c.transfer_stocks('Stock Option Pool', 'Johannes', n_stocks=1100, external_desription='Johannes worked a lot on the POC')
c.transfer_stocks('Stock Option Pool', 'Sara', n_stocks=1500, external_desription='Worked on agreement with first customer')
c.transfer_stocks('Stock Option Pool', 'Backend 1', n_stocks=800, external_desription='Ready for first customer')
c.transfer_stocks('Stock Option Pool', 'Frontend 1', n_stocks=1400, external_desription='Frontend ready for intital customer')
c.transfer_stocks('Stock Option Pool', 'Crime 1', n_stocks=600, external_desription='Collected even more cases')
c.transfer_stocks('Stock Option Pool', 'Sales 1', n_stocks=800, external_desription='Got an example customer')
print(c)

# Startuplab sells out to a new investor, new investor takes 500 000 stocks from the stock option pool as well
c.transfer_stocks('Startup Lab', 'Investor 1', n_stocks=100_000_000, external_desription='Startup Lab sells out') # of stocks here is just tol show that it is all it has
c.transfer_stocks('Stock Option Pool', 'Investor 1', n_stocks=500_000, external_desription='Investor also gets stocks form the stock option pool')

# Paying out stock options two times for work (Duplicate of the above)
c.transfer_stocks('Stock Option Pool', 'Johannes', n_stocks=500, external_desription='Johannes had to focus on his Phd')
c.transfer_stocks('Stock Option Pool', 'Sara', n_stocks=1900, external_desription='Sara worked a lot')
c.transfer_stocks('Stock Option Pool', 'Backend 1', n_stocks=1800, external_desription='Continued developing the backend')
c.transfer_stocks('Stock Option Pool', 'Frontend 1', n_stocks=1200, external_desription='Added more features to the frontend')
c.transfer_stocks('Stock Option Pool', 'Crime 1', n_stocks=400, external_desription='Added more cases')
c.transfer_stocks('Stock Option Pool', 'Sales 1', n_stocks=200, external_desription='Started the sales prosess')

c.transfer_stocks('Stock Option Pool', 'Johannes', n_stocks=1100, external_desription='Johannes worked a lot on the POC')
c.transfer_stocks('Stock Option Pool', 'Sara', n_stocks=1500, external_desription='Worked on agreement with first customer')
c.transfer_stocks('Stock Option Pool', 'Backend 1', n_stocks=800, external_desription='Ready for first customer')
c.transfer_stocks('Stock Option Pool', 'Frontend 1', n_stocks=1400, external_desription='Frontend ready for intital customer')
c.transfer_stocks('Stock Option Pool', 'Crime 1', n_stocks=600, external_desription='Collected even more cases')
c.transfer_stocks('Stock Option Pool', 'Sales 1', n_stocks=800, external_desription='Got an example customer')

# Paying out stock options two times for work (Duplicate of the above)
c.transfer_stocks('Stock Option Pool', 'Johannes', n_stocks=500, external_desription='Johannes had to focus on his Phd')
c.transfer_stocks('Stock Option Pool', 'Sara', n_stocks=1900, external_desription='Sara worked a lot')
c.transfer_stocks('Stock Option Pool', 'Backend 1', n_stocks=1800, external_desription='Continued developing the backend')
c.transfer_stocks('Stock Option Pool', 'Frontend 1', n_stocks=1200, external_desription='Added more features to the frontend')
c.transfer_stocks('Stock Option Pool', 'Crime 1', n_stocks=400, external_desription='Added more cases')
c.transfer_stocks('Stock Option Pool', 'Sales 1', n_stocks=200, external_desription='Started the sales prosess')

c.transfer_stocks('Stock Option Pool', 'Johannes', n_stocks=1100, external_desription='Johannes worked a lot on the POC')
c.transfer_stocks('Stock Option Pool', 'Sara', n_stocks=1500, external_desription='Worked on agreement with first customer')
c.transfer_stocks('Stock Option Pool', 'Backend 1', n_stocks=800, external_desription='Ready for first customer')
c.transfer_stocks('Stock Option Pool', 'Frontend 1', n_stocks=1400, external_desription='Frontend ready for intital customer')
c.transfer_stocks('Stock Option Pool', 'Crime 1', n_stocks=600, external_desription='Collected even more cases')
c.transfer_stocks('Stock Option Pool', 'Sales 1', n_stocks=800, external_desription='Got an example customer')

# Paying out stock options two times for work (Duplicate of the above)
c.transfer_stocks('Stock Option Pool', 'Johannes', n_stocks=500, external_desription='Johannes had to focus on his Phd')
c.transfer_stocks('Stock Option Pool', 'Sara', n_stocks=1900, external_desription='Sara worked a lot')
c.transfer_stocks('Stock Option Pool', 'Backend 1', n_stocks=1800, external_desription='Continued developing the backend')
c.transfer_stocks('Stock Option Pool', 'Frontend 1', n_stocks=1200, external_desription='Added more features to the frontend')
c.transfer_stocks('Stock Option Pool', 'Crime 1', n_stocks=400, external_desription='Added more cases')
c.transfer_stocks('Stock Option Pool', 'Sales 1', n_stocks=200, external_desription='Started the sales prosess')

c.transfer_stocks('Stock Option Pool', 'Johannes', n_stocks=1100, external_desription='Johannes worked a lot on the POC')
c.transfer_stocks('Stock Option Pool', 'Sara', n_stocks=1500, external_desription='Worked on agreement with first customer')
c.transfer_stocks('Stock Option Pool', 'Backend 1', n_stocks=800, external_desription='Ready for first customer')
c.transfer_stocks('Stock Option Pool', 'Frontend 1', n_stocks=1400, external_desription='Frontend ready for intital customer')
c.transfer_stocks('Stock Option Pool', 'Crime 1', n_stocks=600, external_desription='Collected even more cases')
c.transfer_stocks('Stock Option Pool', 'Sales 1', n_stocks=800, external_desription='Got an example customer')

# Emision 1: Getting the secound investor by emision
c.add_owner_percentage(name='Investor 2', n_presentages=20, expansion=True, external_description='Adding another investor providing 30 MNOK in founding for 30%')

# Paying out stock options two times for work (Duplicate of the above)
c.transfer_stocks('Stock Option Pool', 'Johannes', n_stocks=500, external_desription='Johannes had to focus on his Phd')
c.transfer_stocks('Stock Option Pool', 'Sara', n_stocks=1900, external_desription='Sara worked a lot')
c.transfer_stocks('Stock Option Pool', 'Backend 1', n_stocks=1800, external_desription='Continued developing the backend')
c.transfer_stocks('Stock Option Pool', 'Frontend 1', n_stocks=1200, external_desription='Added more features to the frontend')
c.transfer_stocks('Stock Option Pool', 'Crime 1', n_stocks=400, external_desription='Added more cases')
c.transfer_stocks('Stock Option Pool', 'Sales 1', n_stocks=200, external_desription='Started the sales prosess')

c.transfer_stocks('Stock Option Pool', 'Johannes', n_stocks=1100, external_desription='Johannes worked a lot on the POC')
c.transfer_stocks('Stock Option Pool', 'Sara', n_stocks=1500, external_desription='Worked on agreement with first customer')
c.transfer_stocks('Stock Option Pool', 'Backend 1', n_stocks=800, external_desription='Ready for first customer')
c.transfer_stocks('Stock Option Pool', 'Frontend 1', n_stocks=1400, external_desription='Frontend ready for intital customer')
c.transfer_stocks('Stock Option Pool', 'Crime 1', n_stocks=600, external_desription='Collected even more cases')
c.transfer_stocks('Stock Option Pool', 'Sales 1', n_stocks=800, external_desription='Got an example customer')

# Paying out stock options two times for work (Duplicate of the above)
c.transfer_stocks('Stock Option Pool', 'Johannes', n_stocks=500, external_desription='Johannes had to focus on his Phd')
c.transfer_stocks('Stock Option Pool', 'Sara', n_stocks=1900, external_desription='Sara worked a lot')
c.transfer_stocks('Stock Option Pool', 'Backend 1', n_stocks=1800, external_desription='Continued developing the backend')
c.transfer_stocks('Stock Option Pool', 'Frontend 1', n_stocks=1200, external_desription='Added more features to the frontend')
c.transfer_stocks('Stock Option Pool', 'Crime 1', n_stocks=400, external_desription='Added more cases')
c.transfer_stocks('Stock Option Pool', 'Sales 1', n_stocks=200, external_desription='Started the sales prosess')

c.transfer_stocks('Stock Option Pool', 'Johannes', n_stocks=1100, external_desription='Johannes worked a lot on the POC')
c.transfer_stocks('Stock Option Pool', 'Sara', n_stocks=1500, external_desription='Worked on agreement with first customer')
c.transfer_stocks('Stock Option Pool', 'Backend 1', n_stocks=800, external_desription='Ready for first customer')
c.transfer_stocks('Stock Option Pool', 'Frontend 1', n_stocks=1400, external_desription='Frontend ready for intital customer')
c.transfer_stocks('Stock Option Pool', 'Crime 1', n_stocks=600, external_desription='Collected even more cases')
c.transfer_stocks('Stock Option Pool', 'Sales 1', n_stocks=800, external_desription='Got an example customer')


print(c)
df = c.history_dataframe()
df.to_excel('Scenario 1.xlsx', index=False)