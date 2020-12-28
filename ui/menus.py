import imaplib, email, time, sys, json
from termcolor import colored
import art
import datetime as dt
import os
from datetime import timezone

#
sys.path.append('.')
from ui.colors import Style
from tools_functions.mail_functions import Mail


class Menu:
    timestamp = time.strftime('%H:%M:%S')
    separator = colored('----------------------------------------------------------------------', color='yellow')
    
    def __init__(self, instance):
        self.instance = instance

    def print_main_menu(self):
        sys.stdout.write(Style.RED)
        art.tprint('XntryScripts')
        sys.stdout.write(Style.RESET)
        print(f'{Menu.separator}\n')

    def set_defalut_menu(self):
        communicate_choice_status = colored('You selected Edit Defaults\n\n',color='yellow')
        print(communicate_choice_status)
        with open('user_settings/gmail_defaults.json') as f:
            data = json.load(f)
            f.close()
            set_json = True
        while set_json == True:
            change_email_json = input('Enter the email that you would like to use\n> ')
            change_password_json = input('Enter the password that you would like to use\n> ')
            if change_email_json:
                confirm_change_json = input('Are you sure you want to use the email '+change_email_json+' & password '+change_password_json+'? [1: Yes | 0: No]\n> ')
                if confirm_change_json == '1':
                    data["email_address"] = change_email_json
                    data["email_password"] = change_password_json
                    json_settings = open('user_settings/gmail_defaults.json','w')
                    json.dump(data,json_settings)
                    json_settings.close()
                    set_json = False
                else:
                    pass

        change_json_settings_success = colored('['+Menu.timestamp+']'+' Successfully Changed Defaults...',color='green')
        print(change_json_settings_success)
        time.sleep(1)
        import main
        main.main_wrapper()
        

    def gmail_start_mail_menu(self):
        with open('user_settings/gmail_defaults.json') as f:
            data = json.load(f)
            gmail_email_address = data["email_address"]
            gmail_email_password = data["email_password"]
        
            

        communicate_choice_status = colored('['+Menu.timestamp+']'+'You selected Mail Scripts\n',color='yellow')
        print(communicate_choice_status)
        gmail_mail_instance = Mail()
        
        try:
            print('['+Menu.timestamp+']'+' You Selected: '+gmail_email_address)
        
        except:
            setup_message = colored('Note: You don\'t have a default email set up, to avoid having to re-type your credentials set one up from the start menu',color='red')
            print(setup_message+'\n')
            gmail_email_address = input('Enter your email\n> ')
            gmail_email_password = input('\nEnter your password\n> ')
        
        gmail_mail_instance.get_mail_credentials(gmail_email_address,gmail_email_password,imap_url='imap.gmail.com')
    
    def outlook_start_mail_menu(self):
        with open('user_settings/outlook_defaults.json') as f:
            data = json.load(f)
            outlook_email_address = data["email_address"]
            outlook_email_password = data["email_password"]
        
            

        communicate_choice_status = colored('['+Menu.timestamp+']'+'You selected Mail Scripts\n',color='yellow')
        print(communicate_choice_status)
        outlook_mail_instance = Mail()
        
        try:
            print('['+Menu.timestamp+']'+' You Selected: '+outlook_email_address)
        
        except:
            setup_message = colored('Note: You don\'t have a default email set up, to avoid having to re-type your credentials set one up from the start menu',color='red')
            print(setup_message+'\n')
            outlook_email_address = input('Enter your email\n> ')
            outlook_email_password = input('\nEnter your password\n> ')
        
        outlook_mail_instance.get_mail_credentials(outlook_email_address,outlook_email_password,imap_url='outlook.office365.com')#mail.outlook.com or outlook.office365.com