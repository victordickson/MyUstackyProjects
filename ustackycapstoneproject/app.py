from flask import Flask, render_template, url_for, request, redirect, flash, current_app
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
from os import environ as env,path
load_dotenv()

app = Flask(__name__)
app.secret_key = 'secret'
app.config["MYSQL_DATABASE_HOST"] = 'localhost'
app.config["MYSQL_DATABASE_DB"] = 'student_db'
app.config["MYSQL_DATABASE_USER"] = ''
app.config["MYSQL_DATABASE_PASSWORD"] = ''
mysql = MySQL(app,cursorclass=DictCursor)

#Function to create the table in database if nonexistent
def create_tb():
    conn = mysql.get_db()
    cur = conn.cursor()
    conn.ping(reconnect=True) #make sure the connection to db is open
    cur.execute('SHOW TABLES')
    found = 0
    for c in cur:
        for title,val in c.items():
            if val == "students":
                found = 1
                break
    if found:
        cur.close()
        pass
    else:
        cur = conn.cursor()
        stmt = 'DROP TABLE IF EXISTS students;'
        cur.execute(stmt)
        stmt = "CREATE TABLE students(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"\
            "first_name VARCHAR(50),"\
            "middle_name VARCHAR(50),"\
            "last_name VARCHAR(50),"\
            "email VARCHAR(50) UNIQUE,"\
            "dob DATE,"\
            "gender VARCHAR(7),"\
            "phone VARCHAR(15),"\
            "address VARCHAR(255),"\
            "state VARCHAR(30),"\
            "local_gov VARCHAR(40),"\
            "kin VARCHAR(50),"\
            "score INT,"\
            "image_name VARCHAR(1024),"\
            "status VARCHAR(20) DEFAULT('undecided')"\
            ");"
        cur.execute(stmt)
        conn.commit()
    conn.close()

#Function to prevent duplicate email registration
def check_email(email):
    conn = mysql.get_db()
    cur = conn.cursor()
    conn.ping(reconnect=True)
    find_stmt = "SELECT email FROM students WHERE email=%s"
    cur.execute(find_stmt,(email))
    rv = cur.fetchall()
    if len(rv) > 0:
        return True
    else:
        return False


@app.route("/")
def home():
    create_tb()
    return render_template("home.html")    

@app.route("/student/new",methods=["GET","POST"])
def student_new():
    create_tb()
    if request.method == "GET":
        return render_template("student_new.html")
    else:
        s_fname = request.form['fname']
        s_mname = request.form['mname']
        s_lname = request.form['lname']
        s_email = request.form['email']
        s_dob = request.form['dob']
        s_gndr = request.form['gndr']
        s_phone = request.form['phone']
        s_addr = request.form['address']
        s_state = request.form['state']
        s_lg = request.form['lg']
        s_kin = request.form['kin']
        s_score = request.form['score']
        s_image = request.files['image']
        var_array = [s_fname,s_mname,s_lname,s_email,s_dob,s_gndr,s_phone,s_addr,s_state,s_lg,s_kin,s_score,s_image]

        #prevent empty values and non-images from being uploaded
        if (not all(var_array)) or (s_image.mimetype.split('/')[0] != "image"):
            flash("Please fill all fields appropriately",'danger')
            return redirect(url_for('student_new'))
        elif check_email(s_email):
            flash("Email has already been registered","danger")
            return redirect(url_for('student_new'))
        else:
            #save image regardless of file extension
            s_imagename = f"{s_fname}{s_lname}.{s_image.mimetype.split('/')[1]}" 
            savepath = path.join(current_app.root_path,f'static/images/{s_imagename}')
            s_image.save(savepath)

            #remove s_image from list and add image name instead
            var_array.pop() 
            var_array.append(s_imagename)

            #some final sanitization
            for val in var_array:
                val = val.strip()
            
            insert_stmt = "INSERT INTO students(first_name,middle_name,last_name,email,dob,gender,phone,address,state,local_gov,kin,score,image_name) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            conn = mysql.get_db()
            conn.ping(reconnect=True)
            cur = conn.cursor()
            cur.execute(insert_stmt,(var_array))
            conn.commit()
            conn.close()

            #confirm the db was affected
            if cur.rowcount > 0:
                flash('Student added successfully','success')
                return redirect(url_for('students_index'))
            else:
                flash('Could not add Student, retry','danger')
                return redirect(url_for('student_new'))
            

@app.route("/admin/students")
def students_index():
    create_tb()
    stmt = "SELECT id,first_name,middle_name,last_name,gender,score,status FROM students;"
    conn = mysql.get_db()
    conn.ping(reconnect=True)
    cur = conn.cursor()
    cur.execute(stmt)
    rv = cur.fetchall()
    return render_template("students_index.html",students=rv)

@app.route("/admin/students/<id>",methods=["GET","POST"])
def student_details(id):
    create_tb()
    student_id = id
    stmt = "SELECT * FROM students WHERE id=%s;"
    conn = mysql.get_db()
    conn.ping(reconnect=True)
    cur = conn.cursor()
    cur.execute(stmt,(student_id))
    rv = cur.fetchall()
    if len(rv) > 0:
        return render_template("student_details.html",student=rv[0])
    else:
        flash("No student found with that ID")
        return redirect(url_for('students_index'))
    

@app.route("/admin/students/<id>/admitted",methods=["POST"])
def student_admitted(id):
    create_tb()
    student_id = id
    stmt = "UPDATE students SET status=%s WHERE id=%s;"
    conn = mysql.get_db()
    cur = conn.cursor()
    conn.ping(reconnect=True)
    try:
        cur.execute(stmt,("admitted",student_id))
        conn.commit()
        conn.close()
        if cur.rowcount > 0:
            return "success"
        else:
            raise Exception()
    except:
        return "failure"

if __name__ == "__main__":
    app.run(debug=True)