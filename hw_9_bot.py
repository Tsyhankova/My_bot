import random


CONTACTS = {}

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
    },
    'actions':{
        'add': {
            'examples':['add', 'Could you add the name', 'Please, add the one name'],
            'responses':['OK', 'No problem', 'I got it']
        },
        'change': {
            'examples':['Change, please', 'change', 'Could you change', "Change contact"],
            'responses':['Yes, Sir', 'I can do it', 'Never give up']
        },
        'show': {
            'examples':['show all', 'Could you show all the contacts', 'Please, show all the contacts'],
            'responses':['OK', 'Look here', 'Sure', 'You got it']
        },
        'phone': {
            'examples':['Phone'],
            'responses':['Sure', 'I can do it', 'Of course']
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

def input_error(func):
    def inner_func(*args, **kwargs):
        try:
            func_action = func(*args)
            return func_action
        except KeyError:
            return "No contact with this name"
        except IndexError:
            return "Enter the name and contact, please: "
        except ValueError:
            return "Enter the name and contact, please: "
    return inner_func


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


def get_action(question):
    action_d = ['add', 'change', 'show', 'phone']
    for action, action_data in BOT_HANDLERS['actions'].items():
        for example in action_data['examples']:
            for i in action_d:
                if filter_text(question).find(filter_text(i)) != -1:
                    action = i
                    return action      
    

def get_answer_by_intent(intent):
    if intent in BOT_HANDLERS['intents']:
        phrases = BOT_HANDLERS['intents'][intent]['responses']
        return random.choice(phrases)


def get_answer_by_action(action, question):
    if action in BOT_HANDLERS['actions']:
        phrases = BOT_HANDLERS['actions'][action]['responses']
        print(random.choice(phrases))
        if action == 'show':
            return show_all_func()
        if action == 'phone':
            contact = question.split(action)[1]
            contact = contact.lstrip()
            return phone_func(contact)
        if action == 'add':
            contact = question.split(action)[1]
            contact = contact.lstrip()
            return add_func(contact)
        if action == 'change':
            contact = question.split(action)[1]
            contact = contact.lstrip()
            return change_func(contact)
         

def get_failure_phrase():
    phrases = BOT_HANDLERS['failure_phrases']
    return random.choice(phrases)


@input_error
def show_all_func():
    tabl = ''
    for name, phone in CONTACTS.items():
        tabl += f"{name}: {phone}\n"
    return tabl


@input_error
def phone_func(contact):
    name = contact.split(' ')[0]
    return f"{name}: {CONTACTS[name]}"


@input_error
def add_func(contact):
    name, phone = contact.split(' ')
    CONTACTS[name] = phone
    return  f'I have added {contact} to your contact book'


@input_error
def change_func(contact):
    name, phone = contact.split(' ')
    previous_number = CONTACTS[name]
    CONTACTS[name] = phone
    return  f'I have changed contact:{contact}. The previous number was: {previous_number}'


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


def main():
    question = None
    while question not in ['exit', 'that is all', 'bye', 'thank you', 'you are free', 'good bye']:
        question = input()
        answer = bot(question)
        print(answer)
    
    

if __name__ == "__main__":
    main()
    
