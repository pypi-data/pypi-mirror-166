import time
from cypherx import *
import os
from rich import print

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Start:

    def __init__(self, argv: list = "") -> None:

        self.banner = str("\n  [bold green]▄████▄▓██   ██▓ ██▓███   ██░ ██ ▓█████  ██▀███  ▒██   ██▒\n" +
            " ▒██▀ ▀█ ▒██  ██▒▓██░  ██▒▓██░ ██▒▓█   ▀ ▓██ ▒ ██▒▒▒ █ █ ▒░\n" +
            " ▒▓█    ▄ ▒██ ██░▓██░ ██▓▒▒██▀▀██░▒███   ▓██ ░▄█ ▒░░  █   ░\n" +
            " ▒▓▓▄ ▄██▒░ ▐██▓░▒██▄█▓▒ ▒░▓█ ░██ ▒▓█  ▄ ▒██▀▀█▄   ░ █ █ ▒\n" +
            " ▒ ▓███▀ ░░ ██▒▓░▒██▒ ░  ░░▓█▒░██▓░▒████▒░██▓ ▒██▒▒██▒ ▒██▒\n" +
            " ░ ░▒ ▒  ░ ██▒▒▒ ▒▓▒░ ░  ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒▓ ░▒▓░▒▒ ░ ░▓ ░\n" +
            "   ░  ▒  ▓██ ░▒░ ░▒ ░      ▒ ░▒░ ░ ░ ░  ░  ░▒ ░ ▒░░░   ░▒ ░\n" +
            " ░       ▒ ▒ ░░  ░░        ░  ░░ ░   ░     ░░   ░  ░    ░\n" +  
            " ░ ░     ░ ░               ░  ░  ░   ░  ░   ░      ░    ░\n" +  
            " ░       ░ ░                                               [/bold green]\n")

        self.menu = str("\n Welcome to [green]CypherX[/green], a simple and easy \r to use cryptography program.\n\n" +
            " Choice an option:\n\n" +
            " [bold]1 - Caesar\n" +
            " 2 - Atbash\n" +
            " 0 - Exit\n[/bold]"
        )

        self.terminalUI()


    def CaesarTUI(self):
        try:
            cls()
            print(self.banner)
            print(" Caesar Cipher\n")
            print(" 1. Encrypt")
            print(" 2. Decrypt")
            print(" 3. Force Decrypt")
            print(" 0. Back")
            caesar_choice = int(input("\n Enter your choice: "))

            if caesar_choice == 1:
                cls()
                print(self.banner)
                print(" Caesar Cipher - Encrypt\n")
                text = input(" [+] Enter the text: ")
                order = int(input(" [+] Enter the order: "))
                print(" [-] Encrypted text: " + str(Caesar(text, order, 0)))

                key = input("\n Press any key to continue...")
            
                if key != "":
                    caesar_choice = 0
                    pass
                
            elif caesar_choice == 2:
                cls()
                print(self.banner)
                print(" Caesar Cipher - Decrypt\n")
                text = input(" [+] Enter the text: ")
                order = int(input(" [+] Enter the order: "))
                print(" [-] Decrypted text: " + str(Caesar(text, order, 1)))

                key = input("\n Press any key to continue...")
            
                if key != "":
                    caesar_choice = 0
                    pass

            elif caesar_choice == 3:
                cls()
                print(self.banner)
                print(" Caesar Cipher - Force Decrypt\n")
                text = input(" [+] Enter the text: ")
                print(" [=] Decrypted text \n" + str(Caesar(text, 0, 2)))

                key = input("\n Press any key to continue...")
            
                if key != "":
                    caesar_choice = 0
                    pass

            elif caesar_choice == 0:
                cls()
            
            cls()

        except ValueError:
            print(" Invalid value. Try again. [!] Caesar Cipher Menu")

    def AtbashTUI(self):
        try:
            cls()
            print(self.banner)
            print(" Atbash Cipher\n")
            print(" 1 Encrypt")
            print(" 2 Decrypt")
            print(" 0 Back")
            atbash_choice = int(input("\n Enter your choice: "))
                
            if atbash_choice == 1:
                cls()
                print(self.banner)
                print(" Atbash Cipher - Encrypt\n")
                text = input(" [+] Enter the text: ")
                print(" [-] Encrypted text: " + str(Atbash(text, 0)))

                key = input("\n Press any key to continue...")
            
                if key != "":
                    atbash_choice = 0
                    pass
                
            elif atbash_choice == 2:
                cls()
                print(self.banner)
                print(" Atbash Cipher - Decrypt\n")
                text = input(" [+] Enter the text: ")
                print(" [-] Decrypted text: " + str(Atbash(text, 1)))

                key = input("\n Press any key to continue...")
            
                if key != "":
                    atbash_choice = 0
                    pass

            elif atbash_choice == 0:
                cls()
                
            cls()

        except ValueError:
            print(" Invalid value. Try again. [!] Atbash Cipher Menu")

    def terminalUI(self):

        try:
            
            choice = 9

            while choice != 0:
                print(self.banner + self.menu)
                choice = None
                try:
                    choice = int(input(" Enter your choice: "))
                except ValueError:
                    cls()
                    print(self.banner + '\r\nInvalid option, try again.', end='', flush=True)
                    time.sleep(1)
                    cls()

                if choice == 1:
                    self.CaesarTUI()

                elif choice == 2:
                    self.AtbashTUI()

                elif choice == 0:
                    break

        except KeyboardInterrupt:
            print("\n Cypherx ended!")
