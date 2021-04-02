from collections import UserDict
from datetime import datetime
from helpers import BOT_HANDLERS, filter_text, get_intent, get_action, get_answer_by_intent, get_failure_phrase
from pathlib import Path
import pickle
import random
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

    def show_func(self, contact):
        Search_result = ""
        for key, value in self.data.items():
            act = re.search(str(contact.lower()), str(value).lower())
            if act:
                Search_result += f"Contact Name:\n{value}\n"
        if Search_result == "":
            return "Nothig has found"
        return Search_result

    def iterator(self, number):
        record_line = ""
        start = 0
        for key, record in self.data.items():
            record_line = f'{str(record)}\n'
            print(record_line)
            start += 1
            if start == number:
                print('done')
                start = 0
                record_line = ""

    def dump(self, path):
        path = "AddressBook.bin"
        with open(path, 'wb') as file:
            pickle.dump(self.data, file)
        

    def load(self, path):
        path = "AddressBook.bin"
        if Path(path).is_file():
            with open(path, 'rb') as file:
                self.data = pickle.load(file)
        else:
            print("You have not Address Book yet")


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

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

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
        bd = self.birthday
        for idx, phone in enumerate(ph.phones):
            result += f"\n{idx+1})+{phone}"
        result += f"\nBirthday: {bd}\n"
        return f'{result}'


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
    PHONE = re.compile(r'^\d{9,11}$')
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
            raise AttributeError(f"Please, enter phone with country code") 
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


def get_answer_by_action(action, question):
    if action in BOT_HANDLERS['actions']:
        phrases = BOT_HANDLERS['actions'][action]['responses']
        print(random.choice(phrases))
        if action == 'showall':
            return addressbook
        if action == 'showme':
            question = question.replace('show me', 'showme')
            contact = question.split(action)[1]
            number = contact.lstrip()[0]
            number = int(number)
            It = addressbook.iterator(number)
            return It
        if action == 'find':
            contact = question.split(action)[1]
            contact = contact.lstrip()
            return addressbook.show_func(contact)
        if action == 'addcontact':
            question = question.replace('add contact', 'addcontact')
            contact = question.split(action)[1]
            contact = contact.lstrip()
            contact = contact.split(' ')
            birthday = [i for i in contact if i[:8]=='birthday']
            if birthday:
                name, *phone = contact[0:-1]
                birthday = birthday[0][-10:]
                contact = Record(name, *phone, birthday = birthday)
                addressbook.add_record(contact)
                return f'I have added {contact}to your contact book'
            name, *phone = contact
            contact = Record(name, *phone, birthday = None)
            addressbook.add_record(contact)
            return f'I have added {contact}to your contact book'
        if action == 'changephone':
            question = question.replace('change phone', 'changephone')
            contact = question.split(action)[1]
            contact = contact.lstrip()
            name, ind, phone = contact.split(' ')
            phone = str(phone)
            ind = int(ind)
            for key, value in addressbook.data.items():
                act = re.search(str(name.lower()), str(value).lower())   
                if act:
                    value.change_phone(ind, phone)
                    return f'I have changed contact:{contact}'
            else:
                return f"Did not find the {contact}"
        if action == 'birthday':
            contact = question.split(action)[1]
            name = contact.lstrip()
            for key, value in addressbook.data.items():
                act = re.search(str(name.lower()), str(value).lower())
                if act:
                    return value.days_to_birthday()
            else:
                raise AttributeError ('This contact has no date of Birth in your book')
        if action == 'addphone':
            question = question.replace('add phone', 'addphone')
            contact = question.split(action)[1]
            contact = contact.lstrip()
            phone, name = contact.split(' ')
            for key, value in addressbook.data.items():
                act = re.search(str(name.lower()), str(value).lower())   
                if act:
                    value.add_phone(phone)
                    return f'I have added {phone} to {name}. Contact: {contact}'
            else:
                return f"Did not find the {name} in your addressbook"
        if action == 'removephone':
            question = question.replace('remove phone', 'removephone')
            contact = question.split(action)[1]
            contact = contact.lstrip()
            phone, name = contact.split(' ')
            for key, value in addressbook.data.items():
                act = re.search(str(name.lower()), str(value).lower())
                if act:
                    value.remove_phone(phone)
                    return f'I have removed {phone} from {name}. Contact: {contact}'
            else:
                return f"Did not find the {name} in your addressbook"
        if action == 'removecontact':
            question = question.replace('remove contact', 'removecontact')
            contact = question.split(action)[1]
            name = contact.lstrip()
            for key, value in addressbook.data.items():
                act = re.search(str(name.lower()), str(key).lower())
                if act:
                    addressbook.data.pop(key)
                    return f'I have removed\n{value}from your address book'
            else:
                return f"Did not find the {name} in your addressbook"
        if action == 'addbirthday' or action == 'changebirthday':
            action = action[0:-8]+' '+action[-8:]
            contact = question.split(action)[1]
            contact = contact.lstrip()
            name, birthday = contact.split(' ')
            for key, value in addressbook.data.items():
                act = re.search(str(name.lower()), str(value).lower())   
                if act:
                    value.add_birthday(birthday)
                    return f'Done, now Birthday: {birthday} added to {name}.'
            else:
                return f"Did not find the {name} in your addressbook"


def bot(question):
    intent = get_intent(question)
    action = get_action(question)

    # finding ready answer
    if intent:
        answer = get_answer_by_intent(intent)
        if answer:
            return answer
              
    answer = get_answer_by_action(action, question)
    if answer:
        return answer
    
    # any answer
    answer = get_failure_phrase()
    return answer


addressbook = AddressBook()

def main():
    
    question = None
    path = "AddressBook.bin"
    addressbook.load(path)
    print("Hello! Hope you are fine! Input help for get an instruction")
    while question not in ['exit', 'that is all', 'bye', 'thank you', 'you are free', 'good bye']:
        question = input()
        answer = bot(question)
        print(answer) 
    addressbook.dump(path)
        

if __name__ == "__main__":
    main()
