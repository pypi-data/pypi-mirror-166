import sys
import string
import argparse
import interface as i

class CypherX:

    def __init__(self):

        if len(sys.argv) > 1:

            parser = argparse.ArgumentParser(prog="cypherx", description="CypherX - A simple and easy to use cryptography program.")


            cipher = parser.add_mutually_exclusive_group()
            cipher.add_argument("-c", "--caesar", help="Caesar Cipher", action="store_true")
            cipher.add_argument("-a", "--atbash", help="Atbash Cipher", action="store_true")
            
            encdec = parser.add_mutually_exclusive_group()
            encdec.add_argument("-e", "--encrypt", help="Encrypt a message.", action="store_true")
            encdec.add_argument("-d", "--decrypt", help="Decrypt a message.", action="store_true")
            
            parser.add_argument("-m", "--message", help="Choose a message to encrypt/decrypt.", action="store", required=True)
            parser.add_argument("-k", "--key", help="Key [Required for: Caesar]", action="store", type=int)
            parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")

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
        else:
            i.Start()

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


def main():
    CypherX()

if __name__ == "__main__":
    main()