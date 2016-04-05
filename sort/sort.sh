#!/bin/bash
IFS=$'\n'
pref=`date +"%d.%m.%y %H:%M"`

echo $pref "====== Начинаем работу ======" > logs.txt 

for i in    videos images documents music
do 
    mkdir -p "$i"
done

function wright_logs() {
    echo $pref "$1" >> logs.txt
}

echo
echo "====== Готов к работе! ======"

function what_to_do {
    wright_logs "  выбор действия"
    echo "  выберите действие:"
    echo "    1. открыть"
    echo "    2. переместить в правильный каталог"
    echo "    3. удалить"
    echo "    4. ничего не делать"
    echo "    5. завершить работу"
}

function move_file {
    case "$file" in
        *.avi|*.mp4|*.flv|*.wmv|*.mov)
            mv "$file" videos
            wright_logs "  перемещаю файл $file в папку видео"
            ;;
        *.jpg|*.jpeg|*.png|*.gif|*.bmp)
            mv "$file" images
            wright_logs "  перемещаю файл $file в папку изображения"
            ;;
        *.docx|*.djvu|*.txt|*.pdf|*.xlsx|*.pptx)
            mv "$file" documents
            wright_logs "  перемещаю файл $file в папку документы"
            ;;
        *.mp3|*.wav|*.flac|*.wma|*.aac)
            mv "$file" music
            wright_logs "  перемещаю файл $file в папку музыка"             
            ;;
    esac
}

function work_hard {
    read -n 1 ch
    echo
    case $ch in
        1)
            wright_logs "  открываю $file"
            open "$file"
            what_to_do
            work_hard
            ;;
        2)
            move_file
            ;;
        3) 
            rm -i "$file"
            wright_logs "  файл $file удален"
            ;;
        4)
            wright_logs "  ничего не делать"
            return 0
            ;;
        5)
            wright_logs "  работа прервана пользователем"
            break 
            ;;
    esac
}

for file in *
do
    if [ -f $file ] && [ $file != logs.txt ] && [ $file != sort.sh ]
    then
        eval $(stat -s $file)
        echo; echo "- $file | $st_size bytes" 
        wright_logs "- $file | $st_size bytes"
        what_to_do
        work_hard
    fi 
done
echo "===== Завершение работы ====="
wright_logs "===== Завершение работы ====="









