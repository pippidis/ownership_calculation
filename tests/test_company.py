import pytest
from company_ownership import Company

# TO RUN: python -m pytest --cov

def test_initiation():
    c = Company(name='Test', n_stocks=100, original_owner='Test Owner 1')
    assert isinstance(c, Company)
    print(c) # Testing that it works

## Testing adding owner functions
def test_add_owner(company: Company):
    company.add_owner(name='Test Owner 3', n_stocks=100, expansion=True)
    assert 'Test Owner 3' in company.owners
    assert company.owners['Test Owner 3'] == 100

    # Testing that if the owner exist, it adds the stocks
    company.add_owner(name='Test Owner 3', n_stocks=100, expansion=True)
    assert company.owners['Test Owner 3'] == 200

    # Testing if there is no expansion: 
    company.add_owner(name='Test Owner 3', n_stocks=300, expansion=False)
    assert company.owners['Test Owner 3'] == 350

    # Testing a compleate takeover
    company.add_owner(name='Test Owner 4', n_stocks=400, expansion=False)
    assert company.owners['Test Owner 4'] == 400
    assert len(company.owners) == 1

    # If there are to few stocks: 
    with pytest.raises(ValueError):
        company.add_owner(name='Test Owner 5', n_stocks=100_000, expansion=False)

def test_add_owners(company: Company):
    company.add_owners({'Random 1':100, 'Random 2':100}, expansion=True)
    assert 'Random 1' in company.owners
    assert company.owners['Random 1'] == 100
    assert 'Random 2' in company.owners
    assert company.owners['Random 2'] == 100

    # Testing non expansion
    company.add_owners({'Random 3':200, 'Random 4':100}, expansion=False)
    assert 'Random 3' in company.owners
    assert company.owners['Random 3'] == 200
    assert 'Random 4' in company.owners
    assert company.owners['Random 4'] == 100
    assert company.owners['Random 1'] == 50 # Testing that the number of stocks for the original has gone down
    
    # Testing a full takeover
    company.add_owners({'Random 5':200, 'Random 6':400}, expansion=False)
    assert company.owners['Random 6'] == 400
    assert len(company.owners) == 2

    # If there are to few stocks: 
    with pytest.raises(ValueError):
        company.add_owners({'Random 5':100_000, 'Random 6':100_000}, expansion=False)

def test_add_owner_percentage():
    company = Company(name='Test', n_stocks=100, original_owner='Test Owner 1')
    
    # Test adding to allready sole owner
    total_stocks = company.number_of_stocks
    company.add_owner_percentage('Test Owner 1', 50, expansion=True)
    assert 'Test Owner 1' in company._owners
    assert company._owners['Test Owner 1'] == total_stocks*2
    assert company.number_of_stocks == total_stocks * 2

    # Test adding new owner with expansion
    company.owners['Test Owner 1'] = 100 # Resetting
    total_stocks = company.number_of_stocks
    company.add_owner_percentage('Test Owner 2', 50, expansion=True)
    assert 'Test Owner 1' in company._owners
    assert company._owners['Test Owner 2'] == 100
    assert company.number_of_stocks == total_stocks * 2

    # Test adding to an existing owner with expansion
    company.add_owner_percentage('Test Owner 1', 50, expansion=True)
    assert company._owners['Test Owner 1'] == total_stocks * 3
    assert company.number_of_stocks == total_stocks * 4

    # Test adding new owner without expansion
    company.add_owner_percentage('Test Owner 3', 50, expansion=False)
    assert 'Test Owner 3' in company._owners
    assert company._owners['Test Owner 3'] == company.number_of_stocks / 2

    # Test adding to an existing owner without expansion
    company.add_owner_percentage('Test Owner 2', 50, expansion=False)
    assert company._owners['Test Owner 2'] == company.number_of_stocks * 0.5 + 25

    # Test adding more than 100 percentage
    with pytest.raises(ValueError):
        company.add_owner_percentage('Test Owner 4', 105, expansion=False)

    # Test adding less than or equal to zero percentage
    with pytest.raises(ValueError):
        company.add_owner_percentage('Test Owner 4', 0, expansion=False)

def test_add_owners_percentage():
    company = Company(name='Test', n_stocks=100, original_owner='Test Owner 1')
    company.add_owner(name='Test Owner 3', n_stocks=100, expansion=True)

    # Add a new owner with 10% ownership, expanding the company
    new_owners = {'Owner 1': 10}
    company.add_owners_percentage(new_owners, expansion=True)
    assert 'Owner 1' in company.owners
    assert company.owners['Owner 1'] == round(company.number_of_stocks * 0.1)

    # Add multiple new owners with various percentages, without expanding the company
    new_owners = {'Owner 2': 20, 'Owner 3': 30}
    company.add_owners_percentage(new_owners, expansion=False)
    assert 'Owner 2' in company.owners
    assert company.owners['Owner 2'] == round(company.number_of_stocks * 0.2)
    assert 'Owner 3' in company.owners
    assert company.owners['Owner 3'] == round(company.number_of_stocks * 0.3)

    # Test that adding an owner with a percentage greater than 100 raises a ValueError
    new_owners = {'Owner 4': 101}
    with pytest.raises(ValueError):
        company.add_owners_percentage(new_owners)

    # Test that adding owners with total percentage greater than 100 raises a ValueError
    new_owners = {'Owner 5': 50, 'Owner 6': 51}
    with pytest.raises(ValueError):
        company.add_owners_percentage(new_owners)
    
## Testing reducing owners
def test_remove_owner():
    company = Company(name='Test', n_stocks=100, original_owner='Test Owner 1')
    company.add_owner(name='Test Owner 3', n_stocks=100, expansion=True)
    assert len(company.owners) == 2
    assert 'Test Owner 3' in company.owners
    assert company.owners['Test Owner 3'] == 100

    # Testing a reduction of stocks
    company.remove_owner(name='Test Owner 3', n_stocks=50, shrink=True)
    assert 'Test Owner 3' in company.owners
    assert company.owners['Test Owner 3'] == 50

    # Testing to add remove negative amount of stocks: 
    with pytest.raises(ValueError):
        company.remove_owner(name='Test Owner 1', n_stocks=-100, shrink=False)

    # Whithout shrinkage
    number_of_stocks = company.number_of_stocks
    company.remove_owner(name='Test Owner 3', n_stocks=20, shrink=False)
    assert 'Test Owner 3' in company.owners
    assert company.owners['Test Owner 3'] == 35 # Due to the shrinkage, the 50 base should become 55, then 55-20=35
    assert company.owners['Test Owner 1'] == 115
    assert len(company.owners) == 2
    assert number_of_stocks == company.number_of_stocks # Checking that the number of stocks in the company is preserved

    # Compleate removal
    company.remove_owner(name='Test Owner 3', shrink=False)
    assert 'Test Owner 3' not in company.owners

    # Trying to remove the last owner: 
    with pytest.raises(RuntimeError):
        company.remove_owner(name='Test Owner 1', shrink=True)
    assert len(company.owners) == 1

    # Trying to remove an owner that is not there
    with pytest.raises(KeyError):
        company.remove_owner(name='Test Owner 100', shrink=True)

def test_remove_owner_percentage(company: Company):
    company = Company(name='Test', n_stocks=100, original_owner='Test Owner 1')
    # Add test owners
    company.add_owner(name='Test Owner 2', n_stocks=100)
    company.add_owner(name='Test Owner 3', n_stocks=100)

    # Removing 20% stocks in absolute terms
    company.remove_owner_percentage_absolute(name='Test Owner 3', n_presentages=20, shrink=True)
    assert 'Test Owner 3' in company.owners
    assert company.owners['Test Owner 3'] == 40  # 20% of 300 stocks is 60, 100-60=40 stocks

    # Removing the rest stocks in absolute terms
    company.remove_owner_percentage_absolute(name='Test Owner 3', n_presentages=100, shrink=True)
    assert 'Test Owner 3' not in company.owners

    # Removing stocks when owner does not exist
    with pytest.raises(AssertionError):
        company.remove_owner_percentage_absolute(name='Test Owner 5', n_presentages=10, shrink=True)

    # Adding an owner and removing stocks with no shrinkage
    company.add_owner(name='Test Owner 6', n_stocks=600, expansion=True)
    company.remove_owner_percentage_absolute(name='Test Owner 6', n_presentages=50, shrink=False)
    assert company.owners['Test Owner 6'] == 400  # 50% of 800 stocks is 400, 600-400=200 stocks Then double it to 400 to keep the total number

    # Removing more stocks than an owner has
    with pytest.raises(ValueError):
        company.remove_owner_percentage_absolute(name='Test Owner 6', n_presentages=101, shrink=True)

def test_remove_owner_percentage_relative():
    company = Company(name='Test', n_stocks=100, original_owner='Test Owner 1')

    # Add an owner with 400 stocks
    company.add_owner(name='Test Owner', n_stocks=400, expansion=True)
    assert 'Test Owner' in company.owners
    assert company.owners['Test Owner'] == 400

    # Test removing 25% of stocks
    company.remove_owner_percentage_relative(name='Test Owner', n_percentages=25, shrink=True)
    assert company.owners['Test Owner'] == 300

    # Test removing another 50% of stocks (relative to current stocks)
    company.remove_owner_percentage_relative(name='Test Owner', n_percentages=50, shrink=True)
    assert company.owners['Test Owner'] == 150

    # Test removing owner when percentage is 100
    company.remove_owner_percentage_relative(name='Test Owner', n_percentages=100, shrink=True)
    assert 'Test Owner' not in company.owners

    # Test removing non-existent owner
    with pytest.raises(KeyError):
        company.remove_owner_percentage_relative(name='Non-existent Owner', n_percentages=50, shrink=True)

    # Test removing more than 100% stocks
    company.add_owner(name='Test Owner', n_stocks=400, expansion=True)
    with pytest.raises(ValueError):
        company.remove_owner_percentage_relative(name='Test Owner', n_percentages=110, shrink=True)

    # Test removing less than 0% stocks
    with pytest.raises(ValueError):
        company.remove_owner_percentage_relative(name='Test Owner', n_percentages=-10, shrink=True)

    # Test removing stocks with no owners left
    with pytest.raises(RuntimeError):
        company.remove_owner_percentage_relative(name='Test Owner', n_percentages=100, shrink=True)
        company.remove_owner_percentage_relative(name='Test Owner 1', n_percentages=100, shrink=True)

## Testing transfering of stocks
def test_transfer_stocks(company: Company):
    # Test normal stock transfer
    company.add_owner(name='Test Owner 1', n_stocks=200)
    company.add_owner(name='Test Owner 2', n_stocks=100)
    company.transfer_stocks(donor='Test Owner 1', receiver='Test Owner 2', n_stocks=50)
    assert company.owners['Test Owner 1'] == 150
    assert company.owners['Test Owner 2'] == 150

    # Test stock transfer from owner with insufficient stocks
    company.transfer_stocks(donor='Test Owner 1', receiver='Test Owner 2', n_stocks=200)
    assert 'Test Owner 1' not in company.owners
    assert company.owners['Test Owner 2'] == 300

    # Test stock transfer to a new owner
    company.transfer_stocks(donor='Test Owner 2', receiver='Test Owner 3', n_stocks=100)
    assert company.owners['Test Owner 2'] == 200
    assert company.owners['Test Owner 3'] == 100

    # Test invalid stock transfer
    with pytest.raises(KeyError):
        company.transfer_stocks(donor='Invalid Owner', receiver='Test Owner 2', n_stocks=50)

    # Test stock transfer to self
    with pytest.raises(RuntimeError):
        company.transfer_stocks(donor='Test Owner 2', receiver='Test Owner 2', n_stocks=50)


## Testing history funcitons
def test_owner_history():
    # Adding initial owners and stocks
    company = Company(name='Test', n_stocks=100, original_owner='Test Owner')
    
    # Test for count of stocks
    history_count = company.owner_history('Test Owner', percentage=False)
    assert isinstance(history_count, list)
    assert all(isinstance(h, int) for h in history_count)

    # Test for percentage of stocks (range 0-100)
    history_percentage = company.owner_history('Test Owner', percentage=True, fraction=False)
    assert isinstance(history_percentage, list)
    assert all(isinstance(h, float) for h in history_percentage)
    assert all(0 <= h <= 100 for h in history_percentage)

    # Test for fraction of stocks (range 0-1)
    history_fraction = company.owner_history('Test Owner', percentage=True, fraction=True)
    assert isinstance(history_fraction, list)
    assert all(isinstance(h, float) for h in history_fraction)
    assert all(0 <= h <= 1 for h in history_fraction)

    # Test for non-existing owner
    with pytest.raises(KeyError):
        company.owner_history('Non-existing Owner')