import random as r
import telegram
import time
import json
import copy

bot = telegram.Bot(token='###')

f = open('words.txt')
data = f.read()
f.close()
data = json.loads(data)
amount = len(data)
wkeys = list(data.keys())
wvalues = list(data.values())

chat_id = 0
right_ans = ''
answer = ''
text = ''
upd_id = 0
wlist = ''

bot_hello = ('Здравствуйте', 'Привет', 'Добро пожаловать',
             'Рад встрече', 'Рад вас видеть')
bot_bye = ('До свидания', 'Пока', 'Буду ждать вашего возвращения',
           'До новых встреч', 'Удачного дня')
bot_help = ('Чем я могу помочь?', 'Что вы хотите узнать?',
            'Могу ли я чем то помочь?')
bot_try = ('Начать игру?', 'Хотите попробовать?', 'Вы готовы?', 'Начнем?')
bot_continue = (
    'Продолжить?', 'Следующее слово?', 'Продолжим?', 'Хотите продолжить?')
bot_right = ('Верно!', 'Правильно!', 'Именно!', 'Вы правы!',
             'Точно!', 'Это правильный ответ!', 'Отлично!')
bot_wrong = (
    'К сожалению, вы не правы', 'Это неверный ответ', 'Неверно', 'Неправильно')
bot_unknown = ('Неизвестная команда', 'Извините, я не могу этого сделать',
               'Я еще не настолько умный', 'Что?')
bot_wait = ('Ищу словечко похитрее...', 'Сейчас что-нибудь подберем...',
            'Так-так...', 'Трясу словарь редких и забытых слов...')

man_hello = ('привет', '/start', '/start start')
man_bye = ('попрощаться', 'пока', 'нет', '/break', 'в другой раз')
man_game = ('игра', 'хочу играть', '/game', 'играть', 'да', 'конечно')
man_rules = ('правила', '/rules')
man_help = ('/help', 'помощь')
man_stats = ('статистика', '/stats')
man_reset = ('сброс', '/reset')
man_commands = ('команды', '/commands')
#================================================#=======================================#

players = {}


class Player():
    name = ''
    chat_id = 0
    word = ''
    right_ans = ''
    words = []
    defins = []
    wlist = []
    possible_points = 0
    points = 0

    def new_list(self):
        self.words = copy.copy(list(data.keys()))
        self.defins = copy.copy(list(data.values()))
        self.points = 0
        self.possible_points = 0

    def pop(self, word):
        try:
            self.words.remove(word)
        except ValueError:
            print('ValueError')

player = Player()


def send_mess(answer, kb):

    if kb == 'SURENO':
        custom_kb = [["Конечно", "В другой раз"]]
        reply = telegram.ReplyKeyboardMarkup(custom_kb)
    elif kb == 'check':
        custom_kb = [["Играть"], ["Попрощаться"]]
        reply = telegram.ReplyKeyboardMarkup(custom_kb)
    elif kb == 'rulescommands':
        custom_kb = [["Правила"], ["Команды"]]
        reply = telegram.ReplyKeyboardMarkup(custom_kb)
    else:
        reply = telegram.ReplyKeyboardHide()
    bot.sendMessage(chat_id=chat_id, text=answer, reply_markup=reply)


def start(player):
    send_mess(r.choice(bot_hello) + ", %s меня зовут TheBench! Я словесная игра, в которой вы можете попробовать угадать значения редкоупотребимых/устаревших слов!\n\nполучить помощь -> /help \n\n%s" %
              (tmp_player.name, r.choice(bot_try)), 'SURENO')


def end(player):
    if player.possible_points != 0:
        stats(player)
    send_mess(r.choice(bot_bye), 0)


def helpme():
    send_mess(r.choice(bot_help), 'rulescommands')


def rules():
    send_mess("Я предлагаю вам слово и три возможных дефиниции. За каждый правильный ответ вы получаете балл. Цель игры - набрать как можно больше баллов. На данный момент максимальное количество баллов: %i. Слова взяты из 'Словаря редких и забытых слов' В.П. Сомова \n\n%s" %
              (amount, r.choice(bot_try)), 'SURENO')


def commands():
    send_mess(
        "запустить бота - /start или 'привет' \nначать игру - /game или 'игра' / 'играть' \nпомощь - /help или 'помощь' \nправила игры - /rules или 'правила' \nпросмотреть статистику - /stats или 'статистика'\nсбросить статистику - /reset или 'сброс' \nзавершить игру - /break или 'пока' \n\nи, безусловно, вы можете пользоваться этими замечательными кнопками", 'check')


def stats(player):
    if player.possible_points == 0:
        send_mess("Вы еще не начали игру \n\n%s" %
                  (r.choice(bot_try)), 'SURENO')

    elif player.possible_points == amount:

        if player.points >= player.possible_points * 0.8:
            final_word = 'Блестящий результат!'

        elif player.points >= player.possible_points * 0.6:
            final_word = 'Превосходно!'

        elif player.points >= player.possible_points * 0.4:
            final_word = 'Достойный результат!'

        else:
            final_word = 'Неплохо!'

        send_mess("Игра окончена, ваш результат:  %i/%i \n\n%s \n\nХотите начать игру заново? Воспользуйтесь командой /reset ('сброс'). Учтите, текущий результат будет утерян" %
                  (tmp_player.points, tmp_player.possible_points, final_word), 0)

    else:
        send_mess("Ваш результат: %i/%i но игра еще не закончена" %
                  (player.points, player.possible_points), 0)


def reset(player):
    player.new_list()
    send_mess("Статистика сброшена", 0)

#================================================#=======================================#

tmp = 0
tmptext = ''

f = open('offset.txt')
off_set = f.read()
f.close()

while True:
    if text.lower() == 'выход':
        break

    updates = bot.getUpdates(offset=off_set)

    for update in updates[1:]:
        upd_id = update.update_id
        if tmp < upd_id:
            chat_id = update.message.chat_id
            f_name = update.message.chat.first_name
            if chat_id not in players.keys():
                tmp_player = Player()
                tmp_player.chat_id = chat_id
                tmp_player.new_list()
                tmp_player.name = f_name
                players[chat_id] = tmp_player

            tmp_player = players[chat_id]

            text = update.message.text
            tmptext = text.lower()

            # print(update)

            if tmptext == 'выход':
                send_mess("I`ll be back..", 0)

            elif text == tmp_player.right_ans:
                tmp_player.pop(tmp_player.word)
                tmp_player.possible_points += 1
                tmp_player.points += 1

                if tmp_player.possible_points == amount:
                    send_mess(r.choice(bot_right), 0)
                    stats(tmp_player)
                else:
                    send_mess(r.choice(bot_right) + '\n\n%s' %
                              (r.choice(bot_continue)), 'SURENO')

            elif text in tmp_player.wlist:
                tmp_player.possible_points += 1
                tmp_player.pop(tmp_player.word)

                if tmp_player.possible_points == amount:
                    send_mess(r.choice(bot_wrong), 0)
                    stats(tmp_player)
                else:
                    send_mess(r.choice(bot_wrong) + '\n\n%s - %s \n\n%s' %
                              (tmp_player.word, tmp_player.right_ans, r.choice(bot_continue)), 'SURENO')

            elif tmptext == '/stop':
                continue

            elif tmptext in man_hello:
                start(tmp_player)

            elif tmptext in man_help:
                helpme()

            elif tmptext in man_rules:
                rules()

            elif tmptext in man_commands:
                commands()

            elif tmptext in man_bye:
                end(tmp_player)

            elif tmptext in man_game:
                if tmp_player.possible_points == amount:
                    stats(tmp_player)
                else:
                    try:
                        tmp_player.word = r.choice(tmp_player.words)
                    except IndexError:
                        print('IndexError')

                    tmp_player.right_ans = data[tmp_player.word]
                    tmp_player.wlist = [tmp_player.right_ans]

                    answer = "\n\n%i/%i   " % (
                        tmp_player.possible_points + 1, amount) + tmp_player.word + "\n"

                    i = 0
                    while i < 2:
                        tmp = r.choice(tmp_player.defins)
                        if tmp not in tmp_player.wlist:
                            i += 1
                            tmp_player.wlist.append(tmp)

                    r.shuffle(tmp_player.wlist)

                    custom_kb = [
                        [tmp_player.wlist[0]], [tmp_player.wlist[1]], [tmp_player.wlist[2]]]
                    reply = telegram.ReplyKeyboardMarkup(custom_kb)
                    bot.sendMessage(
                        chat_id=chat_id, text=r.choice(bot_wait) + answer, reply_markup=reply)

            elif tmptext in man_stats:
                stats(tmp_player)

            elif tmptext in man_reset:
                reset(tmp_player)

            else:
                send_mess(r.choice(bot_unknown) + '\n\n%s' %
                          (bot_try[0]), 'SURENO')

            tmp = upd_id
        else:
            continue

    howmany = len(players)

    f = open('offset.txt', 'w')
    f.write("%i" % upd_id)
    f.close()
    time.sleep(1)

#================================================#=======================================#
