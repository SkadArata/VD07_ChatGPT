# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from app import db
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Пароль ещё раз', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    # Методы валидации должны быть внутри класса
    def validate_username(self, username):
        db.session.expire_all()  # Обновите сессию перед запросом
        user = User.query.filter_by(username=username.data).first()
        print('Проверка имени пользователя: ', username.data)  # Отладочный вывод
        if user:
            print('Имя пользователя занято: ', username.data)
            raise ValidationError('Это имя уже есть. Попробуйте другое')

    def validate_email(self, email):
        db.session.expire_all()  # Обновите сессию перед запросом
        user = User.query.filter_by(email=email.data).first()
        print('Проверка электронной почты: ', email.data)  # Отладочный вывод
        if user:
            print('Электронная почта занята: ', email.data)
            raise ValidationError('Этот адрес э-почты уже есть. Попробуйте другой')

class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class UpdateAccountForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя уже используется. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот адрес электронной почты уже используется. Пожалуйста, выберите другой.')

