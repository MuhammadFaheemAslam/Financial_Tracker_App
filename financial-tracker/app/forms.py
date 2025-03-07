# from flask_wtf import FlaskForm
# from wtforms import StringField, FloatField, SelectField, SubmitField, TextAreaField, PasswordField
# from wtforms.validators import DataRequired,Email, EqualTo


# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Login')


# class TransactionForm(FlaskForm):
#     amount = FloatField('Amount', validators=[DataRequired()])
#     category = StringField('Category', validators=[DataRequired()])
#     transaction_type = SelectField('Type', choices=[('income', 'Income'), ('expense', 'Expense')], validators=[DataRequired()])
#     description = TextAreaField('Description')
#     submit = SubmitField('Add Transaction')
       

# class RegisterForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Register')
