import imaplib, email, time, sys, json, re
from termcolor import colored
import art
import bs4
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
        self.link_set = set()
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
            self.substring_filter = str(input('Which substring filter would you like to search for?(CASE SENSITIVE)\n> '))
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
                self.link_set = set()
                pattern = '(?P<url>https?://[^\s]+)'
                prog = re.compile(pattern)

                self.amount_matching_criteria = self.amount_matching_criteria[0]
                amount_matching_criteria_str = str(self.amount_matching_criteria)
                num_mails = re.search(r"\d.+",amount_matching_criteria_str)
                num_mails = ((num_mails.group())[:-1]).split(' ')
    
                sys.stdout.write(Style.GREEN)
                self.timestamp = time.strftime('%H:%M:%S')
                print(f'[{self.timestamp}] Status code of {self.search_mail_status}')
                sys.stdout.write(Style.RESET)
                sys.stdout.write(Style.YELLOW)
                self.timestamp = time.strftime('%H:%M:%S')
                print(f'[{self.timestamp}] Found {len(num_mails)} emails')
                sys.stdout.write(Style.RESET)
                
                counter = 0
                self.start_time = time.time()
                sys.stdout.write(Style.MAGENTA)
                for message_num in self.amount_matching_criteria.split():
                    counter += 1
                    _, self.individual_response_data = self.login_session.fetch(message_num, '(RFC822)')
                    self.raw = email.message_from_bytes(self.individual_response_data[0][1])
                    raw = self.raw
                    self.scraped_email_value = email.message_from_bytes(Mail.scrape_email(raw))
                    self.scraped_email_value = str(self.scraped_email_value)
                    self.returned_links = prog.findall(self.scraped_email_value)
                  
                    for i in self.returned_links:
                        if self.substring_filter in i:
                            self.link_set.add(i)
                    self.timestamp = time.strftime('%H:%M:%S')
                    print(f'[{self.timestamp}] Links scraped: [{counter}/{len(num_mails)}]')
                sys.stdout.write(Style.RESET)
                self.end_time = time.time()
                self.time_taken = self.end_time - self.start_time
                sys.stdout.write(Style.YELLOW)
                self.timestamp = time.strftime('%H:%M:%S')
                print(f'[{self.timestamp}] Time taken:{self.time_taken}')
                sys.stdout.write(Style.RESET)
                self.write_to_text_file(self.link_set)
                Mail.enter_to_continue()
                import main
                main.main_wrapper()
        except Exception as e:
            print(e)
            print(Mail.logging_in_error)
            Mail.enter_to_continue()
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
                        Mail.enter_to_continue()
                        import main
                        main.main_wrapper()
                elif view_settings == '0':
                    import main
                    main.main_wrapper()
                else:
                    print(Mail.not_an_option)
                    pass
    
    def write_to_text_file(self,link_set):
        with open('out.txt','a') as f:
            for i in self.link_set:
                f.write(i+'\r')
            f.close()
        print(self.link_set)

    @staticmethod
    def scrape_email(raw):
        
        if raw.is_multipart():
            
            return Mail.scrape_email(raw.get_payload(0))
        else:
            return raw.get_payload(None,True)

    @staticmethod
    def enter_to_continue():
        await_input = input('Press ENTER to continue...')
        if bool(await_input) == True:
            except_block = False