import imaplib, email, time, sys, json, re
from termcolor import colored
import art
import datetime as dt
import os
from datetime import timezone
#
sys.path.append('.')
from ui.colors import Style



class Mail():
    #GENERAL USE VARIABLES
    timestamp = time.strftime('%H:%M:%S')
    CHARSET = None

    #MESSAGES
    logging_in_error = colored('['+timestamp+']'+' Something went wrong', color='red')
    not_an_option = colored('['+timestamp+']'+' That is not an option...',color='red')
    #default message for after an error has occurred or your task is done
    def enter_to_contine():
        await_input = input('Press ENTER to continue...')
        if bool(await_input) == True:
            except_block = False

    inbox_options = {
            "INBOX":"INBOX",
            "SPAM":"[Gmail]/Spam",
            "SENT":"[Gmail]/Sent",
            "TRASH":'[Gmail]/Trash"',
            "DRAFTS":"[Gmail]/Drafts"
        }

    def init(self, email_name, email_password):

        self.email_name = email_name
        self.email_password = email_password

    def get_mail_credentials(self,user,password,imap_url):
        
        self.current_user = user
        self.current_password = password
        self.imap_url = imap_url
        self.login_to_email()
    
    def scrape_inbox(self):
        inbox_choice = input('Which inbox would you like to scrape?[1: Inbox | 2: Spam | 3: Trash | 4: Drafts | 5: Sent]\n> ')
        if inbox_choice == '1':
            self.selected_inbox = Mail.inbox_options["INBOX"]
        elif inbox_choice == '2':
            self.selected_inbox = Mail.inbox_options["SPAM"]
        elif inbox_choice == '3':
            self.selected_inbox = Mail.inbox_options["TRASH"]
        elif inbox_choice == '4':
            self.selected_inbox = Mail.inbox_options["DRAFTS"]
        elif inbox_choice == '5':
            self.selected_inbox = Mail.inbox_options["SENT"]
        try:
            self.inbox_found_status, inbox_length = self.login_session.select(self.selected_inbox)
            amount_of_mails = inbox_length[0]
            amount_of_mails = str(amount_of_mails)
            num_mails = re.search(r"\d+",amount_of_mails)
            sys.stdout.write(Style.CYAN)
            print(f'[{Mail.timestamp}] Found {num_mails.group()} emails in selected inbox')
            sys.stdout.write(Style.RESET)
            search_criteria = "FROM 'questions_en@footlocker.eu'"
            sys.stdout.write(Style.YELLOW)
            print(f'[{Mail.timestamp}] Scanning inbox')
            sys.stdout.write(Style.RESET)
            self.search_mail_status, self.amount_matching_criteria = self.login_session.search(Mail.CHARSET,search_criteria)
            
            if self.amount_matching_criteria == 0 or self.amount_matching_criteria == '0':
                print(f'[{Mail.timestamp}] No mails from that email address could be found...')
                Mail.enter_to_continue()
                import main
                main.main_wrapper()
            else:
                pattern = '(?P<url>https?://[^\s]+)'
                prog = re.compile(pattern)

                #message =str(individual_response_data[0][1])
                    
               #     print(prog.search(message).group("url"))

                self.amount_matching_criteria = self.amount_matching_criteria[0]
                self.amount_matching_criteria_str = str(self.amount_matching_criteria)
                num_mails = re.search(r"\d.+",self.amount_matching_criteria_str)
                num_mails = ((num_mails.group())[:-1]).split(' ')
    
                sys.stdout.write(Style.GREEN)
                print(f'[{Mail.timestamp}] Status code of {self.search_mail_status}')
                sys.stdout.write(Style.RESET)
                sys.stdout.write(Style.YELLOW)
                print(f'[{Mail.timestamp}] Found {len(num_mails)} emails')
                sys.stdout.write(Style.RESET)
                num_mails = self.amount_matching_criteria.split()
                for message_num in num_mails:
                    individual_response_code, individual_response_data = self.login_session.fetch(message_num, '(RFC822)')
                    message = email.message_from_bytes(individual_response_data[0][1])
                    if message.is_multipart():
                        print('multipart')

                        multipart_payload = message.get_payload()
                        for sub_message in multipart_payload:
                            string_payload = str(sub_message.get_payload())
                            print(prog.search(string_payload))
                    else:
                        print('not multipart')
                  
                    
                Mail.enter_to_contine()
                import main
                main.main_wrapper()
        except:
            print(Mail.logging_in_error)
            Mail.enter_to_contine()
            import main
            main.main_wrapper()

    def login_to_email(self):
        sys.stdout.write(Style.YELLOW)
        print(f'[{Mail.timestamp}] Logging into {self.current_user}...')
        try:
            self.login_session = imaplib.IMAP4_SSL(self.imap_url,993)
            self.login_session.login(self.current_user,self.current_password)
            sys.stdout.write(Style.RESET)
            sys.stdout.write(Style.GREEN)
            print(f'[{Mail.timestamp}] Successfully Logged in...')
            sys.stdout.write(Style.RESET)
            self.scrape_inbox()
        except:
            except_block = True
            print(Mail.logging_in_error)
            while except_block == True:
                
                view_settings = input('Would you like to check your login credentials? [1: Yes | 0: No]\n> ')
                if view_settings == '1':
                    with open('user_settings/defaults.json','r') as f:
                        check_credentials_file = f.read()
                        print(check_credentials_file)
                        Mail.enter_to_contine()
                        import main
                        main.main_wrapper()
                elif view_settings == '0':
                    import main
                    main.main_wrapper()
                else:
                    print(Mail.not_an_option)
                    pass
