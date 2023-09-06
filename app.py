from flask import Flask, render_template,redirect,request,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'email_campaign_manager'

mysql = MySQL(app)



@app.route('/')
def Index():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM subscriber")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', subscriber = data)


#route/method to add new User to list of subscribers
@app.route('/insert', methods = ['POST'])
def insert():    
    if request.method =="POST":
        name = request.form['name']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO subscriber (name,email) VALUES (%s, %s)", (name,email))

        mysql.connection.commit()
        return redirect(url_for('Index'))

#route/method to unsubscribe an user from subscribers list
@app.route('/unsubscribe/<string:email_data>', methods = ['POST','GET'])
def unsubscribe(email_data):
    cur = mysql.connection.cursor()
    cur.execute(""" 
                UPDATE  subscriber
                SET status = "Inactive"
                WHERE email = %s                    
                """, (email_data,))

    mysql.connection.commit()
    return redirect(url_for('Index'))

#route/method to add user(unsubscribed User) back to subscribers list. (if user wish to Subscribe again)
@app.route('/subscribe/<string:email_data>', methods = ['POST','GET'])
def subscribe(email_data):
    cur = mysql.connection.cursor()
    cur.execute(""" 
                UPDATE  subscriber
                SET status = "Active"
                WHERE email = %s                    
                """, (email_data,))

    mysql.connection.commit()
    return redirect(url_for('Index'))

#route for delete the User from DB
@app.route('/delete/<string:email_data>', methods = ['POST','GET'])
def delete(email_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE from subscriber WHERE email LIKE %s", (email_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(debug=True)

