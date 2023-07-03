import datetime

class Pen:
    __HEADER = '\033[95m'
    __OKBLUE = '\033[94m'
    __OKCYAN = '\033[96m'
    __OKGREEN = '\033[92m'
    __WARNING = '\033[93m'
    __FAIL = '\033[91m'
    __ENDC = '\033[0m'
    __BOLD = '\033[1m'
    __UNDERLINE = '\033[4m'
    
    current_time = datetime.datetime.now()
    
    @staticmethod
    def print_red(string):
        print(Pen.__FAIL+Pen.__BOLD+str(Pen.current_time)+str(string)+Pen.__ENDC)
        
    @staticmethod
    def print_green(string):
        print(Pen.__OKGREEN+Pen.__BOLD+Pen.__BOLD+str(Pen.current_time)+str(string)+Pen.__ENDC)
        
    @staticmethod
    def print_yellow(string):
        print(Pen.__WARNING+Pen.__BOLD+Pen.__BOLD+str(Pen.current_time)+str(string)+Pen.__ENDC)
    
    