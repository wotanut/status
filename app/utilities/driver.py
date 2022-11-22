import sqlite3

class Driver():
    """
    Internal Driver file for use in the database file

    Parameters
    ----------
    table_name : str
        The name of the table to be created
    columns : str
        The columns to be created in the table

    Methods
    -------
    __init__(table_name:str,columns:str) -> None
        Constructor for the Driver class
    create_table(table_name:str,columns:str) -> None
        Creates a table in the database
    insert(columns:str,values:str) -> None
        Inserts a row into the table
    select(columns:str,where:str) -> None
        Selects a row from the table
    update(where:str,columns:list,values:list) -> None
        Updates a row in the table
    delete(where:str) -> None
        Deletes a row from the table
    close() -> None
        Closes the connection to the database

    Returns
    -------
    Driver
        The driver object
    """
    def __init__(self,table_name,columns=""):
        """
        Generates a database object

        Parameters
        ----------
        table_name : str
            The name of the table to be created
        columns : str
            The columns to be created in the table
        """
        self.conn = sqlite3.connect("database.db")
        self.table_name = table_name

        self.create_table(f"{table_name}",f"{columns}")
    
    def create_table(self,table_name,columns):
        """
        Creates a table in the database

        Parameters
        ----------
        table_name : str
            The name of the table to be created
        columns : str
            The columns to be created in the table
        """

        self.conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({columns})")
        self.conn.commit()

    def insert(self,columns,values):
        """
        Inserts a row into the table

        Parameters
        ----------
        columns : str
            The columns to be inserted into
        values : str
            The values to be inserted into the columns
        """
        self.conn.execute(f"INSERT INTO {self.table_name}({columns}) VALUES({values})")
        self.conn.commit()

    def select(self,columns,where=None):
        """
        Selects a row from the table

        Parameters
        ----------
        columns : str
            The columns to be selected from
        Where : str, optional
            The where statement to be used, defualts to None
        """
        if where:
            return self.conn.execute(f"SELECT {columns} FROM {self.table_name} WHERE {where}")
        else:
            return self.conn.execute(f"SELECT {columns} FROM {self.table_name}")

    def update(self,where,columns=[],values=[]):
        """
        Updates a row in the table

        Parameters
        ----------
        where : str
            The where statement to be used
        columns : list, optional
            The columns to be updated, defualts to []
        values : list, optional
            The values to be updated, defualts to []
        """
        if len(columns) != len(values):
            raise Exception("columns and values must be the same length")
        else:
            statement = ""
            for c in columns:
                statement = statement + (f"{c} = {values[columns.index(c)]}")
                if columns.index(c) != len(columns) - 1:
                    statement = statement + ", "
            print(f"UPDATE {self.table_name} SET {statement} WHERE {where}")
        self.conn.execute(f"UPDATE {self.table_name} SET {statement} WHERE {where}")
        self.conn.commit()
    
    def delete(self,where):
        """
        Deletes a row from the table

        Parameters
        ----------
        where : str
            The where statement to be used
        """
        self.conn.execute(f"DELETE FROM {self.table_name} WHERE {where}")
        self.conn.commit()
    
    def close(self):
        """ 
        Closes the connection to the database

        Returns
        -------
        Void
        """
        self.conn.close()