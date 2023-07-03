from Validation import Register, Login

def test1():
    Register.register(
        email='joeittabjxa@gmail.com123',
        password='ReDbLue@123',
        username='joelabjxa@umail.com123',
    )
def test2():
    Register.register()
    
def return_function():
    return (1,2,3)

def test3():
    a,b,c = return_function()
    print(a,b,c)
    
def test4():
    print(
        Login.login(
            email='susangeorge.123@gmail.com',
            password='Tiger@123'
        )
    )
    
test4()