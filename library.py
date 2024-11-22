import json
import os
from typing import List, Dict, Union

class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict[str, Union[int, str]]:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

class Library:
    def __init__(self, filename: str):
        self.filename = filename
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Загрузка книг из файла JSON."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.books = [
                        Book(book_id=book["id"], title=book["title"], author=book["author"], year=book["year"], status=book["status"]) 
                        for book in data
                    ]
            except (json.JSONDecodeError, ValueError):
                print("Ошибка: файл содержит некорректные данные. Создаётся новый файл.")
                self.books = []
        else:
            print("Файл не найден. Создаётся новый файл.")
            self.books = []

    def save_books(self):
        """Сохранение книг в файл JSON."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """Добавление новой книги в библиотеку."""
        book_id = len(self.books) + 1  # Генерация уникального ID
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга '{title}' добавлена в библиотеку.")

    def remove_book(self, book_id: int):
        """Удаление книги по ID."""
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с ID {book_id} удалена.")
                return
        print(f"Книга с ID {book_id} не найдена.")

    def search_books(self, query: str) -> List[Book]:
        """Поиск книг по заголовку, автору или году."""
        results = [book for book in self.books if query.lower() in book.title.lower() or
                   query.lower() in book.author.lower() or
                   query == str(book.year)]
        return results

    def display_books(self):
        """Отображение всех книг в библиотеке."""
        if not self.books:
            print("Библиотека пуста.")
            return
        for book in self.books:
            print(f"ID: {book.id}, Название: '{book.title}', Автор: '{book.author}', Год: {book.year}, Статус: '{book.status}'")

    def change_status(self, book_id: int, new_status: str):
        """Изменение статуса книги."""
        for book in self.books:
            if book.id == book_id:
                if new_status in ["в наличии", "выдана"]:
                    book.status = new_status
                    self.save_books()
                    print(f"Статус книги с ID {book_id} изменен на '{new_status}'.")
                else:
                    print("Неверный статус. Используйте 'в наличии' или 'выдана'.")
                return
        print(f"Книга с ID {book_id} не найдена.")

current_directory = os.path.dirname(os.path.abspath(__file__)) # Возварщает путь до папки со скриптом
json_file_path = os.path.join(current_directory, 'library.json') #  Возвращает путь до папки с json

def main():
    library = Library(json_file_path)

    while True:
        print("\n--- Управление библиотекой ---")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            while True:
                try:
                    year = int(input("Введите год издания: "))
                    break  # Выход из цикла, если ввод корректен
                except ValueError:
                    print("Пожалуйста, введите корректный год (число).")
            library.add_book(title, author, year)
        elif choice == '2':
            book_id = int(input("Введите ID книги для удаления: "))
            library.remove_book(book_id)
        elif choice == '3':
            query = input("Введите название, автора или год для поиска: ")
            results = library.search_books(query)
            if results:
                print("Найденные книги:")
                for book in results:
                    print(f"ID: {book.id}, Название: '{book.title}', Автор: '{book.author}', Год: {book.year}, Статус: '{book.status}'")
            else:
                print("Книги не найдены.")
        elif choice == '4':
            library.display_books()
        elif choice == '5':
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.change_status(book_id, new_status)
        elif choice == '6':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
