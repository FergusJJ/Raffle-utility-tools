import email
import imaplib
import datetime
import email.mime.multipart
import base64
import sys
import time
import random 
import os
import re
sys.path.append('.')
from ui.colors import Style
#imap_server = "outlook.office365.com"
#imap_port = 993

#smtp_server = "smtp.office365.com"
#smtp_port = 587

class Outlook():

    timestamp = time.strftime('%H:%M:%S')

    outlook_inbox_options = {
        "INBOX":'Inbox',
        "JUNK":'Junk'
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
        Outlook.timestamp = time.strftime('%H:%M:%S')
        print(f'[{Outlook.timestamp}] Logging into {self.current_user}...')
        
        self.attempts = 0
        if self.imap_url == 'outlook.office365.com':
            self.login_session = imaplib.IMAP4_SSL(self.imap_url)
            self.logging_in_active = True
        while self.logging_in_active == True:
            r, _ = self.login_session.login(self.current_user,self.current_password)
            sys.stdout.write(Style.RESET)
            if r == 'OK':
                sys.stdout.write(Style.GREEN)
                Outlook.timestamp = time.strftime('%H:%M:%S')
                print(f'[{Outlook.timestamp}] Successfully Logged in...')
                sys.stdout.write(Style.RESET)
                self.logging_in_active = False
            else:
                self.attempts +=1
                if self.attempts > 3:
                    sys.stdout.write(Style.RED)
                    Outlook.timestamp = time.strftime('%H:%M:%S')
                    print(f'[{Outlook.timestamp}] Too many failed login attempts, returning to main menu...')
                    time.sleep(1)
                    sys.stdout.write(Style.RESET)
                    import main
                    main.main_wrapper()
        if self.imap_url == 'imap-mail.outlook.com':
            self.outlook_scrape_inbox()
        elif self.imap_url == 'outlook.office365.com':
            self.outlook_scrape_inbox()
    
    def outlook_scrape_inbox(self):
        self.session_id = random.randint(0,100000)
        self.link_set = set()
        inbox_choice = input('Which inbox would you like to scrape?[1: Inbox | 2: Spam | 3: Trash | 4: Drafts | 5: Sent]\n> ')
        if inbox_choice == '1':
            self.selected_inbox = Outlook.outlook_inbox_options["INBOX"]
        elif inbox_choice == '2':
            self.selected_inbox = Outlook.outlook_inbox_options["JUNK"]
        
        self.substring_filter = str(input('Which substring filter would you like to search for?(CASE SENSITIVE)\n> '))

        self.senders = self.read_frequent_senders()
        list_of_senders_addresses = self.display_senders()
        print(list_of_senders_addresses)
        sys.stdout.write(Style.YELLOW)
        self.search_criteria = int(input('Type the number of the address you\'d like to scrape...\n> '))
        self.search_criteria = (self.senders[self.search_criteria]).strip()
        self.search_criteria = f'FROM "{self.search_criteria}"'
        #self.inbox_found_status, inbox_length = self.login_session.select("INBOX")
        self.login_session.select(self.selected_inbox)
        resp, items = self.login_session.uid("search",None, self.search_criteria)
        
        
        num_mails = items
        self.amount_matching_criteria = num_mails
        print(num_mails)
        num_mails = len(num_mails[0].decode("utf-8").split(' '))
        sys.stdout.write(Style.CYAN)
        print(f'[{Outlook.timestamp}] Found {num_mails} emails in selected inbox')
        
        #getting email address you'd like to scrape
        

        self.is_new_file = int(input('Would you link to create a new file to save links to [ 1: Yes | 0: No ]\n> '))
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

        

        sys.stdout.write(Style.YELLOW)
        print(f'[{Outlook.timestamp}] Scanning inbox')
        sys.stdout.write(Style.RESET)
        
        if self.amount_matching_criteria == 0 or self.amount_matching_criteria == '0':
            print(f'[{Outlook.timestamp}] No mails from that email address could be found...')
            Outlook.enter_to_continue()
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
            print(self.num_mails)

            sys.stdout.write(Style.GREEN)
            self.timestamp = time.strftime('%H:%M:%S')
            print(f'[{self.timestamp}] Status code of {resp}')
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

            if self.run_type == '1':
                self.scrape_link_from_email_outlook(self.substring_filter)
            
            with open(self.link_output_file,'r') as all_links:
                links_returned = all_links.readlines()                
                print(links_returned)
               
            self.end_time = time.time()
            self.time_taken = self.end_time - self.start_time

            self.timestamp = time.strftime('%H:%M:%S')
            print(f'[{self.timestamp}] Time taken:{self.time_taken}')
        
                #self.write_to_text_file(self.link_set)
            Outlook.enter_to_continue()
            import main
            main.main_wrapper()


    def scrape_link_from_email_outlook(self,substring_filter):
        pattern = '(?P<url>https?://[^\s]+)'
        link_regex = re.compile(pattern)
        
        for num_message in self.arr_of_emails[self.start_index:]:
            
            with open(self.last_email_save_file,'r+b') as collected_nums: #used to count how many are already done
                with open(self.link_output_file,'a+') as collected_emails: # needs to be an array so that we can read it again
                    self.open_files.append(collected_nums)
                    self.open_files.append(collected_emails)
                    self.file_counter +=1
                    self.counter +=1
                    _,indiviual_response_data = self.login_session.fetch(num_message,'(RFC822)')
                    #_,individual_response_data = self.login_session.fetch(num_message,'(RFC822)')
                    individual_body = individual_response_data[0][1]
                    print(individual_response_data)
                    time.sleep(2000)
                    self.individual_body_parsed = email.message_from_string(individual_body)
                    if self.individual_body_parsed.is_multipart():
                        for payload in self.individual_body_parsed.get_payload():
                            body = (
                                payload.get_payload()
                                .split(self.email_message['from'])[0]
                                .split('\r\n\r\n2015')[0]
                                )
                            
                    else:
                        body = (
                        self.email_message.get_payload()
                        .split(self.email_message['from'])[0]
                        .split('\r\n\r\n2015')[0]
                        )
                        


                    #self.raw = email.message_from_bytes(self.individual_response_data[0][1])
                    #self.scraped_email_value = str(email.message_from_string(Mail.scrape_email(self.raw)))
                    #self.returned_links = link_regex.findall(str(individual_body_parsed))
                    substring_filter = str(substring_filter)
                    self.returned_links = []
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





##

    def logout(self):
        return self.login_session.logout()

    def getEmail(self, id):
        r, d = self.login_session.fetch(id, "(RFC822)")
        self.raw_email = d[0][1]
        self.email_message = email.message_from_string(self.raw_email)
        return self.email_message






    def mailbody(self):
        if self.email_message.is_multipart():
            for payload in self.email_message.get_payload():
                # if payload.is_multipart(): ...
                body = (
                    payload.get_payload()
                    .split(self.email_message['from'])[0]
                    .split('\r\n\r\n2015')[0]
                )
                return body
        else:
            body = (
                self.email_message.get_payload()
                .split(self.email_message['from'])[0]
                .split('\r\n\r\n2015')[0]
            )
            return body

    @staticmethod
    def enter_to_continue():
        await_input = input('Press ENTER to continue...')
        if bool(await_input) == True:
            except_block = False
    @staticmethod
    def scrape_email(raw):
        
        if raw.is_multipart():
           
            return Outlook.scrape_email(raw.get_payload(0))
        else:
            return raw.get_payload(None,True)

'''

    def unreadToday(self):
        list = self.unreadIdsToday()
        latest_id = list[-1]
        return self.getEmail(latest_id)

    def mailsubject(self):
        return self.email_message['Subject']

    def mailfrom(self):
        return self.email_message['from']

    def mailto(self):
        return self.email_message['to']

    def maildate(self):
        return self.email_message['date']

    def mailreturnpath(self):
        return self.email_message['Return-Path']

    def mailreplyto(self):
        return self.email_message['Reply-To']

    def mailall(self):
        return self.email_message

    def mailbodydecoded(self):
        return base64.urlsafe_b64decode(self.mailbody())

'''
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