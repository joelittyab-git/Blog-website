from Database import database

db = database()

def test1():
      db.add_entry(
            table_name='User',
            data_list={
                  'user_id':1003,
                  'username': "admin@123",
                  'password':"admin@123",
                  'email':"admin@123@gmail.com",
                  'profile_image_url':"default.jpg",
                  'join_date':"CURDATE()"
            }
      )
      
def test2():
      x = {
            "Joel":"Abraham",
            "John":"Vaading",
            "Joe":"Tribilani",
            "Abel":"Mathew",
            "Susan":"George",

      }
      
      for ret in x:
            print (ret)
            
def test3():
      print('lmao')
def test4():
      db.add_entry(
            table_name='User',
            data_list={
                  'user_id':db.generate_p2k(table='User'),
                  'username':'John',
                  'password':'Tiger@123',
                  'email':'John123@gmail.com',
                  'join_date':db.get_currentdate_query()   ,
                  'profile_image_url' : 'default.jpg'
            }
      )
      
def test5():
      x = db._get_password(
            user = db.get_row(
                  data_list={
                        'username':'joelab@umail.com'
                  }
            )
      )
      
      print(x)

def test6():
      db.update_entry(
            table_name='Dummy',
            search_list_where={
                 'age' :10,
                 'age':100,
                 'name':'joel'
            },
            
            update_list_set={
                  'name':'Father Abraham'
            }
      )
      
def test7():
      dic = {
            'Joel':'LMAOO'
      }
      
      dic2 = {
            'x':f"{dic['Joel']}"
      }
      
      print(dic2['x'])
      
      
def test8():
      h = (db.get_table_data(table_name='category_list'))
      b = []
      
            
      b = [(x[0],x[0]) for x in h]
            
      print(b)

def test9():
      print(db.get_table_data(table_name='category_list'))
test9()
db.shut_database_conection()
