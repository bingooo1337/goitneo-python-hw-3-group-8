from collections import UserDict, defaultdict
from datetime import datetime, timedelta


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
            updated_args[1] = datetime.strptime(
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

    def __str__(self):
        return self.value.strftime(Birthday.date_format)


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
        old = Phone(old_phone)
        for i, phone in enumerate(self.phones):
            if (phone.value == old.value):
                self.phones[i] = Phone(new_phone)

    def find_phone(self, phone):
        find = Phone(phone)
        for p in self.phones:
            if (p.value == find.value):
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        res = f"Contact name: {self.name.value}, phones: {
            '; '.join(p.value for p in self.phones)}"
        if (self.birthday != None):
            res += f", birthday {self.birthday}"
        return res


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        del self.data[name]

    def get_birthdays_per_week(self):
        users_to_congratulate_by_days = self._get_users_to_congratulate(
            self.data.values()
        )

        lines = []
        for day in sorted(users_to_congratulate_by_days.items()):
            lines.append(f'{day[0].strftime("%A")}: {", ".join(day[1])}')

        return '\n'.join(lines)

    def _get_users_to_congratulate(self, users: list[Record]):
        start = datetime.now().date()
        end = (start + timedelta(days=6))

        users_to_congratulate = defaultdict(list)
        for user in users:
            if (user.birthday == None):
                continue

            congratulation_day = self._get_congratulation_day(
                start,
                user.birthday.value.date()
            )

            if (start <= congratulation_day and congratulation_day <= end):
                users_to_congratulate[congratulation_day].append(
                    user.name.value
                )

        return users_to_congratulate

    def _get_congratulation_day(self, today, birthday):
        birthday_this_year = birthday.replace(year=today.year)

        congratulation_day = birthday_this_year

        # birthday will be next year
        if (birthday_this_year < today):
            congratulation_day = birthday_this_year.replace(
                year=today.year + 1)

        weekday = congratulation_day.weekday()
        # 4 - Friday index
        if (weekday > 4):
            # birthday is on weekend, congratulation on next work day
            congratulation_day = congratulation_day + \
                timedelta(days=7 - weekday)

        return congratulation_day


def main():
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("12.3.2000")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("10.3.1990")
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

    print(book.get_birthdays_per_week())

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == "__main__":
    main()
