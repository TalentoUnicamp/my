from django.utils.crypto import get_random_string
import subprocess
from shutil import copyfile
import os


def ask_user(name, title, required, default=None, next_questions={}):
    print()
    print(f'{title} {"(Opcional)" if not required else ""}')
    if list(next_questions.keys()) != []:
        print(f'Opções: {list(next_questions.keys())}')
    if default is not None:
        default = str(default)
        print(f'Não digite nada para escolher "{default}"')
    answer = input(f'{name}: ')
    if required and next_questions != {}:
        while answer not in list(next_questions.keys()):
            print(f'{answer} deve estar em {list(next_questions.keys())}!')
            answer = input(f'{name}: ')
        for question in next_questions[answer]:
            process_question(question)
    if required and answer == '':
        if default is not None:
            answer = default
        while answer == '':
            print(f'{name} é obrigatório!')
            answer = input(f'{name}: ')
    return answer


def process_question(question):
    name = question['name']
    title = question['title']
    default = question.get('default', None)
    ask = question.get('ask', True)
    required = question.get('required', False)
    next_questions = question.get('next', {})
    value = default
    if ask:
        value = ask_user(name, title, required, default, next_questions)
    env_string = f'\n# {title}\n{name}={value}\n'
    with open(".env-temp", "a") as file:
        file.write(env_string)


def process_questions(questions):
    with open(".env-temp", "w+") as file:
        file.write('# Environment Variables\n')
    for question in questions:
        process_question(question)


env = [
    {
        'name': 'DEBUG',
        'title': 'Ativar modo de debug',
        'default': True,
        'ask': False
    },
    {
        'name': 'SECRET_KEY',
        'title': 'Chave privada de encriptação usada pelo Django',
        'default': get_random_string(32),
        'ask': False,
    },
    {
        'name': 'EMAIL_ACCOUNT',
        'title': 'Endereço de email para envio de logs de erro',
        'ask': True,
        'required': True
    },
    {
        'name': 'EMAIL_PASSWORD',
        'title': 'Senha do endereço de email',
        'ask': True,
        'required': True
    },
    {
        'name': 'ADMIN_ACCOUNT',
        'title': 'Conta de admin para receber logs de erro',
        'default': 'gustavomaronato@gmail.com',
        'ask': True,
        'required': True
    },
    {
        'name': 'ROOT_URL',
        'title': 'URL base do seu app',
        'default': 'localhost:8000',
        'ask': True,
        'required': True
    },
]


if __name__ == "__main__":
    try:
        process_questions(env)
        print()
        print("Salvar alterações? (s/n)")
        r = 'd'
        while r not in ['s', 'n']:
            r = input()
        if r == 's':
            print('Salvando...')
            copyfile('.env-temp', '.env')
    except KeyboardInterrupt:
        print('\n')
        print('Revertendo alterações...')
        pass
    os.remove('.env-temp')
    print()
    print('Migrando banco de dados...')
    print(subprocess.check_output(['python', 'manage.py', 'migrate']).decode("utf-8"))
