import os
import pickle
import pandas as pd
import sqlite3
def transfermoney(fromuser,touser,sum):
  mcon1 = sqlite3.connect('SQLite_Python.db')
  c1 = mcon1.cursor()
  c1.execute("SELECT Balance FROM Accounts WHERE Username= :Username",{'Username':fromuser})
  x = c1.fetchone()
  c1.execute("SELECT Balance FROM Accounts WHERE Username= :Username",{'Username':touser})
  y = c1.fetchone()
  c1.execute("""UPDATE Accounts SET Balance = :Balance 
               WHERE Username = :Username """,{'Balance':x[0]-sum ,'Username':fromuser })
  c1.execute("""UPDATE Accounts SET Balance = :Balance 
               WHERE Username = :Username """,{'Balance':y[0]+sum ,'Username':touser })
  m=x[0]-sum
  n=y[0]+sum
  mmm=sqlite3.connect("PROJECT.db")
  mcursor=mmm.cursor()
  mcursor.execute("UPDATE USERDETAILS SET BALANCE=%s WHERE USERNAME='%s'"%(m,fromuser))
  mcursor.execute("UPDATE USERDETAILS SET BALANCE=%s WHERE USERNAME='%s'"%(n,touser))
  mmm.commit()
  mmm.close()
  mcon1.commit()

def buyproduct(fromuser,pid):
  sum = price(pid)
  mcon2 = sqlite3.connect('SQLite_Python.db')
  c2 = mcon2.cursor()
  c2.execute("SELECT SELLER FROM stocks WHERE P_ID = :P_ID",{'P_ID':pid})
  z = c2.fetchone()
  toseller = z[0]
  c2.execute("SELECT Balance FROM Accounts WHERE Username= :Username",{'Username':fromuser})
  x = c2.fetchone()
  c2.execute("SELECT Balance FROM Accounts WHERE Username= :Username",{'Username':toseller})
  y = c2.fetchone()
  c2.execute("""UPDATE Accounts SET Balance = :Balance 
               WHERE Username = :Username """,{'Balance':x[0]-sum ,'Username':fromuser })
  c2.execute("""UPDATE Accounts SET Balance = :Balance 
               WHERE Username = :Username """,{'Balance':y[0] + sum*9/10 ,'Username':toseller })
  m=x[0]-sum
  n=y[0]+sum*9/10
  mmm=sqlite3.connect("PROJECT.db")
  mcursor=mmm.cursor()
  mcursor.execute("UPDATE USERDETAILS SET BALANCE=%s WHERE USERNAME='%s'"%(m,fromuser))
  mcursor.execute("UPDATE USERDETAILS SET BALANCE=%s WHERE USERNAME='%s'"%(n,toseller))
  mmm.commit()
  mmm.close()
  mcon2.commit()

def viewaccount(user):
  mycon3 = sqlite3.connect('SQLite_Python.db')
  c3 = mycon3.cursor()
  c3.execute("SELECT * FROM Accounts WHERE Username = :Username",{'Username':user})
  x3 = c3.fetchone()
  print("")

def price(p_id):
  mycon4 = sqlite3.connect('SQLite_Python.db')
  c4 = mycon4.cursor()
  c4.execute("SELECT PRICE,DISCOUNT FROM stocks WHERE P_ID = :P_ID ",{'P_ID':p_id})
  x = c4.fetchone()
  y = x[0] - int(x[1])
  mycon4.commit()
  return y

def addmoney(user,sum):
  mcon5 = sqlite3.connect('SQLite_Python.db')
  c5 = mcon5.cursor()
  c5.execute("SELECT Balance FROM Accounts WHERE Username= :Username",{'Username':user})
  x = c5.fetchone()
  c5.execute("""UPDATE Accounts SET Balance = :Balance 
               WHERE Username = :Username """,{'Balance':x[0]+sum ,'Username':user })
  m=x[0]+sum
  mmm=sqlite3.connect("PROJECT.db")
  mcursor=mmm.cursor()
  mcursor.execute("UPDATE USERDETAILS SET BALANCE=%s WHERE USERNAME='%s'"%(m,user))
  mmm.commit()
  mmm.close()
  mcon5.commit()

def checkbalance(user,price):
  mcon6 = sqlite3.connect('SQLite_Python.db')
  c6 = mcon6.cursor()
  c6.execute("SELECT Balance FROM Accounts WHERE Username= :Username",{'Username':user})
  x = c6.fetchone()
  if x[0] >= price:
    return 1
  else:
    return 0


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
print("Hi. Welcome to python version of amazon india")
print("If you are a buyer press 1")
print("If you are an employee press 2")
print("If you are seller press 3")
print("If you wish to see your amazon pay account press 4")
print("Enter your choice:")
while True:
  #try:
    x=int(input())
    if x==2:
      def hello():
        fin=open("password.dat",'rb')
        list=pickle.load(fin)
        fin.close()
        l=input("Enter your amazon code")
        if l==list:
          print("If you have to see the product database press 1")
          print("If you have to view users database press 2")
          print("If you want to message any user press 3")
          print("If you want to quit type 4")
          count1=0
          while count1!=1:
            m=int(input())
            if m==1:
              mmmm=sqlite3.connect("compdb.db")
              df=pd.read_sql_query("SELECT * FROM stocks",mmmm) 
              print(df)
              mmmm.close()
              continue
            elif m==2:
              mmm=sqlite3.connect("PROJECT.db")
              df=pd.read_sql_query("SELECT * FROM USERDETAILS",mmm)
              print(df)
              mmm.close()
              continue
            elif m==3:
              def message():
                user=input("Enter username(case sensitive)")
                mmm=sqlite3.connect("PROJECT.db")
                mmmcursor=mmm.cursor()
                mmmcursor.execute("SELECT USERNAME FROM USERDETAILS")
                w=mmmcursor.fetchall()
                hello=0
                for i in w:
                  if user in i[0]:
                    message=input("Enter your message")
                    fin=open("MESSAGE.dat",'wb')
                    messagelist=[[user,message]]
                    pickle.dump(messagelist,fin)
                    fin.close()
                    hello+=1
                if hello==0:
                   print("Incorrect username")
                   x=int(input("If you want to try again type 1 else type 2"))
                   if x==1:
                     message()
                   elif x==2:
                     return
              message()
              return                   
            elif m==4:
              return
            else:
              print("Your choice is not valid.please try again")
        else:
          print("The amazon code is invalid.")
          print("If you want to try again press 0")
          print("If you want to reset your amazon code press 1")
          p=int(input("enter your choice"))
          try:
            if p==0:
              hello()
            elif p==1:
              count2=0
              while count2==0:
                date=int(input("Enter your date of birth in the format ddmmyyyy"))
                try:
                  if date==17112003:
                    newp=input("Enter your new amazon code")
                    fin=open("passwordnew.dat",'wb')
                    pickle.dump(newp,fin)
                    fin.close()
                    os.remove('password.dat')
                    os.rename('passwordnew.dat','password.dat')
                    count2=1
                    hello()

                  else:
                    print("Please enter your date of birth correctly in the format ddmmyyyy")
                except TypeError:
                  print("Please enter your date of birth correctly in the format ddmmyyyy")   
            else:
              print("Your choice is invalid. Please try again")
          except TypeError:
            print("Your choice is invalid. Please try again")
      hello()
      break
    elif x==1:

      #Buyer's Space
      mycon=sqlite3.connect("SQLite_Python.db")
      cursor=mycon.cursor()
      

      def welcome_buyer():
        print("Hi! Welcome to the Python Version of Amazon India. Hope you enjoy your hassle free shopping.")
        print("\n Choose any of the following menus. Don't forget to sign up to your Amazon Pay account.")
        print("\n Choose any of the options below to either sign up/login to Amazon Pay")
        print("\n Press 1 for Sign up \n Press 2 for Login \n")
 
      def amazonpay_buyer():
        
        def sort_product(sts):
          
           ktk = int(input("If you want to sort product based an price from highest to lowest, press 1. \n If you want to sort based on price from lowest to highest, press 2. \n If you want to sort based on popularity press 3. \n "))
           
           l = []
           m = []
           
           if ktk == 1:
               for i in range(len(sts)):
                 l += [sts[i][4],]
               l.sort()
               for i in range (0,len(l)):
                 for j in range (0,len(sts)):
                   if sts[j][4] == l[i]:
                     m+= [sts[j],]
                     
           if ktk == 2:
               for i in range(len(sts)):
                 l += [sts[i][4],]
               l.sort()
               for i in range (0,len(l)):
                 for j in range (0,len(sts)):
                   if sts[j][4] == l[i]:
                     m+= [sts[j],]
               m.reverse() 
                     
           if ktk == 3:
               for i in range(len(sts)):
                l += [sts[i][3],]
               l.sort()
               for i in range (0,len(l)):
                   for j in range (0,len(sts)):
                     if sts[j][3] == l[i]:
                        m+= [sts[j],]

           for row in m:
              print("P_ID = ",row[0])
              print("SUBCATEGORY = ",row[1])
              print("STOCK_AVAILABLE = ",row[2])
              print("RATING = ",row[3])
              print("PRICE = ",row[4])
              print("DISCOUNT = ",row[5])
              print("NO_OF_RATING = ",row[6])
              print("\n")
           

        a1 = int(input("Enter your preference \t"))
        f = 0
        #Enter signup details
        if a1 == 1:
          a2 = input("Enter your username (Case Sensitive) \t")
          a3 = input("Enter your Password (Should have a minimum of 6 chararcters) \t")
          b = input("Enter valid EMmail ID \t")
          while len(a3) < 6:
             print("Enter the password again. Mentioned password is too short. \t")
             a3 = input("Enter your Password (Should have a minimum of 6 characters)\t")
        #Check entered details
          a4 = input("Confirm your Password \t")
          def a3equalsa4():
            if a3 == a4:
              mycon110 = sqlite3.connect('SQLite_Python.db')
              cursor = mycon110.cursor()
              a5 = "insert into Accounts values(?,?,?,?)"
              pk = (a2,a3,b,100)
              cursor.execute(a5,pk)
              mmm=sqlite3.connect("PROJECT.db")
              mcursor=mmm.cursor()
              mcursor.execute("INSERT INTO USERDETAILS VALUES(?,?,?,?)",[a2,a3,b,100])
              mmm.commit()
              mmm.close()
              mycon110.commit()
              print("\n Congratulations you have succesfully created your personal Amazon Pay account. An amount of 100.00 rupees has been added to your account from Amazon as a token of goodwill.")
          a3equalsa4()
          while a3 != a4:
            print("Check your password")
            a4 = input("Confirm your password. \t")
            if a3 ==a4:
              a3equalsa4()
              break
            else:
              continue
        else:
          f = 1
          var = 0
          while  var== 0:
            a6 = input("\nEnter your username \t") 
            a7 = input("Enter your password \t")
            mycon100 = sqlite3.connect('SQLite_Python.db')
            cursor = mycon100.cursor()
            cursor.execute("SELECT * FROM Accounts")
            d = cursor.fetchall()
            for i in d:
              if i[0]==a6 and i[1]==a7:
                var = 1
                a11=i
                break;
            else:
              print("Your Username or Password is incorrect. Please try again")
          
          print("\n Welcome to your Amazon Pay Account, the leading service for all online transactions. ")
          fin=open("MESSAGE.dat","rb")
          fout=open("MESSAGEtemp.dat",'wb')
          try:
              while True:
                  for i in pickle.load(fin):
                      if i[0]==SELLER:
                          print("message from owner:",i[1])
                      else:
                          pickle.dump(i,fout)
          except EOFError:
              fin.close()
              fout.close()
              os.remove("MESSAGE.dat")
              os.rename("MESSAGEtemp.dat","MESSAGE.dat")
          print("\n Username : ",a11[0]," \nPassword : ",a11[1]," \nCash : ",a11[3])  
      
      
        print("\nGreat now you are all set to shop. With glittering deals to freebies, indulge youselves in the ultimate shopping destination.")
        print("\nEnter 1 for Electronics  \n Enter 2 for Day to Day Appliances \n Enter 3 for Sports wears and equipments \n Enter 4 for Musical instruments \n Enter 5 for Travel and Fashion  ")
        a11 = int(input(("\nWhat's your choice \t")))
        if a11==1:  
            a12 = "SELECT P_ID,SUB_CATEGORY,STOCK_AVAILABLE,RATING,PRICE,DISCOUNT,NO_OF_RATING from stocks WHERE CATEGORY = 'ELECTRONICS'  "
            mycon = sqlite3.connect('compdb.db')
            cursor = mycon.cursor()
            cursor.execute(a12)
            a101 = []
            for row in cursor.fetchall():
              print("P_ID = ",row[0])
              print("SUBCATEGORY =n",row[1])
              print("STOCK_AVAILABLE = ",row[2])
              print("RATING = ",row[3])
              print("PRICE = ",row[4])
              print("DISCOUNT = ",row[5])
              print("NO_OF_RATING = ",row[6])
              print("\n")
              a101 = a101 + [row,]
            mycon.commit()
            sort_product(a101)
            
            a23 = []
            a24 = 'Y'
            while a24 == 'y' or a24=='Y':
              a25 = int(input("\nEnter the product id of the product of your choice \t"))
              a23 += [a25,]
              a24 = input("\nI hope you do want to continue shopping. If so please do enter Y \t")
        if a11==2:
            a13 = "SELECT P_ID,SUB_CATEGORY,STOCK_AVAILABLE,RATING,PRICE,DISCOUNT,NO_OF_RATING from stocks WHERE CATEGORY = 'HOME_APPLIANCES'"
            mycon = sqlite3.connect('compdb.db')
            cursor = mycon.cursor()
            cursor.execute(a13)
            a101 = []
            for row in cursor.fetchall():
              print("P_ID = ",row[0])
              print("SUBCATEGORY = ",row[1])
              print("STOCK_AVAILABLE = ",row[2])
              print("RATING = ",row[3])
              print("PRICE = ",row[4])
              print("DISCOUNT = ",row[5])
              print("NO_OF_RATING = ",row[6])
              print("\n")
              a101 = a101 + [row,]
            mycon.commit()
            sort_product(a101)
            
            a23 = []
            a24 = 'Y'
            while a24 == 'y' or 'Y':
              a25 = int(input("\nEnter the product id of the product of your choice \t"))
              a23 += [a25,]
              a24 = input("\nI hope you do want to continue shopping. If so please do enter Y \t")
        if a11==3:
            a14 = "SELECT P_ID,SUB_CATEGORY,STOCK_AVAILABLE,RATING,PRICE,DISCOUNT,NO_OF_RATING from stocks WHERE CATEGORY = 'SPORTS'"
            mycon = sqlite3.connect('compdb.db')
            cursor = mycon.cursor()
            cursor.execute(a14)
            a101 = []
            for row in cursor:
              print("P_ID = ",row[0])
              print("SUBCATEGORY = ",row[1])
              print("STOCK_AVAILABLE = ",row[2])
              print("RATING = ",row[3])
              print("PRICE = ",row[4])
              print("DISCOUNT = ",row[5])
              print("NO_OF_RATING = ",row[6])
              print("\n")
              a101 = a101 + [row,]
            mycon.commit()
            sort_product(a101)
            
            a23 = []
            a24 = 'Y'
            while a24 == 'y' or 'Y':
              a25 = int(input("\nEnter the product id of the product of your choice \t"))
              a23 += [a25,]
              a24 = input("\nI hope you do want to continue shopping. If so please do enter Y \t")
        if a11==4:
            a15 = "SELECT P_ID,SUB_CATEGORY,STOCK_AVAILABLE,RATING,PRICE,DISCOUNT,NO_OF_RATING from stocks WHERE CATEGORY = 'MUSICAL_INSTRUMENTS'"
            mycon = sqlite3.connect('compdb.db')
            cursor = mycon.cursor()
            cursor.execute(a15)
            a101 = []
            for row in cursor:
              print("P_ID = ",row[0])
              print("SUBCATEGORY = ",row[1])
              print("STOCK_AVAILABLE = ",row[2])
              print("RATING = ",row[3])
              print("PRICE = ",row[4])
              print("DISCOUNT = ",row[5])
              print("NO_OF_RATING = ",row[6])
              print("\n")
              a101 = a101 + [row,]
            mycon.commit()
            sort_product(a101)
            
            a23=[]
            a24 = 'Y'
            while a24 == 'y' or 'Y':
              a25 = int(input("\nEnter the product id of the product of your choice \t"))
              a23 += [a25,]
              a24 = input("\nI hope you do want to continue shopping. If so please do enter Y \t")
        if a11 == 5:
            a16 = "SELECT P_ID,SUB_CATEGORY,STOCK_AVAILABLE,RATING,PRICE,DISCOUNT,NO_OF_RATING from stocks WHERE CATEGORY = 'FASHION'"
            mycon = sqlite3.connect('compdb.db')
            cursor = mycon.cursor()
            cursor.execute(a16)
            a101 = []
            for row in cursor:
              print("P_ID = ",row[0])
              print("SUBCATEGORY = ",row[1])
              print("STOCK_AVAILABLE = ",row[2])
              print("RATING = ",row[3])
              print("PRICE = ",row[4])
              print("DISCOUNT = ",row[5])
              print("NO_OF_RATING = ",row[6])
              print("\n")
              a101 = a101 + [row,]
            mycon.commit()
            sort_product(a101)
            
            a23 = []
            a24 = 'Y'
            while a24 == 'y' or 'Y':
              a25 = int(input("\nEnter the product id of the product of your choice \t"))
              a23 += [a25,]
              a24 = input("\nI hope you do want to continue shopping. If so please do enter Y \t")
        p=0
        if f == 1:
          for i in a23:
              p = p + price(i)
          suff = checkbalance(a6,p)
          if suff == 1:
              for i in a23:
                buyproduct(a6,i)
              print("money detected")
          else:
                print("Sorry. You do not have sufficient funds")
     

        if f == 0:
          for i in a23:
              p = p + price(i)
          suff = checkbalance(a2,p)
          if suff == 1:
                for i in a23:
                   buyproduct(a2,i)
                print("money detected")
          else:
                print("Sorry. You do not have sufficient funds")
     
      welcome_buyer()
      amazonpay_buyer()
      break 
    elif x==3:
      #gokul
      def login():
                while True:
                    SELLER=input("Enter your username = ")
                    PASSWORD=input("Enter your password = ")
                    mydb=sqlite3.connect("compdb.db")
                    cursor=mydb.cursor()
                    find_user="SELECT * FROM stocks where SELLER= '%s' AND PASSWORD= '%s'"%(SELLER,PASSWORD)
                    cursor.execute(find_user)
                    results1=cursor.fetchall()
                    if len(results1)!=0:
                        print("Welcome ",SELLER)
                        fin=open("MESSAGE.dat","rb")
                        fout=open("MESSAGEtemp.dat",'wb')
                        try:
                          while True:
                            for i in pickle.load(fin):
                              if i[0]==SELLER:
                                 print("message from owner:",i[1])
                              else:
                                pickle.dump(i,fout)
                        except EOFError:
                          fin.close()
                          fout.close()
                          os.remove("MESSAGE.dat")
                          os.rename("MESSAGEtemp.dat","MESSAGE.dat")
                        less_stocks="SELECT P_NAME,STOCK_AVAILABLE FROM stocks where STOCK_AVAILABLE<10 AND SELLER= '%s'"%(SELLER)
                        cursor.execute(less_stocks)
                        
                        results5=cursor.fetchall()
                        if len(results5)!=0:
                            print("The following products have less stocks available")
                            print(results5)
                        print("Enter 1 to view your stocks")
                        print("Enter 2 to view your ratings")
                        print("Enter 3 to modify your product's price or discount")
                        print("Enter 4 to view your bank details")
                        print("Enter 5 to delete a product")
                        print("Enter 6 to log out")
                        while True:
                            a1=int(input("Enter your choice: "))
                            if a1==1:
                                view_stocks="SELECT P_ID,P_NAME,STOCK_AVAILABLE FROM stocks where SELLER= '%s' AND PASSWORD= '%s'"%(SELLER,PASSWORD)
                                cursor.execute(view_stocks)
                                results2=cursor.fetchall()
                                for row in results2:
                                    print(row)
                                continue
                            elif a1==2:
                                view_ratings="SELECT P_ID,P_NAME,RATING,NO_OF_RATING FROM stocks where SELLER= '%s' AND PASSWORD= '%s'"%(SELLER,PASSWORD)
                                cursor.execute(view_ratings)
                                results3=cursor.fetchall()
                                for row in results3:
                                    print(row)
                                continue
                            elif a1==3:
                                select_productid="SELECT P_ID FROM stocks where SELLER= '%s' AND PASSWORD= '%s'"%(SELLER,PASSWORD)
                                cursor.execute(select_productid)
                                results6=cursor.fetchall()
                                lenres6=len(results6)
                                list1=[]
                                for i in range(0,lenres6):
                                    list1.append(results6[i][0])
                                while True:
                                    P_ID1=int(input("Enter the product id of the product you wish to update:"))
                                    if P_ID1 in list1:
                                        PRICE1=(input("Enter the new Price: "))
                                        DISCOUNT1=(input("Enter the new Discount: "))
                                        update="UPDATE stocks SET PRICE= '%s',DISCOUNT= '%s' where P_ID= '%s'"%(PRICE1,DISCOUNT1,P_ID1)
                                        cursor.execute(update)
                                        mydb.commit()
                                        view_table="SELECT * from stocks WHERE SELLER= '%s' AND PASSWORD= '%s'"%(SELLER,PASSWORD)
                                        cursor.execute(view_table)
                                        results4=cursor.fetchall()
                                        for row in results4:
                                            print(row)
                                        break
                                    else:
                                        print("Invalid product id")
                                        again3=input("Do you want to try again(y/n): ")
                                        if again3=="n":
                                            break
                                        else:
                                            continue
                                continue
                            elif a1==4:
                                select_account="SELECT * FROM Accounts where Username= '%s' AND Password= '%s'"%(SELLER,PASSWORD)
                                cursor255.execute(select_account)
                                results7=cursor255.fetchall()
                                for row in results7:
                                    print(row)
                                continue
                            elif a1==5:
                                select_productid1="SELECT P_ID FROM stocks where SELLER= '%s' AND PASSWORD= '%s'"%(SELLER,PASSWORD)
                                cursor.execute(select_productid1)
                                results8=cursor.fetchall()
                                lenres8=len(results8)
                                list2=[]
                                for i in range(0,lenres8):
                                    list2.append(results8[i][0])
                                while True:
                                    P_ID2=int(input("Enter the product id of the product you wish to delete:"))
                                    if P_ID2 in list2:
                                        delete_row="DELETE FROM stocks WHERE P_ID= '%s'"%(P_ID2)
                                        cursor.execute(delete_row)
                                        mydb.commit()
                                        print("Successfully Deleted")
                                        break
                                    else:
                                        print("Invalid product id")
                                        again4=input("Do you want to try again(y/n): ")
                                        if again4=="n":
                                            break
                                        else:
                                            continue
                                continue
                            elif a1==6:
                                break
                            else:
                                print("Invalid choice entered")
                                again2=input("Do you want to try again(y/n) : ")
                                if again2 == "n":
                                    break
                                else:
                                    continue
                                                  
                    else:
                        print("Username and Password not recognised")
                        again=input("Do you want to try again(y/n) : ")
                        if again == "n":
                            print("Goodbye")
                            break
                        if again == "y":
                            continue
                    mydb.close()
                    break
                return
                
      while True:
              mydb=sqlite3.connect("compdb.db")        
              cursor=mydb.cursor()
              mydb255=sqlite3.connect("SQLite_Python.db")
              cursor255=mydb255.cursor()
                    

              a2=input("Do you already have an account(y/n): ")
              if a2=="y":
                 login()
                 break
              elif a2=="n":
                  print("Enter the following details")
                  P_ID2=input("Enter your product id")
                  P_NAME2=input("Enter your product name")
                  CATEGORY2=input("Enter your product category")
                  SUB_CATEGORY2=input("Enter your product sub category")
                  STOCK_AVAILABLE2=input("Enter your product stock available")
                  RATING2=0
                  PRICE2=input("Enter your product price")
                  DISCOUNT2=input("Enter your product discount")
                  NO_OF_RATING2=0
                  SELLER2=input("Enter your username")
                  PASSWORD2=input("Enter your password")
                  update_table="INSERT INTO stocks VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(P_ID2,P_ID2,P_NAME2,CATEGORY2,SUB_CATEGORY2,STOCK_AVAILABLE2,RATING2,PRICE2,DISCOUNT2,NO_OF_RATING2,SELLER2,PASSWORD2)
                  cursor.execute(update_table)
                  mydb.commit()
                  print("succesfully created")
                  cursor255.execute(update_table)
                  mydb255.commit()
                  EmailID2=input("Enter your email id")
                  Balance2=input("Enter your account balance")
                  update_table2="INSERT INTO Accounts VALUES ('%s','%s','%s','%s')"%(SELLER2,PASSWORD2,EmailID2,Balance2)
                  cursor255.execute(update_table2)
                  mydb255.commit()
                  print("succesfully created")
                  a3=input("Do you want to login to your account(y/n) : ")

                  if a3=="y":
                      login()
                  else:
                      break
              else:
                  print("Invalid choice entered")
                  again1=input("Do you want to try again(y/n) : ")
                  if again1 == "n":
                      print("Goodbye")
                      break
      break
      
 

    elif x==4:
      mcon1 = sqlite3.connect('SQLite_Python.db')
      cursor = mcon1.cursor()
      var = 0
      while var == 0:
        nam = input("Enter your username") 
        pas = input("Enter your password")
        cursor.execute("SELECT * FROM Accounts")
        d = cursor.fetchall()
        for i in d:
          if i[0]==nam and i[1]==pas:
            var = 1
            break;
        else:
          print("Your Username or Password is incorrect. Please try again")
          
      if var ==1:
        p = 0
        while p==0:
         print("\n Welcome to your Amazon Pay Account, the leading service for all online transactions. ") 
         print("Enter 1 to view your account details")
         print("Enter 2 to add money to your account")
         print("Enter 3 to transfer money to another account")
         choice = int(input(" "))       
         wi = 'y'
         if choice == 1:
          cursor.execute("SELECT * FROM Accounts WHERE Username = :Username ",{'Username':nam})
          det = cursor.fetchone()
          print("Username: ",det[0])
          print("Password: ",det[1])
          print("Email Address: ",det[2])
          print("Account Balance:",det[3])
         elif choice == 2:
          s = int(input("Enter the amount to be added: "))
          addmoney(nam,s)
          print("Money added successfully")
         elif choice == 3:
          nam1 = input("Enter the name of user to whom money is to be transferred: ")
          s = int(input("Enter the amount to be transferred: "))
          if checkbalance(nam,s) == 1:
            transfermoney(nam,nam1,s)
            print("money transferred successfully")
          else:
            print("insufficient funds")
         wi = input("Press e to exit amazonpay ")
         if wi == 'e':
           p=1                     
      break     

    else:
      print("the choice you have entered is invalid.please try again")
  #except TypeError:
   # print("the choice you have entered
