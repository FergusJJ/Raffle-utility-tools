import imaplib, email, time, sys, json, re, os, random
from termcolor import colored
import art
import bs4
import datetime as dt
from datetime import timezone
from threading import Timer
import concurrent.futures
import multiprocessing
#
sys.path.append('.')
from ui.colors import Style

class Mail():
    #GENERAL USE VARIABLES
    timestamp = time.strftime('%H:%M:%S')
    CHARSET = None
    shared_links_array = []
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

        except imaplib.IMAP4.error:
            except_block = True
            print(Mail.logging_in_error)
            while except_block == True:
                
                view_settings = input('Would you like to check your login credentials? [1: Yes | 0: No]\n> ')
                if view_settings == '1':
                    with open('user_settings/gmail_defaults.json','r') as f:
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
        except KeyboardInterrupt:
            for i in self.open_files:
                try:
                    i.close()
                except:
                    pass
            print('closing...')
            time.sleep(0.5)
#you cannot reuse ssl socket so you have to create a new login each time    
    def scrape_link_from_email_single(self,current_user,current_password,counter,imap_url,num_message,substring_filter,link_regex,lock):
        current_user_mp = self.current_user
        current_password_mp = self.current_password
        self.lock.acquire()
        login_session_mp = imaplib.IMAP4_SSL(self.imap_url,993)
        login_session_mp.login(current_user_mp,current_password_mp)
        self.search_mail_status, self.amount_matching_criteria = login_session_mp.search(Mail.CHARSET,self.search_criteria)
        _,individual_response_data = login_session_mp.fetch(self.num_message,'(RFC822)')
        self.lock().release
        raw = email.message_from_bytes(individual_response_data[0][1])
        scraped_email_value = str(email.message_from_bytes(Mail.scrape_email(raw)))
        print(scraped_email_value)
        returned_links = str(link_regex.findall(scraped_email_value))
        #collected_emails.write(self.returned_links+'\n')
        #collected_nums.write(self.num_message+b'\n')
     #self.timestamp = time.strftime('%H:%M:%S')   
        for i in returned_links:
            if substring_filter:
                self.lock.acquire()            
                with open(self.link_output_file,'a+') as link_file:
                    link_file.write(i +'\n')
                    link_file.close()
                self.lock.release()

    def scrape_link_mp(self):
        self.file_counter = 0
        self.login_session.logout()
        self.Manager = multiprocessing.Manager()
        self.lock = self.Manager.RLock()
        futures = []           
        with concurrent.futures.ThreadPoolExecutor() as Executor:    
            for self.num_message in self.arr_of_emails[self.start_index:]:
                task_params = self.current_user,self.current_password,self.counter,self.imap_url,self.num_message,self.substring_filter,self.link_regex,self.lock
                futures.append(
                        Executor.submit(
                            self.scrape_link_from_email_single,
                            *task_params
                            )
                        )
            for future in concurrent.futures.as_completed(futures):
                self.counter+=1
                self.timestamp = time.strftime('%H:%M:%S')
                print(f'[{self.timestamp}] DONE: {self.counter}/{len(self.num_mails)}')
                print(future.result())

    def scrape_link_from_email(self,substring_filter):
        pattern = '(?P<url>https?://[^\s]+)'
        link_regex = re.compile(pattern)
        for num_message in self.arr_of_emails[self.start_index:]:
            with open(self.last_email_save_file,'r+b') as collected_nums: #used to count how many are already done
                with open(self.link_output_file,'a+') as collected_emails: # needs to be an array so that we can read it again
                    self.open_files.append(collected_nums)
                    self.open_files.append(collected_emails)
                    self.file_counter +=1
                    self.counter +=1
                    _,self.individual_response_data = self.login_session.fetch(num_message,'(RFC822)')
                    self.raw = email.message_from_bytes(self.individual_response_data[0][1])
                    self.scraped_email_value = str(email.message_from_bytes(Mail.scrape_email(self.raw)))
                    self.returned_links = link_regex.findall(self.scraped_email_value)
                    substring_filter = str(substring_filter)
                    
                    for i in self.returned_links:         
                        if substring_filter in i:
                        
                            print(f'[{self.timestamp}] LINKS FETCHED: [{self.counter}/{len(self.arr_of_emails)-self.start_index}]')
                            collected_emails.write(i.replace('"','')+'\r')
                    collected_nums.write(num_message+b'\n')
                    self.timestamp = time.strftime('%H:%M:%S')
                    
                    collected_emails.close()
                    self.open_files.remove(collected_emails)
                collected_nums.close()
                self.open_files.remove(collected_nums)
                self.FILTERED_LINKS = []

#this is where the rest of the options are set, the actual link scraping functions are called here
    def scrape_inbox(self):
        self.session_id = random.randint(0,10000)
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
        
        self.substring_filter = str(input('Which substring filter would you like to search for?(CASE SENSITIVE)\n> '))
        self.inbox_found_status, inbox_length = self.login_session.select(self.selected_inbox)
        amount_of_mails = inbox_length[0]
        amount_of_mails = str(amount_of_mails)
        num_mails = re.search(r"\d+",amount_of_mails)
        sys.stdout.write(Style.CYAN)
        print(f'[{Mail.timestamp}] Found {num_mails.group()} emails in selected inbox')
        sys.stdout.write(Style.RESET)
        #getting email address you'd like to scrape
        self.senders = self.read_frequent_senders()
        list_of_senders_addresses = self.display_senders()
        print(list_of_senders_addresses)
        sys.stdout.write(Style.YELLOW)
        search_criteria = int(input('Type the number of the address you\'d like to scrape...\n> '))
        self.is_new_file = int(input('Would you link to create a new file to save links to [ 1: Yes | 0: No ]'))
        if self.is_new_file == 0:
            output_directory = os.listdir('output/')
            if len(output_directory) == 0:
                sys.stdout.write(Style.RED)
                print('There were no files located in the output folder, creating one now...')
                sys.stdout.write(Style.RESET)
                self.is_new_file = 1
            elif len(output_directory) >= 2:
                [print(f'{output_directory.index(files)} : {files}') for files in output_directory]

                self.link_output_file = int(input('Please enter the number of the links file you would like to choose\n> '))
                self.last_email_save_file = int(input('Please enter the number for the corresponding save file\n> '))
                self.link_output_file = 'output/'+output_directory[self.link_output_file]
                self.last_email_save_file = 'output/'+output_directory[self.last_email_save_file]
                
        if self.is_new_file == 1:
            self.link_output_file = 'links_'+str(self.session_id)+'.txt'
            self.last_email_save_file = 'last_save_'+str(self.session_id)+'.txt'
            self.link_output_file = 'output/'+self.link_output_file
            self.last_email_save_file = 'output/'+self.last_email_save_file
            with open(self.link_output_file,'w') as link_file:
                link_file.close()
            with open(self.last_email_save_file,'w') as save_file:
                save_file.close()

        sys.stdout.write(Style.RESET)
        search_criteria = (self.senders[search_criteria]).strip()
        self.search_criteria = f"FROM '{search_criteria}'"

        sys.stdout.write(Style.YELLOW)
        print(f'[{Mail.timestamp}] Scanning inbox')
        sys.stdout.write(Style.RESET)
        
        self.search_mail_status, self.amount_matching_criteria = self.login_session.search(Mail.CHARSET,self.search_criteria)
            
        if self.amount_matching_criteria == 0 or self.amount_matching_criteria == '0':
            print(f'[{Mail.timestamp}] No mails from that email address could be found...')
            Mail.enter_to_continue()
            import main
            main.main_wrapper()
        else:
            self.run_type = '1'
            # self.run_type = input('Would you like concurrency? [ 0:Yes | 1:No ]')
            pattern = '(?P<url>https?://[^\s]+)'
            self.link_regex = re.compile(pattern)
            self.link_set = set()
            

            self.amount_matching_criteria = self.amount_matching_criteria[0]
            amount_matching_criteria_str = str(self.amount_matching_criteria)
            num_mails = re.search(r"\d.+",amount_matching_criteria_str)
            self.num_mails = ((num_mails.group())[:-1]).split(' ')

            sys.stdout.write(Style.GREEN)
            self.timestamp = time.strftime('%H:%M:%S')
            print(f'[{self.timestamp}] Status code of {self.search_mail_status}')
            sys.stdout.write(Style.RESET)
            sys.stdout.write(Style.YELLOW)
            self.timestamp = time.strftime('%H:%M:%S')
            print(f'[{self.timestamp}] Found {len(self.num_mails)} emails')
            sys.stdout.write(Style.RESET)
                
            self.counter = 0
            self.arr_of_emails = self.amount_matching_criteria.split()
            self.arr_of_emails_decoded = []
            for i in self.arr_of_emails:
                d = i.decode("utf-8")
                self.arr_of_emails_decoded.append(d)

                #want to see if i can store the emails in fetched form so i dont have to call them each time
            try:
                
                read_email = getLastLine(self.last_email_save_file,len(self.num_mails))
                read_email = read_email.decode("utf-8").strip()
                self.start_index = self.arr_of_emails_decoded.index(read_email)
            except:
                self.counter = 0
                read_email = None
                self.start_index = 0
                    #this opens the file containing the indexes used. It add the b'num' to the collected.txt file once if has been scraped
                    #After this it also add the body of that b'num' to the collected_emails file so that we can import them and then filter them for links
            self.open_files = []
            self.start_time = time.time()  
            print(f'STARTING FROM {self.start_index}')
            sys.stdout.write(Style.MAGENTA)
            self.file_counter = 0
            
            if self.run_type == '0':
                self.scrape_link_mp()
            
            if self.run_type == '1':
                self.scrape_link_from_email(self.substring_filter)
            
            with open(self.link_output_file,'r') as all_links:
                links_returned = all_links.readlines()                
                print(links_returned)
               
            self.end_time = time.time()
            self.time_taken = self.end_time - self.start_time

            self.timestamp = time.strftime('%H:%M:%S')
            print(f'[{self.timestamp}] Time taken:{self.time_taken}')
        
                #self.write_to_text_file(self.link_set)
            Mail.enter_to_continue()
            import main
            main.main_wrapper()   

    def read_frequent_senders(self):
        with open('user_settings/frequent_senders.txt') as frequent_senders:
            lines = frequent_senders.readlines()
            stripped_lines = []
            for line in lines:
                line = line.strip()
                stripped_lines.append(line)
        frequent_senders.close()
        del lines
        return stripped_lines

    def display_senders(self):
        return [f"{self.senders.index(name)} : {name}  " for name in self.senders]

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

def getLastLine(fname, maxLineLength):
    print('Reading last scraped email...')
    with open(fname, "rb") as fp:
        seekd = fp.seek(maxLineLength, 2) # 2 means "from the end of the file"
    fp.close()
    if seekd == '' or seekd == None:
        getLastLine(fname,maxLineLength-1)
    else:
        with open(fname,'rb') as fp:
            read_line = fp.readlines()[-1]
        fp.close()
    return read_line
            