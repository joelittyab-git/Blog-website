import secrets
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import(
        StringField,
        PasswordField,
        EmailField,
        SubmitField,
        BooleanField,
        TelField,
        DateField,
        IntegerField,
        SelectMultipleField,
        TextAreaField,
        MultipleFileField
    ) 
from wtforms.validators import DataRequired, Length, EqualTo, Email, Optional, NumberRange
import os
from backend.Validation import SuperDatabase

class RegistrationForm(FlaskForm):
    
    username_field = StringField(
        label='Username:',
        validators=[
            DataRequired(),
            Length(
                min=5,
                max = 30
            )
        ]
    )
    
    email_field = EmailField(
        label='Email:',
        validators=[
            DataRequired(),
            Email()   
        ]
    )
    
    password_field = PasswordField(
        label='Password:',
        validators=[
            DataRequired(),
            Length(
                min=4,
                max = 30
            )
        ]    
    )
    
    confirm_password_field = PasswordField(
        'Confirm Password:',
        validators=[
            DataRequired(), 
            EqualTo('password_field')
        ]
    )
    
    
    #Excess---------------------
    name = StringField(
        label='Name:',
        validators=[
            DataRequired(),
        ]
    )
    
    telephone = IntegerField(
        label='Telephone No. :',
        validators=[
            Optional(),
            NumberRange(
                min = 1000000000,
                max = 9999999999999
            )
        ]
    )
    
    age = IntegerField(
        label='Age:',
        validators=[
            Optional(),
        ]
    )
    
    dob = DateField(
        label='Date of Birth:',
        validators=[
            Optional(),
        ]
        
    )
    #----------------------------
    
    submit_field = SubmitField(
        label='Sign Up',
    )
    
class LoginForm(FlaskForm):
    email_entry = EmailField(
        label='Email:',
        validators=[
            DataRequired(),
        ]
    )
    
    password_entry = PasswordField(
        label='Password:',
        validators=[
            DataRequired(),
        ]
    )
        
    
    remember_entry = BooleanField(
        label='Remember Me:',
        validators=[
            Optional()
        ]
    )
    
    login_entry  = SubmitField(
        label='Log In'
    )
    
class AccountUpdateForm(FlaskForm):
    username_field = StringField(
        'Username:',
        validators=[
            Optional(),
            Length(
                min=5,
                max=30
            )
        ]
    )
    
    email_field = EmailField(
        'Email:',
        validators=(
            Optional(),
            Email()
        )
    )
    
    profile_img_field = FileField(
        'Profile Image:',
        validators=[
            Optional(),
            FileAllowed(
                upload_set=[
                    '.jpg',
                    '.png'
                ]
            )
        ]    
    )
    
    name = StringField(
        label='Name:',
        validators=[
            Optional(),
        ]
    )
    
    telephone = IntegerField(
        label='Telephone No. :',
        validators=[
            Optional(),
            NumberRange(
                min = 1000000000,
                max = 9999999999999
            )
        ]
    )
    
    update_button = SubmitField(
        'Update'
    )
    
    
class BlogPostForm(FlaskForm):
    title_field = StringField(
        label='Title:',
        validators=[
            DataRequired(),
            Length(
                max=40,
                min = 2
            )
        ]
    )
    
       
    tags_field = StringField(
        label='Category:',
        validators=[
            Optional(),
        ]
    )
    
    
    others_field = StringField(
        label='Category:',
        validators=[
            DataRequired()
        ]
    )


    
    
    images_field = MultipleFileField(
        label='Upload:',
        validators=[
            Optional(),
            FileAllowed(
                [
                    '.png',
                    '.jpg',
                    '.JPG'
                ]
            )
        ]
    )
                                      
    user_tags = StringField(
        label='User Tags:',
        validators=[
            Optional(),
            Length(
                min=0,
                max = 50
            )
        ]
    )

    tagged_topics = StringField(
        label='Topics:',
        validators=[
            Optional(),
            Length(
                min=0,
                max =50
            )
        ]
    )
    
    submit = SubmitField(
        'Post'
    )

class File:
    @staticmethod
    def save_file(app, file):
        rand_hex = secrets.token_hex(8)
        _, ext = os.path.split(file.filename)
        file_nm = rand_hex+ext
        path = os.path.join(
            app.root_path,
            'static/files',
            file_nm
        )
        file.save(path)
        
        return file_nm
        
    
    @staticmethod
    def save_path_to_database(user_email, file_nm):
        
        SuperDatabase.db.update_entry(
            table_name='User',
            search_list_where={
                'email': user_email
            },
            update_list_set={
                'profile_image_url':file_nm,
            }
        )
        
    @staticmethod
    def save_blog_files(user_email,app, files = []):
        
        for file in files:
            
            #Saving the file to the files/blog folder as a custom file name
            file_nm, file_ext = os.path.splitext(file.filename)
            rand_hex = str(secrets.token_hex(5))
            file_nm = file_nm+rand_hex+file_ext
            path = os.path.join(
                app.root_path,
                'static/files/blog',
                file_nm
            )
            file.save(path)
            
            #Saving the file name to the database

            