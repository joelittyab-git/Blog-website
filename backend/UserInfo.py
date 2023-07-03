from backend.Validation import SuperDatabase
from backend.Database import database
from random import randint
class Data(SuperDatabase):
    @staticmethod
    def get_user_blogs_posted(session_email):
        if(SuperDatabase.db is None or SuperDatabase.db.get_connection_status() is False):
            SuperDatabase.db = database(
                username='root',
                password='Tiger@123',
                database='utilities_website_db'
            )
        
        user_id = SuperDatabase.db.get_row(
            table_name='User',
            data_list={
                'email':session_email
            }
        )[0]
        
        if(SuperDatabase.db.get_row_OR(
                    table_name='Blog',
                    data_list={
                        'user_id':user_id
                    }
                ) is None):
            return 0
        else:
    
        
            return len(
                SuperDatabase.db.get_row_OR(
                    table_name='Blog',
                    data_list={
                        'user_id':user_id[0]
                    }
                )
            )
            
    @staticmethod
    def get_following_categories(session_email):
        return SuperDatabase.db.get_row(
            table_name='User',
            data_list={
                'email':session_email
            }
        )[9]
        
    @staticmethod
    def get_user_age(session_email):
        return randint(16,44)
    
    @staticmethod
    def get_username(session_email):
        return SuperDatabase.db.get_row(
            table_name='User',
            data_list={
                'email':session_email
            }
        )[1]
        
    @staticmethod
    def get_user_profile_img(session_email):
        return SuperDatabase.db.get_row(table_name = 'User', data_list = {'email':session_email})[4]
    
    @staticmethod
    def get_current_date():
        raw_date =  SuperDatabase.db.execute_query('SELECT CURDATE();')
        fmt_date = raw_date[0][0]
        
        return fmt_date
    
    @staticmethod 
    def get_blog_categories():
        category_list = []
        db_list = SuperDatabase.db.get_table_data(table_name = 'category_list')
        
        for item in db_list:
            category_list.append(item[0])
            
        return category_list
    
    