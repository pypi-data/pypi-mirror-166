#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import string

import time
import os
from rich import print
from rich.console import Console
from rich.layout import Layout
from rich.live import Live

class CypherX:

    def __init__(self, args):
        
        self.console = Console()

        if len(sys.argv) >= 1:
            
            self.__version__ = '1.3.1'

            if args.caesar:
                if args.encrypt:
                    if args.key and args.message:
                        if args.verbose:
                            print(f"[bold gray]\nCypherX version {self.__version__}[/bold gray]. [bold red]Caesar[/bold red] cipher, [bold green]encrypt[/bold green] method in [bold yellow]verbose[/bold yellow] mode.\n")
                        elif args.quiet:
                            pass
                        else:
                            print(f"[bold gray]\nCypherX version {self.__version__}[/bold gray]. [bold red]Caesar[/bold red] cipher, [bold green]encrypt[/bold green] method in [bold yellow]normal[/bold yellow] mode.\n")
                            
                        with self.console.status("[bold green] Encrypting...[/bold green]",) as status:
                            caesar = Caesar(args.message, int(args.key), 0)
                            time.sleep(1)

                        if args.verbose:
                            print(f"[bold][\N{check mark}] Message encrypted successfully![/bold]", end="\n", flush=True)
                            print(f"\n[gray][+] Message:[/gray] [bold yellow]{args.message}[/bold yellow]")
                            print(f"[gray][+] Key/Order:[/gray] [bold orange]{args.key}[/bold orange]")
                            print(f"[gray][=] Encrypted message:[/gray] [bold green]{caesar}[/bold green]")
                            print(f"\n[gray][\N{check mark}][/gray][bold green] Done![/bold green]")
                        
                        elif args.quiet:
                            print(caesar)
                        
                        else:
                            print(f"[bold][\N{check mark}] Message encrypted successfully![/bold]", end="\n\n", flush=True)
                            print(f"[gray][=] Encrypted message:[/gray] [bold green]{caesar}[/bold green]")
                            print(f"\n[gray][\N{check mark}][/gray][bold green] Done![/bold green]")
                    
                    else:
                        print("[!] Error: Missing key arguments.\nUse 'cypherx -h' for more information.")
                
                elif args.decrypt:
                    if args.key and args.message:
                        if args.verbose:
                            print(f"[bold gray]\nCypherX version {self.__version__}[/bold gray]. [bold red]Caesar[/bold red] cipher, [bold green]decrypt[/bold green] method in [bold yellow]verbose[/bold yellow] mode.\n")
                        elif args.quiet:
                            pass
                        else:
                            print(f"[bold gray]\nCypherX version {self.__version__}[/bold gray]. [bold red]Caesar[/bold red] cipher, [bold green]decrypt[/bold green] method in [bold yellow]normal[/bold yellow] mode.\n")
                            
                        with self.console.status("[bold green] Decrypting...[/bold green]",) as status:
                            caesar = Caesar(args.message, int(args.key), 1)
                            time.sleep(1)

                        if args.verbose:
                            print(f"[bold][\N{check mark}] Message decrypted successfully![/bold]", end="\n", flush=True)
                            print(f"\n[gray][+] Message:[/gray] [bold yellow]{args.message}[/bold yellow]")
                            print(f"[gray][+] Key/Order:[/gray] [bold orange]{args.key}[/bold orange]")
                            print(f"[gray][=] Decrypted message:[/gray] [bold green]{caesar}[/bold green]")
                            print(f"\n[gray][\N{check mark}][/gray][bold green] Done![/bold green]")
                        
                        elif args.quiet:
                            print(caesar)
                        
                        else:
                            print(f"[bold][\N{check mark}] Message encrypted successfully![/bold]", end="\n\n", flush=True)
                            print(f"[gray][=] Encrypted message:[/gray] [bold green]{caesar}[/bold green]")
                            print(f"\n[gray][\N{check mark}][/gray][bold green] Done![/bold green]")
                    else:
                        print("[!] Error: Missing key arguments.\nUse 'cypherx -h' for more information.")

                elif args.force_decrypt:
                    if args.message != None or args.message != "":
                        if args.verbose:
                            print(f"[bold gray]\nCypherX version {self.__version__}[/bold gray]. [bold red]Caesar[/bold red] cipher, [bold green]decrypt[/bold green] method in [bold yellow]verbose[/bold yellow] mode.\n")
                        elif args.quiet:
                            pass
                        else:
                            print(f"[bold gray]\nCypherX version {self.__version__}[/bold gray]. [bold red]Caesar[/bold red] cipher, [bold green]decrypt[/bold green] method in [bold yellow]normal[/bold yellow] mode.\n")
                            
                        with self.console.status("[bold green] Decrypting...[/bold green]",) as status:
                            caesar = Caesar(args.message, args.key, 2).force()
                            time.sleep(1)
                        
                        if args.verbose:
                            print(f"[bold][\N{check mark}] Message decrypted successfully![/bold]", end="\n", flush=True)
                            print(f"\n[gray][+] Message:[/gray] [bold yellow]{args.message}[/bold yellow]\n")
                            for d in caesar:
                                print(f"[gray][-] Decrypted message:[/gray] [bold green]{d}[/bold green]")
                            print(f"\n[gray][\N{check mark}][/gray][bold green] Done![/bold green]")
                        elif args.quiet:
                            print(caesar)
                        else:
                            print(f"[bold][\N{check mark}] Message encrypted successfully![/bold]", end="\n\n", flush=True)
                            for d in caesar:
                                print(f"[gray][-] Decrypted message:[/gray] [bold green]{d}[/bold green]")
                            print(f"\n[gray][\N{check mark}][/gray][bold green] Done![/bold green]")

                else:
                    print("[!] Error: You must choose between encrypt or decrypt.")
            elif args.atbash:

                if args.verbose:
                    print(f"[bold gray]\nCypherX version {self.__version__}[/bold gray]. [bold red]Atbash[/bold red] cipher, [bold green]encrypt[/bold green] method in [bold yellow]verbose[/bold yellow] mode.\n")
                elif args.quiet:
                    pass
                else:
                    print(f"[bold gray]\nCypherX version {self.__version__}[/bold gray]. [bold red]Atbash[/bold red] cipher, [bold green]encrypt[/bold green] method in [bold yellow]normal[/bold yellow] mode.\n")
                    
                if args.encrypt:  
                    with self.console.status("[bold green] Encrypting...[/bold green]",) as status:
                        atbash = Atbash(args.message, 0)
                        time.sleep(1)

                    if args.message:
                        if args.verbose:
                            print(f"[bold][\N{check mark}] Message encrypted successfully![/bold]", end="\n", flush=True)
                            print(f"\n[gray][+] Message:[/gray] [bold yellow]{args.message}[/bold yellow]")
                            print(f"[gray][=] Encrypted message:[/gray] [bold green]{atbash}[/bold green]")
                            print(f"\n[gray][\N{check mark}][/gray][bold green] Done![/bold green]")
                        elif args.quiet:
                            print(atbash)
                        else:
                            print(f"[bold][\N{check mark}] Message encrypted successfully![/bold]", end="\n\n", flush=True)
                            print(f"[gray][=] Encrypted message:[/gray] [bold green]{atbash}[/bold green]")
                            print(f"\n[gray][\N{check mark}][/gray][bold green] Done![/bold green]")

                elif args.decrypt:
                    with self.console.status("[bold green] Decrypting...[/bold green]",) as status:
                        atbash = Atbash(args.message, 1)
                        time.sleep(1)

                    if args.message:
                        if args.verbose:
                            print(f"[bold][\N{check mark}] Message decrypted successfully![/bold]", end="\n", flush=True)
                            print(f"\n[gray][+] Message:[/gray] [bold yellow]{args.message}[/bold yellow]")
                            print(f"[gray][=] Decrypted message:[/gray] [bold green]{atbash}[/bold green]")
                            print(f"\n[gray][\N{check mark}][/gray][bold green] Done![/bold green]")
                        elif args.quiet:
                            print(atbash)
                        else:
                            print(f"[bold][\N{check mark}] Message decrypted successfully![/bold]", end="\n\n", flush=True)
                            print(f"[gray][=] Decrypted message:[/gray] [bold green]{atbash}[/bold green]")
                            print(f"\n[gray][\N{check mark}][/gray][bold green] Done![/bold green]")
                else:
                    print("[!] Error: You must choose between encrypt or decrypt.")
            elif args.command == 'start':
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
        forced_data = []
        for i in range(26):
            self.order = i
            forced_data.append(self.decrypt())

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
            raise ValueError("[!] Invalid mod")

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
            " ░       ░ ░                                               [/bold green]")

        self.menu = str("\n Welcome to [link=https://github.com/yuritorresf/cypherx.git][green]CypherX[/green][/link], a simple and easy \r to use cryptography program.\n\n" +
            " Choice an option:\n\n" +
            " [bold]1 - Caesar\n" +
            " 2 - Atbash\n" +
            " 0 - [red]Exit[/red]\n[/bold]"
        )

        self.terminalUI()


    def CaesarTUI(self):
        try:
            try:
                self.cls()
                print(self.banner)
                print(" Caesar Cipher\n")
                print(" 1 - Encrypt")
                print(" 2 - Decrypt")
                print(" 3 - Force Decrypt")
                print(" 0 - [bold red]Back[/bold red]")
                caesar_choice = int(input("\n [=] Enter your choice: "))

                if caesar_choice == 1:
                    self.cls()
                    print(self.banner)
                    print(" Caesar Cipher - Encrypt\n")
                    text = input(" [+] Enter the text: ")
                    order = int(input(" [+] Enter the key: "))
                    print(" [-] Encrypted text: " + str(Caesar(text, order, 0)))

                    key = input("\n [!] Press any key to continue...")
                
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

                    key = input("\n [!] Press any key to continue...")
                
                    if key != "":
                        caesar_choice = 0
                        pass

                elif caesar_choice == 3:
                    self.cls()
                    print(self.banner)
                    print(" Caesar Cipher - Force Decrypt\n")
                    text = input(" [+] Enter the text: ")
                    print()
                    caesar = Caesar(text, 0, 2).force()
                    for c in caesar:
                        print(" [-] Decrypted text: " + str(c))

                    key = input("\n [!] Press any key to continue...")
                
                    if key != "":
                        caesar_choice = 0
                        pass

                elif caesar_choice == 0:
                    self.cls()
                
                self.cls()

            except ValueError:
                print(" [!] Invalid value. Try again. Caesar Cipher Menu")
        except KeyboardInterrupt:
            print("\n\n Cypherx ended!")

    def AtbashTUI(self):
        try:
            try:
                self.cls()
                print(self.banner)
                print(" Atbash Cipher\n")
                print(" 1 - Encrypt")
                print(" 2 - Decrypt")
                print(" 0 - [bold red]Back[/bold red]")
                atbash_choice = int(input("\n [=] Enter your choice: "))
                    
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

                    key = input("\n [!] Press any key to continue...")
                
                    if key != "":
                        atbash_choice = 0
                        pass

                elif atbash_choice == 0:
                    self.cls()
                    
                self.cls()

            except ValueError:
                print(" [!] Invalid value. Try again. Atbash Cipher Menu")

        except KeyboardInterrupt:
            print("\n\n Cypherx ended!")

    def terminalUI(self):

        try:
            
            choice = 9

            while choice != 0:
                print(self.banner + self.menu)
                choice = None
                try:
                    choice = int(input(" [=] Enter your choice: "))
                except ValueError:
                    self.cls()
                    print(self.banner + '\r\n [!] Invalid option, try again.', end='', flush=True)
                    time.sleep(1)
                    self.cls()

                if choice == 1:
                    self.CaesarTUI()

                elif choice == 2:
                    self.AtbashTUI()

                elif choice == 0:
                    break

        except KeyboardInterrupt:
            print("\n\n Cypherx ended!")
