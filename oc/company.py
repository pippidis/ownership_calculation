from operator import itemgetter
import pandas as pd

from .owner import Owner

class Company2:
    '''The company that is beeing owned'''
    def __init__(self, name:str, original_owner:str=None, n_stocks:int=100) -> None:
        self._name: str = name
        self._owners: dict = dict()
        self._history: list = []
        if original_owner: 
            self.add_owner(name=original_owner, n_stocks=n_stocks) # Adding the original owner - if it is given

    def __repr__(self): 
        r = f'Company: {self._name} --- # Stocks: {self.number_of_stocks}\nOwners:\n'
        for name, n_stocks in self._ordered_owner_dict().items():
            prs = self._get_owner_presentage(name)
            r+= f' {prs:5.2f} % {name} - {n_stocks}\n'
        return r

    def _ordered_owner_dict(self, reverse=True) -> dict:
        '''Return an ordered version of the owners dict'''
        return dict(sorted(self._owners.items(), key=itemgetter(1), reverse=reverse))

    def _get_owner_presentage(self, name:str) -> float:
        '''Get the ownership presentage for the given owner'''
        return (self._owners[name] / self.number_of_stocks)*100

    def _get_scaled_owner_dict(self, desired_number_of_stocks:int) -> int:
        '''Returns a dict with all the owners with a scaled number of stocks'''
        assert isinstance(desired_number_of_stocks, int) # Must be int
        current_number_of_stocks = self.number_of_stocks
        scale_ratio = desired_number_of_stocks / current_number_of_stocks
        new_owners_dict:dict = {}
        for name, owner_number_of_stocks in self._owners.items():
            new_owners_dict[name] = round(owner_number_of_stocks * scale_ratio)
        return new_owners_dict

    @property
    def owners(self):
        return self._owners
    
    @owners.setter
    def owners(self, v):
        self._owners = v

    @property
    def history(self):
        return self._history
    
    @history.setter
    def history(self, v):
        event_type, description, owners = v
        self._history.append({'id':len(self.history)+1, 'event_type':str(event_type), 'description':description, 'owners':owners})

    @property
    def number_of_stocks(self): 
        return int(sum(self._owners.values()))
    
    @number_of_stocks.setter
    def number_of_stocks(self, number_of_stocks:int=1000): 
        '''Scales the total number of stocks to the the desired number of stocks based upon the current ownership distrobution'''
        assert number_of_stocks > 0 # Must be a non zero amount of stocks
        current_number_of_stocks = self.number_of_stocks
        self.owners = self._get_scaled_owner_dict(desired_number_of_stocks=number_of_stocks)
        self.history = ('Rescaling of the total number of stocks',f'{current_number_of_stocks} -> {number_of_stocks}', self.owners)

    def add_owner(self, name:str, n_stocks:int, expansion=True, write_history=True) -> int:
        '''Adds stocks to the owner. If the owner does not exist, adds that owner'''

        if expansion: # Id it just adds stocks to the end
            if name in self._owners: 
                owner_current_stocks = self._owners[name]
                self._owners[name]+=n_stocks
                if write_history: self.history = ('Adding stocks to owner (expansion)',f'{name}: {owner_current_stocks} -> {self.owners[name]}', self.owners)
                return self._owners[name]
            else: 
                self._owners[name] = n_stocks
                if write_history: self.history = ('Adding new owner (expansion)',f'{name}: 0 -> {self.owners[name]}', self.owners)
                return n_stocks

        # If it is a rescaling of the current number of stocks
        current_number_of_stocks = self.number_of_stocks
        if n_stocks > current_number_of_stocks: raise ValueError(f'There is not that many stocks: Desired = {n_stocks}, Current total = {current_number_of_stocks}')
        new_dict = self._get_scaled_owner_dict(desired_number_of_stocks=current_number_of_stocks-n_stocks)
        if name in self._owners: 
            owner_current_stocks = self._owners[name]
            new_dict[name]+=n_stocks
            self.owners = new_dict
            if write_history: self.history = ('Adding stocks to owner (not expansion)',f'{name}: {owner_current_stocks} -> {self.owners[name]}', self.owners)
            return self._owners[name]
        else: 
            new_dict[name] = n_stocks
            self.owners = new_dict
            if write_history: self.history = ('Adding new owner (not expansion)',f'{name}: 0 -> {self.owners[name]}', self.owners)
            return n_stocks

    def add_owner_presentage(self, name:str, n_presentages:float, expansion=True, write_history=True) -> int:
        '''Adds or updates a new owner with a given presentage of the company. It is added to the current holdings if the owner exist'''
        assert n_presentages > 0
        assert n_presentages <= 100

        current_number_of_stocks = self.number_of_stocks

        if expansion:
            desired_number_of_stocks: int = round( (n_presentages/100*current_number_of_stocks)/(1-n_presentages/100))
            return self.add_owner(name, desired_number_of_stocks, True, write_history)
        
        desired_number_of_stocks: int = round(n_presentages/100 * current_number_of_stocks)
        return self.add_owner(name, desired_number_of_stocks, False, write_history)
        
    def remove_owner(self, name, n_stocks:int=None, shrink=True, write_history=True) -> int:
        '''Removes an owner or removes the given number of stocks form the owner'''
        assert name in self.owners

        if shrink: 
            if not n_stocks or n_stocks >= self.owners[name]:
                owner_current_stocks = self.owners[name]
                del self.owners[name]
                if write_history: self.history = ('Removing owner (shrink)',f'{name}: {owner_current_stocks} -> 0', self.owners)
                return 0
            else: 
                owner_current_stocks = self.owners[name]
                self.owners[name]-= n_stocks
                if write_history: self.history = ('Reducing owners stocks (shrink)',f'{name}: {owner_current_stocks} -> {self.owners[name]}', self.owners)
                return self.owners[name]

        # If there is no shrinking:
        current_number_of_stocks = self.number_of_stocks
        if not n_stocks or n_stocks >= self.owners[name]:
            owner_current_stocks = self.owners[name]
            del self.owners[name]
            self.owners = self._get_scaled_owner_dict(desired_number_of_stocks=current_number_of_stocks)
            if write_history: self.history = ('Removing owner (no shrink)',f'{name}: {owner_current_stocks} -> 0', self.owners)
            return 0
        else: 
            owner_current_stocks = self.owners[name]
            self.owners[name]-= n_stocks
            self.owners = self._get_scaled_owner_dict(desired_number_of_stocks=current_number_of_stocks)
            if write_history: self.history = ('Removing owner (no shrink)',f'{name}: {owner_current_stocks} -> {self.owners[name]}', self.owners)
            return self.owners[name]

    def remove_owner_presentage(self, name, n_presentages:float=None, shrink=True, write_history=True) -> int:
        '''reomves the owner or reduce the number of stocks based on a presentage'''
        assert name in self.owners

        if shrink: 
            if not n_presentages or n_presentages >= self._get_owner_presentage(name):
                return self.remove_owner(name, shrink=True, write_history=write_history)
            else: 
                stocks_to_remove = round(n_presentages/100 * self.number_of_stocks)
                return self.remove_owner(name, stocks_to_remove, shrink=True, write_history=write_history)

        # If there is no shrink: 
        if not n_presentages or n_presentages >= self._get_owner_presentage(name):
            return self.remove_owner(name, shrink=False, write_history=write_history)
        stocks_to_remove = round(n_presentages/100 * self.number_of_stocks)
        return self.remove_owner(name, stocks_to_remove, shrink=False, write_history=write_history)

    def remove_owner_presentage_relative(self, name, n_presentages:float=None, shrink=True, write_history=True) -> int:
        '''reomves the owner or reduce the number of stocks based on a presentage relative to the owners current number of stocks'''
        assert name in self.owners
        owners_current_number_of_stocks = self.owners[name]
        
        if shrink: 
            if not n_presentages or n_presentages >= 100:
                return self.remove_owner(name, shrink=True, write_history=write_history)
            else: 
                stocks_to_remove = round(n_presentages/100 * owners_current_number_of_stocks)
                return self.remove_owner(name, stocks_to_remove, shrink=True, write_history=write_history)

        # If there is no shrink: 
        if not n_presentages or n_presentages >= 100:
            return self.remove_owner(name, shrink=False, write_history=write_history)
        stocks_to_remove = round(n_presentages/100 * owners_current_number_of_stocks)
        return self.remove_owner(name, stocks_to_remove, shrink=False, write_history=write_history)

    def add_owners(self, new_owners:dict, expansion=True, write_hisory=True) -> int:
        '''Adds multiple owners at the same time. This is so that the number of stocks stays the same'''
        number_of_stocks_to_add_total = int(sum(new_owners.values()))
        current_number_of_stocks = self.number_of_stocks
        if number_of_stocks_to_add_total > current_number_of_stocks and not expansion: 
            raise ValueError(f'There is not that many stocks: Desired = {n_stocks}, Current total = {current_number_of_stocks}')
        
        if expansion:
            new_dict = self.owners
        else: 
            new_dict = self._get_scaled_owner_dict(desired_number_of_stocks=current_number_of_stocks-number_of_stocks_to_add_total)
        
        for name, n_stocks in new_owners.items():
            if name in new_dict: 
                new_dict[name]+= n_stocks
            else: 
                new_dict[name] = n_stocks
        self.owners = new_dict
        expansion_txt = 'expansion' if expansion else 'not expasion'
        number_of_owners_to_be_added = int(len(new_owners))
        if write_hisory: self.history = (f'Adding multiple owners ({expansion_txt})', f'Number of owners: {number_of_owners_to_be_added}, with a total of {number_of_stocks_to_add_total} stocks', self.owners)
        return number_of_stocks_to_add_total

    def add_owners_presentage(self, new_owners:dict, expansion=True, write_hisory=True) -> int:
        '''Adds owner based on the presentage of the company that they should own.'''
        # It funcitons by converting the presentage based dict to a number of stocks based dict
        current_number_of_stocks = self.number_of_stocks
        total_presentages_to_add = sum(new_owners.values())
        
        if expansion: 
            total_number_of_stocks = round( ((total_presentages_to_add/100)*current_number_of_stocks)/(1-total_presentages_to_add/100))
            new_dict = self.owners
            for name, n_presentages in new_owners.items():
                if name in new_dict: 
                    new_dict[name] += round( (n_presentages/100*current_number_of_stocks)/(1-n_presentages/100))
                else: 
                    new_dict[name] = round( (n_presentages/100*current_number_of_stocks)/(1-n_presentages/100))
        else: 
            total_number_of_stocks = round(current_number_of_stocks * total_presentages_to_add/100)
            new_dict = self._get_scaled_owner_dict(round(current_number_of_stocks * (1-total_presentages_to_add/100)))
            for name, n_presentages in new_owners.items():
                if name in new_dict: 
                    new_dict[name] += round(current_number_of_stocks*n_presentages/100)
                else: 
                    new_dict[name] = round(current_number_of_stocks*n_presentages/100)

        self.owners = new_dict

        expansion_txt = 'expansion' if expansion else 'not expasion'
        number_of_owners_to_be_added = int(len(new_owners))
        if write_hisory: self.history = (f'Adding multiple owners by presentage ({expansion_txt})', f'Number of owners: {number_of_owners_to_be_added}, with a total of {total_number_of_stocks} stocks', self.owners)
        return total_number_of_stocks

    def owner_history(self, name:str, presentage=True) -> list:
        '''Returns a list of the hisory of owner'''
        oh = []
        for history_dict in self.history:
            owner_dict = history_dict['owners']
            if name in owner_dict:
                n_stocks = owner_dict[name]
                if presentage: 
                    n_stocks_total = int(sum(owner_dict.values()))
                    oh.append(n_stocks/n_stocks_total)
                else:
                    oh.append(n_stocks)
        return oh
    
    def history_dataframe(self, presentage:bool=True): 
        '''Returns the history as a dataframe'''
        df_base = []
        for history_dict in self.history:
            owners_dict = history_dict['owners']
            d = history_dict
            del d['owners']
            if presentage:
                n_total_stocks = int(sum(owners_dict.values()))
                owners_dict = {k: (v/n_total_stocks) for k,v in owners_dict.items()}
            d.update(owners_dict)
            df_base.append(d)
        return pd.DataFrame(df_base)