class Term:
    END = '\033[0m'

    BLUE = '\033[94m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    PINK = '\033[95m'

    BOLD = '\033[00;01m'
    BBLUE = '\033[94;01m'
    BGREEN = '\033[92;01m'
    BORANGE = '\033[93;01m'
    BRED = '\033[91;01m'
    BPINK = '\033[95;01m'

    @staticmethod
    def get_size():
        return os.popen('stty size', 'r').read().split()

    @staticmethod
    def print_line():
        print('-' * 42)

    @staticmethod
    def print_info(msg):
        print('{0}{1}{2}'.format(Term.BGREEN, msg, Term.END))

    @staticmethod
    def print_error(error):
        print('{0}{1}{2}'.format(Term.BRED, error, Term.END))
