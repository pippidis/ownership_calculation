import os
import sys
import pytest

# TO RUN: python -m pytest --cov

# Creates the paths for the testing environment.
local_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(local_path, '..'))

# The classes
from company_ownership import Company

@pytest.fixture(scope="module")
def company():
    c = Company(name='Test', n_stocks=100, original_owner='Test Owner 1')
    c.add_owner(name='Test Owner 2', n_stocks=100, expansion=True)
    return c 