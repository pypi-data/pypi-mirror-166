#!/usr/bin/python3

import sys
import string
import argparse

import time
import os
from rich import print

class CypherX:

    def __init__(self):

        if len(sys.argv) >= 1:

            parser = argparse.ArgumentParser(prog="cypherx", description="CypherX - A simple and easy to use cryptography program.")

            parser.add_argument(dest="start", help="Start the program in TUI mode.", action="store", default='start')

            cipher = parser.add_mutually_exclusive_group()
            cipher.add_argument("-c", "--caesar", help="Caesar Cipher", action="store_true")
            cipher.add_argument("-a", "--atbash", help="Atbash Cipher", action="store_true")
            
            encdec = parser.add_mutually_exclusive_group()
            encdec.add_argument("-e", "--encrypt", help="Encrypt a message.", action="store_true")
            encdec.add_argument("-d", "--decrypt", help="Decrypt a message.", action="store_true")
            
            parser.add_argument("-m", "--message", help="Choose a message to encrypt/decrypt.", action="store", type=str, default=None)
            
            parser.add_argument("-k", "--key", help="Key [Required for: Caesar]", action="store", type=int)
            parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.2")

            args = parser.parse_args()

            if args.caesar:
                if args.encrypt:
                    if args.key and args.message:
                        print(Caesar(args.message, int(args.key), 0))
                    else:
                        print("[!] Error: Missing key arguments.")
                elif args.decrypt:
                    if args.key and args.message:
                        print(Caesar(args.message, int(args.key), 1))
                    else:
                        print("[!] Error: Missing key arguments.")
                else:
                    print("[!] Error: You must choose between encrypt or decrypt.")
            elif args.atbash:
                if args.encrypt:
                    if args.message:
                        print(Atbash(args.message, 0))
                elif args.decrypt:
                    if args.message:
                        print(Atbash(args.message, 1))
                else:
                    print("[!] Error: You must choose between encrypt or decrypt.")
            elif args.start == 'start':
                StartTUI()
class Caesar:

    def __init__(self, text, order, mod):
        self.text, self.order, self.mod = text, order, mod
        self.order = order
        
        self.alphabet = string.ascii_lowercase
        self.alphabet_upper = string.ascii_uppercase

        if self.mod == 0:
            self.data = self.encrypt()
        elif self.mod == 1:
            self.data = self.decrypt()
        elif self.mod == 2:
            self.data = self.force()
        else:
            raise ValueError("Invalid mod")
    
    def encrypt(self):
        encrypted = ""
        for char in self.text:
            if char in self.alphabet:
                encrypted += self.alphabet[(self.alphabet.index(char) + self.order) % 26]
            elif char in self.alphabet_upper:
                encrypted += self.alphabet_upper[(self.alphabet_upper.index(char) + self.order) % 26]
            else:
                encrypted += char
        return encrypted
    
    def decrypt(self):
        decrypted = ""
        for char in self.text:
            if char in self.alphabet:
                decrypted += self.alphabet[(self.alphabet.index(char) - self.order) % 26]
            elif char in self.alphabet_upper:
                decrypted += self.alphabet_upper[(self.alphabet_upper.index(char) - self.order) % 26]
            else:
                decrypted += char
        return decrypted

    def force(self):
        forced_data = ""
        for i in range(26):
            self.order = i
            forced_data += str(" [-] " + self.decrypt() + "\n")

        return forced_data

    def __str__(self):
        return self.data

class Atbash:

    def __init__(self, text=str, mod=int) -> None:
        self.__text = text
        self.__mod = mod

        self.alphabet = string.ascii_lowercase
        self.alphabet_upper = string.ascii_uppercase

        if self.__mod == 0:
            self.data = self.encrypt()
        elif self.__mod == 1:
            self.data = self.decrypt()
        else:
            raise ValueError("Invalid mod")

    def encrypt(self):
        encrypted = ""
        for char in self.__text:
            if char in self.alphabet:
                encrypted += self.alphabet[25 - self.alphabet.index(char)]
            elif char in self.alphabet_upper:
                encrypted += self.alphabet_upper[25 - self.alphabet_upper.index(char)]
            else:
                encrypted += char
        return encrypted

    def decrypt(self):
        decrypted = ""
        for char in self.__text:
            if char in self.alphabet:
                decrypted += self.alphabet[25 - self.alphabet.index(char)]
            elif char in self.alphabet_upper:
                decrypted += self.alphabet_upper[25 - self.alphabet_upper.index(char)]
            else:
                decrypted += char
        return decrypted
    
    def __str__(self):
        return self.data

class StartTUI:

    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')

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
            self.cls()
            print(self.banner)
            print(" Caesar Cipher\n")
            print(" 1. Encrypt")
            print(" 2. Decrypt")
            print(" 3. Force Decrypt")
            print(" 0. Back")
            caesar_choice = int(input("\n Enter your choice: "))

            if caesar_choice == 1:
                self.cls()
                print(self.banner)
                print(" Caesar Cipher - Encrypt\n")
                text = input(" [+] Enter the text: ")
                order = int(input(" [+] Enter the key: "))
                print(" [-] Encrypted text: " + str(Caesar(text, order, 0)))

                key = input("\n Press any key to continue...")
            
                if key != "":
                    caesar_choice = 0
                    pass
                
            elif caesar_choice == 2:
                self.cls()
                print(self.banner)
                print(" Caesar Cipher - Decrypt\n")
                text = input(" [+] Enter the text: ")
                order = int(input(" [+] Enter the key: "))
                print(" [-] Decrypted text: " + str(Caesar(text, order, 1)))

                key = input("\n Press any key to continue...")
            
                if key != "":
                    caesar_choice = 0
                    pass

            elif caesar_choice == 3:
                self.cls()
                print(self.banner)
                print(" Caesar Cipher - Force Decrypt\n")
                text = input(" [+] Enter the text: ")
                print(" [=] Decrypted text \n" + str(Caesar(text, 0, 2)))

                key = input("\n Press any key to continue...")
            
                if key != "":
                    caesar_choice = 0
                    pass

            elif caesar_choice == 0:
                self.cls()
            
            self.cls()

        except ValueError:
            print(" Invalid value. Try again. [!] Caesar Cipher Menu")

    def AtbashTUI(self):
        try:
            self.cls()
            print(self.banner)
            print(" Atbash Cipher\n")
            print(" 1 Encrypt")
            print(" 2 Decrypt")
            print(" 0 Back")
            atbash_choice = int(input("\n Enter your choice: "))
                
            if atbash_choice == 1:
                self.cls()
                print(self.banner)
                print(" Atbash Cipher - Encrypt\n")
                text = input(" [+] Enter the text: ")
                print(" [-] Encrypted text: " + str(Atbash(text, 0)))

                key = input("\n Press any key to continue...")
            
                if key != "":
                    atbash_choice = 0
                    pass
                
            elif atbash_choice == 2:
                self.cls()
                print(self.banner)
                print(" Atbash Cipher - Decrypt\n")
                text = input(" [+] Enter the text: ")
                print(" [-] Decrypted text: " + str(Atbash(text, 1)))

                key = input("\n Press any key to continue...")
            
                if key != "":
                    atbash_choice = 0
                    pass

            elif atbash_choice == 0:
                self.cls()
                
            self.cls()

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
                    self.cls()
                    print(self.banner + '\r\nInvalid option, try again.', end='', flush=True)
                    time.sleep(1)
                    self.cls()

                if choice == 1:
                    self.CaesarTUI()

                elif choice == 2:
                    self.AtbashTUI()

                elif choice == 0:
                    break

        except KeyboardInterrupt:
            print("\n Cypherx ended!")
