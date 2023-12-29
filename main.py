from collections import UserDict
from datetime import datetime
import json


class Field:
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return str(self.__value)
        
    def is_valid(self, value):
        return True
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self.__value = value


class Name(Field):
    pass


class Phone(Field):
    def is_valid(self, value):
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    def is_valid(self, value):
        return isinstance(value, datetime)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None


    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break

    def edit_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                break
        else:
            raise ValueError("The old phone number does not exist.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def days_to_birthday(self):
        if not self.birthday:
            return None
        next_birthday = datetime(datetime.now().year, self.birthday.value.month,
                                 self.birthday.value.day)
        if datetime.now() > next_birthday:
            next_birthday = datetime(datetime.now().year + 1, self.birthday.value.month,
                                     self.birthday.value.day)
        return (next_birthday - datetime.now()).days

    def __str__(self):
        return f"""Contact name: {self.name.value},
                    phones: {'; '.join(p.value for p in self.phones)}"""
    

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.current_page = 0

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, n):
        self.current_page = 0
        self.page_size = n
        while self.current_page < len(self.data):
            yield list(self.data.items())[self.current_page:self.current_page + self.page_size]
            self.current_page += self.page_size

    def save_to_file(self, filename='address_book.json'):
        with open(filename, 'w') as file:
            json.dump(self.data, file, default=lambda o: o.__dict__)

    def load_from_file(self, filename='address_book.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.data = {name: Record(**record_data) for name, record_data in data.items()}
        except FileNotFoundError:
            pass

    def search(self, query):
        results = []
        for record in self.data.values():
            if query.lower() in record.name.value.lower() or any(query in phone.value for phone in record.phones):
                results.append(record)
        return results
