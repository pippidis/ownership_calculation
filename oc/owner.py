

class Owner:
    '''One of the owners of the company'''
    def __init__(self, name:str, presentage:float) -> None:
        self.name = str(name)
        self.presentage = float(presentage)

    def accomidate_new_owner(self, new_owner) -> None:
        '''Modifies the owners presentage by accomidating the new owner'''
        self.presentage = float(self.presentage) * (1-new_owner.presentage/100)

    def accomidate_removal_of_owner(self, removed_owner):
        '''Modifies the presentage by removing another owner'''
        self.presentage = self.presentage + removed_owner.presentage*(self.presentage/100)