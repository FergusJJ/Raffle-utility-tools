import imaplib, email, time, sys, json, re, random
import os
from termcolor import colored



#
sys.path.append('.')
from ui.colors import Style

#Globals

CHARSET = None
shared_links_array = []

logging_in_error = colored('['+time.strftime('%H:%M:%S')+']'+' Something went wrong', color='red')
not_an_option = colored('['+time.strftime('%H:%M:%S')+']'+' That is not an option...',color='red')

inbox_options = {
            "INBOX":"INBOX",
            "SPAM":"[Gmail]/Spam",
            "SENT":"[Gmail]/Sent",
            "TRASH":'[Gmail]/Trash"',
            "DRAFTS":"[Gmail]/Drafts"
        }

current_options =  {
    "CURRENT_USER":None,
    "CURRENT_PASSWORD":None,
    "IMAP_URL":None,
    "stored_login":None,
    "SELECTED_INBOX":None,
    "SUBSTR":None,
    "SENT_SINCE_DATE":None,
    "SENDERS":None,
    "counter":0,
    "session_id":None
}   

#


def calc_ts():
    return time.strftime('%H:%M:%S')



def logging_in_error():
    return colored('['+time.strftime('%H:%M:%S')+']'+' Something went wrong', color='red')

def not_an_option():
    return colored('['+time.strftime('%H:%M:%S')+']'+' That is not an option...',color='red')

def get_credentials(user,password,imap_url):
    current_options["CURRENT_USER"] = user
    current_options["CURRENT_PASSWORD"] = password
    current_options["IMAP_URL"] = imap_url
    
    gmail_login()

def gmail_login():
    sys.stdout.write(Style.YELLOW)
    print(f'[{calc_ts()}] Logging into {current_options["CURRENT_USER"]}...')
    if current_options["IMAP_URL"] == 'imap.gmail.com':
        current_options["stored_login"] = imaplib.IMAP4_SSL(current_options["IMAP_URL"],993)
    try:
        current_options["stored_login"].login(current_options["CURRENT_USER"],current_options["CURRENT_PASSWORD"])
    except imaplib.IMAP4.error:
        print(f"{logging_in_error()}\nCheck your password")
        enter_to_continue()
        import main
        main.main_wrapper()
        

    sys.stdout.write(Style.RESET)
    sys.stdout.write(Style.GREEN)
    print(f'[{calc_ts()}] Successfully Logged in...')
    sys.stdout.write(Style.RESET)
    get_gmail_inbox()

def get_gmail_inbox():
    current_options["session_id"] = random.randint(0,100000)
    link_set = set()
    inbox_choice = input('Which inbox would you like to scrape?[1: Inbox | 2: Spam | 3: Trash | 4: Drafts | 5: Sent]\n> ')
    if inbox_choice == '1':
        current_options["SELECTED_INBOX"] = inbox_options["INBOX"]
    elif inbox_choice == '2':
        current_options["SELECTED_INBOX"] = inbox_options["SPAM"]
    elif inbox_choice == '3':
        current_options["SELECTED_INBOX"] = inbox_options["TRASH"]
    elif inbox_choice == '4':
        current_options["SELECTED_INBOX"] = inbox_options["DRAFTS"]
    elif inbox_choice == '5':
        current_options["SELECTED_INBOX"] = inbox_options["SENT"]
    get_date()
    start_scraping()

def get_date():
    sent_since_date = str(input('What starting date would you like to search from? [dd/mm/yyyy]\n> '))
    if '/' not in sent_since_date:
        sys.stdout.write(Style.RED)
        print('Invalid format...')
        sys.stdout.write(Style.RESET)
        time.sleep(0.5)
        os.system('cls')
        get_gmail_inbox()
    current_options["SENT_SINCE_DATE"] = sent_since_date.split('/')
    if current_options["SENT_SINCE_DATE"][1] == '01':
        sent_since_mon = 'Jan'
    elif current_options["SENT_SINCE_DATE"][1] == '02':
        sent_since_mon = 'Feb'
    elif current_options["SENT_SINCE_DATE"][1] == '03':
        sent_since_mon = 'Mar'
    elif current_options["SENT_SINCE_DATE"][1] == '04':
        sent_since_mon = 'Apr'
    elif current_options["SENT_SINCE_DATE"][1] == '05':
        sent_since_mon = 'May'
    elif current_options["SENT_SINCE_DATE"][1] == '06':
        sent_since_mon = 'Jun'
    elif current_options["SENT_SINCE_DATE"][1] == '07':
        sent_since_mon = 'Jul'
    elif current_options["SENT_SINCE_DATE"][1] == '08':
        sent_since_mon = 'Aug'
    elif current_options["SENT_SINCE_DATE"][1] == '09':
        sent_since_mon = 'Sep'
    elif current_options["SENT_SINCE_DATE"][1] == '10':
        sent_since_mon = 'Oct'
    elif current_options["SENT_SINCE_DATE"][1] == '11':
        sent_since_mon = 'Nov'
    elif current_options["SENT_SINCE_DATE"][1] == '12':
        sent_since_mon = 'Dec'
    current_options["SENT_SINCE_DATE"] = f'{current_options["SENT_SINCE_DATE"][0]}-{sent_since_mon}-{current_options["SENT_SINCE_DATE"][2]}'

def start_scraping():
    inbox_found_status, inbox_length = current_options["stored_login"].select(current_options["SELECTED_INBOX"])
    amount_of_mails = inbox_length[0]
    amount_of_mails = str(amount_of_mails)
    num_mails = re.search(r"\d+",amount_of_mails)
    sys.stdout.write(Style.CYAN)
    print(f'[{calc_ts()}] Found {num_mails.group()} emails in selected inbox')
    sys.stdout.write(Style.RESET)
    #
    search_criteria = get_selected_sent_address()
    
    #
    is_new_file = int(input('Would you link to create a new file to save links to [ 1: Yes | 0: No ]\n> '))
    if is_new_file == 0:
        output_directory = os.listdir('output/')
        if len(output_directory) == 0:
            sys.stdout.write(Style.RED)
            print('There were no files located in the output folder, creating one now...')
            sys.stdout.write(Style.RESET)
            is_new_file = 1
        elif len(output_directory) >= 2:
            print('Task files found...')
            sys.stdout.write(Style.RESET)
            [print(f'{output_directory.index(files)} : {files}') for files in output_directory]
            sys.stdout.write(Style.YELLOW)
            link_output_file = int(input('Please select the file(s) that you would like to run... [ "ALL" : start all ] \n> '))
            sys.stdout.write(Style.RESET)
            last_email_save_file = int(input('Please enter the number for the corresponding save file\n> '))
            link_output_file = 'output/'+output_directory[link_output_file]
            last_email_save_file = 'output/'+output_directory[last_email_save_file]
    if is_new_file == 1:
        link_output_file = 'links_'+str(current_options["session_id"])+'.txt'
        last_email_save_file = 'last_save_'+str(current_options["session_id"])+'.txt'
        link_output_file = 'output/'+link_output_file
        last_email_save_file = 'output/'+last_email_save_file
        with open(link_output_file,'w') as link_file:
            link_file.close()
        with open(last_email_save_file,'w') as save_file:
            save_file.close()
    sys.stdout.write(Style.RESET)
    is_keyword_in_file = check_keyword(selected_email=search_criteria)
    print(search_criteria)
    if is_keyword_in_file:
        search_criteria = current_options["SENDERS"][search_criteria].split(" ")[0].strip()
        print(search_criteria)
    else:
        search_criteria = (current_options["SENDERS"][search_criteria]).strip()
    search_criteria = f'FROM "{search_criteria}" '
    search_criteria_2 = f'SINCE "{current_options["SENT_SINCE_DATE"]}"'
    criteria = search_criteria+search_criteria_2
    sys.stdout.write(Style.YELLOW)
    print(f'[{calc_ts()}] Scanning inbox')
    sys.stdout.write(Style.RESET)
    search_mail_status, amount_matching_criteria = current_options['stored_login'].search(CHARSET,criteria)
    print(search_mail_status)
    if amount_matching_criteria == 0 or amount_matching_criteria == '0':
        print(f'[{calc_ts()}] No mails from that email address could be found...')
        enter_to_continue()
        import main
        main.main_wrapper()
    pattern = '(?P<url>https?://[^\s]+)'
    link_regex = re.compile(pattern)
    link_set = set()
    amount_matching_criteria = amount_matching_criteria[0]
    amount_matching_criteria_str = str(amount_matching_criteria)
    num_mails = re.search(r"\d.+",amount_matching_criteria_str)
    #print(f"NUMMAILS {num_mails}")
    if not num_mails:
        print(f'[{calc_ts()}] No mails from that email address could be found...')
        enter_to_continue()
        import main
        main.main_wrapper()
    num_mails = ((num_mails.group())[:-1]).split(' ')
#
    sys.stdout.write(Style.GREEN)
    print(f'[{calc_ts()}] Status code of {search_mail_status}')
    sys.stdout.write(Style.RESET)
    sys.stdout.write(Style.YELLOW)
    print(f'[{calc_ts()}] Found {len(num_mails)} emails')
    sys.stdout.write(Style.RESET)
    current_options["counter"] = 0
    current_options["arr_of_emails"] = amount_matching_criteria.split()
    current_options["arr_of_emails_decoded"] = []

    for i in current_options["arr_of_emails"]:
        d = i.decode("utf-8")
        current_options["arr_of_emails_decoded"].append(d)

    read_email = getLastLine(last_email_save_file,len(num_mails))

    if read_email == None:
        #there are no previous checkpoints to get links from
        current_options["counter"] = 0
        read_email = None
        current_options["start_index"] = 0
    else:
        read_email = read_email.decode("utf-8").strip()
        current_options["start_index"] = current_options["arr_of_emails_decoded"].index(read_email)
    current_options["open_files"] = []
    current_options["START_TIME"] = time.time()  
    print(f'STARTING FROM {current_options["start_index"]}')
    sys.stdout.write(Style.MAGENTA)
    current_options["file_counter"] = 0

    scrape_link_from_email(current_options["SUBSTR"],last_email_save_file=last_email_save_file,link_output_file=link_output_file)
    sys.stdout.write(Style.YELLOW)
    print(f"Links can be found in: {link_output_file}")
    current_options["END_TIME"] = time.time()

    time_taken = float(current_options["END_TIME"]) - float(current_options["START_TIME"])
    
    print(f'[{calc_ts()}] Time taken: {time_taken}seconds')
    sys.stdout.write(Style.RESET)
    enter_to_continue()
    import main
    main.main_wrapper() 

def scrape_link_from_email(substring_filter,last_email_save_file,link_output_file):
        pattern = '(?P<url>https?://[^\s]+)'
        link_regex = re.compile(pattern)
        
        for num_message in current_options["arr_of_emails"][current_options["start_index"]:]:
            
            with open(last_email_save_file,'r+b') as collected_nums: #used to count how many are already done
                with open(link_output_file,'a+') as collected_emails: # needs to be an array so that we can read it again
                    current_options["open_files"].append(collected_nums)
                    current_options["open_files"].append(collected_emails)
                    current_options["file_counter"] +=1
                    current_options["counter"] +=1
                    _,individual_response_data = current_options["stored_login"].fetch(num_message,'(RFC822)')
                    
                    raw = email.message_from_bytes(individual_response_data[0][1])
                    scraped_email_value = str(email.message_from_bytes(scrape_email(raw)))
                    returned_links = link_regex.findall(scraped_email_value)
                    substring_filter = str(substring_filter)
                    
                    for i in returned_links:         
                        if substring_filter in i:
                            #up to here
                            
                            print(f'[{calc_ts()}] LINKS FETCHED: [{current_options["counter"]}/{len(current_options["arr_of_emails"])-current_options["start_index"]}]')
                            collected_emails.write(i.replace('"','')+'\r')
                    collected_nums.write(num_message+b'\n')
                    timestamp = time.strftime('%H:%M:%S')
                    
                    collected_emails.close()
                    current_options["open_files"].remove(collected_emails)
                collected_nums.close()
                current_options["open_files"].remove(collected_nums)
               # self.FILTERED_LINKS = []


def get_selected_sent_address() -> int:
        current_options["SENDERS"] = read_frequent_senders()
        
        
        list_of_senders_addresses = display_senders()
        print(list_of_senders_addresses)
        sys.stdout.write(Style.RESET)
        search_criteria = int(input('Type the number of the address you\'d like to scrape...\n> '))
        if search_criteria> len(current_options["SENDERS"]):
            sys.stdout.write(Style.RED)
            print('That email is not listed')
            sys.stdout.write(Style.RESET)
            get_selected_sent_address()
        else:
            return search_criteria

def check_keyword(selected_email: int) -> bool:
    selected_line_list = current_options["SENDERS"][selected_email].split(" ")
    if len(selected_line_list) > 1:
        current_options["SUBSTR"] = selected_line_list[1].strip()
        return True
    else:
        current_options["SUBSTR"] = str(input('Which substring filter would you like to search for?(CASE SENSITIVE)\n> '))
        return False
    


def display_senders():
     return [f"{current_options['SENDERS'].index(name)} : {name} " for name in current_options["SENDERS"]]

def read_frequent_senders():
    with open('user_settings/frequent_senders.txt') as frequent_senders:
        lines = frequent_senders.readlines()
        stripped_lines = []
        for line in lines:
            line = line.strip()
            stripped_lines.append(line)
    frequent_senders.close()
    del lines
    return stripped_lines

def enter_to_continue():
    await_input = input('Press ENTER to continue...')
    if bool(await_input) == True:
        except_block = False

def getLastLine(fname, maxLineLength):
    print('Reading last scraped email...')
    with open(fname, "rb") as fp:
        seekd = fp.seek(maxLineLength, 2) # 2 means "from the end of the file"
    fp.close()
    if seekd == '' or seekd == None:
        getLastLine(fname,maxLineLength-1)
    else:
        with open(fname,'rb') as fp:
            
            #
            #shouldn't break if no lines in file
            line_count = 0
            ts = time.time()
            if not ((ts+2) <time.time()) and line_count != 0:
                for line in fp:
                    if line != "\n":
                        line_count += 1

            if line_count == 0:
                return None
            #
            read_line = fp.readlines()[-1]
        fp.close()
    return read_line

def scrape_email(raw):
        
        if raw.is_multipart():
           
            return scrape_email(raw.get_payload(0))
        else:
            return raw.get_payload(None,True)