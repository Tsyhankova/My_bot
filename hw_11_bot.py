from collections import UserDict
from datetime import datetime
import re


class IncorrectInput(Exception):
    pass


class AttributeError(Exception):
    pass


class AddressBook(UserDict):
    def add_record(self, record):
        self.record = Record(self)
        self.data[record.name] = record  

    def __str__(self):
        record_line = ""
        for key, record in self.data.items():
            record_line += f'{str(record)}\n'
        return f'Address Book:\n{record_line}'

    def iterator(self, number):
        #возвращает генератор по записям AddressBook
        #и за одну итерацию возвращает представление для number записей
        record_line = ""
        start = 0
        for key, record in self.data.items():
            record_line = f'{str(record)}\n'
            print(record_line)
            start += 1
            if start == number:
                start = 0
                record_line = ""
        

class Record:
    record = dict()
    
    def __init__(self, name, *phones, birthday =None):
        self.name = Name(name)
        if birthday:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = None
        self.phones = Phone(list(phones))

    def add_phone(self, phone):
        self.phone = Record._phone_check(phone, phone)
        ph = self.phones
        ph.phones.append(self.phone)

    def remove_phone(self, phone):
        self.phone = Record._phone_check(phone, phone)
        ph = self.phones
        ph.phones.remove(self.phone)

    def change_phone(self, ind, phone):
        self.phone = Record._phone_check(phone, phone)
        ph = self.phones
        self.ind = ind - 1
        ph.phones[self.ind] = self.phone
        
    def _phone_check(self, phone):
        search_phone = re.match(Phone.PHONE, str(phone))
        if search_phone:
            phon = search_phone.group(0)
        else:
            raise IncorrectInput(f"Please, check how you enter the phone, right format is 'country code+number'") 
        phone = f'{phon}'
        return phone
       
    def days_to_birthday(self):
        if self.birthday == None:
            raise AttributeError ('This contact has no date of Birth in your book')
        current_datetime = datetime.now()
        bd = datetime.strptime(str(self.birthday), '%d/%m/%Y').date()
        if bd.month < current_datetime.month:
            delta_1 = datetime(year = current_datetime.year+1, month = bd.month, day = bd.day)
            difference = (delta_1 - current_datetime).days
        elif bd.month == current_datetime.month and bd.day <= current_datetime.day:
            delta_1 = datetime(year = current_datetime.year+1, month = bd.month, day = bd.day)
            difference = (delta_1 - current_datetime).days
        else:
            delta_1 = datetime(year = current_datetime.year, month = bd.month, day = bd.day)
            difference = (delta_1 - current_datetime).days
        return f"{self.name}`s birthday will be in {difference} days"
       
    def __str__(self):
        result = str(self.name)
        ph = self.phones
        for idx, phone in enumerate(ph.phones):
            result += f"\n{idx+1})+{phone}"
        return f'{result}\n'


class Field:
    def __init__(self, value):
        self.__value = value
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return self.__value
    

class Name(Field):
    def __init__(self, name):
        super().__init__(name)
        self.value = name


class Phone(Field):
    PHONE = re.compile(r'^\d{11}$')
    phones = list()
    
    def __init__(self, phones):
        self.phones = list(phones)
        for val in phones:
            super().__init__(val)

    @Field.value.setter
    def value(self, val):
        search_phone = re.match(self.PHONE, str(val))
        try:
            phone = search_phone.group(0)
        except AttributeError:
            raise IncorrectInput(f"Please, enter phone with country code") 
        self.__value = f'{phone}'
        

class Birthday(Field):
    
    def __init__(self, birthday):
        super().__init__(birthday)
        self.birthday = birthday
        
    @Field.value.setter
    def value(self, value):
        try:
            birthday = datetime.strptime(str(value), '%d/%m/%Y').date()
        except ValueError:
            raise IncorrectInput(f"Please, enter birthday in day/month/year format")
        self.__value = birthday
        return birthday




"""
a = AddressBook()


b = Record('Daniel','48575725504', '48123456789', birthday ='04/01/2006')
c = Record('Ania','48575725505', birthday ='27/02/2012')
d = Record('Ikar','48575725554', '48111111119', birthday ='07/05/1989')
e = Record('Tata','48575725500', birthday ='09/07/2000')
f = Record('Giz','48575720000', birthday =None)
#print(b)

a.add_record(b)
a.add_record(c)
a.add_record(e)
a.add_record(d)
a.add_record(f)

print(a)
"""


"""
b.change_phone(1, '48111111111')
print(b)
d.change_phone(1, '48555555555')
print(d)

b.add_phone('48333333333')
print(b)

b.remove_phone('48111111111')
print(b)


b.days_to_birthday()
print(b.days_to_birthday())
c.days_to_birthday()
print(c.days_to_birthday())
d.days_to_birthday()
print(d.days_to_birthday())
e.days_to_birthday()
print(e.days_to_birthday())

b = Birthday('04/01/2000')

print(b.value)

It = a.iterator(3)

print(It)
"""

