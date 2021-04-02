import random


def get_failure_phrase():
    phrases = BOT_HANDLERS['failure_phrases']
    return random.choice(phrases)


def filter_text(text):
    text = text.lower()
    text = [c for c in text if c in 'abcdefghijklmnopqrstuvyzxw']
    text = ''.join(text)
    return text


def get_intent(question):
    for intent, intent_data in BOT_HANDLERS['intents'].items():
        for example in intent_data['examples']:
            if filter_text(question) in filter_text(example):
                return intent


def get_answer_by_intent(intent):
    if intent in BOT_HANDLERS['intents']:
        phrases = BOT_HANDLERS['intents'][intent]['responses']
        return random.choice(phrases)


def get_action(question):
    action_d = ['showme', 'addcontact', 'changebirthday', 'addbirthday', 'changephone', 'showall', 'find', 'birthday', 'addphone', 'removephone', 'removecontact']
    for action, action_data in BOT_HANDLERS['actions'].items():
        for example in action_data['examples']:
            for i in action_d:
                if filter_text(question).find(filter_text(i)) != -1:
                    action = i
                    return action


BOT_HANDLERS = {
    'intents': {
        'hello': {
            'examples':['Hi', 'Hello'],
            'responses':['Hi. How could I help you?', 'Hello. What do you want, guy?', 'Good day. I ready to help you']
        },
        'bye': {
            'examples':['Bye', 'Exit', 'Thank you', "That`s all"],
            'responses':['Bye', 'Have a nice day', 'It was pleasure to help you']
        },
        'help': {
            'examples':['Help', 'need help', 'help me'],
            'responses':["""
My name is Addy and I am your AddressBook assistant.
I was created to help you fill out your address book.
The address book consists of the
contact's name, phone numbers, and the contact's birthday, for now.
Together, we can expand it.
Below you will find all the commands that I can perform for you:

1. show all - I'll show you the whole addressbook
2. show me {number} - I'll show you the {number} contacts from the addressbook
3. add contact John 44123456789 birthday=01/01/2000 - I'll add the new contact to you addressbook
4. add phone 48123456789 John - I'll add the new phone to the contact
5. add birthday John 01/01/2000 - I'll add birth day to the contact
6. remove contact John - I'll remove the contact with all data about him
7. remove phone 48123456789 John - I'll remove the phone from the contact
8. change phone John 1 48123456789 - I'll change the first phone of the contact on new one
9. change birthday John 01/01/2000 - I'll change birth day of the contact
10. birthday John - I'll show you - I'll show you in how many days the contact's birthday will be.
11. find {} - search through the contents of the contact book. I will show you all the
information about one or more users by a few digits of the phone number or letters of the name                       
                        """]
        },
    },
    'actions':{
        'addcontact': {
            'examples':['add contact', 'Could you add the name', 'Please, add the one name'],
            'responses':['OK', 'No problem', 'I got it']
        },
        'changephone': {
            'examples':['Change phone', 'change', 'Could you change phone'],
            'responses':['Yes, Sir', 'I can do it', 'Never give up']
        },
        'showall': {
            'examples':['show all', 'Could you show all the contacts', 'Please, show all the contacts'],
            'responses':['OK', 'Look here', 'Sure', 'You got it']
        },
        'phone': {
            'examples':['Phone'],
            'responses':['Sure', 'I can show it', 'Of course']
        },
        'find': {
            'examples':['find'],
            'responses':['Sure', 'I can find it', 'Of course']
        },
        'birthday': {
            'examples':['birthday'],
            'responses':['Just a second', 'Look below', 'Don`t forget about it']
        },
        'addphone': {
            'examples':['add phone'],
            'responses':['OK', 'No problem', 'I got it']
        },
        'removephone': {
            'examples':['Remove phone'],
            'responses':['OK', 'No problem', 'I got it']
        },
        'removecontact': {
            'examples':['Remove contact'],
            'responses':['OK', 'No problem', 'I got it']
        },
        'addbirthday': {
            'examples':['add birthday'],
            'responses':['OK', 'No problem', 'I got it']
        },
        'changebirthday': {
            'examples':['change birthday'],
            'responses':['OK', 'No problem', 'I got it']
        },
        'showme': {
            'examples':['show me', 'Could you show me some', 'Please, show me'],
            'responses':['OK', 'Look here', 'Sure', 'You got it']
        },
    },
    'failure_phrases': [
        "Could you repeat, please?",
        "I did not understand you",
        "Please, repeat one more time",
        "Could you rephrase, please?",
        "Иди погуляй с такими запросами",
        "Выспись",
        ]
    }



