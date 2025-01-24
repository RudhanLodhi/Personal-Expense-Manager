import pandas as pd

class Manager():
    def __init__(self):

        try:
            self.data = pd.read_csv('DATA.csv')
            self.total = self.data['Ammount'].sum()
        except:
            self.data = pd.DataFrame(columns=['Ammount', 'Date', 'Category', 'Notes'])
            self.data["Date"] = pd.to_datetime(self.data["Date"])
            self.total = 0

    #-------------------Getters------------------------------

    def get_Dataframe(self):
        '''
        Returns
        -------
        type: Pandas Dataframe
            Returns the DataFrame.
        '''
        return self.data
    
    def get_Amount_Category(self,cat:str) -> int:
        '''
        Returns the total amount for a given category.

        Parameters
        ----------
        parameter1 : Category (cat)
            name of the category

        Returns
        -------
        type: Int
            Sum of all the amount in that Category
        '''
        try:
            return self.data[self.data['Category'] == cat]['Ammount'].sum()
        except:
            print("No such Category Found!")
            return 0

  
    def get_Amount_Date(self, start=None, end=None):
        '''
        Returns the total amount for a given Date range.

        Parameters
        ----------
        start : str or pd.Timestamp
            Start date from which the amount will be summed.
            Default is the least recent entry added (min date).
        end : str or pd.Timestamp, optional
            End date to which the amount will be summed.
            Default is the most recent entry added (max date).

        Returns
        -------
        type: Int
            Sum of all the amount within the date range.
        '''

        
        if start:
            start_date = pd.to_datetime(start)
        else:
            start_date = self.data['Date'].min()

        if end:
            end_date = pd.to_datetime(end)
        else:
            end_date = self.data['Date'].max()

        if start_date > end_date:
            print("Invalid Date")
            return 0  

        filtered = self.data[(self.data['Date'] >= start_date) & (self.data['Date'] <= end_date)]
        return filtered['Ammount'].sum()
    
    #-----------------------Filters--------------------------
    
    def sort_by_Date(self,ascnding=True):
        '''
        Sorts the data by date in ascending or deseding order.
        Parameters
        ----------
        ascnding : bool 
            True means ascending, False means desending
        '''
        self.data.sort_values(by='Date', inplace=True, ascending=ascnding)
    
    def sort_by_cat(self):
        '''
        Sorts the data by date in ascending by category.
        Parameters
        ----------
        ascnding : bool 
            True means ascending, False means desending
            Default is True
        '''
        self.data.sort_values(by='Category', inplace=True, ascending=True)
    
    def sort_by_Amount(self,ascnding=True):
        '''
        Sorts the data by date in ascending by category.
        Parameters
        ----------
        ascnding : bool 
            True means ascending, False means desending
            Default is True
        '''
        self.data.sort_values(by='Ammount', inplace=True, ascending=ascnding)

    #-----------------------------Main functions------------------------

    def add_entry(self,amount, date, cat, notes) -> None:
        '''
        Adds a new entry to the data.

        Parameters
        ----------
        Amount : int 
            Amount spent that will be added to dataframe
        Date: str or pd.Timestamp
            Date of the transcation
        Cat: str
            Category of the expense
        notes: str
            Any additional info or description for the transcation
        '''
        date = pd.to_datetime(date)
        new = {'Ammount': amount, 'Date': date, 'Category': cat, 'Notes': notes}
        self.data = pd.concat([self.data, pd.DataFrame([new])], ignore_index=True)
    
    def export(self):
        '''
        Exports the data to a csv file.
        '''
        self.data.to_csv('data.csv', index=False)