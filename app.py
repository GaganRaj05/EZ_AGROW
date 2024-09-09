from flask import Flask, url_for, render_template, session, redirect, request, flash
from forms import Labour_login, Farmer_login, Farmer_Registeration, Labour_Registration
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_DB'] = 'EZ_AGROw'
app.config['MYSQL_PASSWORD'] = 'Wanderer89'
mysql = MySQL(app)

@app.route("/")
def home():
    session['user_name'] = None
    session['password'] = None
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    formF = Farmer_login()
    formL = Labour_login()
    form_type = request.args.get("form_type")
    if form_type == "farmer" and formF.validate_on_submit():
        cursor = mysql.connection.cursor()
        username = formF.username.data
        passwd = formF.password.data
        cursor.execute("select username, password from FARMER where username=%s and password=%s", (username, passwd))
        valid = cursor.fetchone()
        if valid:
            session['user_name'] = username
            session['password'] = passwd
            flash(f"Successfully Logged-In", "success")
            return redirect(url_for('home'))
        else:
            flash(f"No farmer entries found or Your email or password is incorrect ", "danger")
            return redirect(url_for('login'))
        
    elif form_type == "labour" and formL.validate_on_submit():
        cursor = mysql.connection.cursor()
        username = formL.username.data
        passwd = formL.password.data
        cursor.execute("select username, password from LABOUR where username=%s and password=%s", (username, passwd))
        valid = cursor.fetchone()
        if valid:
            session['user_name'] = username
            session['password'] = passwd
            flash(f"Successfully Logged-In", "success")
            return redirect(url_for('home'))
        else:
            flash(f"No farmer entries found or Your email or password is incorrect ", "danger")
            return redirect(url_for('login'))
    else:
        return render_template("login.html", formF = formF, formL = formL)
        

@app.route("/register", methods=['GET','POST'])
def register():
    formF = Farmer_Registeration()
    formL = Labour_Registration()
    cursor = mysql.connection.cursor()
    
    form_type = request.args.get("form_type")
    if form_type =="farmer" and formF.validate_on_submit():
        current_username = formF.farmer_username.data
        cursor.execute("select username from FARMER where username=%s", (current_username,))
        db_username = cursor.fetchone()
        if db_username is not None and current_username == db_username[0]:
            flash(f"Username already exists!!.. Please enter a new username", "danger")
            return redirect(url_for('register'))
        elif formF.farmer_confirm_password.data != formF.farmer_new_password.data:
            flash(f"Passwords do not match", "danger")
            return redirect(url_for('register'))
        else:
            cursor.execute("select max(farmer_id) from FARMER")
            user_id=cursor.fetchone()[0]
            if user_id is None:
                user_id = 1
            else:
                user_id = user_id + 1
            
            cursor.execute("insert into FARMER values ( %s, %s, %s, %s, %s, %s, %s, %s, %s)", (user_id, formF.farmer_name.data,  formF.farmer_date_of_birth.data, formF.farmer_gender.data, formF.farmer_phone_no.data, formF.farmer_email.data, formF.farmer_farm_type.data, formF.farmer_new_password.data, formF.farmer_username.data))
            mysql.connection.commit()

            flash(f"Account created successfull, Please Login", "success")
            return redirect(url_for('login', alert="success"))
    elif form_type=="labour" and formL.validate_on_submit():
        current_username = formL.labour_username.data
        cursor.execute("select username from LABOUR where username=%s", (current_username,))
        db_username = cursor.fetchone()
        if db_username is not None and current_username == db_username[0]:
            flash(f"Username already exists!!.. Please enter a new username", "danger")
            return redirect(url_for('register'))

        elif formL.labour_confirm_password.data != formL.labour_new_password.data:
            flash(f"Passwords do not match ", "danger")
            return redirect(url_for("register"))
        else:
            cursor.execute("select max(labour_id) from LABOUR")
            user_id = cursor.fetchone()[0]
            if user_id:
                user_id += 1
            else:
                user_id = 1
            cursor.execute("insert into LABOUR values(%s,%s,%s,%s,%s,%s,%s, %s)", (formL.labour_name.data, user_id, formL.labour_date_of_birth.data, formL.labour_gender.data, formL.labour_phone_no.data, formL.labour_email.data, formL.labour_new_password.data, formL.labour_username.data))
            mysql.connection.commit()
            flash(f"Account created successfully, Please Login", "success")
            return redirect(url_for('login'))
    else:
        return render_template("register.html", formF=formF, formL=formL)
    
    
if __name__ == '__main__':
    app.run(debug=True)
    