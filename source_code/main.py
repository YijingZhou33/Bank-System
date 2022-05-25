import sqlite3
import hashlib
import os

conn = None
c = None

salt = "$6cab6b2acabc"
start_month = (2022, 4)  # may 2022
month_str = ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]


def initDB():
    # username max. length 64 bytes
    # password: sha-256 64 chars, username+password+salt
    # role: admin or client
    c.execute("drop table if exists user;")
    c.execute('''create table user
       (username char(64) primary key,
       password char(64) not null,
       role  char(16)    not null);''')
    passwd_admin = hashlib.sha256(("adminadmin" + salt).encode("utf8")).hexdigest()
    c.execute(f"insert into user values('admin', '{passwd_admin}', 'admin');")

    # loan rate/ deposit rate: integer x in db. real rate is (x/100)%
    # asset: integer x in db.  real asset is x/100
    # timestamp: months start from May, 2022
    c.execute("drop table if exists bank;")
    c.execute('''create table bank
       (id bigint primary key,
       asset bigint not null,
       loanrate bigint not null,
       depositrate bigint not null,
       timestamp bigint not null);''')
    c.execute(f"insert into bank values(1, 1000000000, 1000, 500, 0);")

    # balance: integer x in db. real balance is x/100
    c.execute("drop table if exists client;")
    c.execute('''create table client
       (username char(64) primary key,
        balance bigint not null);''')

    # loan amount/remaining amount: integer x in db. real amount is x/100
    # opening/due date: timestamp integers
    c.execute("drop table if exists loan;")
    c.execute('''create table loan
       (id integer primary key AUTOINCREMENT,
       username char(64) not null,
       loanamount bigint not null,
       remainingamount bigint not null,
       openingdate bigint not null,
       duedate bigint not null);''')
    c.execute("create index loan_user on loan(username);")

    conn.commit()


if os.path.exists("./proj.db"):
    conn = sqlite3.connect("./proj.db")
    c = conn.cursor()
else:
    conn = sqlite3.connect("./proj.db")
    c = conn.cursor()
    initDB()


"""
floating point to int(*100), and int(*100) to floating point
max. 2 digits after decimal point
"""


def int2DecStr(a):
    return str(a // 100) + "." + str((a % 100) // 10) + str(a % 10)


def decStr2Int(s):
    try:
        return int(s) * 100
    except Exception:
        try:
            if len(s.split(".")[1]) > 2:
                return None
            return round(float(s) * 100)
        except Exception:
            return None


def timestamp2Str(a):
    month = start_month[1] + a
    year = start_month[0] + month // 12
    month %= 12
    return month_str[month] + ", " + str(year)


def register():
    """
    input username and password from CLI. on error return to main menu.
    TODO: check input with regex
    """
    username = input("Please enter your username (no more than 16 characters): ")
    if (len(username) <= 0):
        print("\nInvalid username, please try again. ")
        return
    if (len(username) > 16):
        print("\nUsername too long, please try again. ")
        return
    data = c.execute("select username from user where username=?", (username,)).fetchone()
    if data is not None:
        print("\nThe username has already existed, please choose a new one. ")
        return

    password = input("Please enter your password: ")
    if (len(password) <= 0):
        print("\nInvalid password, please try again. ")
        return
    password = hashlib.sha256((username + password + salt).encode("utf8")).hexdigest()
    c.execute("insert into user values(?, ?, 'client');", (username, password))
    c.execute("insert into client values(?, 0);", (username,))
    conn.commit()
    print("\nCongratulations, your account has been successfully created. ")


def changeRates():
    data = c.execute("select asset, loanrate, depositrate from bank where id=1").fetchone()
    # init asset = 10,000,000.00
    init_asset = 1000000000
    # target loan rate = 10 - (asset-init_asset)/100,000.00
    # target deposit rate = 5 - (asset-init_asset)/100,000.00
    asset = int(data[0])
    loanrate = int(data[1])
    depositrate = int(data[2])
    target_loanrate = round(1000 - (asset - init_asset) / 100000)
    target_depositrate = round(500 - (asset - init_asset) / 100000)
    min_loanrate, max_loanrate = loanrate, loanrate
    if target_loanrate < loanrate:
        min_loanrate = max(target_loanrate, loanrate - 50, 0)
    else:
        max_loanrate = min(target_loanrate, loanrate + 50)

    min_depositrate, max_depositrate = depositrate, depositrate
    if target_depositrate < depositrate:
        min_depositrate = max(target_depositrate, depositrate - 50, 0)
    else:
        max_depositrate = min(target_depositrate, depositrate + 50)
    print(
        f"\nTotal Assets : {int2DecStr(asset)} \nLoan Rate : {int2DecStr(loanrate)}%\nDeposit Rate : {int2DecStr(depositrate)}%\n")
    print(f"The new loan rate should be in range {int2DecStr(min_loanrate)}%-{int2DecStr(max_loanrate)}%")
    print(f"The new deposit rate should be in range {int2DecStr(min_depositrate)}%-{int2DecStr(max_depositrate)}%")
    print(
        "Your input number should have at most 2 decimal places. If you want to change the rate to 4.56%, then input '4.56' (without quotes) and press enter.\n")

    new_loanrate = decStr2Int(input("Please enter the new loan rate: "))
    if new_loanrate is None or new_loanrate < min_loanrate or new_loanrate > max_loanrate:
        print("Loan rate change failed: Invalid input.")
    else:
        c.execute("update bank set loanrate=? where id=1;", (new_loanrate,))
        conn.commit()
        print("Loan rate has been successfully changed!\n")

    new_depositrate = decStr2Int(input("Please enter the new deposit rate:"))
    if new_depositrate is None or new_depositrate < min_depositrate or new_depositrate > max_depositrate:
        print("Deposit rate change failed: Invalid input.")
    else:
        c.execute("update bank set depositrate=? where id=1;", (new_depositrate,))
        conn.commit()
        print("Deposit rate has been successfully changed!\n")


def admin():
    while True:
        print("\n---------------- Admin Dashboard ---------------")
        data = c.execute("select asset, loanrate, depositrate,timestamp from bank where id=1").fetchone()
        print("Current Time : " + timestamp2Str(int(data[3])) + "\nTotal Assets : " + int2DecStr(int(data[0])))
        print(
            "Loan Rate : " + int2DecStr(int(data[1])) + "%\nDeposit Rate : " + int2DecStr(int(data[2])) + "%")
        print("""------------------------------------------------ 
              1. Change Interest Rates
              2. Log Out
------------------------------------------------                  
        """)
        id = input("Please enter your option: ")
        if id == "1":
            changeRates()
        elif id == "2":
            break
        else:
            print("Invalid option, please try again.\n")


def deposit(username):
    print("\nYour input amount should be in range [0.01, 10000], with at most 2 decimal places.")
    deposit = decStr2Int(input("Please enter your deposit amount: "))
    if deposit is None or deposit <= 0 or deposit > 1000000:
        print("\nDeposit failed: invalid input, please try again.")
        return
    elif deposit > 0:
        c.execute("update client set balance=balance+? where username=?;", (deposit, username))
        c.execute("update bank set asset=asset+? where id=1;", (deposit,))
        conn.commit()
    print("\nYour deposit has been successfully processed!")


def withdraw(username, balance):
    print(
        "\nYour input amount should be in range [0.01, 2000] (and not greater than your balance), with at most 2 decimal places.")
    withdraw = decStr2Int(input("Please enter your withdrawal amount: "))
    if withdraw is None or withdraw <= 0 or withdraw > 200000 or withdraw > balance:
        print("\nWithdraw failed: invalid input, please try again. ")
        return
    elif withdraw > 0:
        c.execute("update client set balance=balance-? where username=?;", (withdraw, username))
        c.execute("update bank set asset=asset-? where id=1;", (withdraw,))
        conn.commit()
    print("\nYour withdrawl has been successfully processed!")


def createLoan(username, timestamp):
    loanrate = c.execute("select loanrate from bank where id=1;").fetchone()
    loanrate = int(loanrate[0])
    print(f"\nCurrent loan rate : {int2DecStr(loanrate)}%")
    exist_loans = c.execute("select duedate from loan where username=?;", (username,)).fetchall()
    # print(exist_loans)
    min_due = min([int(i[0]) for i in exist_loans]) if len(exist_loans) > 0 else timestamp + 1
    if min_due <= timestamp:
        print("You have loan(s) overdue.")
    elif len(exist_loans) >= 3:
        print("\nYou have already reached limitation of total loan amount (3).")
    else:
        print("Your input amount should be in range [0.01, 10000], with at most 2 decimal places.")
        loan = decStr2Int(input("Please enter your loan amount: "))
        if loan is None or loan <= 0 or loan > 1000000:
            print("\nLoan initialization failed: invalid input, please try again.")
            return
        else:
            print("\nYour loan has been successfully initialized!")
        loaninterest = round(loan * loanrate / 10000)
        c.execute("update client set balance=balance+? where username=?;", (loan, username))
        c.execute("insert into loan (username, loanamount, remainingamount, openingdate, duedate) values(?,?,?,?,?);"
                  , (username, loan, loan + loaninterest, timestamp, timestamp + 12))
        conn.commit()


def payLoan(username, balance):
    exist_loans = c.execute("select id, loanamount, remainingamount, openingdate, duedate  from loan where username=?;",
                            (username,)).fetchall()
    if (len(exist_loans) == 0):
        print("You don't have any loan.")
        return
    print()
    print("----------------------------------------------------------------------------------------------------------")
    print(f"{'Option':8} | {'Loan Id':12} | {'Loan Amount':16} | {'Remaining Amount':20} | {'Opening Date':20} | {'Due Date':20}")
    print("----------------------------------------------------------------------------------------------------------")
    cnt = 0
    for loan in exist_loans:
        cnt += 1
        print(
            f"{cnt:<8} | {loan[0]:<12} | {int2DecStr(loan[1]):16} | {int2DecStr(loan[2]):20} | {timestamp2Str(loan[3]):20} | {timestamp2Str(loan[4]):20}")
    print("----------------------------------------------------------------------------------------------------------")

    if (balance == 0):
        print("\nYour balance is 0, please make a deposit first!")
        return
    id = input("\nPlease enter your option: ")
    if id == "1":
        id = 0
    elif id == "2" and cnt >= 2:
        id = 1
    elif id == "3" and cnt >= 3:
        id = 2
    else:
        print("\nInvalid option, please try again.")
        return
    loan = exist_loans[id]
    remaining = int(loan[2])
    max_payment = min(balance, remaining)
    print(
        f"\nYour input amount should be in range [0.01, {int2DecStr(max_payment)}], with at most 2 decimal places.")
    payment = decStr2Int(input("Please enter your payment amount: "))
    if payment is None or payment <= 0 or payment > max_payment:
        print("\nRepayment failed: invalid input, please try again.")
        return
    c.execute("update client set balance=balance-? where username=?;", (payment, username))
    if payment == remaining:
        c.execute("delete from loan where id=?;", (int(loan[0]),))
    else:
        c.execute("update loan set remainingamount=remainingamount-? where id=?;", (payment, int(loan[0])))
    conn.commit()
    print("\nYour repayment has been successfully processed!")


def pass1Month():
    # TODO: pass 1 month, add deposit interest, auto-pay
    c.execute("update client set balance=balance+round(balance*(select depositrate from bank where id=1)/120000.0,0);")
    expired_loans = c.execute(
        "select id,username,remainingamount from loan where duedate<=(select timestamp from bank where id=1)+1;").fetchall()
    for loan in expired_loans:
        loan_id, username, remaining = int(loan[0]), loan[1], int(loan[2])
        balance = c.execute("select balance from client where username=?;", (username,)).fetchone()
        balance = int(balance[0])
        if balance == 0:
            continue
        if balance >= remaining:
            c.execute("update client set balance=balance-? where username=?;", (remaining, username))
            c.execute("delete from loan where id=?;", (loan_id,))
        else:
            c.execute("update client set balance=0 where username=?;", (username,))
            c.execute("update loan set remainingamount=remainingamount-? where id=?;", (balance, loan_id))

    c.execute("update bank set timestamp=timestamp+1 where id=1;")
    conn.commit()


def checkLoans(username):
    expired_loans = c.execute("select id,remainingamount from loan where username=? \
    and duedate<=(select timestamp from bank where id=1);", (username,)).fetchall()
    res = 0
    for loan in expired_loans:
        balance = c.execute("select balance from client where username=?;", (username,)).fetchone()
        balance = int(balance[0])
        loan_id, remaining = int(loan[0]), int(loan[1])
        if balance == 0:
            res += remaining
        elif balance >= remaining:
            c.execute("update client set balance=balance-? where username=?;", (remaining, username))
            c.execute("delete from loan where id=?;", (loan_id,))
        else:
            res += remaining-balance
            c.execute("update client set balance=0 where username=?;", (username,))
            c.execute("update loan set remainingamount=remainingamount-? where id=?;", (balance, loan_id))
    return res

def client(username):
    while True:
        print("\n-------------- Customer Dashboard -------------")
        expired_loans = checkLoans(username)
        # timestamp = int((c.execute("select timestamp from bank where id=1").fetchone())[0])
        timestamp = c.execute("select timestamp from bank where id=1;").fetchone()
        timestamp = int(timestamp[0])
        balance = c.execute("select balance from client where username=?;", (username,)).fetchone()
        balance = int(balance[0])
        print(f"Current Time : {timestamp2Str(timestamp)}\nYour Balance : {int2DecStr(balance)}")
        if expired_loans > 0:
            print("Account is locked now, please pay off the loan first.")
        print("""-----------------------------------------------
                1. Deposit
                2. Withdrawal
                3. Loan
                4. Repayment
                5. Time Forward
                6. Log Out       
-----------------------------------------------
        """)
        id = input("Please input your option: ")
        if id == "1":
            deposit(username)
        elif id == "2":
            withdraw(username, balance)
        elif id == "3":
            createLoan(username, timestamp)
        elif id == "4":
            payLoan(username, balance)
        elif id == "5":
            pass1Month()
        elif id == "6":
            break
        elif id == "greedisgood":  # magic string (warcraft 3 cheat code, gives you 500 gold)
            c.execute("update client set balance=balance+50000 where username=?;", (username,))
            conn.commit()
        else:
            print("\nInvalid option, please try again.")


def login():
    """
    input username and password from CLI. on error return to main menu.
    If it is admin, goto admin dashboard. else goto client dashboard.
    """
    username = input("Please enter your username (no more than 16 characters): ")
    if (len(username) <= 0):
        print("\nInvalid username, please try again.")
        return
    if (len(username) > 16):
        print("\nUsername too long, please try again.")
        return
    password = input("Please enter your password: ")
    if (len(password) <= 0):
        print("\nInvalid password, please try again.")
        return
    password = hashlib.sha256((username + password + salt).encode("utf8")).hexdigest()
    data = c.execute("select username, role from user where username=? and password=?", (username, password)).fetchone()
    if data is None:
        print("\nWrong username/password, please try again.\n")
        return

    if data[1] == "admin":
        admin()
    else:
        client(username)


# initDB()
if __name__ == "__main__":
    while True:
        print("""\n------------------------------------------------
                  1. Register
                  2. Login
                  3. Exit
------------------------------------------------
    """)
        id = input("Please enter your option: ")
        if id == "1":
            register()
        elif id == "2":
            login()
        elif id == "3":
            break
        else:
            print("Invalid option, please try again.\n")

# cursor = c.execute("select username, password from user")
# for row in cursor:
#    print(row[0], row[1])

# cursor = c.execute("select * from bank")
# for row in cursor:
#    print(row[0], row[1], row[2], row[3], row[4])
# #initDB()
conn.close()