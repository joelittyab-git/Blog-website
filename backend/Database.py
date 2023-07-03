from mysql.connector import connect
from backend.Console import Pen
import re


class database:
    
    '''
    >> Instance Variables
    -> self.__cursor
    -> self.__connection
    '''
    def __init__(
        self,
        username = 'root',
        password = 'Tiger@123',
        database = 'utilities_website_db'
    ):
        self.__database = database
        
        self.__connection = connect(
            username = username,
            password = password,
            database = database
        )
        
        if(not self.__connection):
            Pen.print_red('()-->> A successful connection to the server was FAILED to be made.')
            Pen.print_red('()-->> Recheck the password and username fields.')
        else:
            Pen.print_green('()-->> A connection to the server was SUCCESSFULLY made.')
            self.__makecursor()
            
            
            
    #returnda list of tables in tuples
    def get_tables(
        self
    ):
        
        query = 'SHOW TABLES;'
        self.__cursor.execute(query)
        tbl_list = self.__cursor.fetchall()
        
        Pen.print_yellow('List of tables:')
            
        return tbl_list
    
    def get_table_data(
        self,
        table_name = 'User'
    ):
        query = f'SELECT * FROM {table_name};'
        self.__cursor.execute(query)
        return self.__cursor.fetchall()
        
        
            
    def describe_table(
        self,
        table_name
    ):
        tb_name = str(table_name).lower()
        flag = False
        
        for tb in self.get_tables():
            if(tb[0]==tb_name):
                flag = True
                query=f'DESCRIBE {tb_name};'
                self.__cursor.execute(query)
                
                result = self.__cursor.fetchall()
        if flag==False:
            Pen.print_yellow(f'{tb_name} able not found')
        else:    
            for data in result:
                print(data)
            
    
    #Method to add a new row to the desired table
    def add_entry(
        self,
        table_name = 'User',
        data_list={}
    ):
        #Formatting the query string
        query = f'INSERT INTO {table_name.strip()} \n VALUES ('
        column_list = self.__gettablecolumns(
            tablename=table_name
        )
        
        #Adding the column data into the query string
        
        for column in column_list:     
            try:
                                    
                if (type(data_list[column]) is int or type(data_list[column]) is float or data_list[column][-2:]=='()'):
                    query += f'{data_list[column]} ,'                   
                else:
                    query += f'"{str(data_list[column]).strip()}" ,'
            except Exception as e:
                raise Exception(f'()-->> Error inserting the passed data: \n{data_list}' + str(e))
            
                    
        #Formatting the query string
        query = query[:-1]
        query += ');'
            
            
        self.__cursor.execute(query)
        self.__connection.commit()
            
        Pen.print_green('()-->> Data successfully inserted')
            
    '''
    returns the entry that satisfies all the given conditions in the data_list
    return None is no user is found,
    returns the user if the user is found, 
    returns only the first occurence of the user satisfying the conditions
    '''
    def get_row(
        self,
        table_name = 'User',
        data_list = {}
    ):
        query = f'SELECT * FROM {table_name} WHERE'
        
        for data in data_list:
            # list out keys and values separately
            key_list = list(data_list.keys())
            val_list = list(data_list.values())
            
            # print key with val 100
            position = val_list.index(data_list[data])
            
            if (type(data_list[data]) is int or type(data_list[data]) is float or data_list[data][-2:]=='()'):
                    query += f" {str(key_list[position]).strip()} = {data_list[data]} AND"                   
            else:
                query += f' {str(key_list[position])} = "{str(data_list[data]).strip()}" AND'
        
        query = query[:-3] +";"
        
        self.__cursor.execute(query)
        x = self.__cursor.fetchall()
        
        if(len(x) == 0):
            Pen.print_red('()-->> This user does not exist in the database')
            return None
        return x[0]
    
    '''
    returns all the list of entries that satisfies any of the conidtions in the data_list
    '''
    def get_row_OR(
        self,
        table_name = 'User',
        data_list = {}
    ):
        query = f'SELECT * FROM {table_name} WHERE'
        
        for data in data_list:
            # list out keys and values separately
            key_list = list(data_list.keys())
            val_list = list(data_list.values())
            
            # print key with val 100
            position = val_list.index(data_list[data])
            
            if (type(data_list[data]) is int or type(data_list[data]) is float or data_list[data][-2:]=='()'):
                    query += f" {str(key_list[position]).strip()} = {data_list[data]} OR"                   
            else:
                query += f' {str(key_list[position])} = "{str(data_list[data]).strip()}" OR'
        
        query = query[:-3] +";"
        
        self.__cursor.execute(query)
        x = self.__cursor.fetchall()
        
        if(len(x) == 0):
            Pen.print_red('()-->> This user does not exist in the database')
            return None
        return x

        
        
    
    #A method to check if an entry occurs in the table based on the clolumn'
    '''
    data_list dict accepetion values based on the clolumn
    -key- --> column name
    -values- --> data to check if the exiast in the table
    **If any of the values in the dictionary list is satisfied reeturn True**
    '''
    def entry_exists(
        self,
        data_list = {},
        table_name = 'User' 
    ):
        val = True
        table_name = table_name.strip()
        
        for data in data_list:
            data = data.strip()
            #Executing query to check the desired condition
            try:
                if(type(data_list[data]) is int or type(data_list[data]) is float or str(data_list[data].strip()[-2:])=='()'):
                    check_query = f'SELECT * FROM {table_name} WHERE {data} = {data_list[data]};'
                elif(type(data_list[data]) is str):
                    check_query = f'SELECT * FROM {table_name} WHERE {data} = "{data_list[data].strip()}";'
                else:
                    Pen.print_red('()-->> Invalid datatype passed to table')
                    break
                self.__cursor.execute(check_query)
            except Exception as e:
                Pen.print_red(e)
                raise Exception(f'\n {e}')
            
            #Check the fetchall for !empty-list
            if(not self.__cursor.fetchall()):
                val = False
                break
            
            
        return val
                
    '''
    updates all the fields that is the satisied in the search list-->> If any condition in the search list satisfes the row, then the entry is altered
    with the new value in the update list
    '''
     
    def update_entry(
        self,
        table_name = 'User',
        search_list_where = {},
        update_list_set = {},
    ):
        query = f'UPDATE {table_name} SET'
        
        key_list = list(update_list_set.keys())

        
        #set query loop
        for key in  key_list:
            if(type(update_list_set[key]) is int or type(update_list_set[key]) is float or update_list_set[key][-2:]=='()' ):
                query += f' {key} = {update_list_set[key]},'
            else:
                query += f' {key} = "{update_list_set[key]}",'
                
                
        query = query[:-1] + " "     
        query+= 'WHERE '
        key_list = list(search_list_where.keys())
        
        #where query loop
        for key in key_list:
            if(type(search_list_where[key]) is int or type(search_list_where[key]) is float or search_list_where[key][-2:]=='()' ):
                query += f' {key} = {search_list_where[key]} OR '
            else:
                query += f' {key} = "{search_list_where[key]}" OR '
            
        query = query[:-3] 
        
        #Executing query
        try:
            print(query)
            self.__cursor.execute(query  +";")
        except Exception as e :
            raise Exception(e)
        self.__connection.commit()
        
            
    def generate_p2k(
        self,
        table = 'User'
    ):
        column_index = -1
        pk_clmn = str(self.get_primary_key_column(table_name=table))
        table_columns = self.__gettablecolumns(tablename=table)

        for x in range (len(table_columns)):
            if(table_columns[x] == str(pk_clmn)):
                column_index = x
                break
            
        if(column_index == -1):
            Pen.print_red('()-->> Primary Key not found')
            raise Exception('While searching the table for primary key, it wasnt found')

        else:
            return(
                self.get_table_data(
                    table_name=table
                    )[
                        len(self.get_table_data(
                        table_name=table)) - 1
                    ][column_index] + 1
            )
            
        
    def execute_query(
        self,
        query
    ):
        try:
            self.__cursor.execute(str(query))
            return self.__cursor.fetchall()
        except Exception as e:
            Pen.print_red('()-->> Failed to execute query'+str(e))
        
        
    def get_currentdate_query(self):
        return 'CURDATE()'

    def get_primary_key_column(
        self,
        table_name  = 'User'
    ):
        return self.execute_query(f'''SHOW INDEX FROM {table_name}  
             WHERE Key_name = 'PRIMARY';  ''')[0][4]
        
        
    #----Database=Connection-Methods---------------------------------------------------------------------------------------------------------------------
    def shut_database_conection(self):
        try:
            self.__cursor.close()
            self.__connection.close()
        except Exception as e:
            Pen.print_red('()-->> Something went wrong')
            Pen.print_red(e)
            raise Exception()
        
        if (not self.__connection.is_connected()):
            Pen.print_green('()-->> Conenction to the database succerssfuly shutdown.')
            self = None
        else:
            Pen.print_red('()-->> Disconnection from the server was unsuccessfull.')
            
            
    def get_connection_status(self):
        try:
            return self.__connection.is_connected()
        except:
            return False
    
    def reestablish_connection(self):
        self = None
        self = self.__init__(
            username = 'root',
            password = 'Tiger@123',
            database = 'utilities_website_db'
        )
        
        
    #----Private-Memebers---------------------------------------------------------------------------------------------------------------------
    def __makecursor(self):
        self.__cursor = self.__connection.cursor()
        
    def __gettablecolumns(
        self,
        tablename = 'User'
    ):
        query = f'DESCRIBE {tablename}'
        self.__cursor.execute(query)
        columns_data = self.__cursor.fetchall()
        
        data_list = []
        
        for column in columns_data:
            data_list.append(column[0])
        
        return data_list
       
    #Returns a list of tables  
    def __gettables(self):
        query = f'SHOW TABLES'
        self.__cursor.execute(query)
        
        tables = self.__cursor.fetchall()
        table_list = []
        
        for table in tables:
            table_list.append(table[0])
            
        return table_list
    
    def _get_password(
        self,
        user_row,
        table_name = 'User',    
    ):
        table_name = table_name.strip()
        columns = self.__gettablecolumns(tablename=table_name)
        index = -1
        for x in range(len(columns)):
            if(re.findall('password$', columns[x]) or re.findall('pswrd$', columns[x])):
                index = x
        if(index == -1):
            Pen.print_red('()-->> No password field found for user')
            return None
        else:
            return user_row[index]