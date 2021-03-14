from collections import UserDict


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    

class Record:
    def __init__(self, name, *phones):
        self.name = name
        self.phones = []
        for phone in phones:
            self.phones.append(phone)

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        for phone in self.phones:
            self.phones.remove(phone)

    def change_phone(self, ind, phone):
        self.ind = ind
        self.phones[self.ind] = phone

    def __str__(self):
        result = str(self.name)
        for idx, phone in enumerate(self.phones):
            result += f"\n{idx+1}){phone}"
        return result
    


class Field:
    pass

class Name(Field):
    pass


class Phone(Field):
    pass
