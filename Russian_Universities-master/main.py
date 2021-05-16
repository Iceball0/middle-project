# импорт библиотек и модулей
import os
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_restful import abort, Api
from requests import get
from sqlalchemy.sql import func
from data import db_session, specialties_api, universities_api
from data.universities_specialties import Universities_Specialties
from data.universities import Universities
from data.specialties import Specialties
from data.reviews import Reviews
from data.news import News
from data.admins import Admin

# инициализация Flask и login manager
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'russian_universities_secret_key_1396'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    # инициализация базы данных
    db_session.global_init("db/universities.db")

    # нициализация api
    api.add_resource(specialties_api.SpecialtiesListResource, '/api/specialties')
    api.add_resource(specialties_api.SpecialtiesResource, '/api/specialties/<int:specialty_id>')

    api.add_resource(universities_api.UniversitiesListResource, '/api/universities')
    api.add_resource(universities_api.UniversitiesResource, '/api/universities/<int:university_id>')

    # запуск приложения
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.2', port=5000)


# загрузка аккаунта администратора
@login_manager.user_loader
def load_admin(admin_id):
    db_sess = db_session.create_session()
    return db_sess.query(Admin).get(admin_id)


# загрузка начальной страницы
@app.route("/", methods=['POST', 'GET'])
def index():
    db_sess = db_session.create_session()

    # проверка на POST запрос
    if request.method == 'POST':
        # перенаправление на главную страницу при попытке отправить POST запрос неавторизованным пользователем
        if not current_user.is_authenticated:
            return redirect("/")

        # если запрос был отправлен из формы добавления университета
        if 'add-submit' in request.form:
            # добавляем данные формы в БД
            university = Universities()
            university.name = request.form['title']
            university.description = request.form['description']
            university.city = request.form['city']
            university.placeInRussianTop = request.form['TopInRussia']

            # получаем файл картинки из формы, сохраняем и заносим название в БД
            f = request.files['photo']
            f.save(f'static/images/universities/{f.filename}')
            university.image = f.filename

            # добавляем все данные в БД, комитим и перенаправляем на главную страницу
            db_sess.add(university)
            db_sess.commit()
            redirect('/')

        # если запрос был отправлен из формы редактирования университета
        else:
            # получаем данные университета из БД по айди
            university = db_sess.query(Universities).filter(Universities.id == request.form['univ-id']).first()

            # если такой университет существует, то редактируем его, иначе вызываем ошибку 404
            if university:
                # редактируем данные, заменяя их на данные из формы
                university.name = request.form['title']
                university.description = request.form['description']
                university.city = request.form['city']
                university.placeInRussianTop = request.form['TopInRussia']

                # если был прикреплён файл картинки, то сохраняем её, удаляем прошлую и запоминаем название в БД
                if request.files['photo']:
                    f = request.files['photo']
                    os.remove(f'static/images/universities/{university.image}')
                    f.save(f'static/images/universities/{f.filename}')
                    university.image = f.filename

                # подтверждаем изменения и возвращаемся на главную страницу
                db_sess.commit()
                redirect('/')
            else:
                abort(404)

    # получаем список всех университетов, а также массивы из оценок и количества отзывов каждого из них
    all_universities = db_sess.query(Universities).all()
    ratings = [db_sess.query(func.avg(Reviews.rating)).filter(Reviews.university_id == item.id).first()[0]
               for item in all_universities]
    counts = [db_sess.query(func.count(Reviews.rating)).filter(Reviews.university_id == item.id).first()[0]
              for item in all_universities]

    # загружаем страницу и передаём все нужные данные
    return render_template('index.html', universities=all_universities, counts=counts, ratings=ratings)


# загрузка страницы отдельного вуза
@app.route("/universities/<int:university_id>", methods=['POST', 'GET'])
def university(university_id):
    # проверяем существование вуза по его айди и в случае успеха создаём сессию
    abort_if_university_not_found(university_id)
    db_sess = db_session.create_session()

    # проверка на POST запрос
    if request.method == 'POST':
        # перенаправление на страницу вуза при попытке отправить POST запрос неавторизованным пользователем
        if not current_user.is_authenticated:
            return redirect(f"/universities/{university_id}")

        # если запрос был отправлен из формы редактирования новостного раздела
        if 'edit-submit' in request.form:
            # получаем данные университета из БД по айди
            news_edit = db_sess.query(News).get(university_id)

            # если данные существуют, то редактируем их и сохраняем
            if news_edit:
                news_edit.url = request.form['url']
                news_edit.title = request.form['title']
                news_edit.image = request.form['image']
                if request.form['text'] == '-':
                    news_edit.text = ''
                else:
                    news_edit.text = request.form['text']
                news_edit.date = request.form['date']
                news_edit.news_url = request.form['news_url']
                db_sess.commit()
                redirect(f'/university/{university_id}')

            # если данные не существуют, то добавляем их и сохраняем
            else:
                news_add = News()
                news_add.university_id = university_id
                news_add.url = request.form['url']
                news_add.title = request.form['title']
                news_add.image = request.form['image']
                if request.form['text'] == '-':
                    news_add.text = ''
                else:
                    news_add.text = request.form['text']
                news_add.text = request.form['text']
                news_add.date = request.form['date']
                news_add.news_url = request.form['news_url']
                db_sess.add(news_add)
                db_sess.commit()
                redirect(f'/university/{university_id}')

        # если запрос был отправлен из формы добавления отзывов
        else:
            # добавляем отзыв в БД
            review = Reviews()
            review.user_name = request.form['name']
            review.text = request.form['opinion']
            review.rating = request.form['rating']
            review.university_id = university_id
            db_sess.add(review)
            db_sess.commit()
            redirect(f'/university/{university_id}')

    # получем данные университета и его новостей из БД, координаты из api поиска по орг, оценку вуза, и парсим новости
    university = db_sess.query(Universities).get(university_id)
    news_ = db_sess.query(News).get(university_id)
    coordinates = finder(university.name)
    if news_:
        news = parser(university_id)
        news_url = news_.url
        avg = db_sess.query(func.avg(Reviews.rating)).filter(Reviews.university_id == university_id).first()[0]
        if not avg:
            avg = 0
        else:
            avg = round(avg, 1)
    else:
        news = []
        avg = 0
        news_url = ''
    return render_template('university.html', university=university, avg=avg, news=news, news_url=news_url,
                           coordinates=coordinates, news_data=news_)


# загрузка страницы со специальностями
@app.route("/specialties", methods=['POST', 'GET'])
def specialties():
    # создание сессии
    db_sess = db_session.create_session()

    # проверка на POST запрос
    if request.method == 'POST':
        # перенаправление на страницу специальностей при попытке отправить POST запрос неавторизованным пользователем
        if not current_user.is_authenticated:
            return redirect("/specialties")

        # если запрос был отправлен из формы добавления специальности
        if 'add-submit' in request.form:
            # добавляем данные формы в БД
            specialty = Specialties()
            specialty.name = request.form['title']
            specialty.description = request.form['description']
            specialty.code = request.form['code']

            # получаем файл картинки из формы, сохраняем и заносим название в БД
            f = request.files['photo']
            f.save(f'static/images/specialties/{f.filename}')
            specialty.image = f.filename

            # добавляем все данные в БД, комитим и перенаправляем на страницу специальностей
            db_sess.add(specialty)
            db_sess.commit()
            redirect('/specialties')

        # если запрос был отправлен из формы редактирования специальности
        else:
            # получаем данные специальности из БД по айди
            specialty = db_sess.query(Specialties).filter(Specialties.id == request.form['spec-id']).first()

            # если такой специальность существует, то редактируем её, иначе вызываем ошибку 404
            if specialty:
                # редактируем данные, заменяя их на данные из формы
                specialty.name = request.form['title']
                specialty.description = request.form['description']
                specialty.code = request.form['code']

                # если был прикреплён файл картинки, то сохраняем её, удаляем прошлую и запоминаем название в БД
                if request.files['photo']:
                    f = request.files['photo']
                    os.remove(f'static/images/specialties/{specialty.image}')
                    f.save(f'static/images/specialties/{f.filename}')
                    specialty.image = f.filename

                # подтверждаем изменения и возвращаемся на страницу специальностей
                db_sess.commit()
                redirect('/specialties')
            else:
                abort(404)

    # получаем список всех специальностей, загружаем страницу и передаём все нужные данные
    all_specialties = db_sess.query(Specialties).all()
    return render_template('specialties.html', specialties=all_specialties)


# функция, проверяющая существование вуза и вызывающая 404 при его отсутствии
def abort_if_university_not_found(university_id):
    session = db_session.create_session()
    university = session.query(Universities).get(university_id)
    if not university:
        abort(404, message=f"University {university_id} not found")


# функция, проверяющая существование специальности и вызывающая 404 при её отсутствии
def abort_if_specialty_not_found(specialty_id):
    session = db_session.create_session()
    specialty = session.query(Specialties).get(specialty_id)
    if not specialty:
        abort(404, message=f"Specialty {specialty_id} not found")


# загрузка страницы с отдельной специально
@app.route("/specialties/<int:specialty_id>")
def specialty(specialty_id):
    # проверяем существование специальности по её айди и в случае успеха создаём сессию, получаем данные и загружаем стр
    abort_if_specialty_not_found(specialty_id)
    db_sess = db_session.create_session()
    specialty = db_sess.query(Specialties).get(specialty_id)
    return render_template('specialty.html', specialty=specialty)


# обработка формы авторизации
@app.route("/login", methods=['POST', 'GET'])
def login():
    # если пользователь уже авторизирован, то возвращаем его на главную страницу
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        # авторизируем пользователя
        db_sess = db_session.create_session()
        admin = db_sess.query(Admin).filter(Admin.login == request.form['login']).first()
        if admin and admin.check_password(request.form['password']):
            if request.form['remember']:
                remember = True
            else:
                remember = False
            login_user(admin, remember=remember)
            return redirect("/")
        else:
            return render_template('login.html',
                                   message="Неправильный логин или пароль")

    # загружаем страницу авторизации
    return render_template('login.html')


# обработка выхода из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# удаление вуза из БД
@app.route('/delete_university/<int:univ_id>', methods=['POST', 'GET'])
@login_required
def delete_univ(univ_id):
    db_sess = db_session.create_session()
    university = db_sess.query(Universities).get(univ_id)

    # если вуз существует то удаляем, иначе вызываем 404
    if university:
        # получаем все связанные с вузом специальности и удаляем связь с ними
        specialties = db_sess.query(Universities_Specialties).filter(Universities_Specialties.university_id == univ_id).all()
        if specialties:
            for i in specialties:
                db_sess.delete(i)
                db_sess.commit()

        # удаляем отзывы к вузу
        for i in university.reviews:
            db_sess.delete(i)

        # удаляем картинку
        os.remove(f'static/images/universities/{university.image}')

        # подтверждаем удаление
        db_sess.delete(university)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/")


# удаление специальности из БД
@app.route('/delete_specialty/<int:spec_id>', methods=['POST', 'GET'])
@login_required
def delete_spec(spec_id):
    db_sess = db_session.create_session()
    specialty = db_sess.query(Specialties).get(spec_id)

    # если специальность существует то удаляем, иначе вызываем 404
    if specialty:
        # получаем все связанные со специальностью вузы и удаляем связь с ними
        universities = db_sess.query(Universities_Specialties).filter(Universities_Specialties.specialty_id == spec_id).all()
        if universities:
            for i in universities:
                db_sess.delete(i)
                db_sess.commit()

        # удаляем картинку
        os.remove(f'static/images/specialties/{specialty.image}')

        # подтверждаем удаление
        db_sess.delete(specialty)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/specialties")


# парсер новостей
def parser(university_id):
    # получаем данные для парсера из БД
    session = db_session.create_session()
    news = session.query(News).get(university_id)

    try:
        # обращаемся к сайту, получаем данные, раскидываем по массивам и возвращаем всё
        r = get(news.url)
        soup = BeautifulSoup(r.text, 'html.parser')

        titles = []
        links = []
        texts = []
        dates = []
        images = []

        for link in soup.find_all(news.title.split()[0], class_=news.title.split()[1])[:5]:
            titles.append(link.text.strip())

        for link in soup.find_all(news.news_url.split()[0], class_=news.news_url.split()[1])[:5]:
            link2 = link.find('a', href=True)['href']
            if link2[0] != '/':
                link2 = f'/{link2}'
            links.append(link2)

        if len(news.image.split()) == 3:
            for link in soup.find_all(news.image.split()[0], class_=news.image.split()[1], style=True)[:5]:
                link2 = link['style'].split("url('")[1][:-2]
                images.append(link2)
        else:
            for link in soup.find_all(news.image.split()[0], class_=news.image.split()[1])[:5]:
                link2 = link.find('img', src=True)['src']
                images.append(link2)

        for link in soup.find_all(news.date.split()[0], class_=news.date.split()[1])[:5]:
            dates.append(' '.join(link.text.strip().split()))

        if news.text != '':
            for link in soup.find_all(news.text.split()[0], class_=news.text.split()[1])[:5]:
                texts.append(link.text.strip())

        url = news.url.split('/')[:3]

        news_li = []
        for i in range(5):
            dict1 = {'url': f"{url[0]}//{url[2]}", 'link': links[i], 'title': titles[i], 'image': images[i],
                     'text': texts[i], 'date': dates[i]}
            news_li.append(dict1)

        return news_li

    # в случае возникновения неполадок, отправляем пустой массив
    except Exception as e:
        print(e)
        return []


# олучаем координаты вуза по названию с api поиска по организациям
def finder(university_name):
    name = university_name.split()[:-1]

    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "cba79e6e-d6c1-4dd8-8f2c-d758602c9480"

    search_params = {
        "apikey": api_key,
        "text": ' '.join(name),
        "lang": "ru_RU",
        "type": "biz"
    }

    response = get(search_api_server, params=search_params)
    if not response:
        return []

    json_response = response.json()

    organization = json_response["features"][0]

    point = organization["geometry"]["coordinates"]
    return point


if __name__ == '__main__':
    main()
