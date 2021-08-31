import sys
import time
import random
import csv
from datetime import date
sys.path.append('.')
from ui.colors import Style

class Jig:

    ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    line_2_prefixes = ['apt','flat','floor','apt.','flat.','floor.','unit','unit.','apartment','room','door','door.','suite','suite.','room.']

    def __init__(self,house_num,suffix,door_number_bool,door_number,street_name):
        self.house_num = house_num
        self.suffix = suffix.lower()
        self.door_number_bool = door_number_bool
        self.door_number = door_number
        self.street_name = street_name
        self.addresses = []
        self._get_amount_of_addresses()
        self._gen_addy()

    def _get_amount_of_addresses(self):
        try:
            sys.stdout.write(Style.CYAN)
            print('How many addresses would you like?')
            sys.stdout.write(Style.RESET)
            self.amount_of_addresses = int(input('> '))
            sys.stdout.write(Style.CYAN)
            print('Would you like to have a 3-letter jig in front of your house number? [ 1:YES | 0:NO ]')
            sys.stdout.write(Style.RESET)
            self.is_four_letter_prefix = bool(int(input('> ')))
            sys.stdout.write(Style.CYAN)
            print('Would you like to jig your street name? [ 1:YES | 0:NO ]')
            sys.stdout.write(Style.RESET)
            self.jig_street_name = bool(int(input('> ')))
            sys.stdout.write(Style.CYAN)
            if self.door_number_bool == False:
                print('Would you like to use an apartment/flat line? [ 1:YES | 0:NO ]')
                sys.stdout.write(Style.RESET)
                self.is_2nd_line = bool(int(input('> ')))
            else:
                self.is_2nd_line = 0
        except ValueError:
            sys.stdout.write(Style.RED)
            print('Please enter a number...')
            sys.stdout.write(Style.RESET)
            time.sleep(1)
            self._get_amount_of_addresses()
        self._get_file_format()
        self._get_suffixes()

    def _get_file_format(self):
        sys.stdout.write(Style.CYAN)
        print('Which format would you like the addresses to be output in? [ 1: CSV | 2: TXT ]')
        sys.stdout.write(Style.RESET)
        self.output_format = int(input('> '))
        if self.output_format == 1:
            self.output_format = 'csv_file'
        elif self.output_format == 2:
            self.output_format = 'txt_file'
        else:
            sys.stdout.write(Style.RED)
            print('Please type a valid option...')
            sys.stdout.write(Style.RESET)
            time.sleep(1)
            self._get_file_format()
    
    def _create_house_number(self):
        four_letter_prefix = ''
        letter_1 = random.randrange(1,26)
        letter_2 = random.randrange(1,26)
        letter_3 = random.randrange(1,26)
        
        letter_1 = Jig.ALPHABET[letter_1]
        letter_2 = Jig.ALPHABET[letter_2]
        letter_3 = Jig.ALPHABET[letter_3]
        if self.is_four_letter_prefix == True:
            four_letter_prefix = (letter_1+letter_2+letter_3+ " ").upper()
        else:
            four_letter_prefix = ''
        house_num_final = four_letter_prefix+str(self.house_num)
        return house_num_final

    def _get_suffixes(self):
        #default array might be a good option, can read user defined suffixes from a file
        if self.suffix == 'annex':
            self.suffix_array = ['annex','anex','anx','ax','anex','aannex','annexx','anneex']

        elif self.suffix == 'avenue':
            self.suffix_array = ['ave','av','avenue','avenu','avenuee','aave','aavenue','avvenue']

        elif self.suffix == 'boulevard':
            self.suffix_array = ['blvd','boulevard','bvd','blvdd','boulevardd','bboulevard','booulevard']

        elif self.suffix == 'canyon':
            self.suffix_array = ['cyn','canyn','cnyn','canyon','canyn','canyonn','ccanyon','canyyon']

        elif self.suffix == 'close':
            self.suffix_array = ['cls','cl','closee','close','cclose','closse','cloosee']

        elif self.suffix == 'drive':
            self.suffix_array = ['drive','dr','drv','drivee','driv','drr','ddrive','drivvee']

        elif self.suffix == 'estate':
            self.suffix_array = ['e','est','estatee','estat','estate','eestate','esttate']

        elif self.suffix == 'grove':
            self.suffix_array = ['grv','grove','gr','grovee','ggrove','grrove']

        elif self.suffix == 'lane':
            self.suffix_array = ['ln','lan','lne','lane','lanee','llane','laane']
            
        elif self.suffix == 'road':
            self.suffix_array = ['rd','roa','roaa','road','roadd','rdd','rroad','rooad','roaad','rrd']
           
        elif self.suffix == 'street':
            self.suffix_array = ['st','street','strt','streett','streeet','sstreet','sstreett','stt']
        else:
            sys.stdout.write(Style.RED)
            print('That is not supported, please enter your own options for suffixes & separate with commas [Eg: st,strt,street,etc]')
            sys.stdout.write(Style.RESET)
            sys.stdout.write(Style.CYAN)
            print('Would you like to leave street suffix unjigged? [ 1:YES || 0:NO ]')
            sys.stdout.write(Style.RESET)
            use_1_suffix = bool(int(input('> ')))
            if use_1_suffix:
                self.suffix_array = [f"{self.suffix}"]
            else:
                self.suffix_array = input('> ')
                self.suffix_array = self.suffix_array.split(sep=',')

    def _gen_2nd_line(self):
        line_2_upper = self.amount_of_addresses/2
        line_2_index = random.randrange(0,14)
        line_2_prefix = Jig.line_2_prefixes[line_2_index]
        line_2_suffix = random.randrange(1,100)
        is_use_alphabet = bool(random.randrange(0,1))
        if is_use_alphabet == True:
            index_alphabet = random.randrange(0,10)
            alpha_suffix = Jig.ALPHABET[index_alphabet]
        else:
            alpha_suffix = ''
        line_2 = f'{line_2_prefix} {line_2_suffix}{alpha_suffix}'
        return line_2

    def _jig_street_name(self):
        
        temp_street_name = self.street_name
        if temp_street_name == "":
            sys.stdout.write(Style.RED)
            print("You don't have a street namer in within your master address file..")
            sys.stdout.write(Style.RESET)
        street_name_arr = []
        for i in temp_street_name:
            street_name_arr.append(i)
        
        duped_character = random.randrange(0,len(street_name_arr))
        street_name_arr.insert(duped_character, street_name_arr[duped_character])
        temp_street_name = "".join(street_name_arr)
        return temp_street_name

    def _gen_street_name(self):
        if len(self.suffix_array) >1:
            upper_bound = len(self.suffix_array)-1
            index = random.randrange(0,upper_bound)
        else:
            index = 0
        street_suffix = self.suffix_array[index]
        length = len(street_suffix)
        roll = random.randrange(1,4)
        if roll == 1:
            street_suffix = street_suffix[:length-1] + '.' + street_suffix[length-1:] 
        elif roll == 2:
            street_suffix = street_suffix[:length-2] + '.' + street_suffix[length-2:] 
        elif roll == 3:
            street_suffix = street_suffix+'.'
        elif roll == 4:
            pass
        

        if self.jig_street_name:
            temp_street_name = self._jig_street_name()
        else:
            temp_street_name = self.street_name
        if len(self.street_name.split(' ')) > 1:
            return_street_name = temp_street_name + street_suffix
        else:
            return_street_name = temp_street_name +' '+ street_suffix

        return return_street_name

    def _output_addresses_to_csv(self):
        sys.stdout.write(Style.CYAN)
        
        output_day = date.today().strftime("%b-%d-%Y")
        fname = f'output/{self.street_name}{self.suffix}{output_day}.csv'
        with open(fname,'w',newline='') as new_address_csv:
            address_writer = csv.writer(new_address_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            counter = 1
            total = len(self.addresses)
            for address in self.addresses:
                timestamp = time.strftime('%H:%M:%S')
                print(f'[{timestamp}] WRITTEN [{counter}/{total}]')
                address_writer.writerow(address)
                counter+=1
        sys.stdout.write(Style.GREEN)
        timestamp = time.strftime('%H:%M:%S')
        print(f'[{timestamp}] DONE, RETURNING TO MAIN MENU...')
        time.sleep(1)
        import main
        main.main_wrapper()

    def _gen_addy(self):
        sys.stdout.write(Style.MAGENTA)
        counter = 1
        try:
            while counter <= self.amount_of_addresses:
                house_number = self._create_house_number()

                street = self._gen_street_name()
                if self.is_2nd_line == True:
                    line_2 = self._gen_2nd_line()
                else:
                    line_2 = self.door_number
                address = (street,house_number,line_2)
                if address not in self.addresses:
                    self.addresses.append(address)
                    timestamp = time.strftime('%H:%M:%S')
                    print(f'[{timestamp}] GENERATED {counter}/{self.amount_of_addresses}')
                    counter+=1
                else:
                    pass
            sys.stdout.write(Style.GREEN)
            timestamp = time.strftime('%H:%M:%S')
            print(f'[{timestamp}] DONE GENERATING')
            self._output_addresses_to_csv()
        except KeyboardInterrupt:
            Jig.failsafe(self)
        
        
    @staticmethod
    def failsafe(self):
        sys.stdout.write(Style.RED)
        print('Would you like to save to csv before exiting? [ 1:YES | 0:NO ]')
        sys.stdout.write(Style.RESET)
        choice = int(input('> '))
        if choice == 1:
            self._output_addresses_to_csv()
        elif choice == 0:
            sys.exit()
        else:
            sys.stdout.write(Style.RED)
            print('Please type a valid option...')

        
    