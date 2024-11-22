import unittest
from library_management import Library


class TestLibrary(unittest.TestCase):

    def setUp(self):
        """Инициализация тестовой библиотеки перед каждым тестом."""
        self.library = Library()

    def test_add_book(self):
        """Тестирование добавления книги."""
        self.library.add_book("Test Book", "Test Author", 2024)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Book")

    def test_remove_book(self):
        """Тестирование удаления книги."""
        self.library.add_book("Book to Remove", "Author", 2023)
        self.assertEqual(len(self.library.books), 1)
        self.library.remove_book(1)
        self.assertEqual(len(self.library.books), 0)

    def test_search_books(self):
        """Тестирование поиска книг по названию и автору."""
        self.library.add_book("Searchable Book", "Searcher", 2020)
        results = self.library.search_books("Searchable")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Searchable Book")

    def test_change_status(self):
        """Тестирование изменения статуса книги."""
        self.library.add_book("Status Book", "Author", 2022)
        self.library.change_status(1, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_save_load_file(self):
        """Тестирование сохранения и загрузки библиотеки из файла."""
        self.library.add_book("File Book", "Author", 2021)
        self.library.save_to_file("test_library.json")

        new_library = Library()
        new_library.load_from_file("test_library.json")

        self.assertEqual(len(new_library.books), 1)
        self.assertEqual(new_library.books[0].title, "File Book")

    def tearDown(self):
        """Очистка после теста (удаление временного файла)."""
        import os
        try:
            os.remove("test_library.json")
        except OSError:
            pass


if __name__ == "__main__":
    unittest.main()
