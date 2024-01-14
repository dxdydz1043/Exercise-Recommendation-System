from flask import Flask, render_template,request,session
import genetic
from csp import *
import csp
from barplot_gen import generate_barplot
from piechart_gen import generate_piechart
import sqlite3

app = Flask(__name__)

app.secret_key='abc@123'

@app.route('/')
def home():
    try:
        if session['loggedin']==True:
            return render_template('home.html')
        else:
            return render_template('index.html')
    except:
        return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    msg=''
    if request.method == 'POST' and 'Email' in request.form and 'Password' in request.form:
        mail=str(request.form['Email'])
        pasw=str(request.form['Password'])
        connection=sqlite3.connect('Customer.db')
        cursor=connection.cursor()
        cursor.execute("SELECT NAME,MAIL,PASSWORD FROM CUSTOMER WHERE MAIL = ? and PASSWORD = ?;",(mail,pasw))
        row=cursor.fetchall()
        if len(row)==1:
            session['loggedin'] = True
            session['name']=row[0][0]
            session['mail']=row[0][1]
            return render_template('home.html')
        else:
            msg='incorrect login credentials! please recheck'
    return render_template('login.html',msg=msg)

@app.route('/register', methods=['GET','POST'])
def register():
    msg=''
    if request.method == 'POST':
        name=str(request.form['Name'])
        mail=str(request.form['Email'])
        pasw=str(request.form['Password'])
        if len(name)<15:
            if len(mail)<25:
                if '@gmail.com'in mail:
                    if len(pasw)<=8:
                        connection=sqlite3.connect('Customer.db')
                        cursor=connection.cursor()
                        cursor.execute("SELECT NAME,MAIL,PASSWORD FROM CUSTOMER WHERE MAIL = ?;",(mail,))
                        row=cursor.fetchall()
                        connection.commit()
                        if len(row)==0:
                            cursor.execute('''INSERT INTO CUSTOMER VALUES(?,?,?);''',(name,mail,pasw))
                            connection.commit()
                            msg='registered successfully!'
                            session['loggedin'] = True
                            session['name']=name
                            session['mail']=mail
                            return render_template('home.html')
                        else:
                            msg='          user already found,please sign in!'
                    else:
                        msg='         password length should be within 8 characters!'
                else:
                    msg='          enter a valid phone number!'
            else:
                msg='         email id should contain @gmail.com!'
        else:
            msg='          email-id too long!'
    else:
        msg='         name is more than the limit of 14 letters!'
    return render_template('login.html',msg=msg)

@app.route('/index', methods=['GET','POST'])
def index():
    session['loggedin']=False
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/gettoknow', methods=['GET','POST'])
def gettoknow():
    msg=''
    global age,skill,push
    global total_plan
    if request.method == 'POST':
        age=int(str(request.form['age']))
        skill=str(request.form['skill-level']).capitalize()
        push=int(str(request.form['pushups']))
        if (15<age<25) and skill=='Beginner':
            skill='Intermediate'
            push+=3
        if (15<age<25) and skill=='intermediate':
            skill='Advanced'
            push+=2
        num_days=5
        total_plan=[]
        fit_score=[]
        day=1
        while day <= num_days:
            best_plan,fitness,cals,exer_contr = genetic.genetic_algorithm(skill,push)
            day_plan=[]
            for category, exercise in best_plan.items():
                day_plan.append((category,exercise,fitness,cals,exer_contr))
            if fitness not in fit_score:
                generate_piechart(exer_contr,day)
                generate_barplot(cals,day)
                total_plan.append(day_plan)
                fit_score+=[fitness]
                day+=1
        return render_template('genetic_exer.html')
    else:
        return render_template('p_details.html',msg=msg)

@app.route('/gene_final/<day>')
def gene_final(day):
    return render_template('genetic_final.html',exercises=total_plan[int(day)-1],push=push,day=day)

@app.route('/w_details')
def w_details():
    return render_template('w_details.html')  # Update to use 'w_details.html'

@app.route('/submit', methods=['GET','POST'])
def submit():
    if request.method=="POST":
        best1=None
        equipment = str(request.form['equip'])
        body_part = str(request.form['body'])
        workout_time = int(request.form['wt'])
        difficulty = int(request.form['diff']) 
        calories = int(request.form['cal']) 
        best1=csp.calculate_best_exercise(equipment,workout_time,difficulty,calories,body_part,i=0,variables=[])
        best1.sort(reverse=True)
        best=best1[:5]
        
        return render_template("submit.html",ex1=best[0][1].capitalize(),ex2=best[1][1].capitalize(),ex3=best[2][1].capitalize(),ex4=best[3][1].capitalize(),ex5=best[4][1].capitalize())

@app.route('/why')
def why():
    return render_template('why.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)