import sys

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QPushButton, QLabel, QWidget, QVBoxLayout, \
    QHBoxLayout, QFormLayout, QLineEdit, QDateTimeEdit, QSpinBox, QDialogButtonBox
from PyQt5.uic import loadUi

import models


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('ui/main_window.ui', self)
        self.setWindowTitle('Кинотеатр')

        self.clientsPushButton.clicked.connect(self.clients_callback)
        self.filmsPushButton.clicked.connect(self.films_callback)
        self.viewsPushButton.clicked.connect(self.views_callback)
        self.createPushButton.clicked.connect(self.create_callback)

        self.window_type = 'views'
        self.views_callback()

    def show_data(self):
        content = QWidget()
        area_layout = QVBoxLayout(content)
        self.scrollArea.setWidget(content)
        self.scrollArea.setWidgetResizable(True)

        data_functions = {
            'views': models.select_all_history,
            'films': models.select_all_films,
            'clients': models.select_all_clients
        }

        row_format = {
            'views': lambda row_: (
                f"id: {row_['id']}\nНазвание фильма: {row_['title']}\nИмя клиента: {row_['name']}\nДата: {row_['date']}"),
            'films': lambda row_: (
                f"id: {row_['id']}\nНазвание фильма: {row_['title']}\nОписание: {row_['description']}"),
            'clients': lambda row_: (f"id: {row_['id']}\nИмя: {row_['name']}\nТелефон: {row_['phone']}")
        }

        rows = data_functions[self.window_type]()
        for row in rows:
            current_id = row['id']
            data_text = row_format[self.window_type](row)
            data_label = QLabel(data_text)
            h_layout = QHBoxLayout()
            edit_button = QPushButton('Редактировать')
            delete_button = QPushButton('Удалить')

            match self.window_type:
                case 'clients':
                    name = row['name']
                    phone = row['phone']

                    edit_button.clicked.connect(lambda: self.edit_callback(name=name, phone=phone))
                    delete_button.clicked.connect(lambda: self.delete_callback(current_id))
                case 'films':
                    title = row['title']
                    description = row['description']

                    edit_button.clicked.connect(lambda: self.edit_callback(title=title, description=description))
                    delete_button.clicked.connect(lambda: self.delete_callback(current_id))
                case 'views':
                    film_title = row['title']
                    client_name = row['name']
                    date = row['date']

                    edit_button.clicked.connect(
                        lambda: self.edit_callback(client_name=client_name, film_title=film_title, date=date))
                    delete_button.clicked.connect(lambda: self.delete_callback(current_id))

            h_layout.addWidget(data_label)
            h_layout.addWidget(edit_button)
            h_layout.addWidget(delete_button)
            area_layout.addLayout(h_layout)

    def edit_callback(self, name=None, phone=None, client_name=None, film_title=None, date=None, title=None,
                      description=None):
        match self.window_type:
            case 'clients':
                add_dialog = AddWindow(self.window_type, name=name, phone=phone)
            case 'films':
                add_dialog = AddWindow(self.window_type, title=title, description=description)
            case 'views':
                add_dialog = AddWindow(self.window_type, client_name=client_name, film_title=film_title, date=date)
            case _:
                add_dialog = 'error'
        add_dialog.exec_()
        self.show_data()

    def clients_callback(self):
        self.window_type = 'clients'
        self.show_data()

    def films_callback(self):
        self.window_type = 'films'
        self.show_data()

    def views_callback(self):
        self.window_type = 'views'
        self.show_data()

    def delete_callback(self, id_: int):
        match self.window_type:
            case 'clients':
                models.delete_client(id_)
            case 'films':
                models.delete_film(id_)
            case 'views':
                models.delete_view_item(id_)
        self.show_data()

    def create_callback(self):
        add_dialog = AddWindow(self.window_type)
        add_dialog.exec_()
        self.show_data()


class AddWindow(QDialog):
    def __init__(self, window_type: str, name=None, phone=None, client_name=None, film_title=None, date=None,
                 title=None, description=None):
        super().__init__()

        if name is not None or film_title is not None or title is not None:

            match window_type:
                case 'clients':
                    loadUi('ui/add_client.ui', self)
                    self.nameLineEdit.setText(name)
                    self.phoneLineEdit.setText(phone)
                case 'films':
                    try:
                        loadUi('ui/add_film.ui', self)
                        self.titleLineEdit.setText(title)
                        self.descriptionLineEdit.setText(description)
                    except Exception as ex:
                        print(ex)
                case 'views':
                    loadUi('ui/add_view.ui', self)

                    films = [i['title'] for i in models.select_all_films()]
                    clients = [i['name'] for i in models.select_all_clients()]

                    self.namesComboBox.addItems(clients)
                    self.filmsComboBox.addItems(films)

                    self.namesComboBox.setCurrentIndex(clients.index(client_name))
                    self.filmsComboBox.setCurrentIndex(films.index(film_title))

                    self.dateEdit.setDate(date)
        else:

            match window_type:
                case 'clients':
                    loadUi('ui/add_client.ui', self)
                    self.buttonBox.accepted.connect(self.create_client)
                case 'films':
                    loadUi('ui/add_film.ui', self)
                    self.buttonBox.accepted.connect(self.create_film)
                case 'views':
                    loadUi('ui/add_view.ui', self)
                    films = [i['title'] for i in models.select_all_films()]
                    clients = [i['name'] for i in models.select_all_clients()]

                    self.namesComboBox.addItems(clients)
                    self.filmsComboBox.addItems(films)

                    today = QDate.currentDate()
                    self.dateEdit.setDate(today)
                    self.buttonBox.accepted.connect(self.create_view)

            self.buttonBox.rejected.connect(self.reject)

    def create_client(self):
        name = self.nameLineEdit.text()
        phone = self.phoneLineEdit.text()
        models.create_client_item(name, phone)

    def create_film(self):
        title = self.titleLineEdit.text()
        description = self.descriptionLineEdit.text()
        models.create_film_item(title, description)

    def create_view(self):
        name = self.namesComboBox.currentText()
        film = self.filmsComboBox.currentText()
        date = self.dateEdit.date().toPyDate()

        client_id = models.get_client_id(name)
        film_id = models.get_film_id(film)

        models.create_view_item(client_id, film_id, date)

    def edit_client(self):
        name = self.nameLineEdit.text()
        phone = self.phoneLineEdit.text()
        models.edit_film(name, phone)

    def edit_film(self):
        title = self.titleLineEdit.text()
        description = self.descriptionLineEdit.text()
        models.edit_film(title, description)

    def edit_view(self):
        name = self.namesComboBox.currentText()
        film = self.filmsComboBox.currentText()
        date = self.dateEdit.date().toPyDate()

        client_id = models.get_client_id(name)
        film_id = models.get_film_id(film)

        models.edit_view_item(client_id, film_id, date)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
