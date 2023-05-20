import flask
from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import function
from flask import jsonify
from datetime import date
from datetime import datetime, timedelta
import pandas as pd
from prophet import Prophet
import statsmodels.api as sm
import warnings
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM



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


# fbprophet多元时序预测
@app.route('/fbprophet')
def fbprophet():
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='sun010628',
        db='test_users',
        charset='utf8'
    )

    df = pd.read_sql_query("select * from data", conn)
    feature_columns = [
        'highest_temp', 'lowest_temp', 'am_wind_toward', 'pm_wind_toward', 'weather_1', 'weather_2'
    ]
    target_column = ['total_active_power']

    train_size = int(0.85 * len(df))

    multivariate_df = df[['date'] + target_column + feature_columns].copy()
    multivariate_df.columns = ['ds', 'y'] + feature_columns

    train = multivariate_df.iloc[:train_size, :]
    x_train, y_train = pd.DataFrame(multivariate_df.iloc[:train_size, [0, 2, 3, 4, 5, 6, 7]]), pd.DataFrame(
        multivariate_df.iloc[:train_size, 1])
    x_valid, y_valid = pd.DataFrame(multivariate_df.iloc[train_size:, [0, 2, 3, 4, 5, 6, 7]]), pd.DataFrame(
        multivariate_df.iloc[train_size:, 1])
    train = multivariate_df.iloc[:train_size, :]

    model = Prophet()
    model.fit(train)
    y_pred = model.predict(x_valid)

    y_pred_ = y_pred['yhat'].values.tolist()
    x_valid_ = y_pred['ds'].dt.strftime('%Y-%m-%d %H:%M:%S').values.tolist()
    y_valid_ = y_valid['y'].values.tolist()

    return jsonify(
                   y_pred = y_pred_,
                   x_valid = x_valid_,
                   y_valid = y_valid_
                   )

# lstm多元时序预测
@app.route('/lstm')
def lstm():
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='sun010628',
        db='test_users',
        charset='utf8'
    )
    df = pd.read_sql_query("select * from data_process", conn)
    train_size = int(0.85 * len(df))
    test_size = len(df) - train_size
    df = df.fillna(0)
    univariate_df = df[['date', 'total_active_power']].copy()
    univariate_df.columns = ['ds', 'y']

    train = univariate_df.iloc[:train_size, :]

    x_train, y_train = pd.DataFrame(univariate_df.iloc[:train_size, 0]), pd.DataFrame(
        univariate_df.iloc[:train_size, 1])
    x_valid, y_valid = pd.DataFrame(univariate_df.iloc[train_size:, 0]), pd.DataFrame(
        univariate_df.iloc[train_size:, 1])

    data = univariate_df.filter(['y'])
    # Convert the dataframe to a numpy array
    dataset = data.values

    scaler = MinMaxScaler(feature_range=(-1, 0))
    scaled_data = scaler.fit_transform(dataset)

    # Defines the rolling window
    look_back = 52
    # Split into train and test sets
    train, test = scaled_data[:train_size - look_back, :], scaled_data[train_size - look_back:, :]

    def create_dataset(dataset, look_back=1):
        X, Y = [], []
        for i in range(look_back, len(dataset)):
            a = dataset[i - look_back:i, 0]
            X.append(a)
            Y.append(dataset[i, 0])
        return np.array(X), np.array(Y)

    x_train, y_train = create_dataset(train, look_back)
    x_test, y_test = create_dataset(test, look_back)

    # reshape input to be [samples, time steps, features]
    x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
    x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))

    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, LSTM

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(x_train, y_train, batch_size=16, epochs=10, validation_data=(x_test, y_test))

    model.summary()

    # Lets predict with the model
    train_predict = model.predict(x_train)
    test_predict = model.predict(x_test)

    # invert predictions
    train_predict = scaler.inverse_transform(train_predict)
    y_train = scaler.inverse_transform([y_train])

    test_predict = scaler.inverse_transform(test_predict)
    y_test = scaler.inverse_transform([y_test])

    y_train = univariate_df.head(train_size)['y']
    x_test_ticks = univariate_df.tail(test_size)['ds']

    y_truth = pd.DataFrame(y_test[0]).values.tolist()
    final_y_truth = [item for sublist in y_truth for item in sublist]

    y_predict = pd.DataFrame(test_predict[:,0].T).values.tolist()
    final_y_predict = [item for sublist in y_predict for item in sublist]


    return jsonify(x = univariate_df.tail(test_size)['ds'].dt.strftime('%Y-%m-%d %H:%M:%S').values.tolist(),
                   truth = final_y_truth,
                   predict = final_y_predict
    )

# 异常值数据及阈值获取
@app.route('/get_threshold_data')
def get_threshold_data():
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='sun010628',
        db='test_users',
        charset='utf8'
    )

    df = pd.read_sql_query("select * from data_process", conn)
    raw_x = df['date']
    raw_y = df['total_active_power']
    df.set_index('date', inplace=True)


    # max/min
    threshold_min = 203505
    threshold_max = 300392.7345

    anomaly_data_max_min = []
    normal_data_max_min = []
    anomalies_max_min = (df['total_active_power'] < threshold_min) | (df['total_active_power'] > threshold_max)
    for index, is_anomaly in enumerate(anomalies_max_min):
        if is_anomaly:
            anomaly_data_max_min.append([df.index[index].strftime('%Y-%m-%d %H:%M:%S'), df['total_active_power'].iloc[index]])
        else:
            normal_data_max_min.append([df.index[index].strftime('%Y-%m-%d %H:%M:%S'), df['total_active_power'].iloc[index]])


    # 分位数
    threshold_quantile_min = df['total_active_power'].quantile(0.03)
    threshold_quantile_max = df['total_active_power'].quantile(0.97)

    anomaly_data_quantile = []
    normal_data_quantile = []
    anomalies_quantile = (df['total_active_power'] < threshold_quantile_min) | (df['total_active_power'] > threshold_quantile_max)
    for index, is_anomaly in enumerate(anomalies_quantile):
        if is_anomaly:
            anomaly_data_quantile.append([df.index[index].strftime('%Y-%m-%d %H:%M:%S'), df['total_active_power'].iloc[index]])
        else:
            normal_data_quantile.append([df.index[index].strftime('%Y-%m-%d %H:%M:%S'), df['total_active_power'].iloc[index]])


    #3Sigama原则 IQR
    q1 = df['total_active_power'].quantile(0.25)
    q3 = df['total_active_power'].quantile(0.75)
    iqr = q3 - q1
    threshold_low = q1 - 0.5 * iqr
    threshold_high = q3 + 0.5 * iqr

    anomaly_data = []
    normal_data = []

    anomalies_ = (df['total_active_power'] < threshold_low) | (df['total_active_power'] > threshold_high)
    for index, is_anomaly in enumerate(anomalies_):
        if is_anomaly:
            anomaly_data.append([df.index[index].strftime('%Y-%m-%d %H:%M:%S'), df['total_active_power'].iloc[index]])
        else:
            normal_data.append([df.index[index].strftime('%Y-%m-%d %H:%M:%S'), df['total_active_power'].iloc[index]])


    return jsonify(raw_x = raw_x.dt.strftime('%Y-%m-%d %H:%M:%S').values.tolist(),
                   raw_y = raw_y.values.tolist(),
                   anomaly_data_max_min = anomaly_data_max_min,
                   normal_data_max_min = normal_data_max_min,
                   anomaly_data_quantile = anomaly_data_quantile,
                   normal_data_quantile = normal_data_quantile,
                   anomaly_data = anomaly_data,
                   normal_data = normal_data)



if __name__ == "__main__":
    db.create_all()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.run(debug=True,host='127.0.0.1',port=5000)
