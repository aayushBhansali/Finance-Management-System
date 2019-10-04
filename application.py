from flask import Flask, render_template, request
import pymysql
from datetime import date

today = date.today()
d1 = today.strftime("%d/%m/%y")

app = Flask(__name__)

id = 0

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    return render_template("signup.html")


@app.route("/signup-success", methods = ['POST', 'GET'])
def signup_success():
    fname = request.form["Name"]
    contact = request.form["contact"]
    uname = request.form["uname"]
    pswd = request.form["passwd"]
    city = request.form["city"]
    email = request.form["email"]

    db = pymysql.connect("localhost", "aayush", "deadpool", "Finance")
    cur = db.cursor()

    cur.execute("INSERT INTO Signup (Name, Contact, Username, Password, City, Email) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(fname, contact, uname, pswd, city, email))
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

    cat_id = []
    amount = []
    cat_name = []

    cur.execute("SELECT * FROM Expenses WHERE ID = {}".format(id))
    exp = cur.fetchall()

    if check == password:
        for i in range(len(exp)):
            amount.append(exp[i][3])
            cur.execute("SELECT * FROM Categories WHERE Cat_ID = '{}'".format(exp[i][1]))
            cat_name.append(cur.fetchall()[0][1])

        data = zip(cat_name, amount)
        return render_template("home.html", Name = username, data = data)
    else:
        return render_template("login.html")


@app.route("/add_expense", methods=['GET', 'POST'])
def add_expense():
    return render_template("add_expense.html")


@app.route("/remove_expense", methods = ['GET', 'POST'])
def remove_expense():
    return render_template("remove_expense.html")


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

    cur.execute("SELECT * FROM Expenses WHERE ID = {}".format(id))
    temp = cur.fetchall()
    name = []
    amt = []

    for i in range(len(temp)):
        cur.execute("SELECT * FROM Categories WHERE Cat_ID = {}".format(temp[i][1]))
        name.append(cur.fetchall()[0][1])
        amt.append(temp[i][3])

    data = zip(name, amt)

    return render_template("home.html", data = data)


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

    cur.execute("SELECT * FROM Expenses WHERE ID = {}".format(id))
    temp = cur.fetchall()
    name = []
    amt = []

    for i in range(len(temp)):
        cur.execute("SELECT * FROM Categories WHERE Cat_ID = {}".format(temp[i][1]))
        name.append(cur.fetchall()[0][1])
        amt.append(temp[i][3])

    print(name)
    print(amt)
    data = zip(name, amt)

    return render_template("home.html", data = data)






if __name__ == "__main__":
    app.run(debug = True)
