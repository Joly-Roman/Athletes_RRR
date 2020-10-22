# испортируем модули стандартнй библиотеки uuid и datetime
import uuid
import datetime
from datetime import datetime, date, time

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

# создаем структуру таблицы
class User(Base):
	__tablename__ = "user"
	id = sa.Column(sa.INTEGER, primary_key=True)
	first_name = sa.Column(sa.TEXT)
	last_name = sa.Column(sa.TEXT)
	gender = sa.Column(sa.TEXT)
	email = sa.Column(sa.TEXT)
	birthdate = sa.Column(sa.TEXT)
	height = sa.Column(sa.REAL)

# структура таблицы атлетов
class Athlete(Base):
    __tablename__ = "athelete"
    id = sa.Column(sa.INTEGER, primary_key=True)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.Text)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()
# функция поиска пользователя 
def find_user(user_id):
    session=connect_db()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()
    return user
# функция поиска по росту
def find_by_height(user_height):
    session = connect_db()
    athletes = session.query(Athlete).filter(Athlete.height > 0).all()
    session.close()
    candidate = athletes[0]
    for athlete in athletes:
        candidate_diff = abs(candidate.height - user_height)
        athlete_diff = abs(athlete.height - user_height)
        if athlete_diff < candidate_diff:
            candidate = athlete
    return candidate

# высчитываем разность дат 
def date_diff(date_1, date_2):
    datetime_1 = datetime.strptime(date_1, "%Y-%m-%d")
    datetime_2 = datetime.strptime(date_2, "%Y-%m-%d")
    diff_time = abs(datetime_1 - datetime_2)
    return diff_time

def find_by_birthdate(user_birthdate):
    session = connect_db()
    athletes_1 = session.query(Athlete).all()
    session.close()
    candidate_1 = athletes_1[0]
    for athlete_1 in athletes_1:
        candidate_diff = date_diff(candidate_1.birthdate, user_birthdate)
        athlete_diff = date_diff(athlete_1.birthdate, user_birthdate)
        if athlete_diff < candidate_diff:
            candidate_1 = athlete_1
    return candidate_1

def main():
    user_id = int(input("Введите id пользователя: "))
    user = find_user(user_id)
    if user:
        athlete_close_height = find_by_height(user.height)
        print("Ближайший результат по росту: {} -- {}".format(athlete_close_height.name,
        athlete_close_height.height))
        athlete_close_birthdate = find_by_birthdate(user.birthdate)
        print("Ближайший результат по возрасту: {} -- {}".format(athlete_close_height.name,
        athlete_close_height.birthdate))
    else:
        print("Такого пользователя не существует")
if __name__=="__main__":
    main()


