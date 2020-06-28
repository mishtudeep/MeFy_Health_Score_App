from flask import *
import json
from datetime import datetime
import pytz
import dbconnect
import mysql.connector

app = Flask(__name__)

@app.route('/healthscoreapp')
def index():
    return render_template("index.html")

@app.route('/api/getAllData')
def getAllData():
    try:
        connection, cursor = dbconnect.getConnection()
        statement = 'Select * from heathscoredata'
        cursor.execute(statement)

        data = cursor.fetchall();
        
        dataModel = {}
        op = []
        for d in data:
            dataModel = {
                'id': d[0],
                'timestamp': str(d[1]),
                'age': d[2],
                'gender': d[3],
                'height': d[4],
                'weight': d[5],
                'heartrate': d[6],
                'bloodpressuresys': d[7],
                'bloodpressuredia': d[8],
                'bmi': d[9],
                'cholestterollevel': d[10],
                'avgBloodSugarLevel': d[11],
                'alcoholConsumptionDaily': d[12],
                'alcoholConsumptionWeekly':d[13],
                'smoker': d[14],
                'score': d[15],
                'username': d[16]
            }
            op.append(dataModel)
        return json.dumps(op)
    except Exception as e:
        print("Error in fetching data", e)
        return json.dumps({'message':'Error in fetching data'})

@app.route('/api/getScore', methods=['POST'])
def getValues():
    age=int(request.form['age'])
    gender=request.form['gender']
    height=float(request.form['height'])
    height = height / 3.281
    weight=float(request.form['weight'])
    heartrate=int(request.form['heartrate'])
    bloodpressuresys=float(request.form['bloodpressuresys'])
    bloodpressuredia=float(request.form['bloodpressuredia'])
    cholestrol=float(request.form['cholestrol'])
    avgbloodsugar=float(request.form['avgbloodsugar'])
    alcoholconsumptiondaily=int(request.form['alcoholconsumptiondaily'])
    alocholconsumptionweekly=int(request.form['alocholconsumptionweekly'])
    smoker=request.form['smoker']
    username=request.form['username']

    score, recommendations = calculatehealthscore(age, gender, height, weight, heartrate, bloodpressuresys, bloodpressuredia, cholestrol, avgbloodsugar, alcoholconsumptiondaily, alocholconsumptionweekly, smoker)
    bmi = weight / (height**2)
    
    #DATABASE TRANSACTION
    
    timestamp = str(datetime.now(pytz.timezone('Asia/Kolkata')))[:-13]
    ts = datetime.now(pytz.timezone('Asia/Kolkata'))
    idno = str(ts.year)+str(ts.month)+str(ts.day)+str(ts.hour)+str(ts.minute)+str(ts.second)
    try:
        connection, cursor = dbconnect.getConnection()
        
        values = (idno, timestamp, age, gender, height, weight, heartrate, bloodpressuresys, bloodpressuredia, bmi, cholestrol, avgbloodsugar, alcoholconsumptiondaily, alocholconsumptionweekly, smoker, score, username)
        statement="INSERT INTO heathscoredata VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(statement, values)
        connection.commit()
        connection.close()
    except Exception as e:
        connection.close()
        print(e)
    
    return json.dumps({'score': score, 'recommendations': recommendations})

@app.route('/api/getScoreApp', methods=['POST'])
def getValuesApp():
    age=int(request.json['age'])
    gender=request.json['gender']
    height=float(request.json['height'])
    height = height / 3.281
    weight=float(request.json['weight'])
    heartrate=int(request.json['heartrate'])
    bloodpressuresys=float(request.json['bloodpressuresys'])
    bloodpressuredia=float(request.json['bloodpressuredia'])
    cholestrol=float(request.json['cholestrol'])
    avgbloodsugar=float(request.json['avgbloodsugar'])
    alcoholconsumptiondaily=int(request.json['alcoholconsumptiondaily'])
    alocholconsumptionweekly=int(request.json['alocholconsumptionweekly'])
    smoker=request.json['smoker']
    username=request.json['username']

    score, recommendations = calculatehealthscore(age, gender, height, weight, heartrate, bloodpressuresys, bloodpressuredia, cholestrol, avgbloodsugar, alcoholconsumptiondaily, alocholconsumptionweekly, smoker)
    bmi = weight / (height**2)
    
    #DATABASE TRANSACTION
    
    timestamp = str(datetime.now(pytz.timezone('Asia/Kolkata')))[:-13]
    ts = datetime.now(pytz.timezone('Asia/Kolkata'))
    idno = str(ts.year)+str(ts.month)+str(ts.day)+str(ts.hour)+str(ts.minute)+str(ts.second)
    try:
        connection, cursor = dbconnect.getConnection()
        
        values = (idno, timestamp, age, gender, height, weight, heartrate, bloodpressuresys, bloodpressuredia, bmi, cholestrol, avgbloodsugar, alcoholconsumptiondaily, alocholconsumptionweekly, smoker, score, username)
        statement="INSERT INTO heathscoredata VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(statement, values)
        connection.commit()
        connection.close()
    except Exception as e:
        connection.close()
        print(e)
    
    return json.dumps({'score': score, 'recommendations': recommendations})

def calculatehealthscore(age, gender, height, weight, heartrate, bloodpressuresys, bloodpressuredia, cholestrol, avgbloodsugar, alcoholconsumptiondaily, alocholconsumptionweekly, smoker):
    totalScore = 0
    recommendations = []
    smokerscore = 0
    bmiScore, bmiMsg = getBMIScore(weight, height)
    heartRateScore, heartRateMsg = getHeartRateScore(age, heartrate)
    alcoholDailyScore, alcoholDailyMsg = getAlcoholDailyScore(gender, alcoholconsumptiondaily)
    alcoholWeeklyScore, alcoholWeeklyMsg = getAlcoholWeeklyScore(gender, alocholconsumptionweekly)
    bloodPressureScore, bpMsg = getBloodPressureScore(bloodpressuresys, bloodpressuredia)
    choleaterolScore, choMsg = getCholesterolScore(cholestrol)
    bloodSugarScore, sugarMsg = getBloodSugarScore(avgbloodsugar)
    if smoker == 'yes':
        smokerscore = 5
        recommendations.append("Smoking: Please Reduce / Quit Smoking. There is a high chance of getting cancer")
    else:
        smokerscore = 20
        recommendations.append("Smoking: You are safe for now, protect yourself from being a passive smoker as much as possible")
    recommendations.append(bmiMsg)
    recommendations.append(heartRateMsg)
    recommendations.append(alcoholDailyMsg)
    recommendations.append(alcoholWeeklyMsg)
    recommendations.append(bpMsg)
    recommendations.append(choMsg)
    recommendations.append(sugarMsg)
    
    print(bmiScore,heartRateScore,alcoholDailyScore,alcoholWeeklyScore,bloodPressureScore,choleaterolScore,bloodSugarScore,smokerscore)
    totalScore = bmiScore + heartRateScore + alcoholDailyScore + alcoholWeeklyScore + bloodPressureScore + choleaterolScore + bloodSugarScore + smokerscore
    healthScore = (totalScore /185) * 100
    return round(healthScore,2), recommendations

def getBMIScore(weight, height):
    BMI = weight / (height**2)
    if BMI < 18.5:
        return 25, "BMI:You are underweight, eat properly, stay safe"
    elif BMI >= 18.5 and BMI <= 24.5:
        return 20, "BMI: You have a healthy weight, stay healthy, stay safe"
    elif BMI > 24.5 and BMI <=29.9:
        return 15, "BMI: You are moderately overweight, eat healthy and do regular exercise to reduce risk of diseases in future"
    elif BMI >= 30 and BMI <= 39.9:
        return 10, "BMI: You are overweight, eat healthy and do regular exercise to reduce risk of diseases in future"
    elif BMI >= 40:
        return 5, "BMI: You are extremely obese, eat healthy and do regular exercise to reduce risk of diseases in future"

def getHeartRateScore(age, heartrate):
    print(heartrate)
    if age >= 18 and age <= 25:
        if heartrate >= 50 and heartrate <60:
            return 25, "HEART RATE: Your heart condition is very good, stay healthy"
        elif heartrate >= 60 and heartrate < 70:
            return 20, "HEART RATE: Your heart condition is good, stay healthy"
        elif heartrate >= 70 and heartrate < 75:
            return 15, "HEART RATE: Your heart condition is average, eat healthy food and exercise"
        elif heartrate >= 75 and heartrate <80:
            return 10, "HEART RATE: Your heart condition might be bad, consider consulting a doctor"
        elif heartrate >= 80:
            return 5, "HEART RATE: You have a risk of heart disease, consider consulting a doctor"
    elif age >= 26 and age <= 35:
        if heartrate >= 50 and heartrate <60:
            return 25, "HEART RATE: Your heart condition is very good, stay healthy"
        elif heartrate >= 60 and heartrate <= 72:
            return 20, "EART RATE: Your heart condition is good, stay healthy"
        elif heartrate >= 73 and heartrate <=76:
            return 15, "HEART RATE: Your heart condition is average, eat healthy food and exercise"
        elif heartrate >= 77 and heartrate <80:
            return 10, "HEART RATE: Your heart condition might be bad, consider consulting a doctor"
        elif heartrate >= 80:
            return 5, "HEART RATE: You have a risk of heart disease, consider consulting a doctor"
    elif age >= 36 and age <= 45:
        if heartrate >= 50 and heartrate <62:
            return 25, "HEART RATE: Your heart condition is very good, stay healthy"
        elif heartrate >= 62 and heartrate < 72:
            return 20, "EART RATE: Your heart condition is good, stay healthy"
        elif heartrate >= 72 and heartrate < 76:
            return 15, "HEART RATE: Your heart condition is average, eat healthy food and exercise"
        elif heartrate >= 76 and heartrate <81:
            return 10, "HEART RATE: Your heart condition might be bad, consider consulting a doctor"
        elif heartrate >= 81:
            return 5, "HEART RATE: You have a risk of heart disease, consider consulting a doctor"
    elif age >= 46 and age <= 55:
        if heartrate >= 50 and heartrate <63:
            return 25, "HEART RATE: Your heart condition is very good, stay healthy"
        elif heartrate >= 63 and heartrate < 73:
            return 20, "EART RATE: Your heart condition is good, stay healthy"
        elif heartrate >= 73 and heartrate < 77:
            return 15, "HEART RATE: Your heart condition is average, eat healthy food and exercise"
        elif heartrate >= 77 and heartrate <82:
            return 10, "HEART RATE: Your heart condition might be bad, consider consulting a doctor"
        elif heartrate >= 82:
            return 5, "HEART RATE: You have a risk of heart disease, consider consulting a doctor"
    elif age >= 56 and age <= 65:
        if heartrate >= 50 and heartrate <63:
            return 25, "HEART RATE: Your heart condition is very good, stay healthy"
        elif heartrate >= 63 and heartrate < 72:
            return 20, "EART RATE: Your heart condition is good, stay healthy"
        elif heartrate >= 72     and heartrate < 76:
            return 15, "HEART RATE: Your heart condition is average, eat healthy food and exercise"
        elif heartrate >= 76 and heartrate <79:
            return 10, "HEART RATE: Your heart condition might be bad, consider consulting a doctor"
        elif heartrate >= 79:
            return 5, "HEART RATE: You have a risk of heart disease, consider consulting a doctor"
    elif age > 65:
        if heartrate >= 50 and heartrate <60:
            return 25, "HEART RATE: Your heart condition is very good, stay healthy"
        elif heartrate >= 60 and heartrate < 69:
            return 20, "EART RATE: Your heart condition is good, stay healthy"
        elif heartrate >= 69 and heartrate < 74:
            return 15, "High"
        elif heartrate >= 74 and heartrate <78:
            return 10, "HEART RATE: Your heart condition might be bad, consider consulting a doctor"
        elif heartrate >= 78:
            return 5, "HEART RATE: You have a risk of heart disease, consider consulting a doctor"

def getAlcoholDailyScore(gender, alcoholconsumptiondaily):
    if gender == 'male':
        if alcoholconsumptiondaily < 3:
            return 25, "DAILY ALCOHOL CONSUMPTION: You have a healthy drinking habit"
        elif alcoholconsumptiondaily >= 3 and alcoholconsumptiondaily <= 7:
            return 20, "DAILY ALCOHOL CONSUMPTION: Your drinking habit is ok, but please dont drink more"
        elif alcoholconsumptiondaily > 7 and alcoholconsumptiondaily <= 12:
            return 15, "DAILY ALCOHOL CONSUMPTION: You have a risk of geting disease because of your drinking habit"
        elif alcoholconsumptiondaily > 12 and alcoholconsumptiondaily <= 19:
            return 10, "DAILY ALCOHOL CONSUMPTION: You have a  high chance of getting sick please reduce your drinking"
        elif alcoholconsumptiondaily >= 20:
            return 5, "DAILY ALCOHOL CONSUMPTION: Please reduce your drinking level ASAP, also consider consulting a doctor"
    if gender == 'female':
        if alcoholconsumptiondaily < 2:
            return 25, "DAILY ALCOHOL CONSUMPTION: You have a healthy drinking habit"
        elif alcoholconsumptiondaily >= 2 and alcoholconsumptiondaily <= 5:
            return 20, "DAILY ALCOHOL CONSUMPTION: Your drinking habit is ok, but please dont drink more"
        elif alcoholconsumptiondaily > 5 and alcoholconsumptiondaily <= 8:
            return 15, "DAILY ALCOHOL CONSUMPTION: You have a risk of geting disease because of your drinking habit"
        elif alcoholconsumptiondaily > 8 and alcoholconsumptiondaily <= 14:
            return 10, "DAILY ALCOHOL CONSUMPTION: You have a  high chance of getting sick please reduce your drinking"
        elif alcoholconsumptiondaily >= 15:
            return 5, "Extremely High"

def getAlcoholWeeklyScore(gender, alcoholconsumptionweekly):
    if gender == 'male':
        if alcoholconsumptionweekly < 14:
            return 25, "WEEKLY ALCOHOL CONSUMPTION: You have a healthy drinking habit"
        elif alcoholconsumptionweekly >= 14 and alcoholconsumptionweekly <= 29:
            return 20, "WEEKLY ALCOHOL CONSUMPTION: Your drinking habit is ok, but please dont drink more"
        elif alcoholconsumptionweekly > 29 and alcoholconsumptionweekly <= 49:
            return 15, "WEEKLY ALCOHOL CONSUMPTION: You have a risk of geting disease because of your drinking habit"
        elif alcoholconsumptionweekly > 49 and alcoholconsumptionweekly <= 79:
            return 10, "WEEKLY ALCOHOL CONSUMPTION: You have a  high chance of getting sick please reduce your drinking"
        elif alcoholconsumptionweekly >= 80:
            return 5, "WEEKLY ALCOHOL CONSUMPTION: Please reduce your drinking level ASAP, also consider consulting a doctor"
    if gender == 'female':
        if alcoholconsumptionweekly < 7:
            return 25, "WEEKLY ALCOHOL CONSUMPTION: You have a healthy drinking habit"
        elif alcoholconsumptionweekly >= 7 and alcoholconsumptionweekly <= 24:
            return 20, "WEEKLY ALCOHOL CONSUMPTION: Your drinking habit is ok, but please dont drink more"
        elif alcoholconsumptionweekly > 24 and alcoholconsumptionweekly <= 39:
            return 15, "WEEKLY ALCOHOL CONSUMPTION: You have a risk of geting disease because of your drinking habit"
        elif alcoholconsumptionweekly > 39 and alcoholconsumptionweekly <= 59:
            return 10, "WEEKLY ALCOHOL CONSUMPTION: You have a  high chance of getting sick please reduce your drinking"
        elif alcoholconsumptionweekly >= 60:
            return 5, "WEEKLY ALCOHOL CONSUMPTION: Please reduce your drinking level ASAP, also consider consulting a doctor"

def getBloodPressureScore(bloodpressuresys, bloodpressuredia):
    if bloodpressuresys < 120 and bloodpressuredia < 80:
        return 25, "BLOOD PRESSURE: Your Blood Pressure is Normal"
    elif (bloodpressuresys >= 120 and bloodpressuresys < 130) and (bloodpressuredia < 80):
        return 20, "BLOOD PRESSURE: Your Blood Pressure is Elevated"
    elif (bloodpressuresys >= 130 and bloodpressuresys < 140) or (bloodpressuredia >= 80 and bloodpressuredia < 90):
        return 15, "BLOOD PRESSURE: Your Blood Pressure is High might be Hypertension Stage 1"
    elif (bloodpressuresys >= 140) or (bloodpressuredia >= 90):
        return 10, "BLOOD PRESSURE: Your Blood Pressure is High might be Hypertension Stage 2"
    elif (bloodpressuresys >= 180  or bloodpressuredia >= 120):
        return 5, "BLOOD PRESSURE: Your Blood Pressure is Extremely High, seek emergency care immediately"

def getCholesterolScore(cholestrol):
    if cholestrol < 200:
        return 20, "CHOLESTROL: You have a low cholestrol level, eat healthy"
    elif cholestrol >= 200 and cholestrol < 240:
        return 15, "CHOLESTEROL: You have high cholesterol level, seek medical attention"
    elif cholestrol >= 240:
        return 5, "CHOLESTEROL: You have extremely high cholesterol level, this might lead to heart disease, stroke. Seek immediate medical help"

def getBloodSugarScore(avgbloodsugar):
    if avgbloodsugar < 140:
        return 20, "BLOOD SUGAR: Your blood sugar is at normal level"
    elif avgbloodsugar >= 140 and avgbloodsugar < 200:
        return 15, "BLOOD SUGAR: Your blood sugar is in pre diabetic condition"
    elif avgbloodsugar >= 200:
        return 5, "BLOOD SUGAR: Your blood sugar is in a diabetic condition, take necessary medical steps to remain healthy"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
