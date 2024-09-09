from flask_wtf import FlaskForm;
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length

class Labour_login(FlaskForm):
    username = StringField("Enter your username: ")
    password = PasswordField("Enter your password: ")
    submit = SubmitField("Submit")
    
    
class Farmer_login(FlaskForm):
    username = StringField("Enter your username: ")
    password = PasswordField("Enter your password: ")
    submit = SubmitField("Log-In")
    
    
class Farmer_Registeration(FlaskForm):
    farmer_name=StringField("Enter your name")
    farmer_email = StringField("Enter your email")
    farmer_new_password = PasswordField("New-Password")
    farmer_confirm_password = PasswordField("Confirm-Password")
    farmer_date_of_birth = DateField()
    choices = [(1, 'Male'), (2, 'Female'), (3, 'Other')]
    farmer_gender = SelectField("Select an option", choices=choices)
    farmer_username = StringField(validators=[DataRequired(), Length(min=12, max=12)])
    farmer_phone_no = StringField("Phone-no", validators=[DataRequired(), Length(min=10, max=10)])
    farmer_farm_type = StringField()
    farmer_sign_up = SubmitField("Sign-up")
    
class Labour_Registration(FlaskForm):
    labour_name=StringField("Enter your name")
    labour_email = StringField("Enter your email")
    labour_username = StringField("Enter your Username", validators=[DataRequired(), Length(min=12, max=12)])
    labour_new_password = PasswordField("New-Password")
    labour_confirm_password = PasswordField("Confirm-Password")
    choices = [(1, 'Male'), (2, 'Female'), (3, 'Other')]
    labour_gender = SelectField("Select an option", choices=choices)
    labour_date_of_birth = DateField(validators =[DataRequired()])
    labour_phone_no = StringField("Phone-no", validators=[DataRequired(), Length(min=10, max=10)])
    labour_sign_up = SubmitField("Sign-up")