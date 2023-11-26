import sqlite3, os

class SQL:
    """Класс, отвечающий за коммуникацию с БД"""
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def add_question(self, question, answer):
        """Функция, которая добавляет новый вопрос"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `faq` (`question`, `answer`) VALUES(?,?)",
                (question, answer))

    def add_keys(self, key, number):
        """Функция, которая добавляет новые ключевые слова"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `keys` (`key`, `numbers`) VALUES(?,?)",
                (key, number))

    def update_number(self, key, new_number):
        list = self.get_number_from_keys(key)
        list.append(str(new_number))
        with self.connection:
            self.cursor.execute("UPDATE `keys` SET `numbers` = ? WHERE `key` = ?",
                                (' '.join(list), key))

    def get_number_from_keys(self, key):
        """Возвращает номер вопроса"""
        with self.connection:
            self.cursor.execute("SELECT `numbers` FROM `keys` WHERE `key` = ?", (key,))
            for res in self.cursor:
                return list(res)


    def update_answer(self, question, answer):
        """Функция, которая изменяет ответ на вопрос"""
        with self.connection:
            return self.cursor.execute("UPDATE `faq` SET `answer` = ? WHERE `question` = ?",
                                       (answer, question))

    def update_question(self, question, answer):
        """Функция, которая изменяет вопрос"""
        with self.connection:
            return self.cursor.execute("UPDATE `faq` SET `question` = ? WHERE `answer` = ?",
                                       (question, answer))

    def set_keywords(self, question, keywords):
        """Изменяет ключевые слова"""
        with self.connection:
            return self.cursor.execute("UPDATE `faq` SET `key_words` = ? WHERE `question` = ?", (keywords, question))

    def get_number(self, question):
        """Возвращает номер вопроса"""
        with self.connection:
            self.cursor.execute("SELECT `number` FROM `faq` WHERE `question` = ?", (question,))
            for res in self.cursor:
                return list(res)

    def dict_factory(self):
        """Возвращает массив, состоящий из ключевых слов"""
        self.connection.row_factory = sqlite3.Row
        self.cursor.execute("SELECT key, numbers  FROM keys")

        list_word = []
        for res in self.cursor:
           list_word.append(list(res))
        return list_word

    def find_key_word(self, word):
        with self.connection:
            self.cursor.execute("SELECT * FROM keys WHERE key = ?", (word,))
            for res in self.cursor:
                return list(res)

    def get_quest_for_number(self, number):
        """Возвращает вопрос по номеру"""
        with self.connection:
            self.cursor.execute("SELECT `question` FROM `faq` WHERE `number` = ?", (number,))
            for res in self.cursor:
                return res

    def get_answ_for_number(self, number):
        """Возвращает ответ по номеру"""
        with self.connection:
            self.cursor.execute("SELECT `answer` FROM `faq` WHERE `number` = ?", (number,))
            for res in self.cursor:
                return res

    # Блок обработки изображении
    def convert_to_binary_data(self, filename):
        """Преобразование данных в двоичный формат"""
        with open(filename, 'rb') as file:
            blob_data = file.read()
        return blob_data

    def insert_blob(self, photo, number_q):
        """Добавление изображения в таблицу faq"""
        with self.connection:
            sqlite_insert_blob_query = """UPDATE `faq` SET `photo` = ? WHERE `number` = ?"""

            emp_photo = self.convert_to_binary_data(photo)
            # Преобразование данных в формат кортежа
            data_tuple = (emp_photo, number_q)
            self.cursor.execute(sqlite_insert_blob_query, data_tuple)
            self.connection.commit()

    def write_to_file(self, data, filename):
        """Преобразование двоичных данных в нужный формат"""
        with open(filename, 'wb') as file:
            file.write(data)
        print("Данный из blob сохранены в: ", filename, "\n")

    def read_blob_data(self, num):
        """Вывод изображения из таблицы faq"""
        with self.connection:
            sql_fetch_blob_query = """SELECT * from faq where number = ?"""
            self.cursor.execute(sql_fetch_blob_query, (num,))
            record = self.cursor.fetchall()
            for row in record:
                photo = row[3]
                self.write_to_file(photo, "photo.jpg")

    def is_image(self, num):
        """Проверяет по номеру вопроса есть ли изображение"""
        with self.connection:
            self.cursor.execute("SELECT `photo` FROM `faq` WHERE `number` = ?", (num,))
            for res in self.cursor:
                return list(res)[0]

    # Блок закончен

    def close(self):
        """Закрывает базу данных"""
        self.connection.close()


