"""
В эндпоинт /registration добавьте все валидаторы, о которых говорилось в последнем видео:

1) email (текст, обязательно для заполнения, валидация формата);
2) phone (число, обязательно для заполнения, длина — десять символов, только положительные числа);
3) name (текст, обязательно для заполнения);
4) address (текст, обязательно для заполнения);
5) index (только числа, обязательно для заполнения);
6) comment (текст, необязательно для заполнения).
"""

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Email, Optional, NumberRange
from module_04_flask.homework.hw1_3.hw2_validators import number_length, NumberLength

app = Flask(__name__)
app.config["WTF_CSRF_ENABLED"] = False


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = IntegerField(
        "Phone",
        validators=[
            DataRequired(),
            NumberRange(min=0),
            NumberLength(10, 10),
        ],
    )
    name = StringField("Name", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    index = IntegerField("Index", validators=[DataRequired()])
    comment = StringField("Comment", validators=[Optional()])


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data
        return f"Successfully registered user {email} with phone +7{phone}"

    # временный лог для отладки
    print("DEBUG ERRORS:", form.errors)
    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.run(debug=True)