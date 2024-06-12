from peewee import *

db = MySQLDatabase("cinema_db", host="localhost", port=3306, user="root", passwd="Tvg120181")


class BaseModel(Model):
    class Meta:
        database = db


class Client(BaseModel):
    name = CharField()
    phone = CharField(unique=True)


class Film(BaseModel):
    title = CharField(unique=True)
    description = CharField()


class View(BaseModel):
    client_id = ForeignKeyField(Client, backref='client')
    film_id = ForeignKeyField(Film, backref='film')
    date = DateField()


def select_all_clients() -> list:
    try:
        return list(Client.select().dicts())
    except Exception as ex:
        return [str(ex)]


def select_all_films() -> list:
    try:
        return list(Film.select().dicts())
    except Exception as ex:
        return [str(ex)]


def select_all_history() -> list:
    try:
        return [
            {'id': i.id, 'film_id': i.film_id.id, 'title': i.film_id.title, 'name': i.client_id.name, 'date': i.date}
            for i in View.select()]
    except Exception as ex:
        return [str(ex)]


def get_client_id(name: str) -> int:
    try:
        client_id = Client.get(Client.name == name)
        return client_id
    except Exception as ex:
        return str(ex)


def get_film_id(title: str) -> int:
    try:
        film_id = Film.get(Film.title == title)
        return film_id
    except Exception as ex:
        return str(ex)


def select_all_client_names() -> list:
    try:
        return list(Client.select(Client.name).dicts())
    except Exception as ex:
        return [str(ex)]


def select_all_film_titles() -> list:
    try:
        return list(Client.select(Client.name).dicts())
    except Exception as ex:
        return [str(ex)]


def delete_client(id_: int) -> bool | str:
    try:
        Client.delete_by_id(id_)
        return True
    except Exception as ex:
        return str(ex)


def delete_film(id_: int) -> bool | str:
    try:
        Film.delete_by_id(id_)
        return True
    except Exception as ex:
        return str(ex)


def delete_view_item(id_: int) -> bool | str:
    try:
        View.delete_by_id(id_)
        return True
    except Exception as ex:
        return str(ex)


def create_client_item(name: str, phone: str) -> bool | str:
    try:
        client = Client(name=name, phone=phone)
        client.save()
        return True
    except Exception as ex:
        return str(ex)


def create_film_item(title: str, description: str) -> bool | str:
    try:
        film = Film(title=title, description=description)
        film.save()
        return True
    except Exception as ex:
        return str(ex)


def create_view_item(client_id: int, film_id: int, date) -> bool | str:
    try:
        view = View(client_id=client_id, film_id=film_id, date=date)
        view.save()
        return True
    except Exception as ex:
        return str(ex)


def edit_view_item(item_id: int, client_id: int, film_id: int, date) -> bool | str:
    try:
        View.update(
            client_id=client_id,
            film_id=film_id,
            date=date
        ).where(View.id == item_id).execute()
        return True
    except Exception as ex:
        return str(ex)


def edit_film(film_id: int, title: str, description: str) -> bool | str:
    try:
        Film.update(
            title=title,
            description=description
        ).where(Film.id == film_id).execute()
        return True
    except Exception as ex:
        return str(ex)


def edit_client(client_id: int, name: str, phone: str) -> bool | str:
    try:
        Client.update(
            name=name,
            phone=phone
        ).where(Client.id == client_id).execute()
        return True
    except Exception as ex:
        return str(ex)


def create_db():
    db.connect()
    db.create_tables([Client, Film, View])


def main_db():
    create_db()


main_db()
