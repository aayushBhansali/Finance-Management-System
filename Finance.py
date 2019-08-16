import sqlite3 as sql
from datetime import date
import pandas as pd
from pandas import ExcelWriter

class Finance:

    def __init__(self):
        self.date = date.today().strftime("%d-%m-%y")
        self.expense_name = "None"
        self.expense_amount = 0
        self.income_name = "None"
        self.income_amount = 0
        self.df = ""


    def showFinance(self):
        print("Date : " + str(self.date))
        print("Income : " + str(self.income_name))
        print("Amount : " + str(self.income_amount))
        print("Expense : " + str(self.expense_name))
        print("Amount : " + str(self.expense_amount))


    def add_expense(self, name, amount):
        self.expense_name = name
        self.expense_amount = amount


    def add_income(self, name, amount):
        self.income_name = name
        self.income_amount = amount


    def write_to_db(self):
        db = sql.connect("Finance.db")
        cur = db.cursor()
        cur.execute("INSERT INTO Finance (Date, Expense_name, Expense_amount, Income_name, Income_amount) VALUES (" + "'" + str(self.date) + "', '" + str(self.expense_name) + "', " + str(self.expense_amount) + ", '" + str(self.income_name) + "', " + str(self.income_amount) + " )")
        db.commit()
        db.close()

    def read_from_db(self):
        db = sql.connect("Finance.db")
        self.df = pd.read_sql_query("SELECT * FROM Finance", db)
        print(self.df)


    def write_to_excel(self):
        writer = ExcelWriter("Finance.xlsx")
        self.df.to_excel(writer, 'Sheet1')
        writer.save()


def procedure():
    f = Finance()
    f.showFinance()
    f.add_expense("Fruits", 100)
    f.add_income("Pocket", 300)
    f.write_to_db()
    f.read_from_db()
    f.write_to_excel()


if __name__ == "__main__":
    procedure()
