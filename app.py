from flask import Flask, render_template, request
import SQL_Control_Functions as SCF
from getpass import getpass

app = Flask(__name__)

@app.route("/")
@app.route("/home", methods = ["post", "get"])
def home():
    output = request.form.to_dict()
    if len(output)>0:
        name = output["name"]
        DOB = output["DOB"]
        cust_id = SCF.AddCustomer(mydb, name, DOB)
        return render_template("home.html", cust_id = cust_id)
    else:
        return render_template("home.html")
    
        

@app.route("/Login")
def Login():
    global arr
    return render_template("Login.html")

@app.route("/AddCustomer", methods = ["post", "get"])
def AddCustomer():
    return render_template("AddCustomer.html")

@app.route("/OpenAccount", methods = ["post", "get"])
def OpenAccount():
    return render_template("OpenAccount.html")

@app.route("/AccountStatus", methods = ["post", "get"])
def AccountStatus():
    output = request.form.to_dict()
    cust_id1 = int(output["cust_id"])
    branch = str(output["Branch"])
    amt = int(output["init_dep"])
    passwd1 = str(output["password"])
    type1 = str(output["AccountType"])
    if SCF.CheckCustomer(mydb, cust_id1):
        num = SCF.OpenAccount(mydb, cust_id1, type1, branch, amt, passwd1)
        return render_template("AccountStatus.html", num = num)
    return render_template("AccountStatus.html")


@app.route("/BankBasedOptions", methods=["post", "get"])
def BankBasedOptions():
    global acc_no, name, type, cust_id, branch_id, balance, password
    output = request.form.to_dict()
    if len(output)!=0:
        acc_no = output["acc_no"]
        password = output["password"]
    name = str()
    type = str()
    cust_id = int()
    branch_id = int()
    balance = int()
    flag = int(0)
    if SCF.CheckAccount(mydb, acc_no) and SCF.CheckPassword2(mydb, acc_no, password):
        print("Account Found!")
        arr = SCF.PrintDetails(mydb, str(acc_no))
        type = str(arr[0])
        cust_id = int(arr[1])
        branch_id = int(arr[2])
        balance = int(arr[3])
        name = str(arr[4])
    elif not SCF.CheckAccount(mydb, acc_no):
        flag+=1
    else:
        flag+= 2

    return render_template("BankBasedOptions.html", name=name, flag=flag)


@app.route("/Statements", methods = ["post", "get"])
def Statements():
    arr = SCF.ShowStatements(mydb, acc_no)
    return render_template("Statements.html", arr = arr)



@app.route("/AccountDetails", methods = ["post", "get"])
def AccoutnDetails():
    return render_template("AccountDetails.html", name=name, bal=balance, cust_id=cust_id, type=type, acc_no=acc_no)


@app.route("/Transaction", methods = ["post", "get"])
def Transaction():
    return render_template("Transaction.html")

@app.route("/TransactionStatus", methods = ["post", "get"])
def TransactionStatus():
    output = request.form.to_dict()
    x = output["amt"]
    amt = int(x)
    type0 = output["TransactionType"]
    if(type0 == "Withdraw"):
        amt = -1*amt
    
    flag0 = SCF.Transaction(mydb, acc_no, amt)
    val = 0
    if flag0==True:
        val+=1
    else:
        val+=2

    return render_template("TransactionStatus.html", amt = amt, flag = val, Transaction = type0)


@app.route("/SendMoney", methods = ["post", "get"])
def SendMoney():
    return render_template("SendMoney.html")


@app.route("/SendStatus", methods = ["post", "get"])
def SendStatus():
    output = request.form.to_dict()
    pwd = output["tranPwd"]
    tranAmt = int(output["tranAmt"])
    payee = output["payee"]
    val = SCF.SendMoney2(mydb, acc_no, payee, tranAmt, pwd)
    return render_template("SendStatus.html", val = val, amt = tranAmt, payee = payee)


if __name__ == '__main__':
    # Enter the password
    passwd = str("")

    #Enter the User Name
    user = str("")
    
    mydb = SCF.connect_server("localhost", user, passwd)
    app.run(debug=True, port=8000)