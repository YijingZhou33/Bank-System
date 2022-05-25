import pytest
from main_test import *
import os, sys
from mock import patch

#----------------------------------------------------------------
#
#  Test Suite 1: FR-1: Main Menu
#
#----------------------------------------------------------------

# TC01: Display the register interface
def test_main_1(monkeypatch, capsys):
    inputs = iter(["1", "3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.register', lambda *_: print("register()"))
    main()
    captured = capsys.readouterr()
    assert "register()" in captured.out

# TC02: Display the login interface
def test_main_2(monkeypatch, capsys):
    inputs = iter(["2", "3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.login', lambda *_: print("login()"))
    main()
    captured = capsys.readouterr()
    assert "login()" in captured.out

# TC03: Quit the application
def test_main_3(monkeypatch, capsys):
    inputs = iter(["3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    a = main()
    captured = capsys.readouterr()
    assert a == None

# TC04: invalid input (123)
def test_main_4(monkeypatch, capsys):
    inputs = iter(["123", "3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "Invalid option, please try again." in captured.out

# TC05: invalid input (empty)
def test_main_5(monkeypatch, capsys):
    inputs = iter(["", "3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "Invalid option, please try again." in captured.out

#----------------------------------------------------------------
#
#  Test Suite 2: FR-2: Registration
#
#----------------------------------------------------------------

# len(username) = 1
# len(password) = 1
def test_register_1(monkeypatch, capsys):
    inputs = iter(["r", "r"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = None
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            register()
            captured = capsys.readouterr()
            assert "Congratulations, your account has been successfully created. " in captured.out

# missing password input 
def test_register_2(monkeypatch, capsys):
    inputs = iter(["r"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["r"]
        register()
        captured = capsys.readouterr()
        assert "The username has already existed, please choose a new one. " in captured.out

# len(username) = 0
# missing password input 
def test_register_3(monkeypatch, capsys):
    inputs = iter([""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    register()
    captured = capsys.readouterr()
    assert "Invalid username, please try again. " in captured.out

# len(username) = 15
def test_register_4(monkeypatch, capsys):
    inputs = iter(["qwertyuiopasdfg", "h"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = None
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            register()
            captured = capsys.readouterr()
            assert "Congratulations, your account has been successfully created. " in captured.out

# len(username) = 16
def test_register_5(monkeypatch, capsys):
    inputs = iter(["qwertyuiopasdfgh", "h"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = None
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            register()
            captured = capsys.readouterr()
            assert "Congratulations, your account has been successfully created. " in captured.out

# len(username) = 17
def test_register_6(monkeypatch, capsys):
    inputs = iter(["qwertyuiopasdfghj", "h"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    register()
    captured = capsys.readouterr()
    assert "Username too long, please try again. " in captured.out

# len(password) = 0
def test_register_7(monkeypatch, capsys):
    inputs = iter(["k", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = None
        register()
        captured = capsys.readouterr()
        assert "Invalid password, please try again. " in captured.out


#----------------------------------------------------------------
#
#  Test Suite 3: FR-3: Login
#
#----------------------------------------------------------------

# customer login: (r, r)
def test_login_1(monkeypatch, capsys):
    inputs = iter(["r", "r"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.client', lambda _: print("client(username)"))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["r", "r"]
        login()
        captured = capsys.readouterr()
        assert captured.out == "client(username)\n"

# admin login (admin, admin)
def test_login_2(monkeypatch, capsys):
    inputs = iter(["admin", "admin"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.admin', lambda: print("admin()"))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["admin", "admin"]
        login()
        captured = capsys.readouterr()
        assert captured.out == "admin()\n"

# wrong password (r, s)
def test_login_3(monkeypatch, capsys):
    inputs = iter(["r", "s"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = None
        login()
        captured = capsys.readouterr()
        assert captured.out == "\nWrong username/password, please try again.\n\n"

# wrong username (ruru, s)
def test_login_4(monkeypatch, capsys):
    inputs = iter(["ruru", "s"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = None
        login()
        captured = capsys.readouterr()
        assert captured.out == "\nWrong username/password, please try again.\n\n"

# len(username) = 0
def test_login_5(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: "") 
    login()
    captured = capsys.readouterr() 
    assert captured.out == "\nInvalid username, please try again.\n"

'''
    cursor = MagicMock(sqlite3.Cursor)
    cursor.fetchall.return_value = ['test2', 'test2']
'''

# len(username) = 15
def test_login_6(monkeypatch, capsys):
    inputs = iter(["qwertyuiopasdfg", "h"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.client', lambda _: print("client(username)"))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["r", "r"]
        login()
        captured = capsys.readouterr()
        assert captured.out == "client(username)\n"

# len(username) = 16
def test_login_7(monkeypatch, capsys):
    inputs = iter(["qwertyuiopasdfgh", "h"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.client', lambda _: print("client(username)"))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["r", "r"]
        login()
        captured = capsys.readouterr()
        assert captured.out == "client(username)\n"

# len(username) = 17
# len(password) = 0
def test_login_8(monkeypatch, capsys):
    inputs = iter(["qwertyuiopasdfghj", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    login()
    captured = capsys.readouterr()
    assert captured.out == "\nUsername too long, please try again.\n"

# len(password) = 0
def test_login_9(monkeypatch, capsys):
    inputs = iter(["k", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = None
        login()
        captured = capsys.readouterr()
        assert captured.out == "\nInvalid password, please try again.\n"



"""
TODO: Test Suite 4, see PROJ
"""


#----------------------------------------------------------------
#
#  Test Suite 4: FR-4: Customer Dashboard
#
#----------------------------------------------------------------

# expired_loan = 1
def test_client_1(monkeypatch, capsys):
    inputs = iter(["1", "6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 1)
    monkeypatch.setattr('main_test.deposit', lambda _: print("deposit(username)"))

    sql_results = [[10],[100000],[10],[100000]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        client("test")
        captured = capsys.readouterr()
        assert ("Account is locked now, please pay off the loan first." in captured.out and "deposit(username)" in captured.out)

# expired_loan = 0
def test_client_2(monkeypatch, capsys):
    inputs = iter(["2", "6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 0)
    monkeypatch.setattr('main_test.withdraw', lambda *_: print("withdraw(username, balance)"))

    sql_results = [[10],[100000],[10],[100000]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        client("test")
        captured = capsys.readouterr()
        assert ("Account is locked now, please pay off the loan first." not in captured.out and "withdraw(username, balance)" in captured.out)

# expired_loan = 0
def test_client_3(monkeypatch, capsys):
    inputs = iter(["3", "6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 0)
    monkeypatch.setattr('main_test.createLoan', lambda *_: print("createLoan(username, timestamp)"))

    sql_results = [[10],[100000],[10],[100000]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        client("test")
        captured = capsys.readouterr()
        assert ("Account is locked now, please pay off the loan first." not in captured.out and "createLoan(username, timestamp)" in captured.out)

# expired_loan = 0
def test_client_4(monkeypatch, capsys):
    inputs = iter(["4", "6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 0)
    monkeypatch.setattr('main_test.payLoan', lambda *_: print("payLoan(username, balance)"))

    sql_results = [[10],[100000],[10],[100000]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        client("test")
        captured = capsys.readouterr()
        assert ("Account is locked now, please pay off the loan first." not in captured.out and "payLoan(username, balance)" in captured.out)

# expired_loan = 0
def test_client_5(monkeypatch, capsys):
    inputs = iter(["5", "6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 0)
    monkeypatch.setattr('main_test.pass1Month', lambda *_: print("pass1Month()"))

    sql_results = [[10],[100000],[10],[100000]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        client("test")
        captured = capsys.readouterr()
        assert ("Account is locked now, please pay off the loan first." not in captured.out and "pass1Month()" in captured.out)

# expired_loan = 0
def test_client_6(monkeypatch, capsys):
    inputs = iter(["6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 0)

    sql_results = [[10],[100000],[10],[100000]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        a = client("test")
        captured = capsys.readouterr()
        assert a == None

# expired_loan = 0
def test_client_7(monkeypatch, capsys):
    inputs = iter(["greedisgood", "6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 0)

    sql_results = [[10],[100000],[10],[100000], []]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            a = client("test")
            captured = capsys.readouterr()
            assert ("Account is locked now, please pay off the loan first." not in captured.out and a == None)

# expired_loan = 0
def test_client_8(monkeypatch, capsys):
    inputs = iter(["7", "6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 0)

    sql_results = [[10],[100000],[10],[100000]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        client("test")
        captured = capsys.readouterr()
        assert "Invalid option, please try again." in captured.out


#----------------------------------------------------------------
#
#  Test Suite 5: FR-5: Make Deposit
#
#----------------------------------------------------------------

# deposit = 0
def test_deposit_1(monkeypatch, capsys):
    inputs = iter(["0"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    deposit("test")
    captured = capsys.readouterr()
    assert ("Deposit failed: invalid input, please try again." in captured.out)

# 0 < deposit <= 1000000
# deposit = 0.01
def test_deposit_2(monkeypatch, capsys):
    inputs = iter(["0.01"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1],[1]]
    with patch('main_test.c') as mocksql:
        mocksql.execute.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            deposit("r")
            captured = capsys.readouterr()
            assert ("Your deposit has been successfully processed!" in captured.out)

# 0 < deposit <= 1000000
# deposit = 9999.99
def test_deposit_3(monkeypatch, capsys):
    inputs = iter(["9999.99"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1],[1]]
    with patch('main_test.c') as mocksql:
        mocksql.execute.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            deposit("r")
            captured = capsys.readouterr()
            assert ("Your deposit has been successfully processed!" in captured.out)

# 0 < deposit <= 1000000
# deposit = 9999.99
def test_deposit_4(monkeypatch, capsys):
    inputs = iter(["10000"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1],[1]]
    with patch('main_test.c') as mocksql:
        mocksql.execute.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            deposit("r")
            captured = capsys.readouterr()
            assert ("Your deposit has been successfully processed!" in captured.out)

# deposit = 1000001
def test_deposit_5(monkeypatch, capsys):
    inputs = iter(["10000.01"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    deposit("r")
    captured = capsys.readouterr()
    assert ("Deposit failed: invalid input, please try again." in captured.out)

# deposit = #
def test_deposit_6(monkeypatch, capsys):
    inputs = iter(["#"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    deposit("r")
    captured = capsys.readouterr()
    assert ("Deposit failed: invalid input, please try again." in captured.out)

# deposit = None
def test_deposit_7(monkeypatch, capsys):
    inputs = iter([""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    deposit("r")
    captured = capsys.readouterr()
    assert ("Deposit failed: invalid input, please try again." in captured.out)


#----------------------------------------------------------------
#
#  Test Suite 6: FR-6: Make Withdrawal
#
#----------------------------------------------------------------

# username: qwertyuiopasdfg
# total assets = 5000
def test_withdraw_deposit_5000(monkeypatch, capsys):
    inputs = iter(["5000"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1],[1]]
    with patch('main_test.c') as mocksql:
        mocksql.execute.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            deposit("qwertyuiopasdfg")
            captured = capsys.readouterr()
            assert ("Your deposit has been successfully processed!" in captured.out)

# withdraw = 0
def test_withdraw_1(monkeypatch, capsys):
    inputs = iter(["0"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    withdraw("qwertyuiopasdfg", 0)
    captured = capsys.readouterr()
    assert ("Withdraw failed: invalid input, please try again." in captured.out)

# 0.01 <= withdraw <= 2000
# withdraw = 0.01, balance = 5000
def test_withdraw_2(monkeypatch, capsys):
    inputs = iter(["0.01"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1],[1]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            balance = 500000
            withdraw("qwertyuiopasdfg", balance)
            captured = capsys.readouterr()
            assert ("Your withdrawl has been successfully processed!" in captured.out)

# 0.01 <= withdraw <= 2000
# withdraw = 1999.99, balance = 4999.99
def test_withdraw_3(monkeypatch, capsys):
    inputs = iter(["1999.99"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1],[1]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            balance = 499999
            withdraw("qwertyuiopasdfg", balance)
            captured = capsys.readouterr()
            assert ("Your withdrawl has been successfully processed!" in captured.out)

# 0.01 <= withdraw <= 2000
# withdraw = 2000, balance = 3000
def test_withdraw_4(monkeypatch, capsys):
    inputs = iter(["2000"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1],[1]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            balance = 300000
            withdraw("qwertyuiopasdfg", balance)
            captured = capsys.readouterr()
            assert ("Your withdrawl has been successfully processed!" in captured.out)

# 0.01 <= withdraw <= 2000
# withdraw = 2000.01, balance = 1000
def test_withdraw_5(monkeypatch, capsys):
    inputs = iter(["2000.01"])
    balance = 1000000
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    withdraw("test", balance)
    captured = capsys.readouterr()
    assert ("Withdraw failed: invalid input, please try again." in captured.out)

# withdraw = #, balance = 1000
def test_withdraw_1(monkeypatch, capsys):
    inputs = iter(["#"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    withdraw("qwertyuiopasdfg", 10000)
    captured = capsys.readouterr()
    assert ("Withdraw failed: invalid input, please try again." in captured.out)


# withdraw = NULL, balance = 1000
def test_withdraw_1(monkeypatch, capsys):
    inputs = iter([""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    withdraw("qwertyuiopasdfg", 10000)
    captured = capsys.readouterr()
    assert ("Withdraw failed: invalid input, please try again." in captured.out)


# Initialize A Loan

# len(exist_loans) = 0
# timestamp = 10
# min_due = 11
# loan = None
def test_createLoan_1(monkeypatch, capsys):
    inputs = iter([""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1000],[]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = sql_results[0]
        mocksql.execute().fetchall.return_value = sql_results[1]
        timestamp = 10
        createLoan("test", timestamp)
        captured = capsys.readouterr()
        assert ("Loan initialization failed: invalid input, please try again." in captured.out)

# len(exist_loans) = 0
# timestamp = 10
# min_due = 11
# loan = 0
def test_createLoan_2(monkeypatch, capsys):
    inputs = iter(["0"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1000],[]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = sql_results[0]
        mocksql.execute().fetchall.return_value = sql_results[1]
        timestamp = 10
        createLoan("test", timestamp)
        captured = capsys.readouterr()
        assert ("Loan initialization failed: invalid input, please try again." in captured.out)

# len(exist_loans) = 0
# timestamp = 10
# min_due = 11
# loan = 1000001
def test_createLoan_3(monkeypatch, capsys):
    inputs = iter(["10000.01"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1000],[]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = sql_results[0]
        mocksql.execute().fetchall.return_value = sql_results[1]
        timestamp = 10
        createLoan("test", timestamp)
        captured = capsys.readouterr()
        assert ("Loan initialization failed: invalid input, please try again." in captured.out)

# len(exist_loans) = 0
# timestamp = 10
# min_due = 11
# 0 < loan <= 1000000
# loan = 50000

def test_createLoan_4(monkeypatch, capsys):
    inputs = iter(["500"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = [1000]
        mocksql.execute().fetchall.return_value = []
        #mocksql.execute.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            timestamp = 10
            createLoan("test", timestamp)
            captured = capsys.readouterr()
            assert ("Your loan has been successfully initialized!" in captured.out)

# len(exist_loans) = 3
# timestamp = 49
# min_due = 50

def test_createLoan_5(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = [1000]
        mocksql.execute().fetchall.return_value = [[50], [60], [70]]
        #mocksql.execute.side_effect = sql_results
        timestamp = 49
        createLoan("test", timestamp)
        captured = capsys.readouterr()
        assert ("You have already reached limitation of total loan amount (3)." in captured.out)

# len(exist_loans) = 1
# timestamp = 50
# min_due = 50

def test_createLoan_6(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = [1000]
        mocksql.execute().fetchall.return_value = [[50]]
        #mocksql.execute.side_effect = sql_results
        timestamp = 50
        createLoan("test", timestamp)
        captured = capsys.readouterr()
        assert ("You have loan(s) overdue." in captured.out)

# Make Time Go Forward

# len(expired_loans) = 1
# balance = 0
def test_pass1Month_1(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [[1, "test", "50000"]]
        mocksql.execute().fetchone.return_value = [0]
        #mocksql.execute.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            pass1Month()

# len(expired_loans) = 1
# balance = 50000
# remaining = 50000
def test_pass1Month_2(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [[1, "test", "50000"]]
        mocksql.execute().fetchone.return_value = ["50000"]
        #mocksql.execute.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            pass1Month()

# len(expired_loans) = 1
# balance = 49999
# remaining = 50000
def test_pass1Month_3(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [[1, "test", "50000"]]
        mocksql.execute().fetchone.return_value = ["49999"]
        #mocksql.execute.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            pass1Month()
            #captured = capsys.readouterr()

# Check Loans

# len(expired_loans) = 1
# balance = 0
def test_checkLoans_1(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [[1, "50000"]]
        mocksql.execute().fetchone.return_value = ["0"]
        #mocksql.execute.side_effect = sql_results
        a = checkLoans("test")
        assert a == 50000

# len(expired_loans) = 1
# balance = 50000
# remaining = 50000
def test_checkLoans_2(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [[1, "50000"]]
        mocksql.execute().fetchone.return_value = ["50000"]
        #mocksql.execute.side_effect = sql_results
        a = checkLoans("test")
        assert a == 0

# len(expired_loans) = 1
# balance = 49999
# remaining = 50000 
def test_checkLoans_3(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [[1, "50000"]]
        mocksql.execute().fetchone.return_value = ["49999"]
        #mocksql.execute.side_effect = sql_results
        a = checkLoans("test")
        assert a == 1

# Admin Dashboard

def test_admin_1(monkeypatch, capsys):
    inputs = iter(["2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    #monkeypatch.setattr('main_test.sqlite3', lambda _: print("client(username)"))
    #mock_cursor = mock_connect.return_value.cursor.return_value
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["1000000000", "1000", "500", "40"]
        a = admin()
        captured = capsys.readouterr()
        assert captured.out and a == None

def test_admin_2(monkeypatch, capsys):
    inputs = iter(["1", "2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.changeRates', lambda: print("changeRates()"))
    #mock_cursor = mock_connect.return_value.cursor.return_value
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["1000000000", "1000", "500", "40"]
        admin()
        captured = capsys.readouterr()
        assert "changeRates()" in captured.out

def test_admin_3(monkeypatch, capsys):
    inputs = iter(["3", "2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    #monkeypatch.setattr('main_test.sqlite3', lambda _: print("client(username)"))
    #mock_cursor = mock_connect.return_value.cursor.return_value
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["1000000000", "1000", "500", "40"]
        a = admin()
        captured = capsys.readouterr()
        assert captured.out and a == None

# Change Interest Rates 

# target_loanrate = 1001
# loanrate = 1000
# target_depositrate = 501
# depositrate = 500
# new_loanrate = None
# new_depositrate = None
def test_changeRates_1(monkeypatch, capsys):
    inputs = iter(["", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    #monkeypatch.setattr('main_test.sqlite3', lambda _: print("client(username)"))
    #mock_cursor = mock_connect.return_value.cursor.return_value
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["999900000", "1000", "500"]
        changeRates()
        captured = capsys.readouterr()
        assert "Loan rate change failed: Invalid input." in captured.out and "Deposit rate change failed: Invalid input." in captured.out

# target_loanrate = 1001
# loanrate = 1000
# target_depositrate = 501
# depositrate = 500
# new_loanrate = 999
# min_loanrate = 1000
# new_depositrate = 499
# min_depositrate = 500
def test_changeRates_2(monkeypatch, capsys):
    inputs = iter(["9.99", "4.99"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    #monkeypatch.setattr('main_test.sqlite3', lambda _: print("client(username)"))
    #mock_cursor = mock_connect.return_value.cursor.return_value
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["999900000", "1000", "500"]
        changeRates()
        captured = capsys.readouterr()
        assert "Loan rate change failed: Invalid input." in captured.out and "Deposit rate change failed: Invalid input." in captured.out

# target_loanrate = 1001
# loanrate = 1000
# target_depositrate = 501
# depositrate = 500
# new_loanrate = 1002
# max_loanrate = 1001
# new_depositrate = 502
# max_depositrate = 501
def test_changeRates_3(monkeypatch, capsys):
    inputs = iter(["10.02", "5.02"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    #monkeypatch.setattr('main_test.sqlite3', lambda _: print("client(username)"))
    #mock_cursor = mock_connect.return_value.cursor.return_value
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["999900000", "1000", "500"]
        changeRates()
        captured = capsys.readouterr()
        assert "Loan rate change failed: Invalid input." in captured.out and "Deposit rate change failed: Invalid input." in captured.out

# target_loanrate = 999
# loanrate = 1000
# target_depositrate = 499
# depositrate = 500
# new_loanrate = 999
# min_loanrate = 999
# max_loanrate = 1000
# new_depositrate = 499
# min_depositrate = 499
# max_depositrate = 500
def test_changeRates_4(monkeypatch, capsys):
    inputs = iter(["9.99", "4.99"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    #monkeypatch.setattr('main_test.sqlite3', lambda _: print("client(username)"))
    #mock_cursor = mock_connect.return_value.cursor.return_value
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchone.return_value = ["1000100000", "1000", "500"]
            changeRates()
            captured = capsys.readouterr()
            assert "Loan rate has been successfully changed!" in captured.out and "Deposit rate has been successfully changed!" in captured.out




# Make A Loan Repayment

# cnt = 0
def test_payLoan_1(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = []
        payLoan("test", 100000)
        captured = capsys.readouterr()
        assert "You don't have any loan." in captured.out

# cnt = 1
# balance = 0
def test_payLoan_2(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["test", 10000, 11000, 63, 75]]
        payLoan("test", 0)
        captured = capsys.readouterr()
        assert "Your balance is 0, please make a deposit first!" in captured.out

# cnt = 1
# balance = 11000
# payment = None
def test_payLoan_3(monkeypatch, capsys):
    inputs = iter(["1", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["test", 10000, 11000, 63, 75]]
        payLoan("test", 11000)
        captured = capsys.readouterr()
        assert "Repayment failed: invalid input, please try again." in captured.out

# cnt = 1
# balance = 11000
# payment = 0
def test_payLoan_4(monkeypatch, capsys):
    inputs = iter(["1", "0"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["test", 10000, 11000, 63, 75]]
        payLoan("test", 11000)
        captured = capsys.readouterr()
        assert "Repayment failed: invalid input, please try again." in captured.out

# cnt = 1
# balance = 11000
# max_payment = 11000
# payment = 11001
def test_payLoan_5(monkeypatch, capsys):
    inputs = iter(["1", "110.01"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["test", 10000, 11000, 63, 75]]
        payLoan("test", 11000)
        captured = capsys.readouterr()
        assert "Repayment failed: invalid input, please try again." in captured.out

# cnt = 1
# balance = 11000
# max_payment = 11000
# payment = 10999
# remaining = 11000
def test_payLoan_6(monkeypatch, capsys):
    inputs = iter(["1", "109.99"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchall.return_value = [["1", 10000, 11000, 63, 75]]
            payLoan("test", 11000)
            captured = capsys.readouterr()
            assert "Your repayment has been successfully processed!" in captured.out

# cnt = 1
# balance = 11000
# max_payment = 11000
# payment = 11000
# remaining = 11000
def test_payLoan_7(monkeypatch, capsys):
    inputs = iter(["1", "110"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchall.return_value = [["1", 10000, 11000, 63, 75]]
            payLoan("test", 11000)
            captured = capsys.readouterr()
            assert "Your repayment has been successfully processed!" in captured.out

# cnt = 2
# balance = 11000
# max_payment = 11000
# payment = 11000
# remaining = 11000
def test_payLoan_8(monkeypatch, capsys):
    inputs = iter(["2", "110"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchall.return_value = [["1", 10000, 11000, 63, 75], ["2", 10000, 11000, 63, 75]]
            payLoan("test", 11000)
            captured = capsys.readouterr()
            assert "Your repayment has been successfully processed!" in captured.out

# cnt = 3
# balance = 11000
# max_payment = 11000
# payment = 11000
# remaining = 11000
def test_payLoan_9(monkeypatch, capsys):
    inputs = iter(["3", "110"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchall.return_value = [["1", 10000, 11000, 63, 75], ["2", 10000, 11000, 63, 75], ["3", 10000, 11000, 63, 75]]
            payLoan("test", 11000)
            captured = capsys.readouterr()
            assert "Your repayment has been successfully processed!" in captured.out


def test_payLoan_10(monkeypatch, capsys):
    inputs = iter(["4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["1", 10000, 11000, 63, 75]]
        payLoan("test", 11000)
        captured = capsys.readouterr()
        assert "Invalid option, please try again." in captured.out

# cnt = 1
def test_payLoan_11(monkeypatch, capsys):
    inputs = iter(["2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["1", 10000, 11000, 63, 75]]
        payLoan("test", 11000)
        captured = capsys.readouterr()
        assert "Invalid option, please try again." in captured.out

# cnt = 2
def test_payLoan_12(monkeypatch, capsys):
    inputs = iter(["3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["1", 10000, 11000, 63, 75], ["2", 10000, 11000, 63, 75]]
        payLoan("test", 11000)
        captured = capsys.readouterr()
        assert "Invalid option, please try again." in captured.out




# just for increasing code coverage, not necessarily a test case
# line 14-56
def test_initDB():
    with patch('main_test.os.path') as mockos:
        mockos.exists.return_value = None
        with patch('main_test.c') as mocksql:
            mocksql.execute.return_value = []
            with patch('main_test.conn') as mockcommit:
                mockcommit.commit.return_value = []
                a = initDB()
                assert a == None
                
def test_decStr2Int():
    a = decStr2Int("100.111")
    assert a == None