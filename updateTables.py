from tabnanny import check
from unicodedata import decimal
from venv import create
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
#Get item by ID
def getItem(itemID):
    mycursor.execute("SELECT * FROM Food WHERE item_no = '%s'" % itemID)
    result = mycursor.fetchall()
    print (result)
    return result
#Add item (id,price,name,description,type,image)
def addItem(id,price,name,description,type,chef,image):
    try:
        sql = "INSERT INTO Food (item_no,price,name,description,itemtype,no_sold,chefID,image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id,price,name,description,type,0,chef,image)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Item added to menu.")
        return True
    except IntegrityError:
        print("Item already exists.")
        return False
    except Exception as e:
        print("An exception occurred. Failed to add item.")
        print(e)
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
def getAllOrders():
    mycursor.execute("SELECT * FROM Orders")
    result = mycursor.fetchall()
    print (result)
    return result
#Get all incomplete orders
def getAllIncompleteOrders():
    mycursor.execute("SELECT * FROM Orders WHERE status != 'done'")
    result = mycursor.fetchall()
    print (result)
    return result
#Get all orders for CustomerID
def getAllOrdersForCust(id):
    mycursor.execute("SELECT * FROM Orders WHERE customerID = "+str(id))
    result = mycursor.fetchall()
    print (result)
    return result
#Get all orders for DeliveryID
def getAllOrdersForDelivery(id):
    mycursor.execute("SELECT * FROM Orders WHERE DeliveryID = "+str(id))
    result = mycursor.fetchall()
    print (result)
    return result
#Get all items from order
def getItemsFromOrder(orderid):
    mycursor.execute("SELECT * FROM OrderItems WHERE order_no = "+str(orderid))
    result = mycursor.fetchall()
    print (result)
    return result
#Create new order (orderid,customerid,arrayof[(item,quantity)])
def createOrder(orderid,customerid,items):
    try:
        sql = "INSERT INTO Orders (order_no,customerID,total_price,status) VALUES (%s, %s, %s, %s)"
        val = (orderid,customerid,0.00,"Order Received")
        mycursor.execute(sql, val)
        price = 0.00
        for i in items:
            price += float(addItemToOrder(orderid,i))
        sql = "UPDATE Orders SET total_price = %s WHERE order_no = %s"
        val = (price,orderid)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Order created successfully")
        return 1
    except Exception as e:
        print("Order failed. Please try again.")
        print(e)
        return 0
#Helper Function additems to add to orderitems table item = (item_no,quantity)
def addItemToOrder(order_no,item):
    try:
        mycursor.execute("SELECT * from Food where item_no = '%s'" % item[0])
        result = mycursor.fetchone()
        t_price = result[1] * item[1]
        sql = "INSERT INTO OrderItems (order_no,item_no,price,quantity) VALUES (%s, %s, %s, %s)"
        val = (order_no,item[0],t_price,item[1])
        mycursor.execute(sql, val)
        mydb.commit()
        return t_price; 
    except Exception as e:
        print("Unable to add Item.")
        print(e)
        return 0
#Delete order(id)
def deleteOrder(orderID):
    try: 
        sql = "DELETE FROM Orders WHERE order_no = %s" % orderID
        mycursor.execute(sql)
        mydb.commit()
    except Exception as e:
        print("Failed to Delete Order")
        print(e)
#Assign delivery people(userid)
def assignDelivery(orderID,deliveryID):
    try:
        sql = "UPDATE Orders SET deliveryID = %s WHERE order_no = %s"
        val = (deliveryID,orderID)
        mycursor.execute(sql, val)
        mydb.commit()
    except Exception as e:
        print ("Failed to add delivery driver")
        print(e)
#Update order status
def updateOrderStatus(orderID,status):
    try:
        sql = "UPDATE Orders SET status = %s WHERE order_no = %s"
        val = (status,orderID)
        mycursor.execute(sql, val)
        mydb.commit()
    except Exception as e:
        print ("Failed to update status")
        print(e)
#Reviews (delivery_rating,delivery_review)
def addDeliveryReview(orderID,delivery_rating,delivery_review):
    try:
        if (delivery_rating is not None):
            sql = "UPDATE Orders SET delivery_rating = %s, delivery_review = %s WHERE order_no = %s"
            val = (delivery_rating,delivery_review,orderID)
            mycursor.execute(sql, val)
        mydb.commit()
    except Exception as e:
        print ("Failed to update status")
        print(e)
#Reviews (arrayof[(item_no,item_rating,item_reveiew)])
def addItemsReview(orderID,item_reviews):
    try:
        for i in item_reviews:
            itemID = i[0]
            itemRating = i[1]
            itemReview = i[2]
            sql = "UPDATE OrderItems SET item_rating = %s, item_review = %s WHERE order_no = %s AND item_no = %s"
            val = (itemRating,itemReview,orderID,itemID)
            mycursor.execute(sql, val)
        mydb.commit()
    except Exception as e:
        print ("Failed to add item reviews")
        print(e)


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