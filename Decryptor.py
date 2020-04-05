import logging
import sys

from Decoders.ASCIICipher import ASCIIDecoder
from Decoders.Base64Cipher import Base64Decoder
from Decoders.CaesarCipher import CaesarDecoder
from Decoders.ReverseCipher import ReverseDecoder
from evaluator import evaluate
import argparse

ARGS_STR = """
    ___                                                 __       
   /   |   _____ ____ _ __  __ ____ ___   ___   ____   / /_ _____
  / /| |  / ___// __ `// / / // __ `__ \ / _ \ / __ \ / __// ___/
 / ___ | / /   / /_/ // /_/ // / / / / //  __// / / // /_ (__  ) 
/_/  |_|/_/    \__, / \__,_//_/ /_/ /_/ \___//_/ /_/ \__//____/  
              /____/                                             
"""


class MyParser(argparse.ArgumentParser):
    def __init__(self,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 parents=[],
                 formatter_class=argparse.HelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
                 add_help=True,
                 allow_abbrev=True):
        super().__init__(prog, usage, description, epilog, parents, formatter_class, prefix_chars,
                         fromfile_prefix_chars,
                         argument_default, conflict_handler, add_help, allow_abbrev)
        self.problem = False

    # the default status on the parent class is 0, we're
    # changing it to be 1 here ...
    def exit(self, status=1, message=None):
        if message:
            self._print_message(message, sys.stderr)
        self.problem = True
        return


DECODERS_MAP = {'ascii': ASCIIDecoder,
                'base64': Base64Decoder,
                'caesar': CaesarDecoder,
                'reverse': ReverseDecoder}


def decryptor_module(arguments):
    # Create argumentParser
    parser = MyParser(usage='%(prog)s [input] [-s]',
                      description='\nThe Ultimate Decoder, Drop your Cipher-text here\n'
                                  'just type the optional arguments that you need from the list\n\n' + ARGS_STR,
                      epilog='Just boring epilogue',
                      formatter_class=argparse.RawTextHelpFormatter,
                      )

    parser.version = '1.1'

    # Add input flag required (string or filename)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-c', '--ciphertext')
    input_group.add_argument('-f', '--filename', type=argparse.FileType('r'))

    # Specific decoder flag
    parser.add_argument('-s', '--specific',
                        help='Choose specific decoder, {%(choices)s}',
                        choices=DECODERS_MAP.keys(),
                        metavar='DECODER')

    # Evaluators flags
    parser.add_argument('-cl', '--checkLetter',
                        help='Evaluate results by letter analysis check',
                        action='store_true')

    parser.add_argument('-cw', '--checkWord',
                        help='Evaluate results by word analysis check',
                        action='store_true')

    parser.add_argument('-cf', '--checkFlag',
                        help='Evaluate results by flag format check',
                        metavar='FORMAT')

    # Version flag
    parser.add_argument('--version', action='version')

    # Verbose flag
    parser.add_argument('-v', '--verbose', help='Verbose mode', action='store_true')

    # parse arguments
    args = parser.parse_args(args=arguments)
    # If there was problem while parsing arguments
    if parser.problem:
        return ''

    if args.verbose:
        logging.basicConfig(level=logging.INFO, format='[INFO] %(message)s')

    # Get the ciphertext from CLI or file
    if args.ciphertext is not None:
        cipher_txt = args.ciphertext
    else:  # It's a file
        cipher_txt = args.filename.read()

    # If specific decoder set (else use all decoders)
    if args.specific is not None:
        logging.info('Use specific decoder: ' + args.specific)
        decoder = DECODERS_MAP[args.specific]
        return decoder(cipher_txt)

    # If specific evaluator set (else use all evaluators)
    functions_string = ['F', 'F', 'F']
    flag_format = ''
    if args.checkLetter or args.checkWord or args.checkFlag:
        if args.checkLetter:
            functions_string[0] = 'T'
            logging.info('Add specific evaluator: letter analysis')
        if args.checkWord:
            functions_string[1] = 'T'
            logging.info('Add specific evaluator: word analysis')
        if args.checkFlag:
            functions_string[2] = 'T'
            logging.info('Add specific evaluator: flag search')
            flag_format = args.checkFlag
        functions_string = ''.join(functions_string)
    else:
        logging.info('Use all evaluators')
        functions_string = 'TFT'  ##############Change this to TTT!!!!!!!!!!!!

    # Try all decoders
    plaintexts = []
    logging.info('Decode ciphertext by Caesar decoder')
    plaintexts += CaesarDecoder(cipher_txt)
    logging.info('Decode ciphertext by ASCII decoder')
    plaintexts += ASCIIDecoder(cipher_txt)
    logging.info('Decode ciphertext by Base64 decoder')
    plaintexts += Base64Decoder(cipher_txt)
    logging.info('Decode ciphertext by Reverse decoder')
    plaintexts += ReverseDecoder(cipher_txt)

    return 'Result:\n' + evaluate(plaintexts, functions_string, flag_format)[0][0]
