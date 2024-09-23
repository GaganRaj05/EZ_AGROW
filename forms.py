from flask_wtf import FlaskForm;
from wtforms import StringField, PasswordField, FileField, SubmitField, IntegerField, DateField, SelectField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileRequired, FileAllowed

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
    
class Forgot_Password(FlaskForm):
    phone_no = StringField(validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField()
    
class OTP(FlaskForm):
    f = StringField(validators=[DataRequired(), Length(min=1, max=1)])
    o = StringField(validators=[DataRequired(), Length(min=1, max=1)])
    u = StringField(validators=[DataRequired(), Length(min=1, max=1)])
    r = StringField(validators=[DataRequired(), Length(min=1, max=1)])
    submit = SubmitField()
    
class FARMER_REQUIREMENTS(FlaskForm):
    farmer_requirements = TextAreaField(validators = [DataRequired(), Length(min=10)])
    submit = SubmitField("Next")
    
class FINAL_WORK_UPLOAD(FlaskForm):
    choices = [(1,"Planting"), (2,"Harvesting"), (3,"Irrigation"), (4,"Plowing"), (5,"pest Control"), (6,"Fertilizing")]
    work_type = SelectField("Select Work Type",choices=choices,  validators=[DataRequired()])
    work_description = TextAreaField("Describe your work here", validators=[DataRequired(), Length(min=10)])
    equipments = StringField(validators=[DataRequired()])
    no_of_workers = IntegerField(validators=[DataRequired()])
    start_date = DateField(validators=[DataRequired()])
    submit=SubmitField()
    
class SELL_PRODUCTS(FlaskForm):
    product_name = StringField( validators=[DataRequired()])
    choices = [(1,"Flowers"), (2, "Fruits"), (3, "Fertilisers"), (4, "Plants"), (5, "Seeds"), (6, "Saplings"), (7, "Insecticides"), (8, "Compost"), (9, "Tools"), (10, "Machinery")]
    category = SelectField(choices = choices)
    product_description = TextAreaField(validators = (DataRequired(), Length(min=10)))
    quantity  = IntegerField(validators = [DataRequired()])
    price = IntegerField(validators=[DataRequired()])
    photo = FileField(validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    seller_name = StringField(validators = [DataRequired()])
    seller_des = TextAreaField(validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class PROFILE_UPDATE(FlaskForm):
    name = StringField()
    phone_no = StringField()
    username = StringField()
    email = StringField()
    submit = SubmitField("Save Info")
    
    
class CHANGE_PASSWORD(FlaskForm):
    old_password = PasswordField()
    new_password = PasswordField()
    confirm_password = PasswordField()
    submit = SubmitField("Save Info")
    
class JobApplicationForm(FlaskForm):
    # Full name field
    full_name = StringField('Full Name', validators=[
        DataRequired(message="Full Name is required"),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters")
    ])
    
    # Proposal description field
    proposal_description = TextAreaField('Proposal Description', validators=[
        DataRequired(message="Proposal description is required"),
        Length(min=10, message="Description must be at least 10 characters long")
    ])
    
    # Money field
    money = DecimalField('Expected Payment (in INR)', validators=[
        DataRequired(message="Payment is required"),
        NumberRange(min=0, message="Payment should be a positive number")
    ])
    
    # Address field
    address = StringField('Address', validators=[
        DataRequired(message="Address is required"),
        Length(min=5, max=255, message="Address must be between 5 and 255 characters")
    ])
    
    # Phone number field
    phone_no = StringField('Phone Number', validators=[
        DataRequired(message="Phone number is required"),
        Length(min=10, max=15, message="Phone number must be between 10 and 15 digits")
    ])
    
    # Submit button
    submit = SubmitField('Submit Application')

