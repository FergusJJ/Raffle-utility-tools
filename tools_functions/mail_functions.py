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
            #search_criteria = input('Type In the email address you would like to scrape from\n> ')
            #search_criteria = f"FROM '{search_criteria.strip()}'"
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
                #want to see if i can store the emails in fetched form so i dont have to call them each time
                MESSAGES_ARRAY = []
                for message_num in self.amount_matching_criteria.split():
                    _, self.individual_response_data = self.login_session.fetch(message_num, '(RFC822)')
                    MESSAGES_ARRAY.append(self.individual_response_data)
                    sys.stdout.write(Style.MAGENTA)
                    print(message_num)
                    print(len(MESSAGES_ARRAY))
                    sys.stdout.write(Style.RESET)
                    
                print(MESSAGES_ARRAY)
                #
                self.start_time = time.time()

                #1 task
                sys.stdout.write(Style.MAGENTA)
                #out is the file which will have links, c has completed tasks
                with open('out.txt','a') as f:
                    with open('completed.txt','a+') as c:
                        found_in_line  = False
                        for message_num in self.amount_matching_criteria.split():
                            message_num_check = str(message_num)

                            
                            
                            counter += 1
                            #individual res data is the raw response which is turned in a readable message with mail.scrape_email
                            _, self.individual_response_data = self.login_session.fetch(message_num, '(RFC822)')
                            #skips the email if it is areadly scraped, also gives us a way to save between sessioons
                            
                            
                            with open('completed.txt','r') as completed_check:
                                for line in completed_check:
                                    if message_num_check in line:
                                        found_in_line = True
                                        self.timestamp = time.strftime('%H:%M:%S')
                                        print(f'[{self.timestamp}] AlREADY SCRAPED')
                                        
                                    else:
                                        found_in_line = False
                                        
                                    

                                
                                
                                                
                                #the b turns \r into byte form so it can be concatenated
                                if found_in_line != True:
                                    c.write(message_num_check)
                                    self.raw = email.message_from_bytes(self.individual_response_data[0][1])
                                    raw = self.raw
                                    self.scraped_email_value = email.message_from_bytes(Mail.scrape_email(raw))
                                    self.scraped_email_value = str(self.scraped_email_value)
                                    self.returned_links = prog.findall(self.scraped_email_value)
                  
                                    for i in self.returned_links:
                                        if self.substring_filter in i:
                                            f.write(i+'\r')
                                #self.link_set.add(i)
        
                                    self.timestamp = time.strftime('%H:%M:%S')
                                    sys.stdout.write(Style.GREEN)
                                    print(f'[{self.timestamp}] Links scraped: [{counter}/{len(num_mails)}]')
                    
                                    sys.stdout.write(Style.RESET)

                        c.close()
                    f.close()
                #end of task
                self.end_time = time.time()
                self.time_taken = self.end_time - self.start_time
                sys.stdout.write(Style.YELLOW)
                self.timestamp = time.strftime('%H:%M:%S')
                print(f'[{self.timestamp}] Time taken:{self.time_taken}')
                sys.stdout.write(Style.RESET)
                #self.write_to_text_file(self.link_set)
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
    
#    def write_to_text_file(self,link_set):
#        with open(self.file,'a') as f:
#            for i in self.link_set:
#                f.write(i+'\r')
#            f.close()
#        print(self.link_set)

    
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
    

def check_if_string_in_file(file_name, string_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
    return False