from flask import Flask, render_template, redirect, request, abort

import api
from data import db_session
from data.congratulations import Congratulations
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from data.holidays import Holidays
from data.roles import Roles
from forms.CongratForm import CongratForm
from forms.HolidayForm import HolidayForm
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from data.users import User
from forms.RoleForm import RoleForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


# служебная функция загрузки пользователя
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Главная страница сайта
@app.route("/")
def index():
    db_sess = db_session.create_session()

    if current_user.is_authenticated:
        congratulations = db_sess.query(Congratulations).filter(
            Congratulations.accepter == current_user)
    else:
        congratulations = db_sess.query(Congratulations).filter()

    return render_template("index.html", congratulations=congratulations)


# регистрация пользователя
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            birth_day=form.birth_date.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


# вход пользователя в систему
@app.route('/login', methods=['GET', 'POST'])
def login():
    global my_id
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            my_id = user.id
            return redirect(f"/{user.id}")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# выход с сайта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# страница пользователя
@app.route('/<int:user_id>')
@login_required
def user_page(user_id):
    db_sess = db_session.create_session()
    list_congrats = db_sess.query(Congratulations).filter(
        (Congratulations.accepter_id == user_id) | (Congratulations.sender_id == user_id)).all()

    user = db_sess.query(User).get(user_id)
    list_holidays = db_sess.query(Holidays).all()

    return render_template('user_page.html', title='Страница', user_id=user_id, list_congrats=list_congrats,
                           name=user.name, about=user.about, birth_day=user.birth_day, list_holidays=list_holidays,
                           role_id=user.role_id)


# страница праздника
@app.route('/holyday_page/<int:hday_id>')
def holyday_page(hday_id):
    db_sess = db_session.create_session()
    list_congrats = db_sess.query(Congratulations).filter(Congratulations.holiday_id == hday_id).all()

    hday = db_sess.query(Holidays).get(hday_id)
    return render_template('holiday_page.html', list_congrats=list_congrats,
                           name=hday.title, hd_id=hday_id, user_role_id=current_user.role_id)


# добавление поздравления
@app.route('/writecong', methods=['GET', 'POST'])
@login_required
def add_cong():
    form = CongratForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        cong = Congratulations()
        cong.holiday_id = form.holiday.data
        cong.send_date = form.hd_date.data
        cong.title = form.title.data
        cong.text = form.text.data
        cong.sender_id = current_user.id
        cong.accepter_id = form.accepter.data
        db_sess.add(cong)

        db_sess.commit()
        return redirect(f'/{cong.accepter_id}')
    db_sess = db_session.create_session()
    list_holidays = [(i.id, i.title) for i in db_sess.query(Holidays).all()]
    form.holiday.choices = list_holidays

    list_users = [(i.id, i.name) for i in db_sess.query(User).all()]
    form.accepter.choices = list_users

    return render_template('congrat.html', title='Добавление поздравления', form=form)


# редактирование поздравления
@app.route('/writecong/<int:id>', methods=['GET', 'POST'])
def writecong(id):
    form = CongratForm()

    if request.method == 'GET':
        db_sess = db_session.create_session()

        cong = db_sess.query(Congratulations).filter(Congratulations.id == id, Congratulations.sender
                                                     == current_user).first()
        if cong:
            form.holiday.data = cong.holiday_id
            form.hd_date.data = cong.send_date
            form.title.data = cong.title
            form.text.data = cong.text
            form.accepter.data = cong.accepter_id
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        cong = db_sess.query(Congratulations).filter(Congratulations.id == id, Congratulations.sender
                                                     == current_user).first()
        if cong:
            cong.holiday_id = form.holiday.data
            cong.send_date = form.hd_date.data
            cong.title = form.title.data
            cong.text = form.text.data
            cong.accepter_id = form.accepter.data
            cong.sender_id = current_user.id
            db_sess.commit()
            return redirect(f'/{current_user.id}')
        else:
            abort(404)
    db_sess = db_session.create_session()

    list_holidays = [(i.id, i.title) for i in db_sess.query(Holidays).all()]
    form.holiday.choices = list_holidays

    list_users = [(i.id, i.name) for i in db_sess.query(User).all()]
    form.accepter.choices = list_users
    return render_template('congrat.html', title='Добавление поздравления', form=form)


# фильтрация по празднику
@app.route('/filter/<int:user_id>/<int:hday_id>', methods=['GET', 'POST'])
def filter(user_id, hday_id):
    db_sess = db_session.create_session()
    list_congrats = db_sess.query(Congratulations).filter(
        (Congratulations.accepter_id == user_id) | (Congratulations.sender_id == user_id),
        Congratulations.holiday_id == hday_id).all()
    user = db_sess.query(User).get(user_id)
    list_holidays = db_sess.query(Holidays).all()
    return render_template('user_page.html', title='Страница', user_id=user_id, list_congrats=list_congrats,
                           name=user.name, about=user.about, birth_day=user.birth_day, list_holidays=list_holidays,
                           role_id=user.role_id)


# удаление поздравления
@app.route('/cong_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    db_sess = db_session.create_session()
    cong = db_sess.query(Congratulations).filter(Congratulations.id == id,
                                                 Congratulations.sender == current_user
                                                 ).first()
    if cong:
        db_sess.delete(cong)
        db_sess.commit()
    else:
        abort(404)
    return redirect(f'/{current_user.id}')


# добавление праздника
@app.route('/holidays', methods=['GET', 'POST'])
@login_required
def add_holiday():
    if current_user.role_id != 1:
        abort(404)

    form = HolidayForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        hol = Holidays()
        hol.title = form.title.data
        hol.date = form.hd_date.data
        db_sess.add(hol)
        db_sess.commit()
        return redirect(f'/{current_user.id}')
    return render_template('holiday.html', title='Добавление праздника',
                           form=form)


# редактирование праздника
@app.route('/holidays/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_holiday(id):
    form = HolidayForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        hol = db_sess.query(Holidays).filter(Holidays.id == id,
                                             current_user.role_id == 1).first()
        if hol:
            form.title.data = hol.title
            form.hd_date.data = hol.date
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        hol = db_sess.query(Holidays).filter(Holidays.id == id,
                                             current_user.role_id == 1).first()
        if hol:
            hol.title = form.title.data
            hol.date = form.hd_date.data
            db_sess.commit()
            return redirect(f'/{current_user.id}')
        else:
            abort(404)
    return render_template('holiday.html', title='Редактирование праздника',
                           form=form)


# удаление праздника
@app.route('/holidays_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def holidays_delete(id):
    db_sess = db_session.create_session()
    hol = db_sess.query(Holidays).filter(Holidays.id == id, current_user.role_id == 1
                                         ).first()
    if hol:
        db_sess.delete(hol)
        db_sess.commit()
    else:
        abort(404)
    return redirect(f'/{current_user.id}')


# добавление роли
@app.route('/role', methods=['GET', 'POST'])
@login_required
def add_role():
    if current_user.role_id != 1:
        abort(404)

    form = RoleForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        role = Roles()
        role.title = form.title.data
        db_sess.add(role)
        db_sess.commit()
        return redirect(f'/{current_user.id}')

    return render_template('role.html', title='Добавление роли',
                           form=form)


# редактирование роли
@app.route('/role/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    form = RoleForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        role = db_sess.query(Roles).filter(Roles.id == id, current_user.role_id == 1
                                           ).first()
        if role:
            form.title.data = role.title
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        role = db_sess.query(Roles).filter(Roles.id == id, current_user.role_id == 1
                                           ).first()
        if role:
            role.title = form.title.data
            db_sess.commit()
            return redirect(f'/{current_user.id}')
        else:
            abort(404)
    return render_template('role.html', title='Добавление роли',
                           form=form)


# удаление роли
@app.route('/role_del/<int:id>', methods=['GET', 'POST'])
@login_required
def role_delete(id):
    db_sess = db_session.create_session()
    role = db_sess.query(Roles).filter(Roles.id == id, current_user.role_id == 1
                                       ).first()

    if role:
        db_sess.delete(role)
        db_sess.commit()
    else:
        abort(404)
    return redirect(f'/{current_user.id}')


def main():
    db_session.global_init("db/holidays.db")
    app.register_blueprint(api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
