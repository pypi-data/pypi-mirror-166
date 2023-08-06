import cypherx
import argparse

def main():
    
    __version__ = '1.3.1'
    
    parser = argparse.ArgumentParser(prog="cypherx", description="CypherX - A simple and easy to use cryptography program.")

    sub_parser = parser.add_subparsers(dest="command", help="Commands")
    sub_parser.add_parser("start", help="Start the program in TUI mode.")
    
    cipher = parser.add_mutually_exclusive_group()
    cipher.add_argument("-c", "--caesar", help="Caesar Cipher", action="store_true")
    cipher.add_argument("-a", "--atbash", help="Atbash Cipher", action="store_true")
    
    encdec = parser.add_mutually_exclusive_group()
    encdec.add_argument("-e", "--encrypt", help="Encrypt a message.", action="store_true")
    encdec.add_argument("-d", "--decrypt", help="Decrypt a message.", action="store_true")
    encdec.add_argument("-f", "--force-decrypt", help="Force decrypt a message.", action="store_true")
    
    parser.add_argument("-m", "--message", help="Choose a message to encrypt/decrypt.", action="store", type=str, default=None)
    
    parser.add_argument("-k", "--key", "-o", "--order", metavar="KEY/ORDER", help="Key [Required for: Caesar]", action="store")
    parser.add_argument("--version", action="version", version="%(prog)s {}".format(__version__))

    parser.add_argument("-v", "--verbose", help="Verbose mode.", action="store_true")
    parser.add_argument("-q", "--quiet", help="Quiet mode.", action="store_true")

    args = parser.parse_args()

    cypherx.CypherX(args)

if __name__ == "__main__":
    main()