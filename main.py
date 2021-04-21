from flask import Flask, render_template, request, redirect
from forms.loginform import LoginForm
from forms.users import RegisterForm
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user

db_session.global_init("db/blogs.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def start():
    return render_template('start.html')


@app.route('/registration', methods=['GET', 'POST'])
def register():
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
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/product_menu")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/product_menu')
@login_required
def shop():
    return render_template('shop.html', title='Магазин "Home Workshop"')


@app.route('/product_menu/hanger')
@login_required
def hanger():
    param = {}
    param['name'] = 'Вешалки'
    param['price'] = '500₽'
    param['about'] = 'Вешалка (также плечики, тремпель) — приспособление для хранения одежды в подвешенном состоянии.'
    param['photo1'] = 'https://sun9-35.userapi.com/impg/lJageeas3J5KmopnrOR3N6tr9MhbXuntT6BorQ/E4IT0I_SWfY.jpg?size=2160x2160&quality=96&sign=296e013d39bd74f6f1768729516267b9&type=album'
    param['photo2'] = 'https://sun9-4.userapi.com/impg/paLn8HVzn2D5nryUFgdhbQOhRWqmpdr67mH6Qw/L3cQftEq4CU.jpg?size=2160x2160&quality=96&sign=811a5adbdccb735f8a6c269683f6f6fe&type=album'
    param['photo3'] = 'https://sun9-27.userapi.com/impg/pRN4fn5X2E7kHLiMAhYUOhRMdKuNnEuJpGwEJA/jusn1-CMtig.jpg?size=2160x2160&quality=96&sign=cf0080d00104127eda83990582a4bb94&type=album'
    return render_template('product.html', **param)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
