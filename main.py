from flask import Flask, render_template, request, redirect, jsonify, make_response
from forms.loginform import LoginForm
from forms.users import RegisterForm
from data import db_session, products_api
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_restful import Api
import product_resurs
from data.product import Product

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(products_api.blueprint)
    # для списка объектов
    api.add_resource(product_resurs.ProductResource, '/api/v2/product')

    # для одного объекта
    api.add_resource(product_resurs.ProductsListResource, '/api/v2/product/<int:product_id>')
    app.run()


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
    param[
        'photo1'] = 'https://sun9-35.userapi.com/impg/lJageeas3J5KmopnrOR3N6tr9MhbXuntT6BorQ/E4IT0I_SWfY.jpg?size=2160x2160&quality=96&sign=296e013d39bd74f6f1768729516267b9&type=album'
    param[
        'photo2'] = 'https://sun9-4.userapi.com/impg/paLn8HVzn2D5nryUFgdhbQOhRWqmpdr67mH6Qw/L3cQftEq4CU.jpg?size=2160x2160&quality=96&sign=811a5adbdccb735f8a6c269683f6f6fe&type=album'
    param[
        'photo3'] = 'https://sun9-27.userapi.com/impg/pRN4fn5X2E7kHLiMAhYUOhRMdKuNnEuJpGwEJA/jusn1-CMtig.jpg?size=2160x2160&quality=96&sign=cf0080d00104127eda83990582a4bb94&type=album'
    return render_template('product.html', title=param['name'], **param)


@app.route('/product_menu/topper')
@login_required
def topper():
    param = {}
    param['name'] = 'Топперы'
    param['price'] = '250₽'
    param[
        'about'] = 'Топперы — необычные сервировочные украшения: зубочистка или шпажка с надписью или картинкой на одном конце. Их применяют в основном для сладостей, тортов, пирожных и капкейков.'
    param[
        'photo1'] = 'https://sun9-29.userapi.com/impg/qGems9uQsmmsAYO1E-I6eaMDRRtzZDM9eaHOTQ/PEgNybtjZys.jpg?size=2160x2160&quality=96&sign=a8bdce7e43f4eaa0e1439581389a104c&type=album'
    param[
        'photo2'] = 'https://sun9-46.userapi.com/impg/_MBQ9ItKK1Xn_GLM-BeVzBBy0jyt0hgdPM-qmg/FNGVwiK2fkM.jpg?size=2160x2160&quality=96&sign=60973e6179aa2ebe1fb8236606fa2dcd&type=album'
    param[
        'photo3'] = 'https://sun9-21.userapi.com/impg/Ep-u9nB5WQ8A0EOZRaz__SuNehsGneXCNAl2lw/v6oRn9C6NGM.jpg?size=2160x2160&quality=96&sign=d7c72314053453fe21f1765dd9c472d0&type=album'
    return render_template('product.html', title=param['name'], **param)


@app.route('/product_menu/accessories')
@login_required
def accessories():
    param = {}
    param['name'] = 'Аксессуары и спортивная атрибутика'
    param['price'] = '100₽'
    param[
        'about'] = 'Аксессуар — необязательный предмет, сопутствующий чему-либо; принадлежность чего-либо. Может улучшить, украсить или дополнить что-либо.'
    param[
        'photo1'] = 'https://sun9-65.userapi.com/impg/sgLSYDZUtcrbTTAYSjtOJnnHgeomu5C4z3FBwQ/my5O00kcrbE.jpg?size=2160x2160&quality=96&sign=a7143747212cfc3cd7ccfc1b44493d35&type=album'
    param[
        'photo2'] = 'https://sun9-53.userapi.com/impg/grziop0qV27_jgBCjhAen9lB0GMJ8q4E7vTXqA/v2lJ52IoIKo.jpg?size=2160x2160&quality=96&sign=9396b17e750ac46144411e9e53b8561b&type=album'
    param[
        'photo3'] = 'https://sun9-63.userapi.com/impg/3vVB__LSt3x2Qx7oYbcyAk5Jwor7MCnXawnTzA/_9THuoJmuf0.jpg?size=2160x2160&quality=96&sign=7d60ba1aa8bcf3d13ac76775fa5a484a&type=album'
    return render_template('product.html', title=param['name'], **param)


@app.route('/product_menu/executiveoffice')
@login_required
def executiveoffice():
    param = {}
    param['name'] = 'Канцелярские товары'
    param['price'] = '400₽'
    param[
        'about'] = 'Канцелярские товары (канцтовары) — это изделия и принадлежности, используемые для переписки и оформления бумажной документации, учебы, творчества. Канцелярские товары составляют отдельную статью в расходах любого предприятия.'
    param[
        'photo1'] = 'https://sun9-15.userapi.com/impg/7-LDE4rUGD8NmOTQmD8REuGGg6QeLMKCRKeNnA/nNcgQTGQgqg.jpg?size=2160x2160&quality=96&sign=9afa2ff5539245490764067ceeb90ecf&type=album'
    param[
        'photo2'] = 'https://sun9-25.userapi.com/impg/o2650_uSsfz2d4yM_Vz4FI89YfY0PcVeziY7UA/3kXOsWYOc7g.jpg?size=2160x2160&quality=96&sign=941c509c48cb457fe257d29e4c0b017e&type=album'
    param[
        'photo3'] = 'https://sun9-8.userapi.com/impg/zWyjZB0v-ofU-lK_V-ca4HP98ShhXI5q6Q0fwA/WjgkJfOJUaA.jpg?size=2160x2160&quality=96&sign=e0d113897d28a5bd7bbbb0fcc0014d0a&type=album'
    return render_template('product.html', title=param['name'], **param)


@app.route('/product_menu/wedding')
@login_required
def wedding():
    param = {}
    param['name'] = 'Свадебная атрибутика'
    param['price'] = '800₽'
    param['about'] = 'Свадебная атрибутика — это важные части декора, которые сделают свадьбу незабываемой.'
    param[
        'photo1'] = 'https://sun9-62.userapi.com/impg/HKmZnDp66Kh37X6-6CWWnJvtfcw-Y13CFymv_Q/F4V63JZEelQ.jpg?size=2160x2160&quality=96&sign=d375e3a833061ce6f0f960e57dbad28b&type=album'
    param[
        'photo2'] = 'https://sun9-75.userapi.com/impg/yKw-b2rJpsOmHFy5w_hH51fZnmPNqJOfGC9tOA/Hg64jWb061U.jpg?size=2160x2160&quality=96&sign=b9436cf946d61add39a0df915ae4cada&type=album'
    param[
        'photo3'] = 'https://sun9-49.userapi.com/impg/74BaKfbNgIsXlF1yduUxxWns3f5RxnAk3TVH9A/88CKxuaYeGY.jpg?size=2160x2160&quality=96&sign=652d61095b86959c757693bf8253faf5&type=album'
    return render_template('product.html', title=param['name'], **param)


@app.route('/product_menu/watch')
@login_required
def watch():
    param = {}
    param['name'] = 'Часы'
    param['price'] = '800₽'
    param['about'] = 'Часы — это приборы для измерения текущего времени.'
    param[
        'photo1'] = 'https://sun9-8.userapi.com/impg/W9xquub8FzdDzbRjcKrAOlnms4uS-kwQJaLC3A/r-xVXQFfdVI.jpg?size=2160x2160&quality=96&sign=38e80db6bbad6312537dd6ce68bfad2b&type=album'
    param[
        'photo2'] = 'https://sun9-3.userapi.com/impg/7OMZyVz1aEd893VXIcaPgYQsPTnt1vgeQ6779w/ohk3wIWGDJs.jpg?size=2160x2160&quality=96&sign=b226422f3932e869f07a200229918551&type=album'
    param[
        'photo3'] = 'https://sun9-35.userapi.com/impg/l4ArqV-d906RCJ4CHaGApjrus5tAD0NoJg-ZsA/spmGgaClW68.jpg?size=2160x2160&quality=96&sign=189dc482f725e649948de8e823fd4b7f&type=album'
    return render_template('product.html', title=param['name'], **param)


@app.route('/product_menu/medallion')
@login_required
def medallion():
    param = {}
    param['name'] = 'Медальницы'
    param['price'] = '1200₽'
    param[
        'about'] = 'Медальницы — это особые держатели и всевозможные шкатулки, которые предназначены для хранения большого количества медалей, памятных знаков, символики и других атрибутов.'
    param[
        'photo1'] = 'https://sun9-62.userapi.com/impg/C52M3AbZSvVmhcTdCsp5n_24lvH82YKTfGjtoA/bfZ2VdljmQM.jpg?size=2160x2160&quality=96&sign=dceb3789b700a5d0ce2154f48c93ad73&type=album'
    param[
        'photo2'] = 'https://sun9-28.userapi.com/impg/Xt07rLOHD5A1SbKSD3wIzYITnTV-IPO9MSEF4g/07R3hm4VQy4.jpg?size=2160x2160&quality=96&sign=46ae4c6c7f8ff8acabe262cb4d966487&type=album'
    param[
        'photo3'] = 'https://sun9-57.userapi.com/impg/fJOpaYNKzx0mF0ER65N4Vr--FzzduX8pC96y_g/_niVCFb2omo.jpg?size=2160x2160&quality=96&sign=85aac44b909450d57c5b7f78febf8688&type=album'
    return render_template('product.html', title=param['name'], **param)


@app.route('/product_menu/box')
@login_required
def box():
    param = {}
    param['name'] = 'Шкатулки'
    param['price'] = '800₽'
    param[
        'about'] = 'Шкатулка — маленькая коробка или ящик обычно, но не всегда, в форме прямоугольного параллелепипеда, используемая для хранения драгоценностей, денег, бумаг и других мелких, но обычно ценных предметов.'
    param[
        'photo1'] = 'https://sun9-62.userapi.com/impg/R_aNiqWoAmOH3KNFB35OyB56VgupzS2UBOZ_Jw/-rj3z3JgwGo.jpg?size=2160x2160&quality=96&sign=da3d9f37bcfae1870a3beac30e0c79a7&type=album'
    param[
        'photo2'] = 'https://sun9-12.userapi.com/impg/_ZJvXMrFZTfSbnogiVmbNNY6LDd3BGRWJ8tMxA/WoSFLlQdBO4.jpg?size=2160x2160&quality=96&sign=c77c656d719c310992352ef71283730c&type=album'
    param[
        'photo3'] = 'https://sun9-42.userapi.com/impg/rQhah8Hs91Uws_1EFyifknmiM8FxiGJiZz3K4Q/EKhxzMg-G0I.jpg?size=2160x2160&quality=96&sign=24283f18e960774aed5b1160cb51015a&type=album'
    return render_template('product.html', title=param['name'], **param)


@app.route('/product_menu/tablet')
@login_required
def tablet():
    param = {}
    param['name'] = 'Таблички на дом'
    param['price'] = '600₽'
    param[
        'about'] = 'Табличка на дом — это не только показатель адреса вашего дома, но и его украшение.'
    param[
        'photo1'] ='https://sun9-76.userapi.com/impg/7EbGXPA-CsBl6LXMFeC6xzKsAf6AR6Wnz0psrg/b8ySQGcqCMc.jpg?size=2160x2160&quality=96&sign=cae9ab7b819259946147d89ce9f8dc75&type=album'
    param[
        'photo2'] = 'https://sun9-15.userapi.com/impg/ufpzDC77kr_Ky1RATvh7kgmZfACIRQMDXKlkSA/Ybw8o_U2bew.jpg?size=2160x2160&quality=96&sign=749f48e162e74940ea6659c0bad5498e&type=album'
    param[
        'photo3'] = 'https://sun9-17.userapi.com/impg/6A6gD1JNsxai7zbFbg9P4f_1fB5TMeKXDm93zw/jEKaiw36Ekg.jpg?size=2160x2160&quality=96&sign=970fcbce329300284d5629ae1fe0b6e9&type=album'
    return render_template('product.html', title=param['name'], **param)


@app.route('/product_menu/photoframe')
@login_required
def photoframe():
    param = {}
    param['name'] = 'Фоторамки'
    param['price'] = '2500₽'
    param[
        'about'] = 'Фоторамки — это не только приспособление для демонстрации фотографий, но и часть декора.'
    param[
        'photo1'] = 'https://sun9-36.userapi.com/impg/In-Xn2Z0_f6-tb2VF4cwNKP65C20HBZnj_15Wg/s9htDjQkPN0.jpg?size=2160x2160&quality=96&sign=7a9e9b23be6be49b8b7474a41f2f4376&type=album'
    param[
        'photo2'] = 'https://sun9-66.userapi.com/impg/3ElZ5i9321x6KqoUx5j-CuBiheOoXLTZru6o2Q/dMwYpiwHea0.jpg?size=2160x2160&quality=96&sign=e6ace99eba451487811415567b080076&type=album'
    param[
        'photo3'] = 'https://sun9-57.userapi.com/impg/JkspwChgSORDNcr4ceHI3dsmdRbp1kJaUNk0GQ/dxF0v4RiPXo.jpg?size=2160x2160&quality=96&sign=bc8d1d19cda81ee6c3b87df6a60fad3e&type=album'
    return render_template('product.html', title=param['name'], **param)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    main()
