from flask import Flask,render_template,url_for,request,redirect,flash #importing Flask class from flask packages
from flask_mysqldb import MySQL

app=Flask(__name__) # it will give current file name 

#MYSQL CONNECTION
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Raji@17'
app.config['MYSQL_DB']='crud'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app) #MySql is inbuild function where is app is constructed


#Loading Home Page
@app.route('/')
def home():
    con=mysql.connection.cursor()
    sql="SELECT * FROM users"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas=res)

#New Users
@app.route("/addUsers",methods=['GET','POST'])
def addUsers():
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        con = mysql.connection.cursor()
        sql="insert into users(NAME,CITY,AGE) value (%s,%s,%s)"
        con.execute(sql,[name,city,age])
        mysql.connection.commit()
        con.close()
        flash("Users Details Added")
        return redirect(url_for("home"))  
    return render_template("addUsers.html")

#update users
@app.route("/editUsers/<string:id>",methods=['GET','POST'])
def editUsers(id):
    con=mysql.connection.cursor()
    if request.method=="POST":
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        sql="update users set NAME=%s,CITY=%s,AGE=%s where ID=%s"
        con.execute(sql,[name,city,age])
        mysql.connection.commit()
        con.close()
        flash("Users Details Updated")
        return redirect(url_for("home"))
        
    sql="select * from users where ID=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("editUsers.html",datas=res)

#Delete User
@app.route("/deleteUsers/<string:id>",methods=['GET','POST'])
def deleteUsers(id):
    con=mysql.connection.cursor()
    sql="delete from users where ID=%s"
    con.execute(sql,id)
    mysql.connection.commit()
    con.close()
    flash("Users Details Deleted")
    return redirect(url_for('home'))


if __name__=="__main__":  # checking main file or not if its means run this file
    app.secret_key="abc123"
    app.run(debug=True)
    