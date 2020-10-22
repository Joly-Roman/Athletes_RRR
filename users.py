# испортируем модули стандартнй библиотеки uuid и datetime
import uuid
import datetime

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

   

def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Мне нужны сведения о тебе.")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    gender = input("Напиши мвой пол: Male-мужской,Female-женский,напиши свой:  ")
    birthdate = input("Также напиши свою дату рождения,в виде YYYY-MM-DD: ")
    height = input("На последок,мне нужен твой рост,ты знаешь,что делать :")
    # генерируем идентификатор пользователя и сохраняем его строковое представление
    user_id = (uuid.uuid4())
    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        gender=gender,
        birthdate=birthdate,
        height=height
    )
    # возвращаем созданного пользователя
    return user

def main():
    # Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    
    session = connect_db()
    # Запрашиваем даННые
    user = request_data()
    # ДОбавляем нового пользователя
    session.add(user)
    # СОхраняем все
    session.commit()
    print("Благодарю,данные сохранены!")
if __name__== "__main__":
	main()

