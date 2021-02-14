from flask import Flask, render_template, request
import sqlite3
from datetime import datetime, date

from el3 import electre_iii
from topsis import topsis_method
import numpy as np

import threading

now = datetime.now()
today = date.today()
d2 = today.strftime("/%B/%d/%Y")
current_time = now.strftime("%H:%M:%S")
current_time += d2

# ignore this
def update_chat():
    message_list=list()
    conn = sqlite3.connect('dss.db')
    c = conn.cursor()
    c.execute('select * from chat')
    w = c.fetchall()
    for i in w:
        message_list.append(i[0] + ' @ ' + i[1] + ' :\n' + i[2])
    # for i in message_list:
    #     print(i)
    conn.commit()
    conn.close()
    return message_list
# ignore this

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign_form")
def sign_form():
    db_connection = sqlite3.connect("dss.db")
    db_cursor = db_connection.cursor()
    username_sign = request.args.get("username_sign")
    password_sign = request.args.get("password_sign")
    db_cursor.execute("INSERT INTO users VALUES(?,?,?,?,?)",(username_sign,password_sign,current_time,current_time,1))
    db_connection.commit()
    db_connection.close()
    message_list = update_chat()
    return render_template("dashboard.html", name="Welcome back, " + username_sign, all_messages=message_list)

@app.route("/log_form")
def log_form():
    db_connection = sqlite3.connect("dss.db")
    db_cursor = db_connection.cursor()
    username_log = request.args.get("username_log")
    password_log = request.args.get("password_log")
    try:
        db_cursor.execute("SELECT password FROM users WHERE username=?",(username_log,))
        passw = db_cursor.fetchone()
        print(' --- passw:',passw[0],'\n --- input:', password_log,'\n --- as', username_log)
        if password_log == passw[0]:
            print(" --- I'm in")
            db_cursor.execute("SELECT logintimes FROM users WHERE username=?",(username_log))
            print(" --- 2")
            i = db_cursor.fetchone()
            print(" --- 3")
            db_cursor.execute("UPDATE users SET last_login=?, logintimes=? WHERE username=?",(current_time,i[0]+1,username_log))
            print(" --- 4")
            db_connection.commit()
            print(" --- 5")
            db_connection.close()
            print(" --- 6")
            message_list = update_chat()
            print(" --- 7")
            return render_template("dashboard.html", name="Welcome back, " + username_log, all_messages=message_list)
        else:
            return render_template("failure.html", error="username or password doesn't exist.")
    except:
        db_connection.close()
        return render_template("failure.html", error="username or password doesn't exist.")

@app.route("/dashboard-chat")
def dashboard_chat():
    # if request.form.action == "refresh":
    #     print("~~~YES")
        # message_list = update_chat()
        # return render_template("failure.html")
    # elif request.form.action == "send":
    # if request.form.action == "send":
    message = request.args.get("message")
    chatname = request.args.get("chatname")

    db_connection = sqlite3.connect("dss.db")
    db_cursor = db_connection.cursor()
    
    message_list = update_chat()
    
    db_cursor.execute("INSERT INTO chat VALUES(?,?,?)",(chatname,current_time,message))
    db_connection.commit()
    db_connection.close()

    message_list = update_chat()
    return render_template("dashboard.html", name="Welcome back", all_messages=message_list)

@app.route("/refresh")
def refresh():
    print(" --- REFRESHING CHAT --- ")
    message_list = update_chat()
    return render_template("dashboard.html", name="Welcome back", all_messages=message_list)

@app.route("/logout")
def logout():
    return render_template("index.html")

@app.route("/gc")
def gc():
    message_list = update_chat()
    return render_template("dashboard.html", name="Welcome back", all_messages=message_list)

@app.route("/electre3", methods=['POST'])
def electre3():
    tQ = request.form['pq'].split()
    Q = list()
    for i in tQ:
        Q.append(float(i))   
    tP = request.form['pp'].split()
    P = list()
    for i in tP:
        P.append(float(i))   
    tV = request.form['pv'].split()
    V = list()
    for i in tV:
        V.append(float(i)) 
    tW = request.form['pw'].split()
    W = list()
    for i in tW:
        W.append(float(i))

    ta1 = request.form['a1'].split()
    a1 = list()
    for i in ta1:
        a1.append(float(i))  
    ta2 = request.form['a2'].split()
    a2 = list()
    for i in ta2:
        a2.append(float(i))  
    ta3 = request.form['a3'].split()
    a3 = list()
    for i in ta3:
        a3.append(float(i))   
    ta4 = request.form['a4'].split()
    a4 = list()
    for i in ta4:
        a4.append(float(i)) 
    ta5 = request.form['a5'].split()
    a5 = list()
    for i in ta5:
        a5.append(float(i)) 
    ta6 = request.form['a6'].split()
    a6 = list()
    for i in ta6:
        a6.append(float(i))

    dataset = np.array([a1, a2, a3, a4, a5, a6])

    rank_D = electre_iii(dataset, P, Q, V, W, graph = False)[2]
    message_list = update_chat()
    return render_template("dashboard.html", name="Welcome back", all_messages=message_list, results=rank_D)

# weights = np.array([ [0.1, 0.4, 0.3, 0.2] ])
# criterion_type = ['max', 'max', 'max', 'min']
# dataset = np.array([
#     [7, 9, 9, 8],   #a1
#     [8, 7, 8, 7],   #a2
#     [9, 6, 8, 9],   #a3
#     [6, 7, 8, 6]    #a4
#     ])
# relative_closeness = topsis_method(dataset, weights, criterion_type, graph = False)
# print(relative_closeness)

@app.route("/tops", methods=['POST'])
def tops():
    weights_input = list()
    criterion_type = list()
    dataset_input = list()
    dataset_temp2 = list()

    i_tops = int(request.form["i_tops"])

    for m in range(i_tops+1):
        dataset_input.append(m)
    print(" --- dataset_input", dataset_input)

    for i in range(i_tops+1):
        weights_input.append(float(request.form["tw"+str(i)]))
        criterion_type.append(request.form["tc"+str(i)])

        dataset_temp1 = request.form["ta"+str(i)].split()
        dataset_input[i] = list()
        for j in dataset_temp1:
            dataset_input[i].append(int(j))

    print('weights_input',weights_input)

    weights = np.array([weights_input])
    dataset = np.array(dataset_input)

    print('\n',weights,'\n',criterion_type,'\n',dataset_input)

    topsis_results = topsis_method(dataset, weights, criterion_type, graph = False)

    message_list = update_chat()
    return render_template("dashboard.html", name="Welcome back", all_messages=message_list, topsis_results=topsis_results)

@app.route("/ftops")
def ftops():
    message_list = update_chat()
    return render_template("dashboard.html", name="Welcome back", all_messages=message_list)
