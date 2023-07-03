from backend.Database import database
from flask_bcrypt import Bcrypt
    

class SuperDatabase():
    db = database(
        username='root',
        password='Tiger@123',
        database='utilities_website_db'
    )
    
    encrypt = Bcrypt()
    
        

class Register(SuperDatabase):
    
    
    '''
    Returns true or false based on the username and email provided 
    *CASE:
    :0: ->> desired case => validation successful
    :1: ->> => The password enetered by the user is invlaid
    :2: ->> => The username enetered by the user is already in use
    :3: ->> => The email enetered by the user is already in use
    '''
    @staticmethod
    def register(
        username,
        password,
        email,
        name = "",
        profile_img_url = "default.jpg",
        phone_number = ""
    ):
        #initializing
        username = str(username)
        password = str(password)
        email = str(email)
        name = str(name)
        profile_img_url = str(profile_img_url)
        
        #initializing database connection
        if(__class__.db == None or not __class__.db.get_connection_status()):
            SuperDatabase.db = database(
                username='root',
                password='Tiger@123',
                database='utilities_website_db'
            )
        
        
        
        x = Register.__validate_registration(
            username=username,
            password=password,
            email=email,
            name=name,
        ) 
        
        if(
            x == 0
        ):
            Register.db.add_entry(
                table_name='User',
                data_list={
                    'user_id':Register.db.generate_p2k(table='User'),
                    'username':username,
                    'password':(Register.__hash_password_utf8(password)),
                    'email':email,
                    'is_active':0,
                    'profile_image_url': profile_img_url,
                    'join_date':Register.db.get_currentdate_query(),
                    'name':name,
                    'phone_no':phone_number,
                    'following_categories':0
                }
            )
        
        return x
    
    #A method for regsitration validation
    '''
    *CASE:
    :0: ->> desired case => validation successful
    :1: ->> => The password enetered by the user is invlaid
    :2: ->> => The username enetered by the user is already in use
    :3: ->> => The email enetered by the user is already in use
    '''
    @staticmethod
    def __validate_registration(
        username,
        password,
        email,
        name,
    ):
        if(Register.__validate_email(email)):
            if(Register.__validate_username(username)):
                if(Register.__validate_password(password)):
                    return 0
                else:
                    print('Enter a valid password')
                    return 1
            else:
                 print('This username is already in use , pease select another')
                 return 2   
        else:
            print('This email is already in use , pease use another')
            return 3
        
    @staticmethod        
    def __validate_email(email):
        return not (
           SuperDatabase.db.entry_exists(
                data_list={
                    'email': email
                },
                table_name='User'
            )
            
        )
        
    @staticmethod
    def __validate_password(passowrd):
        return True
        
    def __validate_username(username):
        return not (
           SuperDatabase.db.entry_exists(
                data_list={
                    'username': username
                },
                table_name='User'
            )
        )
    
    @staticmethod
    def __hash_password_utf8(password):        
        hashed_user_password_utf8 =  Register.encrypt.generate_password_hash(password).decode('utf-8')
        return hashed_user_password_utf8
    
    
    
    
class Login(SuperDatabase):
    
    @staticmethod
    def login(
        email,
        password
    ):
        if(__class__.db == None or not __class__.db.get_connection_status()):
            SuperDatabase.db = database(
                username='root',
                password='Tiger@123',
                database='utilities_website_db'
            )
            
        return Login.validate_login(email, password)
        
    
    
    @staticmethod
    def validate_login(
        email,
        password
    ):
        user_login_request = Login.__validate_email(email)
        
        if(user_login_request is not None):
            if(__class__.__validate_password(
                 user_login_request,password=password
                )
            ):
                return True
            else:
                return False
        else:
            return False
            
        
    
    @staticmethod  
    def __validate_email(email):
        return __class__.db.get_row(
            table_name='User',
            data_list={
                'email': email
            }
        )
        
    @staticmethod
    def __validate_password(user,password):
        true_hashed_pwd_utf8 = __class__.db._get_password(
            table_name='User',
            user_row=user
        )        
        
        return __class__.encrypt.check_password_hash(true_hashed_pwd_utf8, password)
    
    @staticmethod
    def __check_hashed_password(hashed_password, entered_password):
        return Register.encrypt.check_password_hash(pw_hash=hashed_password, password=entered_password)
    
    
class UpdateAccount(SuperDatabase):
    
    #A method for account update validation
     
     
    '''
    *CASE:
    :(1, 1): ->> desired case => validation successful
    :(0, 1): ->> => The email entered by the user is already in use
    :(1(or)2, 0): ->> => The username enetered by the user is already in use
    :(2, 1): ->> Desired Case => The meail has changed and therefor the session has to be updated
    :(0, 0): ->>=> The email and the username has been taken
    '''
     
    @staticmethod
    def update_account(
        user_email_session,
        username,
        email,
        name,
        phone_no,
        profile_img = None,
    ):
        
        phone_no = str(phone_no)
        x = 1
        y = 1
        if(__class__.db == None or not __class__.db.get_connection_status()):
            SuperDatabase.db = database(
                username='root',
                password='Tiger@123',
                database='utilities_website_db'
            )
            
        #Checks if the entries are empty, none or defualt
        if(not (name is None
           or name.strip() == ""
           or name ==  
            __class__.db.get_row(
                    table_name='User',
                    data_list={
                        'email':user_email_session
                    }
                )[7])
           ):
            __class__.__update_name(user_email_session,str(name).strip())
            
        if(not (phone_no is None
           or phone_no.strip() == ""
           or phone_no ==  
            __class__.db.get_row(
                    table_name='User',
                    data_list={
                        'email':user_email_session
                    }
                )[8]
            or phone_no.strip() =='None')
           ):
            __class__.__update_phone(user_email_session,phone_no)
            
        if(not (username is None
           or username.strip() == ""
           or username ==  
            __class__.db.get_row(
                    table_name='User',
                    data_list={
                        'email':user_email_session
                    }
                )[1])
           ):
            y = __class__.__update_username(user_email_session,str(username).strip())
            
        if(not (email is None
           or email.strip() == ""
           or email ==  
            __class__.db.get_row(
                    table_name='User',
                    data_list={
                        'email':user_email_session
                    }
                )[3])
           ):
            x = __class__.__update_email(user_email_session,str(email).strip())
            
        return (x,y)
        
    
    @staticmethod
    def __update_email(user_email_session, new_email):
        
        if(not (
                __class__.db.entry_exists(
                    table_name='User',
                    data_list={
                        'email':new_email
                    }
                )
            )
        ):
        
            __class__.db.update_entry(
                table_name='User',
                search_list_where={
                    'email':user_email_session
                },
                update_list_set={
                    'email':new_email
                }
            )
            
            return 2
            

        return 0 
        
    @staticmethod
    def __update_username(user_email_session, new_username):
        
        if( not(
                __class__.db.entry_exists(
                    table_name='User',
                    data_list={
                        'username':new_username
                    }
                )
            )
        ):
        
            __class__.db.update_entry(
                table_name='User',
                search_list_where={
                    'email':user_email_session
                },
                update_list_set={
                    'username':new_username
                }
            )
            return 1
         
        return 0
        
    @staticmethod
    def __update_phone(user_email_session, new_phone):
        __class__.db.update_entry(
            table_name='User',
            search_list_where={
                'email':user_email_session  
            },
            update_list_set={
                'phone_no':str(new_phone)
            }
        )
        
    @staticmethod
    def __update_name(user_email_session, new_name):
        __class__.db.update_entry(
            table_name='User',
            search_list_where={
                'email':user_email_session  
            },
            update_list_set={
                'name':str(new_name)
            }
        )