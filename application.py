from flask import Flask, render_template, request
import pymysql
from datetime import date

today = date.today()
d1 = today.strftime("%y/%m/%d")

app = Flask(__name__)

id = 0

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    return render_template("signup.html")


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    return render_template("login.html")


@app.route("/signup-success", methods = ['POST', 'GET'])
def signup_success():

    db = pymysql.connect("localhost", "aayush", "deadpool", "Finance")
    cur = db.cursor()

    cur.execute("INSERT INTO Signup (Name, Contact, Username, Password, City, Email) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(request.form['Name'], request.form['contact'], request.form['uname'], request.form['passwd'], request.form['city'], request.form['email']))
    db.commit()
    return render_template('login.html')


@app.route("/login-success", methods = ['GET', 'POST'])
def log_success():
    global id
    username = request.form['usname']
    password = request.form['passwd']

    db = pymysql.connect("localhost", "aayush", "deadpool", "Finance")
    cur = db.cursor()

    cur.execute("SELECT * FROM Signup WHERE Username = '{}'".format(username))
    temp = cur.fetchall()
    id = int(temp[0][0])
    check = temp[0][4]

    cat_id, eamount, ecatname, iamount, icat_name, date, date1 = [], [], [], [], [], [], []

    cur.execute("SELECT * FROM Expenses WHERE ID = {}".format(id))
    exp = cur.fetchall()
    cur.execute("SELECT * FROM Income WHERE ID = {}".format(id))
    inc = cur.fetchall()

    if check == password:
        for i in range(len(exp)):
            eamount.append(exp[i][3])
            cur.execute("SELECT * FROM Categories WHERE Cat_ID = '{}'".format(exp[i][1]))
            ecatname.append(cur.fetchall()[0][1])
            date.append(exp[i][2])

        for i in range(len(inc)):
            iamount.append(inc[i][3])
            cur.execute("SELECT * FROM Income_category WHERE ICat_ID = '{}'".format(inc[i][1]))
            icat_name.append(cur.fetchall()[0][1])
            date1.append(inc[i][2])

        data1 = zip(ecatname, eamount, date)
        data2 = zip(icat_name, iamount, date1)
        return render_template("home.html", Name = username, data1 = data1, data2 = data2)
    else:
        return render_template("login.html")


@app.route("/add_expense", methods=['GET', 'POST'])
def add_expense():
    return render_template("add_expense.html")


@app.route("/remove_expense", methods = ['GET', 'POST'])
def remove_expense():
    return render_template("remove_expense.html")


@app.route("/add_income", methods = ['GET', 'POST'])
def add_income():
    return render_template("add_income.html")


@app.route("/remove_income", methods = ['GET', 'POST'])
def remove_income():
    return render_template("remove_income.html")


@app.route("/iremove_success", methods = ['GET', 'POST'])
def iremove_success():
    ename = request.form['ename']

    db = pymysql.connect("localhost", "aayush", "deadpool", "Finance")
    cur = db.cursor()

    cur.execute("SELECT Income_category.ICat_ID FROM Income_category, Income WHERE ID = {} AND Income_category.ICat_ID = Income.ICat_ID AND Income_category.I_name = '{}'".format(id, ename))
    temp = cur.fetchall()
    catid = []

    for i in range(len(temp)):
        catid.append(int(temp[i][0]))

    cur.execute("DELETE FROM Income WHERE ICat_ID = {}".format(catid[0]))
    db.commit()

    page, data1, data2 = display()
    
    return render_template(page, data1 = data1, data2 = data2)


@app.route('/iadd_success', methods = ['GET', 'POST'])
def iadd_success():
    global id
    global d1

    cat = request.form['income']
    amount = request.form['amount']

    db = pymysql.connect("localhost", "aayush", "deadpool", "Finance")
    cur = db.cursor()

    cur.execute("SELECT I_name FROM Income_category")
    temp = cur.fetchall()[0]

    catid = 1

    cur.execute("SELECT ICat_ID FROM Income_category WHERE I_name = '{}'".format(cat))
    temp1 = cur.fetchall()

    if temp1 == ():
        cur.execute("SELECT max(ICat_ID) FROM Income_category")
        catid = cur.fetchall()
        catid = catid[0][0]
        catid += 1
        cur.execute("INSERT INTO Income_category (ICat_ID, I_name) VALUES ('{}', '{}')".format(catid, cat))
        db.commit()

    else:
        catid = temp1[0][0]

    cur.execute("INSERT INTO Income (ID, ICat_ID, Date, Amount) VALUES ('{}', '{}', '{}', '{}')".format(id, catid, d1, amount))
    db.commit()

    page, data1, data2 = display()

    return render_template(page, data1 = data1, data2 = data2)


@app.route("/remove_success", methods = ['GET', 'POST'])
def remove_success():
    ename = request.form['ename']

    db = pymysql.connect("localhost", "aayush", "deadpool", "Finance")
    cur = db.cursor()

    cur.execute("SELECT Categories.Cat_ID FROM Categories, Expenses WHERE ID = {} AND Categories.Cat_ID = Expenses.Cat_ID AND Categories.Cat_name = '{}'".format(id, ename))
    temp = cur.fetchall()
    catid = []

    for i in range(len(temp)):
        catid.append(int(temp[i][0]))

    cur.execute("DELETE FROM Expenses WHERE Cat_ID = {}".format(catid[0]))
    db.commit()

    page, data1, data2 = display()

    return render_template(page, data1 = data1, data2 = data2)


@app.route("/add_success", methods=["GET", "POST"])
def add_success():
    global id
    global d1

    cat = request.form['expense']
    amount = request.form['amount']

    db = pymysql.connect("localhost", "aayush", "deadpool", "Finance")
    cur = db.cursor()

    cur.execute("SELECT Cat_name FROM Categories")
    temp = cur.fetchall()[0]

    catid = 1

    cur.execute("SELECT Cat_ID FROM Categories WHERE Cat_name = '{}'".format(cat))
    temp1 = cur.fetchall()

    if temp1 == ():
        cur.execute("SELECT max(Cat_ID) FROM Categories")
        catid = cur.fetchall()
        catid = catid[0][0]
        catid += 1
        cur.execute("INSERT INTO Categories (Cat_ID, Cat_name) VALUES ('{}', '{}')".format(catid, cat))
        db.commit()

    else:
        catid = temp1[0][0]

    cur.execute("INSERT INTO Expenses (ID, Cat_ID, Date, Amount) VALUES ('{}', '{}', '{}', '{}')".format(id, catid, d1, amount))
    db.commit()

    page, data1, data2 = display()
    return render_template(page, data1 = data1, data2 = data2)


def display():
    db = pymysql.connect("localhost", "aayush", "deadpool", "Finance")
    cur = db.cursor()

    cur.execute("SELECT * FROM Expenses WHERE ID = {}".format(id))
    temp = cur.fetchall()

    cur.execute("SELECT * FROM Income WHERE ID = {}".format(id))
    temp1 = cur.fetchall()

    name, amt, date, name2, amt2, date2 = [], [], [], [], [], []

    for i in range(len(temp)):
        cur.execute("SELECT * FROM Categories WHERE Cat_ID = {}".format(temp[i][1]))
        name.append(cur.fetchall()[0][1])
        amt.append(temp[i][3])
        date.append(temp[i][2])

    for i in range(len(temp1)):
        cur.execute("SELECT * FROM Income_category WHERE ICat_ID = {}".format(temp1[i][1]))
        name2.append(cur.fetchall()[0][1])
        amt2.append(temp1[i][3])
        date2.append(temp1[i][2])

    data1 = zip(name, amt, date)
    data2 = zip(name2, amt2, date2)

    return 'home.html', data1, data2


app.run(debug = True)
