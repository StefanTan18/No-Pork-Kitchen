from tabnanny import check
from webbrowser import get
import mysql.connector
from mysqlx import IntegrityError

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Youshallnotpass!", # Change accordingly
    database = "NoPorkKitchenDB"
)

mycursor = mydb.cursor()

############################################################################################
#---------------------------------------USERS-----------------------------------------------
############################################################################################

#Get all Users
def getAllUsers():
    mycursor.execute("SELECT * FROM Users");
    result = mycursor.fetchall();
    print (result)
    return result
#Check credentials (username,password)
def checkCredentials(username,password):
    try:
        mycursor.execute("Select password FROM Users WHERE username = '"+username+"'")
        result = mycursor.fetchone();
        if (result[0] != password):
            #print (result)
            print ("Invalid username or password")
            return False
        else:
            print ("Credentials match. Success")
            return True
    except:
        print ("Unable to log in. If you do not have an account please register first.")
        return False
#Create User (id,username,name,password,usertype)
def createUser(id,username,name,password,usertype):
    try:
        sql = "INSERT INTO Users (userID,name,username,password,usertype, flag) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (id,name,username,password,usertype+"pending",0)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Account Created Succesfully")
        return True
    except IntegrityError:
        print("Username already exists. Please try another.")
        return False
    except:
        print("An exception occurred.")
        return False
#Change UserType - Ban/Register/etc. (userid, status)
def updateUserType(userid,status):
    sql = "UPDATE Users SET userType = %s WHERE userID = %s"
    val = (status,userid)
    mycursor.execute(sql, val)
    if (status=="manager"):
        #add to manager table
        sql = "INSERT INTO Managers (userID,salary,hours_worked) VALUES (%s, %s, %s)"
        val = (userid,0,0)
        mycursor.execute(sql, val)
    if(status=="customer"):
        #add to customer table
        sql = "INSERT INTO Customers (userID,balance,address,VIP_STATUS) VALUES (%s, %s, %s, %s)"
        val = (userid,0,0,0)
        mycursor.execute(sql, val)
    if(status=="chef"):
        #add to chef table
        sql = "INSERT INTO Chefs (userID,salary,hours_worked) VALUES (%s, %s, %s)"
        val = (userid,0,0)
        mycursor.execute(sql, val)
    if(status=="delivery"):
        #add to chef table
        sql = "INSERT INTO Delivery (userID,distance,earnings,no_deliveries) VALUES (%s, %s, %s, %s)"
        val = (userid,0,0,0)
        mycursor.execute(sql, val)
    mydb.commit()

#---------------------------------------Manager-----------------------------------------------
#Get all Managers
def getAllManagers():
    mycursor.execute("SELECT * FROM Managers");
    result = mycursor.fetchall();
    print (result)
    return result
#Change salary (userid, newsalary)
def updateManagerSalary(userid,newsalary):
    if (newsalary > 0):
        sql = "UPDATE Managers SET salary = %s WHERE userID = %s"
        val = (newsalary,userid)
        mycursor.execute(sql, val)
        mydb.commit()
        return True
    else:
        print("Employee must have a valid salary > 0.")
        return False
#Get balance (userid)
def getManagerSalary(userid):
    sql = "Select salary FROM Managers WHERE userID = "
    mycursor.execute(sql+str(userid))
    result = mycursor.fetchall()[0][0]
    print (result)
    return result
#Update hours worked (userid, hours)
def updateManagerHours(userid,hours):
    if (hours > 0):
        sql = "UPDATE Managers SET hours_worked = hours_worked+%s WHERE userID = %s"
        val = (hours,userid)
        mycursor.execute(sql, val)
        mydb.commit()
        return True
    else:
        print("Employee must have worked more than 0 hours.")
        return False
#Get balance (userid)
def getManagerHours(userid):
    sql = "Select hours_worked FROM Managers WHERE userID = "
    mycursor.execute(sql+str(userid))
    result = (mycursor.fetchall())[0][0]
    print (result)
    return result


#---------------------------------------Chefs-----------------------------------------------
#Get all chefs
def getAllChefs():
    mycursor.execute("SELECT * FROM Chefs");
    result = mycursor.fetchall();
    print (result)
    return result
#Change salary (userid, newsalary)
def updateChefSalary(userid,newsalary):
    if (newsalary > 0):
        sql = "UPDATE Chefs SET salary = %s WHERE userID = %s"
        val = (newsalary,userid)
        mycursor.execute(sql, val)
        mydb.commit()
        return True
    else:
        print("Employee must have a valid salary > 0.")
        return False
#Get balance (userid)
def getChefSalary(userid):
    sql = "Select salary FROM Chefs WHERE userID = "
    mycursor.execute(sql+str(userid))
    result = mycursor.fetchall()[0][0]
    print (result)
    return result
#Update hours worked (userid, hours)
def updateChefHours(userid,hours):
    if (hours > 0):
        sql = "UPDATE Chefs SET hours_worked = hours_worked+%s WHERE userID = %s"
        val = (hours,userid)
        mycursor.execute(sql, val)
        mydb.commit()
        return True
    else:
        print("Employee must have worked more than 0 hours.")
        return False
#Get balance (userid)
def getChefHours(userid):
    sql = "Select hours_worked FROM Chefs WHERE userID = "
    mycursor.execute(sql+str(userid))
    result = (mycursor.fetchall())[0][0]
    print (result)
    return result

#---------------------------------------Delivery-----------------------------------------------
#Get all delivery
def getAllDelivery():
    mycursor.execute("SELECT * FROM Delivery");
    result = mycursor.fetchall();
    print (result)
    return result
#Update number of deliveries(userid, numbertoadd)
def updateNumDeliveries(userid,numDelivered):
    if (numDelivered > 0):
        sql = "UPDATE Delivery SET no_deliveries = no_deliveries+%s WHERE userID = %s"
        val = (numDelivered,userid)
        mycursor.execute(sql, val)
        mydb.commit()
        return True
    else:
        print("Delivery person must have made more than 0 trips.")
        return False
#Get number of deliveries(userid)
def getNumDeliveries(userid):
    sql = "Select no_deliveries FROM Delivery WHERE userID = "
    mycursor.execute(sql+str(userid))
    result = (mycursor.fetchall())[0]
    print (result[0])
    return result[0]
#Update distance travelled(userid, distancetoadd)
def updateDistance(userid,distance):
    if (distance > 0):
        sql = "UPDATE Delivery SET distance = distance+%s WHERE userID = %s"
        val = (distance,userid)
        mycursor.execute(sql, val)
        mydb.commit()
        return True
    else:
        print("Delivery person must have made more than 0 trips.")
        return False
#Get distance travelled(userid)
def getDistance(userid):
    sql = "Select distance FROM Delivery WHERE userID = "
    mycursor.execute(sql+str(userid))
    result = (mycursor.fetchall())[0]
    print (result[0])
    return result[0]
#Update total earnings(userid, moneytoadd)
def updateDeliveryEarnings(userid,amount):
    if (amount > 0):
        sql = "UPDATE Delivery SET earnings = earnings+%s WHERE userID = %s"
        val = (amount,userid)
        mycursor.execute(sql, val)
        mydb.commit()
        return True
    else:
        print("Delivery person must have made more than 0 dollars.")
        return False
#Get total earnings(userid)
def getDeliveryEarnings(userid):
    sql = "Select earnings FROM Delivery WHERE userID = "
    mycursor.execute(sql+str(userid))
    result = (mycursor.fetchall())[0]
    print (result[0])
    return result[0]


#---------------------------------------Customers-----------------------------------------------
#Get all customers
def getAllCustomers():
    mycursor.execute("SELECT * FROM Customers");
    result = mycursor.fetchall();
    print (result)
    return result
#Update balance(userid, changeinbalance,+1or-1)
def updateBalance(userid,changeinbalance,trans_type):
    sql = "UPDATE Customers SET balance = balance + %s WHERE userID = %s"
    val = (trans_type*changeinbalance,userid)
    mycursor.execute(sql, val)
    mydb.commit()
#Get balance (userid)
def getBalance(userid):
    sql = "Select balance FROM Customers WHERE userID = "
    mycursor.execute(sql+str(userid))
    result = mycursor.fetchall()
    print (result)
    return result
#Change address(userid, address)
def changeAddress(userid,address):
    sql = "UPDATE Customers SET address = %s WHERE userID = %s"
    val = (address,userid)
    mycursor.execute(sql, val)
    mydb.commit()
#Change VIP status (userid, vip)
def changeVIP(userid,vip):
    sql = "UPDATE Customers SET VIP_STATUS = %s WHERE userID = %s"
    val = (vip,userid)
    mycursor.execute(sql, val)
    mydb.commit()

#############################################################################################
#-----------------------------------------Menu-----------------------------------------------
#############################################################################################

#Get all food
def getAllItems():
    mycursor.execute("SELECT * FROM Food")
    result = mycursor.fetchall()
    print (result)
    return result
#Get all beverages,appetizers,entrees,others
def getAllOfType(type):
    mycursor.execute("SELECT * FROM Food WHERE itemtype = '%s'" % type)
    result = mycursor.fetchall()
    print (result)
    return result
#Add item (id,price,name,description,type,image)
def addItem(id,price,name,description,type,image):
    try:
        sql = "INSERT INTO Food (item_no,price,name,description,itemtype,no_sold,image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (id,price,name,description,type,0,image)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Item added to menu.")
        return True
    except IntegrityError:
        print("Item already exists.")
        return False
    except:
        print("An exception occurred.")
        return False
#Update item description(id, description)
def updateItemDescription(id, description):
    sql = "UPDATE Food SET description = %s WHERE item_no = %s"
    val = (description,id)
    mycursor.execute(sql, val)
    mydb.commit()
#Update item image(id, image)
def updateItemImage(id, image):
    sql = "UPDATE Food SET image = %s WHERE item_no = %s"
    val = (image,id)
    mycursor.execute(sql, val)
    mydb.commit()
#Update rating with new rating from completed order
def updateRating(id,new_rating):
    sql = "SELECT rating, no_sold FROM Food Where item_no = " + str(id)
    mycursor.execute(sql)
    result = mycursor.fetchall()[0]
    tmp_rating = 0
    if (result[0] == None):
        tmp_rating = new_rating
    else:
        tmp_rating = (result[0]*result[1] + new_rating) / (result[1]+1)
    sql = "UPDATE Food SET rating = %s, no_sold = no_sold+1 WHERE item_no = %s"
    val = (tmp_rating,id)
    mycursor.execute(sql,val)
    mydb.commit()
    print (result)
#Delete item(id)
def deleteItem(id):
    sql = "DELETE FROM Food WHERE item_no = " + str(id)
    mycursor.execute(sql)
    mydb.commit()

#############################################################################################
#-----------------------------------------ORDERS---------------------------------------------
#############################################################################################

#Get all orders
#Get all incomplete orders
#Get all orders for CustomerID
#Get all orders for DeliveryID
#Get all orders for ChefID
#Create new order (orderid,customerid,arrayof[chefID,item,price,quantity])
#Assign delivery people(userid)
#Update order status
#Reviews (delivery_rating,delivery_review,arrayof[item_rating,item_reviews])
#Delete order(id)

#File complaint/compliment (entry_no,fault_id,reviewer_id,type(+ or -),critique,status)
#Update complaint/compliment(status)
#Complete complaint/compliment(verdict,id_affected,merit_change(+or-))

#---------------------------------------Discussion-----------------------------------------------
#Create new post (userid,title,body)
#Add reply(userid,reply)
#Get posts
#Get posts/replies for userid
#Delete post
#Delete reply



mycursor.close()
mydb.close()