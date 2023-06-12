from operator import itemgetter
import pandas as pd
from copy import deepcopy

class Company:
    def __init__(self, name:str, original_owner:str=None, n_stocks:int=100) -> None:
        '''
        Initiate a new company with its name, the original owner, and the number of stocks.
        
        Parameters:
        name (str): The name of the company.
        original_owner (str): The name of the original owner of the company.
        n_stocks (int): The number of stocks the original owner has.
        '''
        self.name: str = name
        self._owners: dict = dict()
        self._history: list = []
        if original_owner: 
            self.add_owner(name=original_owner, n_stocks=n_stocks) # Adding the original owner - if it is given

    def __repr__(self):
        '''
        Return a string representation of the Company object.
        
        Returns:
        str: A string representation of the company's name and the current stock owners.
        '''
        n_owners = len(self.owners)
        return f"{self.name}: {n_owners} owner(s)"

    def __str__(self) -> str:
        '''
        Returns a formatted string representation of the Company object including its name, 
        the original owner, the total number of stocks, and the current stock owners 
        along with their percentage ownership. Intended for human reading.
        
        Returns:
        str: A formatted string representation of the Company object.
        '''
        owners_str = ''.join([f" {self._get_owner_percentage(owner):5.2f}% {owner}: {stocks} stocks\n" for owner, stocks in self._ordered_owner_dict().items()])

        return (f"Company '{self.name}'\n"
                f"Total stocks: {self.number_of_stocks}\n"
                f"Current ownership:\n"
                f"{owners_str}")

    def _ordered_owner_dict(self, reverse=True) -> dict:
        '''
        Order the owner dictionary based on the number of stocks each owner has.
        
        Returns:
        dict: A dictionary with owners sorted by their stocks' quantity.
        '''  
        return dict(sorted(self._owners.items(), key=itemgetter(1), reverse=reverse))

    def _get_owner_percentage(self, name:str, multiplicator:float=100) -> float:
        """
        Returns the percentage of company stocks owned by a given owner.

        Parameters:
        name (str): The name of the owner.
        multiplicator (float): The value by which the raw ownership ratio is multiplied. 
                            Default is 100 (i.e., ownership percentage). 
                            For a different scale, adjust this value accordingly.

        Returns:
        float: The percentage (or other scaled value) of stocks owned by the specified owner.

        Raises:
        KeyError: If the specified owner does not exist in the owners dictionary.
        ZeroDivisionError: If the total number of stocks is 0.
        """
        if name not in self._owners:
            raise KeyError(f"{name} is not an owner of this company.")
        
        if self.number_of_stocks == 0:
            raise ZeroDivisionError("The company does not have any stocks.")
            
        return (self._owners[name] / self.number_of_stocks) * multiplicator
    
    def _get_scaled_owner_dict(self, desired_number_of_stocks:int) -> dict:
        """
        Returns a dictionary with each owner's scaled number of stocks.

        Parameters:
        desired_number_of_stocks (int): The total number of stocks to which the current ownership ratios should be scaled.

        Returns:
        dict: A dictionary of owners and their scaled number of stocks.

        Raises:
        AssertionError: If 'desired_number_of_stocks' is not an integer.
        ZeroDivisionError: If the current number of stocks is zero (scaling is impossible).
        """
        assert isinstance(desired_number_of_stocks, int), "'desired_number_of_stocks' must be an integer."

        current_number_of_stocks = self.number_of_stocks
        if current_number_of_stocks == 0:
            raise ZeroDivisionError("The current number of stocks is zero, scaling is impossible.")

        scale_ratio = desired_number_of_stocks / current_number_of_stocks
        new_owners_dict = {name: round(owner_number_of_stocks * scale_ratio)
                        for name, owner_number_of_stocks in self._owners.items()}
        return new_owners_dict

    @property
    def owners(self) -> dict:
        """
        Get the owners of the stocks.

        Returns:
        dict: A dictionary of owners and their respective stocks.
        """
        return self._owners

    @owners.setter
    def owners(self, owners: dict) -> None:
        """
        Set the owners of the stocks.

        Parameters:
        owners (dict): A dictionary of owners and their respective stocks.
        """
        assert isinstance(owners, dict), "'owners' must be a dictionary."
        self._owners = owners
        self._owners_cleanup() # Every time it is updated, it also cleans up
        assert len(self._owners) > 0, "A company cannot be ownerless"

    def _owners_cleanup(self) -> None:
        '''Cleans up the owner dictionary by removing any that has 0 stocks'''
        self._owners = {k:v for k,v in self._owners.items() if v > 0}

    @property
    def history(self) -> list:
        """
        Get the history of stock ownership.

        Returns:
        list: A list of ownership history.
        """
        return self._history

    @history.setter
    def history(self, history: list) -> None:
        """
        Set the history of stock ownership.

        Parameters:
        history (list): A list of ownership history.
        """
        assert isinstance(history, list), "'history' must be a list."
        self._history = list(history)

    def add_to_history(self, event_type: str = '', description: str = '', external_description: str = '') -> None:
        """
        Adds an event to the history.

        Parameters:
        event_type (str, optional): The type of event. Defaults to an empty string.
        description (str, optional): Description of the event. Defaults to an empty string.
        external_description (str, optional): External description of the event. Defaults to an empty string.
        """
        id = len(self.history)
        self._history.append({'id': id, 'event_type': event_type, 'description': description, 'owners': deepcopy(self.owners), 'external_description': external_description})

    @property
    def number_of_stocks(self) -> int:
        """
        Get the total number of stocks.

        Returns:
        int: The total number of stocks.
        """
        return sum(self._owners.values())

    @number_of_stocks.setter
    def number_of_stocks(self, number_of_stocks: int = 1000) -> None:
        """
        Scales the total number of stocks to the desired number based upon the current ownership distribution.

        Parameters:
        number_of_stocks (int, optional): The desired total number of stocks. Defaults to 1000.

        Raises:
        AssertionError: If 'number_of_stocks' is not a positive integer.
        """
        assert isinstance(number_of_stocks, int) and number_of_stocks > 0, "'number_of_stocks' must be a positive integer."
        current_number_of_stocks = self.number_of_stocks
        self.owners = self._get_scaled_owner_dict(desired_number_of_stocks=number_of_stocks)
        self.add_to_history('Rescaling of the total number of stocks', f'{current_number_of_stocks} -> {number_of_stocks}', str(self.owners))


    ## Adding functions
    def add_owner(self, name:str, n_stocks:int, expansion:bool=True, write_history:bool=True, external_description:str='') -> int:
        """
        Modifies the stock count of an owner based on the expansion flag.

        If the owner does not exist, a new owner will be added to the self._owners dict.

        Parameters:
            name (str): The name of the owner.
            n_stocks (int): The number of stocks to be added to or removed from the owner.
            expansion (bool): Flag that indicates the mode of operation.
                            If True, new stocks are added to the owner.
                            If False, the total number of stocks are readjusted (rescaled).
            write_history (bool): Flag to decide if the action should be recorded in history.
            external_description (str): Additional notes about the action to be added to history.

        Returns:
            int: The updated number of stocks the owner has after the operation.

        Raises:
            ValueError: If the desired number of stocks is more than the current total stocks during rescaling.
        """

        if not expansion: # Rescales the current number of stocks
            current_number_of_stocks = self.number_of_stocks
            if n_stocks > current_number_of_stocks: 
                raise ValueError(f'There is not that many stocks: Desired = {n_stocks}, Current total = {current_number_of_stocks}')
            self._owners = self._get_scaled_owner_dict(desired_number_of_stocks=current_number_of_stocks-n_stocks)

        owner_exists = name in self._owners
        owner_current_stocks = self._owners[name] if owner_exists else 0

        self._owners[name] = owner_current_stocks + n_stocks

        if write_history:
            action = 'Adding new owner' if not owner_exists else 'Adding stocks to owner'
            action += ' (expansion)' if expansion else ' (not expansion)'
            self.add_to_history(action, f'{name}: {owner_current_stocks} -> {self._owners[name]}',  external_description)

        self._owners_cleanup() # Cleans up the owners dict

        return self._owners[name]
    
    def add_owners(self, new_owners:dict, expansion:bool=True, write_history:bool=True, external_description:str='') -> int:
        """
        Adds multiple owners with their respective stock counts at the same time. 

        If expansion is True, new stocks are added. If False, the total number of stocks are readjusted.

        Parameters:
            new_owners (dict): Dictionary containing owner names as keys and their corresponding stocks as values.
            expansion (bool): Flag to indicate whether the operation is expansion (adding stocks) or rescaling.
            write_history (bool): Flag to decide if the action should be recorded in history.
            external_description (str): Additional notes about the action to be added to history.

        Returns:
            int: The total number of stocks that were added across all new owners.

        Raises:
            ValueError: If the desired number of stocks is more than the current total stocks during rescaling.
        """

        total_stocks_to_add = sum(new_owners.values())
        current_number_of_stocks = self.number_of_stocks

        if total_stocks_to_add > current_number_of_stocks and not expansion:
            raise ValueError(f'There is not that many stocks: Desired = {total_stocks_to_add}, Current total = {current_number_of_stocks}')

        if expansion:
            owners_dict = self._owners
        else:
            owners_dict = self._get_scaled_owner_dict(desired_number_of_stocks=current_number_of_stocks-total_stocks_to_add)

        for name, stocks in new_owners.items():
            if name in owners_dict: 
                owners_dict[name] += stocks
            else: 
                owners_dict[name] = stocks

        self._owners = owners_dict

        if write_history: 
            expansion_text = 'expansion' if expansion else 'not expansion'
            self.add_to_history(f'Adding multiple owners ({expansion_text})', f'Number of owners: {len(new_owners)}, with a total of {total_stocks_to_add} stocks',  external_description)

        self._owners_cleanup() # Cleans up the owners dict

        return total_stocks_to_add

    def add_owner_percentage(self, name:str, n_percentages:float, expansion=True, write_history=True, external_description:str='') -> int:
        """
        Adds or updates a new owner with a given percentage of the company. 
        If the owner exists, the percentage is added to the current holdings.
        
        Parameters:
            name (str): The name of the owner.
            n_percentages (float): The percentage of the company to be owned. Should be a positive number not exceeding 100.
            expansion (bool): Flag that indicates the mode of operation.
                            If True, the total number of stocks are increased.
                            If False, the total number of stocks are kept constant.
            write_history (bool): Flag to decide if the action should be recorded in history.
            external_description (str): Additional notes about the action to be added to history.

        Returns:
            int: The total number of stocks the owner has after the operation.

        Raises:
            ValueError: If the n_percentages value is not in the range (0, 100].
        """

        if (not 0 < n_percentages <= 100):
            raise ValueError("The percentage should be a positive number not exceeding 100")

        current_number_of_stocks = self.number_of_stocks

        if expansion:
            desired_number_of_stocks = round((n_percentages / 100 * current_number_of_stocks) / (1 - n_percentages / 100))
        else:
            desired_number_of_stocks = round(n_percentages / 100 * current_number_of_stocks)

        return self.add_owner(name, desired_number_of_stocks, expansion, write_history, external_description)

    def add_owners_percentage(self, new_owners: dict, expansion=True, write_history=True, external_description='') -> int:
        """
        Adds multiple owners based on the percentage of the company that they should own.

        Parameters:
            new_owners (dict): A dictionary where the keys are the names of the new owners and the values are the percentages of the company that they should own.
            expansion (bool): If true, it adds the stocks to the current holdings and increase the total number of stocks. If false, it rescales the current number of stocks.
            write_history (bool): If true, the action will be recorded in the history.
            external_description (str): Additional description to be added in the history.

        Returns:
            int: The total number of stocks after the operation.

        Raises:
            ValueError: If the total percentages to add is greater than 100.
        """

        current_number_of_stocks = self.number_of_stocks
        total_percentages_to_add = sum(new_owners.values())

        if total_percentages_to_add > 100:
            raise ValueError('The total percentages to add cannot exceed 100%')

        if expansion: 
            new_dict = self._owners.copy()
            for name, percentage in new_owners.items():
                n_stocks = round( (percentage / 100 * current_number_of_stocks) / (1 - percentage / 100))
                new_dict[name] = new_dict.get(name, 0) + n_stocks
        else: 
            new_dict = self._get_scaled_owner_dict(round(current_number_of_stocks * (1 - total_percentages_to_add / 100)))
            for name, percentage in new_owners.items():
                n_stocks = round(current_number_of_stocks * percentage / 100)
                new_dict[name] = new_dict.get(name, 0) + n_stocks

        self._owners = new_dict

        expansion_txt = 'expansion' if expansion else 'not expansion'
        number_of_owners_to_be_added = len(new_owners)
        total_stocks_added = sum(new_owners.values())
        
        if write_history: 
            self.add_to_history(
                f'Adding multiple owners by percentage ({expansion_txt})', 
                f'Number of owners: {number_of_owners_to_be_added}, with a total of {total_stocks_added} stocks', 
                external_description
            )
            
        self._owners_cleanup()  # Cleans up the owners dict

        return self.number_of_stocks


    ## Removal functions
    def remove_owner(self, name:str, n_stocks:int=None, shrink=True, write_history=True, external_description:str='') -> int:
        """
        Removes an owner or reduces the number of stocks for the owner based on the shrink flag.

        Parameters:
            name (str): The name of the owner.
            n_stocks (int): The number of stocks to be removed from the owner. If not specified, or larger than the current stocks of the owner, the owner is removed.
            shrink (bool): Flag that indicates the mode of operation.
                            If True, the total number of stocks are reduced.
                            If False, the total number of stocks are kept constant (rescaled).
            write_history (bool): Flag to decide if the action should be recorded in history.
            external_description (str): Additional notes about the action to be added to history.

        Returns:
            int: The updated number of stocks the owner has after the operation. If the owner is removed, returns 0.

        Raises:
            KeyError: If the name does not exist in self._owners.
            RuntimeError: If the removal action would result in no owners left.
            ValueError: If the number of stocks to be removed is negative or more than the total stocks owned by the owner.
        """

        if name not in self._owners:
            raise KeyError(f"The owner {name} does not exist in owners")

        if len(self._owners) <= 1:
            raise RuntimeError("There must be at least one owner")

        owner_current_stocks = self._owners[name]
        
        if n_stocks is None or n_stocks >= owner_current_stocks:
            n_stocks = owner_current_stocks
            action = 'Removing owner'
        else:
            if n_stocks < 0:
                raise ValueError("The number of stocks to be removed cannot be negative")
            action = 'Reducing owner\'s stocks'

        original_total_stocks = self.number_of_stocks

        self._owners[name] -= n_stocks

        if self._owners[name] == 0:
            del self._owners[name]

        if not shrink:  # Rescales the current number of stocks
            self._owners = self._get_scaled_owner_dict(desired_number_of_stocks=original_total_stocks)

        action += ' (shrink)' if shrink else ' (no shrink)'
        if write_history:
            self.add_to_history(action, f'{name}: {owner_current_stocks} -> {self._owners.get(name, 0)}',  external_description)

        self._owners_cleanup()  # Cleans up the owners dict

        return self._owners.get(name, 0)

    def remove_owner_percentage_absolute(self, name:str, n_presentages:float=None, shrink=True, write_history=True, external_description:str='') -> int:
        """
        Removes an owner or reduces the number of stocks for the owner based on a percentage in absolute terms.

        Parameters:
            name (str): The name of the owner.
            n_presentages (float): The percentage of stocks to be removed from the owner. If not specified, or larger than the current percentage of the owner, the owner is removed.
            shrink (bool): Flag that indicates the mode of operation.
                        If True, the total number of stocks are reduced.
                        If False, the total number of stocks are kept constant (rescaled).
            write_history (bool): Flag to decide if the action should be recorded in history.
            external_description (str): Additional notes about the action to be added to history.

        Returns:
            int: The updated number of stocks the owner has after the operation. If the owner is removed, returns 0.

        Raises:
            AssertionError: If the name does not exist in self._owners.
            RuntimeError: If the removal action would result in no owners left.
            ValueError: If the number of stocks to be removed is negative or more than 100%.
        """
        assert name in self._owners, f"{name} does not exist in owners"
        
        if n_presentages is not None:
            if n_presentages < 0 or n_presentages > 100:
                raise ValueError("The percentage of stocks to be removed should be between 0 and 100")
            
            if n_presentages >= self._get_owner_percentage(name):
                n_presentages = None  # Triggers the removal of the owner

        if not n_presentages:  # Remove the owner
            return self.remove_owner(name, shrink=shrink, write_history=write_history, external_description=external_description)

        # Calculate the number of stocks to be removed
        stocks_to_remove = round(n_presentages / 100 * self.number_of_stocks)

        # Remove the stocks
        removed_stocks = self.remove_owner(name, stocks_to_remove, shrink=shrink, write_history=write_history, external_description=external_description)

        self._owners_cleanup()  # Clean up the owners dict

        return removed_stocks

    def remove_owner_percentage_relative(self, name:str, n_percentages:float=None, shrink=True, write_history=True, external_description:str='') -> int:
        """
        Removes an owner or reduces the number of stocks for the owner based on a percentage relative to the owner's current number of stocks.

        Parameters:
            name (str): The name of the owner.
            n_percentages (float): The percentage of stocks to be removed from the owner. If not specified, or larger than or equal to 100, the owner is removed.
            shrink (bool): Flag that indicates the mode of operation.
                        If True, the total number of stocks are reduced.
                        If False, the total number of stocks are kept constant (rescaled).
            write_history (bool): Flag to decide if the action should be recorded in history.
            external_description (str): Additional notes about the action to be added to history.

        Returns:
            int: The updated number of stocks the owner has after the operation. If the owner is removed, returns 0.

        Raises:
            KeyError: If the name does not exist in self._owners.
            RuntimeError: If the removal action would result in no owners left.
            ValueError: If the percentage of stocks to be removed is less than 0 or more than 100.
        """
        if not name in self._owners: 
            raise KeyError(f"{name} does not exist in owners")
        
        if n_percentages is not None:
            if n_percentages < 0 or n_percentages > 100:
                raise ValueError("The percentage of stocks to be removed must be in the range of 0 to 100")

        if len(self._owners) <= 1 and n_percentages != 0:
            raise RuntimeError("There must be at least one owner")

        owners_current_number_of_stocks = self._owners[name]

        if not n_percentages or n_percentages >= 100:
            return self.remove_owner(name, shrink=shrink, write_history=write_history, external_description=external_description)

        stocks_to_remove = round(n_percentages / 100 * owners_current_number_of_stocks)

        return self.remove_owner(name, n_stocks=stocks_to_remove, shrink=shrink, write_history=write_history, external_description=external_description)

        
    ## Transfering stocks from one owner to another
    def transfer_stocks(self, donor:str, receiver:str, n_stocks:int, write_history:bool=True, external_description:str='') -> int:
        """
        Transfers stocks from one owner to another.

        If the donor has fewer stocks than the specified number, all of the donor's stocks will be transferred.

        Parameters:
            donor (str): The name of the owner from whom the stocks are transferred.
            receiver (str): The name of the owner to whom the stocks are transferred.
            n_stocks (int): The number of stocks to be transferred.
            write_history (bool): Flag to decide if the action should be recorded in history.
            external_description (str): Additional notes about the action to be added to history.

        Returns:
            int: The actual number of stocks transferred.

        Raises:
            KeyError: If the donor does not exist in owners.
            RuntimeError: If the donor and reciver is the same.
        """

        if donor not in self._owners:
            raise KeyError(f"The donor {donor} does not exist in owners")
        
        if donor == receiver:
            raise RuntimeError(f"The donor and reciver cannot be the same owner ({donor}) ")

        n_trans = min(n_stocks, self._owners[donor])  # The number of stocks to transfer

        self._owners[donor] -= n_trans
        self._owners[receiver] = self._owners.get(receiver, 0) + n_trans

        if self._owners[donor] == 0:
            del self._owners[donor]

        self._owners_cleanup()  # Cleans up the owners dict

        if write_history:
            self.add_to_history('Transfering stocks', f'{donor} -[{n_trans}]-> {receiver}', external_description)

        return n_trans


    ## History related functions
    def owner_history(self, name:str, percentage:bool=True, fraction:bool=False) -> list[int|float]:
        """
        Retrieves the history of a specific owner.

        Parameters:
            name (str): The name of the owner.
            percentage (bool): Flag that decides whether the stock amount should be returned as a percentage. Defaults to True.
            fraction (bool): Flag that decides whether the stock amount should be returned as a fraction of total stocks. Defaults to False.

        Returns:
            list: A list of the owner's history of stocks as counts, percentages, or fractions.

        Raises:
            KeyError: If the name does not exist in the history.
        """

        if not any(name in history_dict['owners'] for history_dict in self.history):
            raise KeyError(f"{name} does not exist in history")
            
        owner_history = []
        for history_dict in self.history:
            owner_dict = history_dict['owners']
            if name in owner_dict:
                stock_count = owner_dict[name]
                if percentage: 
                    total_stock_count = sum(owner_dict.values())
                    if fraction:
                        owner_history.append(stock_count / total_stock_count)
                    else:
                        owner_history.append(stock_count / total_stock_count * 100)
                else:
                    owner_history.append(stock_count)

        return owner_history

    def history_dataframe(self, percentage:bool=True) -> pd.DataFrame:
        """
        Returns the history as a DataFrame.
        
        Parameters:
            percentage (bool): If True, the ownerships are converted to percentages. Default is True.
            
        Returns:
            pd.DataFrame: The history as a DataFrame, with each row being an event in the history.
        """
        # Not tested as it is difficult
        df_base = []

        for history_dict in self.history:
            new_dict = history_dict.copy()  # To avoid modifying the original history_dict
            owners_dict = new_dict.pop('owners', {})  # Extract owners from the dictionary and remove the entry

            if percentage:
                n_total_stocks = sum(owners_dict.values())
                if n_total_stocks != 0:  # To avoid division by zero
                    owners_dict = {k: (v/n_total_stocks) for k,v in owners_dict.items()}

            new_dict.update(owners_dict)
            df_base.append(new_dict)

        return pd.DataFrame(df_base)