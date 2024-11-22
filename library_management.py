import json
from typing import List, Dict, Any
import os


class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии") -> None:
        """Инициализация объекта книги.

        :param book_id: Уникальный идентификатор книги.
        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год выпуска книги.
        :param status: Статус книги (по умолчанию "в наличии").
        """
        self.book_id: int = book_id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование объекта книги в словарь для сериализации.

        :return: Словарь с данными книги.
        """
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }


class Library:
    def __init__(self) -> None:
        """Инициализация объекта библиотеки.

        Создает пустой список книг и устанавливает следующий доступный ID книги.
        """
        self.books: List[Book] = []
        self.next_id: int = 1

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавление новой книги в библиотеку.

        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год выпуска книги.
        """
        book = Book(self.next_id, title, author, year)
        self.books.append(book)
        self.next_id += 1



    def remove_book(self, book_id: int) -> None:
        """Удаление книги из библиотеки по идентификатору.

        :param book_id: Уникальный идентификатор книги для удаления.
        :raises ValueError: Если книга с указанным ID не найдена.
        """
        try:
            # Проверка наличия книги с указанным идентификатором.
            if len(self.books) == 0 or not any(book.book_id == book_id for book in self.books):
                raise ValueError("Книга с указанным ID не найдена.")
            self.books = [book for book in self.books if book.book_id != book_id]
        except Exception as e:
            print(f"Ошибка при удалении книги: {e}")

    def search_books(self, search_term: str) -> List[Book]:
        """Поиск книг по заданному термину.

        :param search_term: Строка для поиска по названию, автору или году выпуска.
        :return: Список книг, соответствующих критериям поиска.
        """
        results = [book for book in self.books if (search_term in book.title or
                                                   search_term in book.author or
                                                   search_term == str(book.year))]
        return results

    def display_books(self) -> None:
        """Вывод информации о всех книгах в библиотеке на экран."""
        for book in self.books:
            print(
                f"ID: {book.book_id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")

    def change_status(self, book_id: int, new_status: str) -> None:
        """Изменение статуса книги.

        :param book_id: Уникальный идентификатор книги.
        :param new_status: Новый статус книги.
        :raises ValueError: Если книга с указанным ID не найдена.
        """
        try:
            for book in self.books:
                if book.book_id == book_id:
                    book.status = new_status
                    return
            raise ValueError("Книга с указанным ID не найдена.")
        except Exception as e:
            print(f"Ошибка при изменении статуса книги: {e}")

    def save_to_file(self, filename: str) -> None:
        """Сохранение данных библиотеки в файл JSON.

        :param filename: Имя файла для сохранения.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f, indent=2, ensure_ascii=False)

    def load_from_file(self, filename: str) -> None:
        """Загрузка данных библиотеки из файла JSON.

        :param filename: Имя файла для загрузки.
        :raises FileNotFoundError: Если файл не найден.
        :raises json.JSONDecodeError: Если ошибка формата JSON.
        """

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                if not os.path.exists(filename) or os.stat(filename).st_size == 0:  # дополнительня проверка на то,
                    # что загружаемые данные не пустые
                    print("Библиотека пуста. Начинаем с пустой библиотеки.")
                    return
                self.books = [
                    Book(book_id=data['book_id'], title=data['title'], author=data['author'], year=data['year'],
                         status=data.get('status', "в наличии")) for data in json.load(f)]
                self.next_id = max(book.book_id for book in self.books) + 1 if self.books else 1
        except FileNotFoundError:
            print("Файл не найден.")
        except json.JSONDecodeError:
            print("Ошибка чтения файла. Пожалуйста, проверьте формат.")


def main_menu() -> None:
    """
    Главное меню для взаимодействия с библиотекой книг.
    """
    library = Library()
    library.load_from_file("library.json")

    while True:
        print("\n1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Сохранить и выйти")

        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            library.add_book(title, author, int(year))

        elif choice == '2':
            book_id = int(input("Введите ID книги для удаления: "))
            library.remove_book(book_id)

        elif choice == '3':
            search_term = input("Введите название или автора для поиска: ")
            results = library.search_books(search_term)
            for book in results:
                print(
                    f"Найдено - ID: {book.book_id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")

        elif choice == '4':
            library.display_books()

        elif choice == '5':
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input("Введите новый статус (в наличии/выдана): ")
            library.change_status(book_id, new_status)

        elif choice == '6':
            library.save_to_file("library.json")
            break

        else:
            print("Неверный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    main_menu()