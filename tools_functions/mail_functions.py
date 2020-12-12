import imaplib, email, time, sys, json
from termcolor import colored
import art
import datetime as dt
import os
from datetime import timezone

sys.path.append('.')
from ui.colors import Style

def callback_func(callback):
        callback()

class Mail():
    timestamp = time.strftime('%H:%M:%S')
    logging_in_error = colored(timestamp+'Something went wrong', color='red')
    not_an_option = colored(timestamp+'That is not an option...',color='red')

    def init(self, email_name, email_password):

        self.email_name = email_name
        self.email_password = email_password

    def get_mail_credentials(self,user,password,imap_url):
        
        self.current_user = user
        self.current_password = password
        self.imap_url = imap_url
        self.login_to_email()
    
    def login_to_email(self):
        sys.stdout.write(Style.YELLOW)
        print(f'[{Mail.timestamp}] Logging into {self.current_user}...')
        try:
            login_session = imaplib.IMAP4_SSL(self.imap_url,993)
            login_session = login_session.login(self.current_user,self.current_password)
        except:
            exept_block = True
            while exept_block == True:
                print(Mail.logging_in_error)
                view_settings = input('Would you like to check your login credentials? [1: Yes | 0: No]\n> ')
                if view_settings == '1':
                    with open('user_settings/defaults.json','r') as f:
                        check_credentials_file = f.read()
                        print(check_credentials_file)
                        await_input = input('Press ENTER to continue...')
                        if await_input:
                            exept_block = False
                elif view_settings == '0':
                    import main
                    main.main_wrapper()
                else:
                    print(Mail.not_an_option)
                    pass
