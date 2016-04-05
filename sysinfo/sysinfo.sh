#!/bin/bash

function show_menu(){
    clear
    echo "Hello, $USER!"
    write_head $(date)
    write_head  What Do You Want To Know?
    echo 1  Load Averages 
    echo 2  Proccesses
    echo 3  Uptime
    echo 4  Last logged users
    echo 5  Active Services
    echo 6  Network
    echo 7  CPU, RAM, Hard Disks
    echo 0  Exit
}

function pause(){
    local b="$@"
    echo
    [ -z $b ] && b="Press any key to continue..."
    read -n 1 -p "$b" key
}

function write_head(){
    local h="$@"
    echo 
    echo "  $h"
    echo
}
function write(){
    local h="$@"
    echo "$h"; echo
}

function load_avg(){
    uptime | grep -o 'load averages.*' | cut -c 16-50
}

function proc_inf(){
    top -l 1 | grep ^CPU; echo  
    ps aux                                   
}

function act_serv(){
    for i in apache nginx mysql ssh
    do
        local is_act="$(ps -A|grep $i|wc -l)"
        if [[ $is_act -eq 1 ]]; then  #вообще должен быть -eq 0, 
            # но если запускать на своей же машине, получается 
            # есть процесс grep $i => неверный результат
            echo "$i is not running"
        else
            echo "$i is running"
        fi
    done
}

function net_info(){
    local dnsips=$(sed -e '/^$/d' /etc/resolv.conf | awk '{if (tolower($1)=="nameserver") print $2}')
    echo "- Hostname: $(hostname -s)"
    echo "- DNS domain: $(hostname)"
    echo "- Network address (IP): $(ifconfig | grep 'inet ' | grep -v 127.0.0.1 | cut -d ' ' -f2)"
    echo "- DNS name servers (DNS IP): ${dnsips}"
    echo "- Active internet connections: "; echo
    netstat | grep tcp4
}

function mem_info(){
    write - CPU:
    write $(top -l 1 | grep ^CPU)
    write - RAM:
    write $(top -l 1 | grep ^PhysMem)
    write - Hard Disks:
    df -mH
}

function read_input(){
    local b; local ch; local t=0; local m=1 
    echo; read -n 1 -p "Enter Your Choice [0-7]: " ch; echo
    case $ch in
        1) write_head " Load Averages "         ; load_avg  ;;
        2) write_head " Active Proccesses "     ; proc_inf  ;;
        3) write_head " Uptime Information "    ; uptime    ;; 
        4) write_head " Last logged users "     ; last      ;; 
        5) write_head " Active Services "       ; act_serv  ;; 
        6) write_head " Network information "   ; net_info  ;;
        7) write_head " CPU, RAM, Hard Disks "  ; mem_info  ;;
        0) clear; echo; write Good Bye, $USER!  ; exit 0    ;;
        *) echo "Inappropriate Choice"          ; read_input
    esac
    echo
    read -n 1 -p "Turn auto-update on? y/n (exit - ^C): " b ; echo
    case $b in
        "n") ((m=b-1)); echo "Auto-update off";;
        "y") ((b=1))  ; echo "Auto-update on" ; read -p "Number of repetitions: " m 
             read -p "Frequency (sec): " t; echo ;;
        *)   ((m=b-1)); echo "Auto-update off"
    esac    
    while (("$b" <= "$m"))
    do  
        echo
        ((b=b+1))
        case $ch in
            1) load_avg ;; 
            2) proc_inf ;;
            3) uptime   ;;
            4) last     ;;
            5) act_serv ;;
            6) net_info ;;
            7) mem_info ;;
        esac
        sleep $t
    done                                     
    pause
}

while true
    do
    show_menu 
    read_input 
done



