import flask
from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import function
from flask import jsonify
from datetime import date
from datetime import datetime, timedelta


pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sun010628@localhost/test_users'
db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

@app.route("/")
def loginpage():
    return render_template("index2.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mail = request.form["mail"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(email=mail, password=passw).first()
        if login is not None:
            return redirect(url_for("index"))
    return render_template("index2.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("loginpage"))
    return render_template("register2.html")

# 主页
@app.route('/homepage')
def index():
    return render_template('homepage.html')


# 环境数据展示
@app.route('/environment_monitor')
def environment_monitor():
    return render_template('environment_monitor.html')


# 总功率监测
@app.route('/total_power_monitor')
def total_power_monitor():
    return render_template('total_power_monitor.html')


# 功率异常点监测
@app.route('/power_outlier_monitor')
def power_outlier_monitor():
    return render_template('power_outlier_monitor.html')

@app.route('/get_environment_data')
def get_environment_data():
    total_active_power = []
    highest_temp = []
    lowest_temp = []
    am_wind_toward = []
    pm_wind_toward = []
    weather_1 = []
    weather_2 = []

    date_time = []

    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='sun010628',
        db='test_users',
        charset='utf8'
    )
    # print("连接数据库成功")
    cur = conn.cursor()
    sql = "select * from data"
    cur.execute(sql)
    result = cur.fetchall()

    for item in result:
        date_time.append(item[0].strftime('%Y-%m-%d %H:%M:%S'))
        total_active_power.append(float(item[1]))
        highest_temp.append(float(item[2]))
        lowest_temp.append(float(item[3]))
        am_wind_toward.append(int(item[4]))
        pm_wind_toward.append(int(item[5]))
        weather_1.append(int(item[6]))
        weather_2.append(int(item[7]))

    mycursor = conn.cursor()
    mycursor.execute("SELECT MIN(date), MAX(date) FROM data")
    date_range = mycursor.fetchone()
    min_date = date_range[0].isoformat()
    max_date = date_range[1].isoformat()

    return jsonify(total_active_power=total_active_power,
                   highest_temp=highest_temp,
                   lowest_temp = lowest_temp,
                   am_wind_toward = am_wind_toward,
                   pm_wind_toward = pm_wind_toward,
                   weather_1 = weather_1,
                   weather_2 = weather_2,
                   min_date = min_date,
                   max_date = max_date,
                   date_time = date_time)

    cur.close()
    conn.close()


if __name__ == "__main__":
    db.create_all()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.run(debug=True,host='127.0.0.1',port=5000)
