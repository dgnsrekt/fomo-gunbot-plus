from colorama import Fore, Back, Style


def show_title():
    ph = '-' * 25
    print()
    print(ph, 'FOMO DRIVEN DEVELOPMENT', ph)

    print(Fore.YELLOW + ph, end='   ')
    print(Fore.YELLOW + 'G', end='')
    print(Fore.GREEN + 'U', end='')
    print(Fore.BLUE + 'N', end='')
    print(Fore.MAGENTA + 'B', end='')
    print(Fore.RED + 'O', end='')
    print(Fore.YELLOW + 'T', end=' ')
    print(Fore.YELLOW + 'SUPER FILTER', end='   ')
    print(Style.RESET_ALL, end='')
    print(Fore.YELLOW + ph)
    print(Style.RESET_ALL, end='')

    # print(ph, '  GUNBOT SUPER FILTER  ', ph)  # TODO: pull version number from setup or __ver__.py
    print(ph, '  VERSION: 0.0.1 BETA  ', ph)
    print()


if __name__ == '__main__':
    show_title()
