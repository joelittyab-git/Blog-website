import flask
from flask import Flask, flash, render_template, redirect, request, session
from flask import url_for
from forms import RegistrationForm, LoginForm, AccountUpdateForm,BlogPostForm, File
from init import app,parent_db,sess,socket
from backend.Validation import Register, Login, UpdateAccount
from backend.Database import database
from backend.UserInfo import Data
from backend.__credentials import (
    USERNAME,
    PASSWORD,
    DATABASE
    
)
site_initial = 'Dot.IO | '
sess.init_app(app)


@app.route('/')
@app.route('/home')
def open_homepage():
    return render_template(
        'home.html',
        title = f'{site_initial}Home'
    )
    
@app.route(
    '/register',
    methods = [
        'GET',
        'POST'
    ]
)
def open_registrationpage():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            x = Register.register(
                    username=form.username_field.data,
                    password=form.password_field.data,
                    email=form.email_field.data,
                    name = form.name.data,
                    phone_number=9606820419
                )
            if(
                x==0
            ):
                flash(f'Account created for {form.username_field.data}!', 'success')
                return redirect(url_for('open_loginpage'))
            elif(
                x==1
            ):
                flash(f'Please use a unique email adress or username or password for the regsitration.', 'danger')
                return render_template(
                    'register.html',
                    title=f'{site_initial}Register',
                    form=form,
                    password_invalidity = 'Invalid password'
                )
                
            elif(
                x==2
            ):
                flash(f'Please use a unique email adress and username or password for the regsitration.', 'danger')
                return render_template(
                    'register.html',
                    title=f'{site_initial}Register',
                    form=form,
                    username_invalidity = 'This username is already in use.'
                )
                
            else:
                flash(f'Please use a unique email adress and username for the regsitration.', 'danger')
                return render_template(
                    'register.html',
                    title=f'{site_initial}Register',
                    form=form,
                    email_invalidity = 'This email is already in use.'
                )
                
        except Exception as e:
            raise e

    return render_template('register.html', title=f'{site_initial}Register', form=form)
    
@app.route(
    '/login',
    methods = [
        'GET',
        'POST'
    ]   
)
def open_loginpage():
    form = LoginForm()
    
    
    parent_db.reestablish_connection()
    if form.is_submitted():
        if(form.email_entry.data =="" or form.password_entry.data==""):
            return render_template(
                'login.html',
                form = form,
                title = f'{site_initial}Login',
                failed_login = True,
            )
        elif(
            Login.login(
                email=form.email_entry.data,
                password=form.password_entry.data
            )
        ):
            db = database(
                username=USERNAME,
                password=PASSWORD
            )
            flash(f'''Logged in as
                  {db.get_row(
                      table_name='User',
                      data_list={
                          'email':form.email_entry.data.strip()
                      }
                  )[1]}
                  ''',
                  category='success'
                )
            session['email'] = form.email_entry.data
            return redirect(url_for('open_homepage'))
        else:
            return render_template(
                'login.html',
                form = form,
                title = f'{site_initial}Login',
                failed_login = True
            )
        
    return render_template(
        'login.html',
        form = form,
        title = f'{site_initial}Login',
        failed_login = False
    )
    
    
@app.route(
    '/my-account',
    methods =[
        'GET',
        'POST'
    ]
)
def open_accountsupdatepage():
    global parent_db
    form = AccountUpdateForm()
    
    parent_db = None
    parent_db = database(
        username=USERNAME,
        password=PASSWORD,
    )
    
    #Checks is the user is logged in
    if(session.get('email') == None):
        flash(
            message='You will have to login first to view your account.',
            category='danger'
        )
        return redirect(
            url_for('open_loginpage')
        )
        
    if(request.method == 'GET'):
        
        parent_db = None
        parent_db = database(
            
        )
        form.email_field.data = parent_db.get_row(
            table_name='User',
            data_list={
                'email':session.get('email'),
            }
        )[3]
        
        form.username_field.data = parent_db.get_row(
            table_name='User',
            data_list={
                'email':session.get('email'),
            }
        )[1]

        return render_template(
            'updateaccount.html',
            title = f'{site_initial}Update Account',
            form = form,
            db = parent_db
            )
    elif form.is_submitted():
        #raise Exception()
        if(form.profile_img_field.data):
            #saving the image to folder adn updating the url in the database
            File.save_path_to_database(
                user_email=session.get('email'),
                file_nm=File.save_file(
                    app=app,
                    file=form.profile_img_field.data
                )
            )
            
            flash('updated', 'success')
        
        username = form.username_field.data
        email = form.email_field.data
        name = form.name.data
        telephone = str(form.telephone.data)
        
        x,y = UpdateAccount.update_account(
            user_email_session=session.get('email'),
            username=username,
            email=email,
            name=name,
            phone_no=telephone
        )
        
        if(x==0 and y==0):
            parent_db.reestablish_connection()
            return render_template(
                'updateaccount.html',
                title = f'{site_initial}Update Account',
                form = form,
                db = parent_db,
                email_err = 'This email is already in use. Please use another.',
                username_err = 'This username is already in use. Please another.'
            )
        elif(x == 0):
            parent_db.reestablish_connection()
            return render_template(
                'updateaccount.html',
                title = f'{site_initial}Update Account',
                form = form,
                db = parent_db,
                email_err = 'This email is already in use. Please use another.',
            )
        elif(y==0):
            parent_db.reestablish_connection()
            return render_template(
                'updateaccount.html',
                title = f'{site_initial}Update Account',
                form = form,
                db = parent_db,
                username_err = 'This username is already in use. Please another.'
            )
        elif(x==2):
            session.pop('email', None)
            session['email'] = parent_db.get_row(
                table_name = 'User',
                data_list={
                    'username':username
                }
            )[3]
            parent_db.reestablish_connection()
            return render_template(
                'updateaccount.html',
                title = f'{site_initial}Update Account',
                form = form,
                db = parent_db,
            )
        else:
            parent_db.reestablish_connection()
            return render_template(
                'updateaccount.html',
                title = f'{site_initial}Update Account',
                form = form,
                db = parent_db,
            )
            
        
        
    flash(
            message='Something went wrong',
            category='danger'
        )
    return redirect(
            url_for('open_loginpage')
        )

   
@app.route(
    '/blogs',
    methods = ['GET']
    )
def open_blogspage():
    if(session.get('email') == None):
        flash('You must be logged in to view blogs', category='warning')
        return redirect(url_for('open_loginpage'))
    else:
        return render_template(
            'blog.html',
            user = parent_db.get_row(
                table_name='User',
                data_list={
                    'email': session.get('email')
                }
            ),
            title = f'{site_initial}Blogs',
            Data = Data,
            db=parent_db
        )
        
@app.route('/blogs/new-post', methods = ['GET','POST'])
def open_newblogspage():
    
    #New blog post form
    form = BlogPostForm()
    
    if(session.get('email') == None):
        return redirect(url_for('open_loginpage'))
    elif(form.is_submitted()):
                    
        return render_template(
            'newblog.html',
            title = f'{site_initial}New Blog',
            user_info = Data,
            form = form,
        )
        
    return render_template(
        'newblog.html',
        title = f'{site_initial}New Blog',
        user_info = Data,
        form = form,
    )
        
@app.route('/profile')
def open_profilepage():
    return redirect(url_for('open_accountsupdatepage'))

@app.route(
    '/logout'
    )
def logout():
    session.pop('email', None)
    Register.db.shut_database_conection()
    session.clear()
    return redirect(url_for('open_homepage'))


    