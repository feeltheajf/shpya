from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import *
import json
import time
import re

app = Tk()
app.title("RSVP reader")
app.geometry("400x500")

MAX_LENGTH = 30
from_ = 50
to = 650
tick = 200
res = 50


class RSVP():
    pattern = re.compile(r"[\w.!?'""]+")
    words = []
    words_amount = 0
    count = 0
    delay = 0.6
    onscreen = 2
    text = StringVar()
    filename = ''
    flag = -1
    flag2 = 0
    mytime = time.time()
    data = {}

    def clean(self):
        progress_scale.set(0)
        self.flag = -1
        self.words = []
        self.words_amount = 0
        self.count = 0
        self.flag2 = 0

    def getsettings(self):
        f = open("settings.txt")
        tmp = f.read()
        f.close()
        if tmp == '':
            return
        tmp = json.loads(tmp)
        self.delay = tmp["delay"]
        self.onscreen = tmp["onscreen"]

    def savesettings(self):
        tmp = {"delay": self.delay, "onscreen": self.onscreen}
        tmp = json.dumps(tmp, sort_keys=True, default='utf8')
        f = open("settings.txt", 'w')
        f.write(tmp)
        f.close()

user = RSVP()
user.getsettings()

f = open('position.txt')
tmp = f.read()
f.close()
if tmp == '':
    user.data = {}
else:
    user.data = json.loads(tmp)


def loadPosition(event):
    if user.filename == '':
        return 1
    f = open('position.txt')
    tmp = f.read()
    f.close()
    if tmp == '':
        return 1
    user.data = json.loads(tmp)
    for key in user.data:
        if user.filename == key:
            user.count = user.data[key] - user.onscreen
            start()
            pause(event)
            return
    return 0


def savePosition(event):
    if user.filename == '':
        return
    user.data[user.filename] = user.count
    tmp = json.dumps(user.data, sort_keys=True, default='utf8')
    f = open("position.txt", 'w')
    f.write(tmp)
    f.close()


def default(event):  # для себя
    f = open("text1.txt")
    user.words = user.pattern.findall(f.read())
    f.close()
    user.filename = "text1"
    user.words_amount = len(user.words)

    if loadPosition(user) == 0:
        user.text.set("** файл загружен **")
    app.update_idletasks()


def loadFile():
    savePosition(user)
    f = Open(app, filetypes=[('*.txt files', '.txt')]).show()
    if f == '':
        return
    user.clean()
    i = f.rfind('/')
    j = f.rfind('.')
    user.filename = f[i+1:j]

    f = open(f)
    user.words = user.pattern.findall(f.read())
    f.close()
    user.words_amount = len(user.words)
    app.title("File: " + user.filename)
    if loadPosition(user) == 0:
        user.text.set("** файл загружен **")


def quit_button():
    if askyesno("Выход", "Вы действительно хотите выйти?"):
        savePosition(user)
        app.quit()


def about():
    showinfo("RSVP reader", "This is RSVP reader. \n\nbeta version: 0.01")


def start_pause(event):
    user.flag = -user.flag
    while user.flag > 0:
        if not user.words_amount:
            break
        start()
        app.update()
        time.sleep(user.delay)
    else:
        pause(event)


def start():
    if user.count < 0:
        user.count = 0
    if user.words_amount < user.count + 1:
        if user.flag2 == 0:
            user.count += user.onscreen
            user.flag2 = 1
        user.text.set("** конец текста **")
        progress_scale.set(100)
        pause(app)
        return
    elif user.count + user.onscreen + 1 > user.words_amount:
        tmp = user.words_amount
    else:
        tmp = user.count+user.onscreen
    show = ''
    for i in user.words[user.count:tmp]:
        if len(show + i) + 1 > MAX_LENGTH:
            break
        else:
            show += i + " "
    user.text.set(show)
    progress_scale.set(round((user.count + 1) / user.words_amount * 100))
    user.count += user.onscreen


def pause(event):
    user.flag = -1


def words_onscreen(event):
    tmp = user.onscreen
    if event.keycode == 1572925:  # равно (у меня + ставить не так удобно)
        onscreen_scale.set(onscreen_scale.get() + 1)
    elif event.keycode == 1769517:  # минус
        onscreen_scale.set(onscreen_scale.get() - 1)
    user.onscreen = onscreen_scale.get()
    if user.words_amount == 0:
        return
    user.count -= tmp
    start()


def change(event):
    if event.keycode == 8320768:  # стрелка вверх
        speed_scale.set(speed_scale.get() + res)
    elif event.keycode == 8255233:  # стрелка вниз
        speed_scale.set(speed_scale.get() - res)
    user.delay = round(60 / speed_scale.get(), 3)

    if user.words_amount == 0:
        return
    if event.keycode == 8124162:  # стрелка влево
        user.flag2 = 0
        if user.count - 2 * user.onscreen >= 0:
            user.count -= 2 * user.onscreen
        else:
            user.count = 0
        start()
    elif event.keycode == 8189699:  # стрелка вправо
        start()


def hotkeys():
    showinfo("Горячие клавиши",
             "\u00B7 Старт/пауза - пробел\n\u00B7 Ускорить/замедлить воспроизведение - стрелка вверх/вниз\n\u00B7 Предыдущий/следующий кадр - стрелка влево/вправо\n\u00B7 Открыть файл - клавиша 'o'\n\u00B7 Перемотка назад/вперед - '[' и ']' соответственно\n\u00B7 Сохранение позиции - клавиша 's'\n\u00B7 Загрузка позиции - клавиша 'l'")

textbox1 = Label(app, text='скорость \n(слов в минуту)',
                 width=25, height=4, font=("PT Mono", "12"))
textbox1.place(anchor='sw', relx=0, rely=0.9)
speed_scale = Scale(app, orient=HORIZONTAL, length=200, from_=from_,
                    to=to, tickinterval=tick, resolution=res, font=("PT Mono", "12"))
speed_scale.place(anchor='sw', relx=0.45, rely=0.9)
speed_scale.set(round(60 / user.delay, 0))

textbox2 = Label(app, text='количество слов\nна экране',
                 width=25, height=3, font=("PT Mono", "12"))
textbox2.place(anchor='sw', relx=0, rely=1)
onscreen_scale = Scale(app, orient=HORIZONTAL, length=200, from_=1, to=3,
                       tickinterval=1, resolution=1, showvalue='False', font=("PT Mono", "12"))
onscreen_scale.place(anchor='sw', relx=0.45, rely=1)
onscreen_scale.set(user.onscreen)

textbox3 = Label(
    app, text='прогресс\n(%)', width=25, height=2, font=("PT Mono", "12"))
textbox3.place(anchor='sw', relx=0, rely=0.78)

show_text = Label(
    app, textvariable=user.text, width=MAX_LENGTH, height=1, font=("PT Mono", "16"))
user.text.set("** выберите файл для чтения **")
show_text.place(anchor="center", relx=0.5, rely=0.3)


def myload(event):
    loadFile()
    return

progress_scale = Scale(app, orient=HORIZONTAL, length=200, from_=0, to=100,
                       tickinterval=25, resolution=1, showvalue='True', font=("PT Mono", "12"))
progress_scale.place(anchor='sw', relx=0.45, rely=0.8)
progress_scale.set(0)


def moveto(event):
    if user.words_amount == 0 or user.flag > 0:
        return
    if event.keycode == 1966173:
        progress_scale.set(progress_scale.get() + 1)
    elif event.keycode == 2162779:
        progress_scale.set(progress_scale.get() - 1)

    user.count = int(progress_scale.get() * user.words_amount / 100)
    user.flag = -1
    user.flag2 = 0
    start()
    if user.count - user.onscreen > 0:
        user.count -= user.onscreen
    else:
        user.count = 0
    pause(event)

app.bind("<space>", start_pause)
app.bind("<Key>", change)
app.bind("<minus>", words_onscreen)
app.bind("<equal>", words_onscreen)
app.bind("<FocusOut>", pause)
app.bind("<Key-d>", default)
app.bind("<Key-o>", myload)
app.bind("<Key-[>", moveto)
app.bind("<Key-]>", moveto)
app.bind("<Key-s>", savePosition)
app.bind("<Key-l>", loadPosition)

speed_scale.bind("<ButtonRelease>", change)
onscreen_scale.bind("<ButtonRelease>", words_onscreen)
progress_scale.bind("<ButtonRelease>", moveto)

m = Menu(app)
app.config(menu=m)

mm = Menu(m)
m.add_cascade(label="RSVP reader", menu=mm)
mm.add_command(label="О программе", command=about)
mm.add_command(label="Выход", command=quit_button)

fm = Menu(m)
m.add_cascade(label="Файл", menu=fm)
fm.add_command(label="Открыть...", command=loadFile)

hm = Menu(m)
m.add_cascade(label="Помощь", menu=hm)
hm.add_command(label="Горячие клавиши", command=hotkeys)


def quit(event):  # для себя
    user.savesettings()
    savePosition(event)
    #delta = time.time() - user.mytime
    #print("%.2f" % delta)
    app.quit()

app.bind("<Key-q>", quit)

app.resizable(False, False)
app.mainloop()
