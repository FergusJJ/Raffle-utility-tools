import imaplib, email, time, sys, json
import tools_functions
from termcolor import colored
import art
from datetime import timezone
import csv
#
sys.path.append('.')
from ui.colors import Style
import tools_functions.mails_refactor as mail



class Menu:
    timestamp = time.strftime('%H:%M:%S')
    separator = colored('----------------------------------------------------------------------', color='yellow')
    
    def __init__(self, instance):
        self.instance = instance

    def print_main_menu(self):
        sys.stdout.write(Style.RED)
        art.tprint('Scripts')
        sys.stdout.write(Style.RESET)
        print(f'{Menu.separator}\n')

    def set_defalut_menu(self):
        communicate_choice_status = colored('You selected Edit Defaults\n',color='yellow')
        print(communicate_choice_status)
        with open('user_settings/gmail_defaults.json') as f:
            data = json.load(f)
            f.close()
            set_json = True
        while set_json == True:
            print(f'Currently using: { data["email_address"] }')
            change_email_json = input('Enter the email that you would like to use\n> ')
            print(f'Currently using: {data["email_password"]}')
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
        
        try:
            print('['+Menu.timestamp+']'+' You Selected: '+gmail_email_address)
        
        except:
            setup_message = colored('Note: You don\'t have a default email set up, to avoid having to re-type your credentials set one up from the start menu',color='red')
            print(setup_message+'\n')
            gmail_email_address = input('Enter your email\n> ')
            gmail_email_password = input('\nEnter your password\n> ')
        mail.get_credentials(gmail_email_address,gmail_email_password,imap_url='imap.gmail.com')
        
    
    def auto_jig_menu(self):

        sys.stdout.write(Style.YELLOW)
        timestamp = time.strftime('%H:%M:%S')
        print(f'[{timestamp}] Auto address jig menu')
        sys.stdout.write(Style.RESET)
        
        with open('user_settings/master_address.csv','r') as fcsv:
            reader = csv.reader(fcsv,skipinitialspace=True,delimiter=',')
            csv_list = []
            for rows in reader:
                csv_list.append(rows)
            master_address_list = csv_list[1:] 
            if len(master_address_list) > 1:
                is_selected_address = True
                sys.stdout.write(Style.CYAN)
                print(f'Enter the number for the address you would like to use')
                Menu.print_csv_addy(master_address_list)
                sys.stdout.write(Style.RESET)
                csv_num = int(input('> '))
                selected_address = master_address_list[csv_num]
            elif len(master_address_list) == 1:
                is_selected_address = True
                selected_address = master_address_list[0]
            elif len(master_address_list) == 0:
                is_selected_address = False
            fcsv.close()
        if is_selected_address == True:
            house_num = selected_address[1]
            if selected_address[2] == '':
                door_number_bool = False
                door_number = None
            else:
                door_number = selected_address[2]
                door_number_bool = True
            temp_line1_list = selected_address[0].split(' ')
            suffix = temp_line1_list[-1]
            if len(temp_line1_list)==2:
                street_name = temp_line1_list[0]
            else:
                street_name = temp_line1_list[:-1]
                strt = ''
                for i in street_name:
                    strt = strt+i+' '
                street_name = strt
            import tools_functions.auto_jig as jig_start
            jig_start.Jig(house_num,suffix,door_number_bool,door_number,street_name)
            import main
            main.main_wrapper()
        else:
            sys.stdout.write(Style.RED)
            print('You don\'t have a master address setup, you can set up multiple addresses for fast use in user_settings/master_addresses.csv')
            sys.stdout.write(Style.RESET)
        try:
            sys.stdout.write(Style.CYAN)
            print('What is your house number?')
            sys.stdout.write(Style.RESET)
            house_num = int(input('> '))
        except ValueError:
            sys.stdout.write(Style.RED)
            print('Please enter a number...')
            sys.stdout.write(Style.RESET)
            self.auto_jig_menu()

        sys.stdout.write(Style.CYAN)
        print('Enter your street name (Not including road/street suffix)')
        sys.stdout.write(Style.RESET)
        street_name = input('> ')

        try:
            sys.stdout.write(Style.CYAN)
            print('Do you have a door number? (Live in an apartment/flat) [ 1:YES | 0:NO ]')
            sys.stdout.write(Style.RESET)
            is_door = int(input('> '))
        except ValueError:
            sys.stdout.write(Style.RED)
            print('Please enter a number...')
            sys.stdout.write(Style.RESET)
            self.auto_jig_menu()

        if is_door == 1:
            door_number_bool = True
            sys.stdout.write(Style.CYAN)
            print('Enter your door number')
            sys.stdout.write(Style.RESET)
            door_number = input('> ')
        else:
            door_number_bool = False
            door_number = None

        sys.stdout.write(Style.CYAN)
        print('What is your street suffix [ Eg: road, street, etc. ]')
        sys.stdout.write(Style.RESET)
        suffix = input('> ')

        import tools_functions.auto_jig as jig_start
        jig_start.Jig(house_num,suffix,door_number_bool,door_number,street_name)
        import main
        main.main_wrapper()
    @staticmethod
    def print_csv_addy(master_address_list):
        sys.stdout.write(Style.WHITE)
        for i in master_address_list:
            print(f'{master_address_list.index(i)}:{i}')
        sys.stdout.write(Style.RESET)