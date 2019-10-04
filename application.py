from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)


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
    username = request.form['usname']
    password = request.form['passwd']

    db = pymysql.connect("localhost", "aayush", "deadpool", "Finance")
    cur = db.cursor()

    cur.execute("SELECT * FROM Signup WHERE Username = '{}'".format(username))
    temp = cur.fetchall()
    id = int(temp[0][0])
    print(id)
    check = temp[0][4]

    cat_id = []
    amount = []
    cat_name = []

    cur.execute("SELECT * FROM Expenses WHERE ID = {}".format(id))
    exp = cur.fetchall()
    print(exp)

    if check == password:
        for i in range(len(exp)):
            amount.append(exp[i][3])
            cur.execute("SELECT * FROM Categories WHERE Cat_ID = '{}'".format(exp[i][1]))
            cat_name.append(cur.fetchall()[0][1])

        data = zip(cat_name, amount)
        return render_template("home.html", Name = username, data = data)
    else:
        return render_template("login.html")




if __name__ == "__main__":
    app.run(debug = True)
