import imaplib, email, time, sys
from termcolor import colored
import art
import datetime as dt
import os
from datetime import timezone
import multiprocessing

#
from ui.colors import Style
from ui.menus import Menu
from tools_functions.mail_functions import Mail

def start():
    options_exit = False
    menu.print_main_menu()
    WWYLTD = input('What would you like to do? [ 1: Start | 2: Manage Credentials | 0: Exit ]\n> ')
    if str(WWYLTD) == '0':
        options_exit = True
        while options_exit == True:
            check_choice = input('Are you sure [ 1:Yes | 0:No ]\n> ')
            if str(check_choice) == '1':
                sys.exit()
            elif str(check_choice) == '0':
                os.system('cls')
                start()
            else:
                check_choice = input('Please type a valid answer\n> ')
    elif str(WWYLTD) == '1':
        return 1
    elif str(WWYLTD) == '2':
        return 2

def main_wrapper():
    os.system('cls')
    global menu
    menu = Menu('main')
    start_running = start()
    if start_running == 1:
        sys.stdout.write(Style.YELLOW)
        which_provider = input('Which would you like to scrape? [ 1: Gmail | 2: Outlook ]\n> ')
        sys.stdout.write(Style.RESET)
        if which_provider == '1':
            menu.gmail_start_mail_menu()
        elif which_provider == '2':
            menu.outlook_start_mail_menu()
        else:
            sys.stdout.write(Style.RED)
            print('That is not an option...')
            sys.stdout.write(Style.RESET)
            os.system('cls')
            main_wrapper()
    elif start_running == 2:
        menu.set_defalut_menu()

if __name__ == '__main__':
    main_wrapper()
