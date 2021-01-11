import sys
import time
import random
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
            print('Would you like to have a 4-letter jig in front of your house number? [ 1:YES | 0:NO ]')
            sys.stdout.write(Style.RESET)
            self.is_four_letter_prefix = bool(int(input('> ')))
            sys.stdout.write(Style.CYAN)
            print('Would you like to use an apartment/flat line? [ 1:YES | 0:NO ]')
            sys.stdout.write(Style.RESET)
            self.is_2nd_line = bool(int(input('> ')))
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
        letter_4 = random.randrange(1,26)
        letter_1 = Jig.ALPHABET[letter_1]
        letter_2 = Jig.ALPHABET[letter_2]
        letter_3 = Jig.ALPHABET[letter_3]
        letter_4 = Jig.ALPHABET[letter_4]
        if self.is_four_letter_prefix == True:
            four_letter_prefix = (letter_1+letter_2+letter_3+letter_4).upper()
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
            self.suffix_array = ['rd','roa','road','roadd','raod','rooad','rroad','rroaad','roaad']
           
        elif self.suffix == 'street':
            self.suffix_array = ['st','street','strt','streett','streeet','sstreet','sstreett','stt']
        else:
            sys.stdout.write(Style.RED)
            print('That is not supported, please enter your own options for suffixes & separate with commas [Eg: st,strt,street,etc]')
            sys.stdout.write(Style.RESET)
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

    def _gen_street_name(self):
        upper_bound = len(self.suffix_array)-1
        index = random.randrange(0,upper_bound)
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
        return_street_name = self.street_name +' '+ street_suffix

        return return_street_name

    def _gen_addy(self):
        sys.stdout.write(Style.MAGENTA)
        counter = 1
        while counter <= self.amount_of_addresses:
            house_number = self._create_house_number()
            street = self._gen_street_name()
            if self.is_2nd_line == True:
                line_2 = self._gen_2nd_line()
            else:
                line_2 = ''
            address = (street,house_number,line_2)
            if address not in self.addresses:
                self.addresses.append(address)
                timestamp = time.strftime('%H:%M:%S')
                print(f'[{timestamp}] GENERATED {counter}/{self.amount_of_addresses}')
                counter+=1
            else:
                pass
        sys.stdout.write(Style.RESET)
        for i in self.addresses:
           print(f'{i}\n')
        print(len(self.addresses))
        

        
    