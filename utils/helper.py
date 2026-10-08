from termcolor import colored, cprint


def printd(s):
    print(f'\n\n{s}\n\n')



def cprint3(s):
    print()
    cprint(f' ** {s} ** ', "blue", "on_green", attrs=['bold'])
    print()

def cprint2(s):
    print()
    cprint(f' ** {s} ** ', "white", "on_magenta", attrs=['bold'])
    print()

def cprint1(s):
    print()
    cprint(f' ** {s} ** ', "white", "on_light_red", attrs=['bold'])
    print()
