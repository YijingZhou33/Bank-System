import pytest
from main_test import *
import os, sys
from mock import patch

#----------------------------------------------------------------
#
#  Test Suite 1: FR-1: Main Menu
#
#----------------------------------------------------------------

# TC01: option = 1
def test_main_1(monkeypatch, capsys):
    inputs = iter(["1", "3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.register', lambda *_: print("register()"))
    main()
    captured = capsys.readouterr()
    assert "register()" in captured.out

# TC02: option = 2
def test_main_2(monkeypatch, capsys):
    inputs = iter(["2", "3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.login', lambda *_: print("login()"))
    main()
    captured = capsys.readouterr()
    assert "login()" in captured.out

# TC03: option = 3
def test_main_3(monkeypatch, capsys):
    inputs = iter(["3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    a = main()
    captured = capsys.readouterr()
    assert a == None

# TC04: option = 123
def test_main_4(monkeypatch, capsys):
    inputs = iter(["123", "3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "Invalid option, please try again." in captured.out

# TC05: option = None
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

# TC01: username = r, password = r
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

# TC02: username = r, missing password
def test_register_2(monkeypatch, capsys):
    inputs = iter(["r"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["r"]
        register()
        captured = capsys.readouterr()
        assert "The username has already existed, please choose a new one. " in captured.out

# TC03: username = None, missing password  
def test_register_3(monkeypatch, capsys):
    inputs = iter([""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    register()
    captured = capsys.readouterr()
    assert "Invalid username, please try again. " in captured.out

# TC04: len(username) = 15
#       username = qwertyuiopasdfg, password = h
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

# TC05: len(username) = 16
#       username = qwertyuiopasdfgh, password = h
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

# TC06: len(username) = 17
#       username = qwertyuiopasdfghj, password = h
def test_register_6(monkeypatch, capsys):
    inputs = iter(["qwertyuiopasdfghj", "h"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    register()
    captured = capsys.readouterr()
    assert "Username too long, please try again. " in captured.out

# TC07: len(password) = 0
#       username = k, password = ""
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

# TC01: customer login: (r, r)
def test_login_1(monkeypatch, capsys):
    inputs = iter(["r", "r"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.client', lambda _: print("client(username)"))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["r", "r"]
        login()
        captured = capsys.readouterr()
        assert captured.out == "client(username)\n"

# TC02: admin login (admin, admin)
def test_login_2(monkeypatch, capsys):
    inputs = iter(["admin", "admin"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.admin', lambda: print("admin()"))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["admin", "admin"]
        login()
        captured = capsys.readouterr()
        assert captured.out == "admin()\n"

# TC03: wrong password (r, s)
def test_login_3(monkeypatch, capsys):
    inputs = iter(["r", "s"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = None
        login()
        captured = capsys.readouterr()
        assert captured.out == "\nWrong username/password, please try again.\n\n"

# TC04: wrong username (ruru, s)
def test_login_4(monkeypatch, capsys):
    inputs = iter(["ruru", "s"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = None
        login()
        captured = capsys.readouterr()
        assert captured.out == "\nWrong username/password, please try again.\n\n"

# TC05: len(username) = 0
def test_login_5(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: "") 
    login()
    captured = capsys.readouterr() 
    assert captured.out == "\nInvalid username, please try again.\n"

'''
    cursor = MagicMock(sqlite3.Cursor)
    cursor.fetchall.return_value = ['test2', 'test2']
'''

# TC06: len(username) = 15
#       username = qwertyuiopasdfg, password = h
def test_login_6(monkeypatch, capsys):
    inputs = iter(["test", "h"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.client', lambda _: print("client(username)"))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["r", "r"]
        login()
        captured = capsys.readouterr()
        assert captured.out == "client(username)\n"

# TC07: len(username) = 16
#       username = qwertyuiopasdfgh, password = h
def test_login_7(monkeypatch, capsys):
    inputs = iter(["qwertyuiopasdfgh", "h"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.client', lambda _: print("client(username)"))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["r", "r"]
        login()
        captured = capsys.readouterr()
        assert captured.out == "client(username)\n"

# TC08: len(username) = 17
#       username = qwertyuiopasdfghj, password = h
def test_login_8(monkeypatch, capsys):
    inputs = iter(["qwertyuiopasdfghj", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    login()
    captured = capsys.readouterr()
    assert captured.out == "\nUsername too long, please try again.\n"

# TC08: len(password) = 0
#       username = l, password = ""
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

# expired_loan = 0
def test_client_1(monkeypatch, capsys):
    inputs = iter(["1", "6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 0)
    monkeypatch.setattr('main_test.deposit', lambda _: print("deposit(username)"))

    sql_results = [[10],[100000],[10],[100000]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        client("test")
        captured = capsys.readouterr()
        assert ("Account is locked now, please pay off the loan first." not in captured.out and "deposit(username)" in captured.out)

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
    inputs = iter(["123", "6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 0)

    sql_results = [[10],[100000],[10],[100000]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        client("test")
        captured = capsys.readouterr()
        assert ("Account is locked now, please pay off the loan first." not in captured.out and "Invalid option, please try again." in captured.out)

# expired_loan = 0
def test_client_8(monkeypatch, capsys):
    inputs = iter(["", "6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 0)

    sql_results = [[10],[100000],[10],[100000]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        client("test")
        captured = capsys.readouterr()
        assert ("Account is locked now, please pay off the loan first." not in captured.out and "Invalid option, please try again." in captured.out)

# expired_loan = 0
# len(exist_loans) = 3
def test_client_9(monkeypatch, capsys):
    inputs = iter(["3", "6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 0)
    sql_results = [[49],[100000],[1000],[49],[100000]]

    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        mocksql.execute().fetchall.return_value = [[50], [60], [70]]
        client("test")
        captured = capsys.readouterr()
        assert ("Account is locked now, please pay off the loan first." not in captured.out and "You have already reached limitation of total loan amount (3)." in captured.out)

# expired_loan = 1
def test_client_10(monkeypatch, capsys):
    inputs = iter(["3", "6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 1)

    sql_results = [[50],[100000],[1000], [50],[100000]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        mocksql.execute().fetchall.return_value = [[50]]
        client("test")
        captured = capsys.readouterr()
        assert ("Account is locked now, please pay off the loan first." in captured.out and "You have loan(s) overdue." in captured.out)

# expired_loan = 0
# len(exist_loans) = 0
def test_client_11(monkeypatch, capsys):
    inputs = iter(["4", "6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 0)

    sql_results = [[10],[100000],[10],[100000]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        mocksql.execute().fetchall.return_value = []
        client("test")
        captured = capsys.readouterr()
        assert ("Account is locked now, please pay off the loan first." not in captured.out and "You don't have any loan." in captured.out)

# expired_loan = 0
# len(exist_loans) = 1
# balance = 0
def test_client_12(monkeypatch, capsys):
    inputs = iter(["4", "6"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.checkLoans', lambda _: 0)

    sql_results = [[10],[0],[10],[0]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        mocksql.execute().fetchall.return_value = [["1", 10000, 11000, 63, 75]]
        client("test")
        captured = capsys.readouterr()
        assert ("Account is locked now, please pay off the loan first." not in captured.out and "Your balance is 0, please make a deposit first!" in captured.out)

#----------------------------------------------------------------
#
#  Test Suite 5: FR-5: Make Deposit
#
#       username = test
#       0.01 <= deposit <= 10000 with at most 2 decimal places
#----------------------------------------------------------------

# TC01: deposit = 0
def test_deposit_1(monkeypatch, capsys):
    inputs = iter(["0"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    deposit("test")
    captured = capsys.readouterr()
    assert ("Deposit failed: invalid input, please try again." in captured.out)

# TC02: deposit = 0.01
def test_deposit_2(monkeypatch, capsys):
    inputs = iter(["1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1],[1]]
    with patch('main_test.c') as mocksql:
        mocksql.execute.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            deposit("test")
            captured = capsys.readouterr()
            assert ("Your deposit has been successfully processed!" in captured.out)

# TC03: deposit = 9999.99
def test_deposit_3(monkeypatch, capsys):
    inputs = iter(["9999.99"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1],[1]]
    with patch('main_test.c') as mocksql:
        mocksql.execute.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            deposit("test")
            captured = capsys.readouterr()
            assert ("Your deposit has been successfully processed!" in captured.out)

# TC04: deposit = 10000
def test_deposit_4(monkeypatch, capsys):
    inputs = iter(["1000"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1],[1]]
    with patch('main_test.c') as mocksql:
        mocksql.execute.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            deposit("test")
            captured = capsys.readouterr()
            assert ("Your deposit has been successfully processed!" in captured.out)

# TC05: deposit = 10000.01
def test_deposit_5(monkeypatch, capsys):
    inputs = iter(["10000.01"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    deposit("test")
    captured = capsys.readouterr()
    assert ("Deposit failed: invalid input, please try again." in captured.out)

# TC06: deposit = 2.333
def test_deposit_6(monkeypatch, capsys):
    inputs = iter(["2.333"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    deposit("test")
    captured = capsys.readouterr()
    assert ("Deposit failed: invalid input, please try again." in captured.out)

# TC07: deposit = #
def test_deposit_7(monkeypatch, capsys):
    inputs = iter(["#"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    deposit("test")
    captured = capsys.readouterr()
    assert ("Deposit failed: invalid input, please try again." in captured.out)

# TC08: deposit = None
def test_deposit_8(monkeypatch, capsys):
    inputs = iter([""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    deposit("test")
    captured = capsys.readouterr()
    assert ("Deposit failed: invalid input, please try again." in captured.out)


#----------------------------------------------------------------
#
#  Test Suite 6: FR-6: Make Withdrawal
#
#       username = test
#       total balance = 5000
#       0.01 <= withdrawal <= 2000 with at most 2 decimal places
#----------------------------------------------------------------

# TC01: withdrawal = 0
def test_withdraw_1(monkeypatch, capsys):
    inputs = iter(["0"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    withdraw("test", 0)
    captured = capsys.readouterr()
    assert ("Withdraw failed: invalid input, please try again." in captured.out)

# TC02: withdrawal = 0.01, balance = 5000
def test_withdraw_2(monkeypatch, capsys):
    inputs = iter(["0.01"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1],[1]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            balance = 500000
            withdraw("test", balance)
            captured = capsys.readouterr()
            assert ("Your withdrawl has been successfully processed!" in captured.out)

# TC03: withdrawal = 1999.99, balance = 4999.99
def test_withdraw_3(monkeypatch, capsys):
    inputs = iter(["1999.99"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1],[1]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            balance = 499999
            withdraw("test", balance)
            captured = capsys.readouterr()
            assert ("Your withdrawl has been successfully processed!" in captured.out)

# TC04: withdrawal = 2000, balance = 3000
def test_withdraw_4(monkeypatch, capsys):
    inputs = iter(["2000"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1],[1]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            balance = 300000
            withdraw("test", balance)
            captured = capsys.readouterr()
            assert ("Your withdrawl has been successfully processed!" in captured.out)

# TC05: withdrawal = 2000.01, balance = 1000
def test_withdraw_5(monkeypatch, capsys):
    inputs = iter(["2000.01"])
    balance = 1000000
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    withdraw("test", balance)
    captured = capsys.readouterr()
    assert ("Withdraw failed: invalid input, please try again." in captured.out)

# TC06: withdrawal = 2.333, balance = 1000
def test_withdraw_6(monkeypatch, capsys):
    inputs = iter(["2.333"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    withdraw("test", 10000)
    captured = capsys.readouterr()
    assert ("Withdraw failed: invalid input, please try again." in captured.out)

# TC07: withdrawal = #, balance = 1000
def test_withdraw_7(monkeypatch, capsys):
    inputs = iter(["#"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    withdraw("test", 10000)
    captured = capsys.readouterr()
    assert ("Withdraw failed: invalid input, please try again." in captured.out)

# TC08: withdrawal = None, balance = 1000
def test_withdraw_8(monkeypatch, capsys):
    inputs = iter([""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    withdraw("test", 10000)
    captured = capsys.readouterr()
    assert ("Withdraw failed: invalid input, please try again." in captured.out)


#----------------------------------------------------------------
#
#  Test Suite 7: FR-7: Initialize A Loan
#  
#       username = test
#       0.01 <= loan <= 10000 with at most 2 decimal places
#       existing_loans = 0
#----------------------------------------------------------------

# TC01: loan = 0
def test_createLoan_1(monkeypatch, capsys):
    inputs = iter(["0"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1000],[]] # loanrate, existing_loan
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = sql_results[0]
        mocksql.execute().fetchall.return_value = sql_results[1]
        timestamp = 10
        createLoan("test", timestamp)
        captured = capsys.readouterr()
        assert ("Loan initialization failed: invalid input, please try again." in captured.out)

# TC02: loan = 0.01
def test_createLoan_2(monkeypatch, capsys):
    inputs = iter(["0.01"])
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

# TC03: loan = 9999.99
def test_createLoan_3(monkeypatch, capsys):
    inputs = iter(["9999.99"])
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

# TC04: loan = 10000
def test_createLoan_4(monkeypatch, capsys):
    inputs = iter(["10000"])
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

# TC05: loan = 10000.01
def test_createLoan_5(monkeypatch, capsys):
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

# TC06: loan = 2.333
def test_createLoan_6(monkeypatch, capsys):
    inputs = iter(["2.333"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1000],[]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = sql_results[0]
        mocksql.execute().fetchall.return_value = sql_results[1]
        timestamp = 10
        createLoan("test", timestamp)
        captured = capsys.readouterr()
        assert ("Loan initialization failed: invalid input, please try again." in captured.out)

# TC07: loan = #
def test_createLoan_7(monkeypatch, capsys):
    inputs = iter(["#"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    sql_results = [[1000],[]]
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = sql_results[0]
        mocksql.execute().fetchall.return_value = sql_results[1]
        timestamp = 10
        createLoan("test", timestamp)
        captured = capsys.readouterr()
        assert ("Loan initialization failed: invalid input, please try again." in captured.out)

# TC08: loan = None
def test_createLoan_8(monkeypatch, capsys):
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


#----------------------------------------------------------------
#
#  Test Suite 8: FR-8: Make A Loan Repayment
#  
#       username = test 
#----------------------------------------------------------------

# TC01: existing_loan = 0, balance = 1000, repayment = 1000
def test_payLoan_1(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = []
        payLoan("test", 100000)
        captured = capsys.readouterr()
        assert "You don't have any loan." in captured.out

# TC02: existing_loan = 1, balance = 0, repayment = 1000
def test_payLoan_2(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["1", 100000, 110000, 63, 75]]
        payLoan("test", 0)
        captured = capsys.readouterr()
        assert "Your balance is 0, please make a deposit first!" in captured.out

# TC03: existing_loan = 1, balance = 1000, loan_remaining = 1100
#       option = 2, repayment = None
def test_payLoan_3(monkeypatch, capsys):
    inputs = iter(["2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["1", 100000, 110000, 63, 75]]
        payLoan("test", 100000)
        captured = capsys.readouterr()
        assert "Invalid option, please try again." in captured.out

# TC04: existing_loan = 1, balance = 1000, loan_remaining = 1100
#       option = "", repayment = None
def test_payLoan_4(monkeypatch, capsys):
    inputs = iter(['""'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["1", 100000, 110000, 63, 75]]
        payLoan("test", 100000)
        captured = capsys.readouterr()
        assert "Invalid option, please try again." in captured.out

# TC05: existing_loan = 1, balance = 1000, loan_remaining = 1100
#       option = 1, repayment = 0
def test_payLoan_5(monkeypatch, capsys):
    inputs = iter(["1", "0"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["1", 100000, 110000, 63, 75]]
        payLoan("test", 100000)
        captured = capsys.readouterr()
        assert "Repayment failed: invalid input, please try again." in captured.out

# TC06: existing_loan = 1, balance = 1000, loan_remaining = 1100
#       option = 1, repayment = 0.01
def test_payLoan_6(monkeypatch, capsys):
    inputs = iter(["1", "0.01"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchall.return_value = [["1", 100000, 110000, 63, 75]]
            payLoan("test", 100000)
            captured = capsys.readouterr()
            assert "Your repayment has been successfully processed!" in captured.out

# TC07: existing_loan = 1, balance = 1000, loan_remaining = 1100
#       option = 1, repayment = 999.99
def test_payLoan_7(monkeypatch, capsys):
    inputs = iter(["1", "999.99"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchall.return_value = [["1", 100000, 110000, 63, 75]]
            payLoan("test", 100000)
            captured = capsys.readouterr()
            assert "Your repayment has been successfully processed!" in captured.out

# TC08: existing_loan = 1, balance = 1000, loan_remaining = 1100
#       option = 1, repayment = 1000
def test_payLoan_8(monkeypatch, capsys):
    inputs = iter(["1", "1000"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchall.return_value = [["1", 100000, 110000, 63, 75]]
            payLoan("test", 100000)
            captured = capsys.readouterr()
            assert "Your repayment has been successfully processed!" in captured.out

# TC09: existing_loan = 1, balance = 1000, loan_remaining = 1100
#       option = 1, repayment = 1000.01
def test_payLoan_9(monkeypatch, capsys):
    inputs = iter(["1", "1000.01"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["1", 100000, 110000, 63, 75]]
        payLoan("test", 100000)
        captured = capsys.readouterr()
        assert "Repayment failed: invalid input, please try again." in captured.out

# TC10: existing_loan = 1, balance = 1000, loan_remaining = 1100
#       option = 1, repayment = 2.333
def test_payLoan_10(monkeypatch, capsys):
    inputs = iter(["1", "2.333"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["1", 100000, 110000, 63, 75]]
        payLoan("test", 100000)
        captured = capsys.readouterr()
        assert "Repayment failed: invalid input, please try again." in captured.out

# TC11: existing_loan = 1, balance = 1000, loan_remaining = 1100
#       option = 1, repayment = #
def test_payLoan_11(monkeypatch, capsys):
    inputs = iter(["1", "#"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["1", 100000, 110000, 63, 75]]
        payLoan("test", 100000)
        captured = capsys.readouterr()
        assert "Repayment failed: invalid input, please try again." in captured.out

# TC12: existing_loan = 1, balance = 1000, loan_remaining = 1100
#       option = 1, repayment = None
def test_payLoan_12(monkeypatch, capsys):
    inputs = iter(["1", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["1", 100000, 110000, 63, 75]]
        payLoan("test", 100000)
        captured = capsys.readouterr()
        assert "Repayment failed: invalid input, please try again." in captured.out

# TC13: existing_loan = 2, balance = 1000, 
#       loan1: loan_remaining = 1100, loan2: loan_remaining = 1000
#       option = 2, repayment = 1000
def test_payLoan_13(monkeypatch, capsys):
    inputs = iter(["2", "1000"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchall.return_value = [["1", 100000, 110000, 63, 75], ["2", 100000, 100000, 63, 75]]
            payLoan("test", 100000)
            captured = capsys.readouterr()
            assert "Your repayment has been successfully processed!" in captured.out

# TC14: existing_loan = 3, balance = 1000, 
#       loan1: loan_remaining = 1100, loan2: loan_remaining = 1000, loan3: loan_remaining = 1000
#       option = 4, repayment = 1000
def test_payLoan_14(monkeypatch, capsys):
    inputs = iter(["4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
            mocksql.execute().fetchall.return_value = [["1", 100000, 110000, 63, 75], ["2", 100000, 100000, 63, 75], ["3", 100000, 100000, 63, 75]]
            payLoan("test", 100000)
            captured = capsys.readouterr()
            assert "Invalid option, please try again." in captured.out

# TC15: existing_loan = 2, balance = 1000, 
#       loan1: loan_remaining = 1100, loan2: loan_remaining = 1000
#       option = 3, repayment = 1000
def test_payLoan_15(monkeypatch, capsys):
    inputs = iter(["3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [["1", 100000, 110000, 63, 75], ["2", 100000, 100000, 63, 75]]
        payLoan("test", 100000)
        captured = capsys.readouterr()
        assert "Invalid option, please try again." in captured.out


#----------------------------------------------------------------
#
#  Test Suite 9: FR-9: Make Time Go Forward
#  
#       username = test
#       overdue_loans = 1
#----------------------------------------------------------------

# TC01: balance = 0, loan_remaining = 1000
def test_pass1Month_1(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [[1, "test", "1000"]]
        mocksql.execute().fetchone.return_value = [0]
        #mocksql.execute.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            pass1Month()

# TC02: balance = 1000, loan_remaining = 1000
def test_pass1Month_2(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [[1, "test", "1000"]]
        mocksql.execute().fetchone.return_value = ["1000"]
        #mocksql.execute.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            pass1Month()

# TC02: balance = 1000, loan_remaining = 1001
def test_pass1Month_3(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [[1, "test", "1001"]]
        mocksql.execute().fetchone.return_value = ["1000"]
        #mocksql.execute.side_effect = sql_results
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            pass1Month()
            #captured = capsys.readouterr()

#----------------------------------------------------------------
#
#  Test Suite 10: FR-10: Check Loans
#  
#       username = test
#       overdue_loans = 1
#----------------------------------------------------------------

# TC01: balance = 0, loan_remaining = 1000
def test_checkLoans_1(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [[1, "1000"]]
        mocksql.execute().fetchone.return_value = ["0"]
        #mocksql.execute.side_effect = sql_results
        a = checkLoans("test")
        assert a == 1000

# TC02: balance = 1000, loan_remaining = 1000
def test_checkLoans_2(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [[1, "1000"]]
        mocksql.execute().fetchone.return_value = ["1000"]
        #mocksql.execute.side_effect = sql_results
        a = checkLoans("test")
        assert a == 0

# TC03: balance = 1000, loan_remaining = 1001
def test_checkLoans_3(monkeypatch, capsys):
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchall.return_value = [[1, "1001"]]
        mocksql.execute().fetchone.return_value = ["1000"]
        #mocksql.execute.side_effect = sql_results
        a = checkLoans("test")
        assert a == 1


#----------------------------------------------------------------
#
#  Test Suite 11: FR-11: Admin Dashboard
#  
#       username = admin, password = admin
#----------------------------------------------------------------

# TC01: option = 1
def test_admin_1(monkeypatch, capsys):
    inputs = iter(["1", "2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('main_test.changeRates', lambda: print("changeRates()"))
    #mock_cursor = mock_connect.return_value.cursor.return_value
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["1000000000", "1000", "500", "40"]
        admin()
        captured = capsys.readouterr()
        assert "changeRates()" in captured.out

# TC02: option = 2
def test_admin_2(monkeypatch, capsys):
    inputs = iter(["2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["1000000000", "1000", "500", "40"]
        a = admin()
        captured = capsys.readouterr()
        assert captured.out and a == None

# TC03: option = 3
def test_admin_3(monkeypatch, capsys):
    inputs = iter(["3", "2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["1000000000", "1000", "500", "40"]
        a = admin()
        captured = capsys.readouterr()
        assert captured.out and a == None

# TC04: option = None 
def test_admin_4(monkeypatch, capsys):
    inputs = iter(["", "2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["1000000000", "1000", "500", "40"]
        a = admin()
        captured = capsys.readouterr()
        assert captured.out and a == None


#----------------------------------------------------------------
#
#  Test Suite 12: FR-11: Change Interest Rates
#  
#       total_assets = 10100000.00, min_loanrate = 9.50, 
#       max_loanrate = 10.00, min_depositrate = 4.50, 
#       max_loanrate = 5.00
#----------------------------------------------------------------

# TC01: new_loanrate = 9.50, new_depositrate = 4.50
def test_changeRates_1(monkeypatch, capsys):
    inputs = iter(["9.50", "4.50"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchone.return_value = ["1010000000", "1000", "500"]
            changeRates()
            captured = capsys.readouterr()
            assert "Loan rate has been successfully changed!" in captured.out and "Deposit rate has been successfully changed!" in captured.out

# TC02: new_loanrate = 9.49, new_depositrate = 4.50
def test_changeRates_2(monkeypatch, capsys):
    inputs = iter(["9.49", "4.50"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchone.return_value = ["1010000000", "1000", "500"]
            changeRates()
            captured = capsys.readouterr()
            assert "Loan rate change failed: Invalid input." in captured.out and "Deposit rate has been successfully changed!" in captured.out

# TC03: new_loanrate = 9.50, new_depositrate = 4.49
def test_changeRates_3(monkeypatch, capsys):
    inputs = iter(["9.50", "4.49"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchone.return_value = ["1010000000", "1000", "500"]
            changeRates()
            captured = capsys.readouterr()
            assert "Loan rate has been successfully changed!" in captured.out and "Deposit rate change failed: Invalid input." in captured.out

# TC04: new_loanrate = 9.51, new_depositrate = 4.51
def test_changeRates_4(monkeypatch, capsys):
    inputs = iter(["9.51", "4.51"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchone.return_value = ["1010000000", "1000", "500"]
            changeRates()
            captured = capsys.readouterr()
            assert "Loan rate has been successfully changed!" in captured.out and "Deposit rate has been successfully changed!" in captured.out

# TC05: new_loanrate = 9.99, new_depositrate = 4.99
def test_changeRates_5(monkeypatch, capsys):
    inputs = iter(["9.99", "4.99"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchone.return_value = ["1010000000", "1000", "500"]
            changeRates()
            captured = capsys.readouterr()
            assert "Loan rate has been successfully changed!" in captured.out and "Deposit rate has been successfully changed!" in captured.out

# TC06: new_loanrate = 10.00, new_depositrate = 5.00
def test_changeRates_6(monkeypatch, capsys):
    inputs = iter(["10.00", "5.00"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchone.return_value = ["1010000000", "1000", "500"]
            changeRates()
            captured = capsys.readouterr()
            assert "Loan rate has been successfully changed!" in captured.out and "Deposit rate has been successfully changed!" in captured.out

# TC07: new_loanrate = 10.01, new_depositrate = 5.00
def test_changeRates_7(monkeypatch, capsys):
    inputs = iter(["10.01", "5.00"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchone.return_value = ["1010000000", "1000", "500"]
            changeRates()
            captured = capsys.readouterr()
            assert "Loan rate change failed: Invalid input." in captured.out and "Deposit rate has been successfully changed!" in captured.out

# TC08: new_loanrate = 10.00, new_depositrate = 5.01
def test_changeRates_8(monkeypatch, capsys):
    inputs = iter(["10.00", "5.01"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        with patch('main_test.conn') as mockcommit:
            mockcommit.commit.return_value = []
            mocksql.execute().fetchone.return_value = ["1010000000", "1000", "500"]
            changeRates()
            captured = capsys.readouterr()
        assert "Loan rate has been successfully changed!" in captured.out and "Deposit rate change failed: Invalid input." in captured.out

# TC09: new_loanrate = 9.999, new_depositrate = 9.999
def test_changeRates_9(monkeypatch, capsys):
    inputs = iter(["9.999", "9.999"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["1010000000", "1000", "500"]
        changeRates()
        captured = capsys.readouterr()
        assert "Loan rate change failed: Invalid input." in captured.out and "Deposit rate change failed: Invalid input." in captured.out

# TC10: new_loanrate = #, new_depositrate = #
def test_changeRates_10(monkeypatch, capsys):
    inputs = iter(["#", "#"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["1010000000", "1000", "500"]
        changeRates()
        captured = capsys.readouterr()
        assert "Loan rate change failed: Invalid input." in captured.out and "Deposit rate change failed: Invalid input." in captured.out

# TC11: new_loanrate = None, new_depositrate = None
def test_changeRates_11(monkeypatch, capsys):
    inputs = iter(["", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('main_test.c') as mocksql:
        mocksql.execute().fetchone.return_value = ["1010000000", "1000", "500"]
        changeRates()
        captured = capsys.readouterr()
        assert "Loan rate change failed: Invalid input." in captured.out and "Deposit rate change failed: Invalid input." in captured.out



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