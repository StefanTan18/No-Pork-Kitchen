import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "5326atAT!", # Change accordingly
    database = "noporkkitchendb"
)

cur = mydb.cursor()

def giveiOrder(ordernum, itemno, price, quantity):
    sql = "INSERT INTO OrderItems (order_no, item_no, price, quantity) VALUES (%s, %s, %s, %s)"
    val = (ordernum, itemno, price, quantity)
    cur.execute(sql, val)
    mydb.commit()

def giveOrder(ordernum, customerID, deliveryID, total_price, status):
    sql = "INSERT INTO Orders (order_no, customerID, deliveryID, total_price, status) VALUES (%s, %s, %s, %s, %s)"
    val = (ordernum, customerID, deliveryID, total_price, status)
    cur.execute(sql, val)
    mydb.commit()

def returnPrice(itemno):
    sql = "SELECT Price FROM Food WHERE item_no = " + str(itemno) + ";"
    cur.execute(sql)
    rows = [x[0] for x in cur.fetchall()]
    for row in rows:
        return row

def setCooked(orderNo):
    sql = "UPDATE Orders SET status = 'Cooked' WHERE order_no = " + str(orderNo) + ";"
    cur.execute(sql)
    mydb.commit()

def setDelivered(orderNo):
    sql = "UPDATE Orders SET status = 'Delivered' WHERE order_no = " + str(orderNo) + ";"
    cur.execute(sql)
    mydb.commit()

def setDriver(orderNo, driverID):
    sql = "UPDATE Orders SET driverID = %s WHERE order_no = %s;"
    val = (driverID, orderNo)
    cur.execute(sql, val)
    mydb.commit()

def giveReview(orderNo, rating, review):
    sql = "UPDATE OrderItems SET item_rating = %s AND item_review = %s WHERE order_no = %s;"
    val = (rating, review, orderNo)
    cur.execute(sql, val)
    mydb.commit()

def giveDReview(orderNo, rating, review):
    sql = "UPDATE Orders SET delivery_rating = %s AND delivery_review = %s WHERE order_no = %s;"
    val = (rating, review, orderNo)
    cur.execute(sql, val)
    mydb.commit()

def currentCus():
        sql = "SELECT currentcus FROM Accumulator;"
        cur.execute(sql)
        rows = [x[0] for x in cur.fetchall()]
        for row in rows:
                return row

def currentOrd():
        sql = "SELECT currentord FROM Accumulator;"
        cur.execute(sql)
        rows = [x[0] for x in cur.fetchall()]
        for row in rows:
                return row

currcus = currentCus()
currord = currentOrd()

class ShoppingCart:
    global currord
    def __init__(self, num, quantity, userID):
        self.num = num
        self.quantity = quantity
        self.userID = userID

    def addItem(self, itemno, itemq):
        num.append(itemno)
        quantity.append(itemq)

    def calculateTotal(self):
        total = 0
        for i in range(len(self.num)):
            total += (returnPrice(self.num[i])*self.quantity[i])
        return total

    def executeOrder(self, driverID):
        global currentOrd
        total = self.calculateTotal()
        try:
            giveOrder(currentOrd, self.userID, driverID, total, 0)
            for i in range(len(self.num)):
                giveiOrder(currentOrd, self.num[i], returnPrice(self.num[i]), self.quantity[i])
            sql = "UPDATE Accumulator SET currentord = " + str(currentOrd()+1) + ";"
            cur.execute(sql)
            currentord+=1
        except:
            print("Order number already pending")

class Bids:
    def __init__(self, orderNo, bids):
        self.orderNo = orderNo
        self.bids = bids

    def addBid(self, bid):
        self.bids.append(bid)

    def acceptBid(self, ID):
        for a, b in self.bids:
            if(a==ID):
                setDriver(self.orderNo, ID)

def login(username, password):
    sql = "SELECT userID FROM Users WHERE username = %s and password = %s;"
    val = (username, password)
    cur.execute(sql,val)
    rows = [x[0] for x in cur.fetchall()]
    for row in rows:
        return row

def selectusertype(username, password):
    sql = "SELECT usertype FROM Users WHERE username = %s and password = %s;"
    val = (username, password)
    cur.execute(sql,val)
    rows = [x[0] for x in cur.fetchall()]
    for row in rows:
        return row

def registerSQL(userID, name, address, username, password, usertype):
    global currcus
    sql = "Select userID FROM Users WHERE username = %s AND password = %s;"
    val = (username, password)
    cur.execute(sql, val)
    if len(cur.fetchall())==0:
        if(usertype=="Customer"):
            sql = "INSERT INTO Users (userID, name, username, password, userType, status, flag) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (userID, name, username, password, usertype, "nil", 0)
            cur.execute(sql, val)
            sql = "INSERT INTO Customers (userID, balance, address, VIP_Status) VALUES (%s, %s, %s, %s)"
            val = (userID, 0, address, 0)
            cur.execute(sql, val)
            sql = "UPDATE Accumulator SET currentcus = " + str(currentCus()+1) + ";"
            cur.execute(sql)
            currcus += 1
            mydb.commit()
        elif (usertype=="Chef"):
            sql = "INSERT INTO Users (userID, name, username, password, userType, status, flag) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (userID, name, username, password, usertype, "nil", 0)
            cur.execute(sql, val)
            sql = "INSERT INTO Chefs (userID, salary, hours_worked) VALUES (%s, %s, %s)"
            val = (userID, 20, 0)
            cur.execute(sql, val)
            sql = "UPDATE Accumulator SET currentcus = " + str(currentCus()+1) + ";"
            cur.execute(sql)
            currcus += 1
            mydb.commit()
        elif (usertype=="Delivery"):
            sql = "INSERT INTO Users (userID, name, username, password, userType, status, flag) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (userID, name, username, password, usertype, "nil", 0)
            cur.execute(sql, val)
            sql = "INSERT INTO Delivery (userID, distance, earnings, no_deliveries) VALUES (%s, %s, %s, %s)"
            val = (userID, 0, 0, 0)
            cur.execute(sql, val)
            sql = "UPDATE Accumulator SET currentcus = " + str(currentCus()+1) + ";"
            cur.execute(sql)
            currcus += 1
            mydb.commit()
    else:
        print("Username already in use.")

def addFood(num, price, name, description, itemtype, chefID, img):
    sql = "INSERT INTO Food (item_no, price, name, description, itemtype, rating, no_sold, chefID, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (num, price, name, description, itemtype, 0, chefID, img)
    try:
        cur.execute(sql, val)
        mydb.commit()
    except:
        print("Food num already registered to another item")

cur.close()
mydb.close()


