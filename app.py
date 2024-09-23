import mimetypes,io,base64, requests, os
from flask import Flask, url_for, render_template, session, redirect, request, flash
from forms import FINAL_WORK_UPLOAD,FARMER_REQUIREMENTS,Labour_login, Farmer_login,JobApplicationForm, Farmer_Registeration, Labour_Registration, Forgot_Password, OTP, SELL_PRODUCTS, PROFILE_UPDATE, CHANGE_PASSWORD 
from flask_mysqldb import MySQL
from dotenv import load_dotenv



app = Flask(__name__)
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_DB'] = 'EZ_AGROw'
app.config['MYSQL_PASSWORD'] = 'Wanderer89'
app.config['UPLOAD_FOLDER'] = os.path.abspath('static/images/')
mysql = MySQL(app)

app.secret_key = '12345678'
load_dotenv()
API_KEY = '4616bc86b7be1c3f9fa4d171f48b5471'



@app.route("/")
def home():
    if not  session.get("user_name"):
        session['user_name'] = None
        session['password'] = None
        return render_template("index.html", login_needed=True)
    return render_template("index.html",login_needed=False )

@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('user_name') is not None :
        flash(f"Already Logged In", "success")
        return redirect(url_for('home'))
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
            print(session['user_name'])
            
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
            flash(f"Username already exists!!.. Please enter a new username", "warning")
            return redirect(url_for('register'))
        elif formF.farmer_confirm_password.data != formF.farmer_new_password.data:
            flash(f"Passwords do not match", "warning")
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
    
    
@app.route("/scheme")
def scheme():
    if not session.get("user_name"):
        return render_template("scheme.html", login_needed=True)
    else:
        return render_template("scheme.html", login_needed=False)

@app.route("/market-place")
def marketplace():
    cursor = mysql.connection.cursor()
    category_type = request.args.get("category_type")
    login_needed=False
    if not session.get('user_name'):
        login_needed=True

    if category_type:
        query = """
        SELECT product_name, product_price, image, product_id 
        FROM PRODUCT_DETAILS 
        WHERE category_name=%s
        """
        temp = True
        cursor.execute(query, (category_type,))
        products = cursor.fetchall()
        if products:
            product_name = [product[0] for product in products]
            product_price = [product[1] for product in products]
            images = [product[2] for product in products]
            product_id = [product[3] for product in products]
        else:
            temp = False
            
            
        if temp and product_name and product_price and images:
            

            return render_template("ecommerce.html", 
                                   product_name=product_name, 
                                   product_price=product_price, 
                                   images=images, zip=zip,
                                   product_id = product_id,
                                   login_needed=login_needed)
        else:
            return render_template("ecommerce.html", 
                                   message="No results found", zip=zip, login_needed=login_needed)
    else:
        cursor.execute("SELECT product_name, product_price,product_id, image FROM PRODUCT_DETAILS")
        products = cursor.fetchall()
        temp = True
        if products:
            product_name = [product[0] for product in products]
            product_price = [product[1] for product in products]
            images = [product[3] for product in products]
            product_id = [product[2] for product in products]
        else:
            temp = False
        if temp and product_name and product_price and images:
            


            return render_template("ecommerce.html", 
                                   product_name=product_name, 
                                   product_price=product_price,
                                   product_id = product_id, 
                                   images=images, 
                                    zip=zip, login_needed=login_needed)
        else:
            return render_template("ecommerce.html", 
                                   message="No results found", zip=zip, login_needed=login_needed)

    return render_template("ecommerce.html", message="Category type not provided",zip=zip, login_needed=login_needed)


    


@app.route("/subsidary")
def subsidary():
    if not session.get('user_name'):
        return render_template("subsidary.html", login_needed = True)
    else:
        return render_template("subsidary.html", login_needed = False)

@app.route("/logout")
def logout():
    session.pop('user_name')
    session.pop('password')
    flash(f"Logout successfull", "success")
    return redirect(url_for('home'))

@app.route("/hiring", methods = ["GET", "POST"])
def hiring():
    if not session.get('user_name'):
        flash(f"Login to use this feature", "warning")
        return redirect(url_for('home'))
    else:
        form = FARMER_REQUIREMENTS()
        if form.validate_on_submit():
            cursor = mysql.connection.cursor()
            cursor.execute("select max(work_id) from WORKS")
            max_id = cursor.fetchone()[0]
            print(max_id)
            if max_id is None:
                max_id =   1
            else:
                max_id = max_id+1
                
            status = False
            cursor.execute("insert into WORKS(work_id,farmers_needs, farmer_username, status) value(%s,%s,%s, %s)",(max_id, form.farmer_requirements.data, session.get('user_name'), status))
            mysql.connection.commit()
            return redirect(url_for('more_hiring_info'))
            
        return render_template("hiring1.html", form = form)
    

@app.route("/more-info")
def more_hiring_info():
    
    return render_template("hiring2.html")

@app.route("/more-hiring-info", methods=["GET","POST"])
def more_hiring_info_needed():
    farm_type = request.args.get('farm_type')
    form = FINAL_WORK_UPLOAD()
    if form.validate_on_submit() and farm_type:
        cursor = mysql.connection.cursor()
        cursor.execute("update WORKS set farm_type=%s,work_type=%s, work_description=%s, equipments=%s, workers_needed=%s, start_date=%s  where farmer_username=%s", (farm_type,form.work_type.data, form.work_description.data,form.equipments.data, form.no_of_workers.data, form.start_date.data ,session.get('user_name') ))
        mysql.connection.commit()    
        flash(f"Work uploaded successfully... Check your DashBoard for further info", "success")
        return redirect(url_for("home"))
    else:
        return render_template("hiring3.html", form = form)
@app.route("/cart")
def cart():
    if not session.get('user_name'):
        flash(f"Login to use this feature", "warning")
        return redirect(url_for('marketplace'))
    else:
        cursor=mysql.connection.cursor()
        cursor.execute("select product_name, price, product_id, image from cart where username=%s", (session.get('user_name'),))
        products = cursor.fetchall()
        
        if  products is not None:
            product_name = [product[0] for product in products]
            product_price = [product[1] for product in products] 
            product_id = [product[2] for product in products] 
            image = [product[3] for product in products]
            total = 0
            
            
            for p in product_price:
                total += p
            session['cart_data'] = {
            'product_id': product_id,
            'product_name': product_name,
            'product_price': product_price,
            'total': total  
        }
            return render_template("cart.html", product_name=product_name, product_price=product_price, image = image, zip=zip, product_id=product_id, total = total)
        else:
            return render_template("cart.html", zip=zip )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error_code=404, error_message="Page Not Found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html', error_code=500, error_message="Internal Server Error"), 500

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot():
    formF = Forgot_Password()
    form_type = request.args.get("form_type")
    if  formF.validate_on_submit() and form_type=="farmer":
        print("coming through")
        cursor = mysql.connection.cursor()
        cursor.execute("select phone_number from FARMER where phone_number =%s", (formF.phone_no.data, ))
        valid = cursor.fetchone()
        if valid:
            return redirect(url_for('enter_otp'))
        else:
            flash(f"No Farmer phone number matches your entry", "danger")
            return redirect(url_for('forgot'))
    elif formF.validate_on_submit() and form_type=="labour":
        print("coming through again")
        cursor = mysql.connection.cursor()
        cursor.execute("select phone_number from LABOUR where phone_number =%s", (formF.phone_no.data, ))
        valid = cursor.fetchone()
        if valid:
            return redirect(url_for('enter_otp'))
        else:
            flash(f"No Labour phone number matches your entry", "danger")
            return redirect(url_for('forgot'))
    else:
        return render_template("otp.html", formF = formF)
        
@app.route('/enter-otp')
def enter_otp():
    return render_template("enterOTP.html", formO=OTP())

@app.route("/jobs", methods=["GET", "POST"])
def jobs():
    if session.get("user_name"):
        cursor = mysql.connection.cursor()
        cursor.execute("select work_id,work_type, work_description from works")
        temp = cursor.fetchall()
        if not temp :
            return render_template("jobs.html",  message="No jobs for now ")
        else:
            work_id = [work[0] for work in temp]
            work_type = [work[1] for work in temp]
            work_description = [work[2] for work in temp]
            
            return render_template("jobs.html",  work_id=work_id,work_type=work_type, work_description=work_description, zip=zip)
    else:
        flash(f"You need to login to use this feature","warning")
        return redirect(url_for('home'))
    
@app.route("/application", methods = ["GET","POST"])
def applications():
    work_id = request.args.get("wk_id")
    print(work_id)
    form = JobApplicationForm()
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute("insert into applications values(%s, %s, %s, %s,%s, %s)", (work_id, form.full_name.data, form.proposal_description.data, form.money.data, form.address.data, form.phone_no.data ))
        mysql.connection.commit()
        return redirect(url_for('success'))
    else:
        return render_template("jobaApplication.html", work_id=work_id, form=form)

@app.route("/success")
def success():
    return render_template("success.html")
@app.route("/loans")
def loans():
    return render_template("loans.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/dashboard")
def dashboard():
    if session.get("user_name"):
        cursor = mysql.connection.cursor()
        username = session.get('user_name')
        
        cursor.execute("SELECT work_type, start_date, status FROM works WHERE farmer_username = %s", (username,))
        temp = cursor.fetchall()
        work_type = []
        start_date = []
        status = []

        if temp:
            work_type = [record[0] for record in temp]
            start_date = [record[1] for record in temp]
            status = [record[2] for record in temp]

        cursor.execute("SELECT work_id FROM works WHERE farmer_username=%s", (username,))
        work_ids = cursor.fetchall()

        full_name = []
        address = []
        phone = []
        
        for work_id_tuple in work_ids:
            work_id = work_id_tuple[0]  # Extract the actual work_id
            cursor.execute("SELECT applicant_name, address, phone_no FROM applications WHERE work_id = %s", (work_id,))
            temp = cursor.fetchall()
            if temp:
                for record in temp:
                    full_name.append(record[0])
                    address.append(record[1])
                    phone.append(record[2])

        cursor.execute("SELECT product_name, buyer_username, total FROM orders WHERE seller_username=%s", (username,))
        temp = cursor.fetchall()
        product_name = []
        buyer_username = []
        total = []
        phone_buyer = []

        if temp:
            product_name = [record[0] for record in temp]
            buyer_username = [record[1] for record in temp]
            total = [record[2] for record in temp]
            
            for buyer in buyer_username:
                cursor.execute("SELECT phone_number FROM Farmer WHERE username=%s", (buyer,))
                temp = cursor.fetchone()
                if temp:
                    phone_buyer.append(temp[0])
                else:
                    cursor.execute("select phone_number from labour where username=%s", (buyer, ))
                    temp=cursor.fetchone()
                    if temp:
                        phone_buyer.append(temp[0])

        return render_template("dashboard.html", 
                               work_type=work_type, 
                               start_date=start_date, 
                               status=status, 
                               full_name=full_name, 
                               address=address, 
                               phone=phone,
                               product_name=product_name,
                               phone_buyer=phone_buyer,
                               total=total,
                               zip=zip)
    else:
        flash("You need to log in to use this feature.", "warning")
        return redirect(url_for('home'))


@app.route("/settings", methods=["GET", "POST"])
def settings():
    formF = PROFILE_UPDATE()
    formG = CHANGE_PASSWORD()

    if formF.validate_on_submit():
        full_name = formF.name.data
        phone_no = formF.phone_no.data
        new_username = formF.username.data
        email = formF.email.data

        cursor = mysql.connection.cursor()

        cursor.execute("SELECT username FROM FARMER WHERE username=%s", (new_username,))
        existing_farmer = cursor.fetchone()

        cursor.execute("SELECT username FROM LABOUR WHERE username=%s", (new_username,))
        existing_labour = cursor.fetchone()

        if existing_farmer or existing_labour:
            flash("Username already exists. Please enter another username.", "warning")
            return redirect(url_for('settings'))

       
        current_username = session.get("user_name")
        if not current_username:
            flash("User not logged in", "warning")
            return redirect(url_for('login'))  

        cursor.execute("SELECT username FROM FARMER WHERE username=%s", (current_username,))
        current_farmer = cursor.fetchone()

        cursor.execute("SELECT username FROM LABOUR WHERE username=%s", (current_username,))
        current_labour = cursor.fetchone()

        if current_farmer:
            cursor.execute("UPDATE FARMER SET full_name=%s, phone_number=%s, email=%s, username=%s WHERE username=%s", 
                           (full_name, phone_no, email, new_username, current_username))
        elif current_labour:
            cursor.execute("UPDATE LABOUR SET labour_name=%s, phone_number=%s, email=%s, username=%s WHERE username=%s", 
                           (full_name, phone_no, email, new_username, current_username))
        else:
            flash("Current user not found in the system", "error")
            return redirect(url_for('settings'))

        mysql.connection.commit()

        session['user_name'] = new_username

        flash("Profile updated successfully!", "success")
        return redirect(url_for('settings'))

    return render_template("settings.html", formF=formF, formG=formG)
@app.route("/banks-and-societies")
def banks_and_societies():
    return render_template("banks&soc.html")

@app.route("/software")
def software(): 
    return render_template('softwarefarm.html')

@app.route("/weather", methods=['GET','POST'])
def weather():
    city_name = "New York"  # Default city
    weather_data = None
    forecast_data = None

    if request.method == 'POST':
        city_name = request.form['city']
        if not city_name:
            city_name = "New York"

    # Fetch current weather data from OpenWeatherMap API
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_KEY}'
    weather_response = requests.get(weather_url).json()

    if weather_response.get('cod') == 200:
        weather_data = {
            "city": weather_response['name'],
            "temperature": weather_response['main']['temp'],
            "description": weather_response['weather'][0]['description'],
            "humidity": weather_response['main']['humidity'],
            "wind_speed": weather_response['wind']['speed'],
            "icon": weather_response['weather'][0]['icon']
        }

    # Fetch 5-day forecast data from OpenWeatherMap API
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&appid={API_KEY}'
    forecast_response = requests.get(forecast_url).json()

    if forecast_response.get('cod') == "200":
        forecast_data = []
        for forecast in forecast_response['list'][::8]:  # Every 8th item is 24 hours apart
            forecast_data.append({
                "day": forecast['dt_txt'].split(" ")[0],
                "temperature": forecast['main']['temp'],
                "description": forecast['weather'][0]['description'],
                "icon": forecast['weather'][0]['icon']
            })

    return render_template('weather.html', weather=weather_data, forecast=forecast_data, city_name=city_name)


@app.route("/sell-crops", methods=['GET', 'POST'])
def sell():
    form = SELL_PRODUCTS()
    
    if session.get('user_name'):
        if form.validate_on_submit():
            cursor=mysql.connection.cursor()
            cursor.execute("select max(product_id) from product_details ")
            max_id = cursor.fetchone()[0]
            print(max_id)
            if max_id is not None:
                max_id = max_id + 1
            else:
                max_id = 1
            file = form.photo.data
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            cursor.execute("insert into product_details values(%s, %s, %s, %s,%s, %s)", (max_id, form.product_name.data, form.price.data, form.category.data,filename, session.get('user_name') ))
            mysql.connection.commit()
            flash(f"product uploaded successfully","success")
            return redirect(url_for('home'))
        else:
            print(form.errors)
            return render_template("sellcrops.html", form = form)
    else:
        flash(f"Login to use this feature", "warning")
        return redirect(url_for('home'))
    
@app.route("/add-to-cart")
def add_to_cart():
    if not session.get('user_name'):
        flash(f"Login to use this feature", "warning")
        return redirect(url_for('marketplace'))
    else:
        product_name = request.args.get('product_name')
        price = request.args.get('price')
        cursor = mysql.connection.cursor()
        product_id = request.args.get('product_id')
        image = request.args.get('image')
        
        cursor.execute("insert into cart values(%s, %s, %s, %s, %s) ", (product_name, price, session.get('user_name'), product_id, image))
        mysql.connection.commit()
        flash(f"Items add to cart successfully", "success")
        return redirect(url_for('marketplace'))
    
@app.route("/about-us")
def about_us():
    return render_template("Aboutus.html")    
@app.route('/delete')
def delete():
    p_id = request.args.get('product_id')
    
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM cart WHERE product_id=%s", (p_id,))
    mysql.connection.commit()

    cart_data = session.get('cart_data', {})
    
    if cart_data:
        product_ids = cart_data.get('product_id', [])
        product_names = cart_data.get('product_name', [])
        product_prices = cart_data.get('product_price', [])
        
        if p_id in product_ids:
            index = product_ids.index(p_id)

            product_ids.pop(index)
            product_names.pop(index)
            product_prices.pop(index)

            cart_data['total'] -= cart_data['product_price'][index]

        session['cart_data'] = {
            'product_id': product_ids,
            'product_name': product_names,
            'product_price': product_prices,
            'total': sum(product_prices)  
        }

    flash(f"Item removed from cart successfully", "success")
    return redirect(url_for('cart'))


@app.route("/order")
def order():
    cart_data = session["cart_data"]
    product_ids = cart_data['product_id']
    product_names = cart_data['product_name']
    product_prices = cart_data['product_price']
    total = cart_data['total']

    cursor = mysql.connection.cursor()
    seller_ids = []
    print(product_ids)
    if product_ids:
        print(product_ids)
        for pid in product_ids:
            cursor.execute("SELECT seller_username FROM product_details WHERE product_id=%s", (pid,))
            seller = cursor.fetchone()
            if seller:
                seller_ids.append(seller[0])  

        for pid, pn, pr, sn in zip(product_ids, product_names, product_prices, seller_ids):
            cursor.execute("INSERT INTO orders (product_id, product_name, product_price, seller_username, buyer_username, total) VALUES (%s, %s, %s, %s, %s, %s)",
                           (pid, pn, pr, sn, session.get('user_name'), total))
            mysql.connection.commit()

        flash(f"Order placed successfully!", "success")
        return render_template('orderconf.html', total=total)
    else:
        flash(f"No items present in the cart", "warning")
        return redirect(url_for('cart'))



if __name__ == '__main__':
    app.run(debug=True)
    