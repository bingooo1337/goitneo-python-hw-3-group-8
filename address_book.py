from collections import UserDict
import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class InvalidPhoneException(Exception):
    def __init__(self):
        super().__init__("Phone number length should be 10")


def phone_validator(func):
    def inner(*args, **kwargs):
        if (len(args[1]) != 10):
            raise InvalidPhoneException
        return func(*args, **kwargs)
    return inner


class Phone(Field):
    @phone_validator
    def __init__(self, value):
        super().__init__(value)


class InvalidBirthDateFormatException(Exception):
    def __init__(self):
        super().__init__("Birthday should have format DD.MM.YYYY")


def birthday_validator(func):
    def inner(*args, **kwargs):
        updated_args = list(args)
        try:
            updated_args[1] = datetime.datetime.strptime(
                args[1],
                Birthday.date_format,
            )
        except ValueError:
            raise InvalidBirthDateFormatException
        return func(*updated_args, **kwargs)
    return inner


class Birthday(Field):
    date_format = "%d.%m.%Y"

    @birthday_validator
    def __init__(self, value):
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if (phone.value == old_phone):
                self.phones[i] = Phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if (p.value == phone):
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data[name]

    def delete(self, name):
        del self.data[name]


def main():
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("15.4.1990")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == "__main__":
    main()
