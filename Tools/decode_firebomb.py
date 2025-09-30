'''
This just base64 decode on the cookies.csv file in case you need it
'''

from base64 import b64decode
import argparse

def decode_file(source_path:str, dest_path:str):
    '''
    Decodes a (presumably firebomb) file from base64.
    Args:
        source_path (str): The path to the base64 encoded file
        dest_path (str): The path to write the decoded file to
    '''
    with open(source_path, "rb") as enc_file:
        with open(dest_path, "wb") as dec_file:
            encrypted_data = enc_file.read()
            decrypted_data = b64decode(encrypted_data)
            dec_file.write(decrypted_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decodes a base64 encoded file (presumably firebomb output)")
    parser.add_argument("--source", type=str, help="The path to read the base64 encoded file", required=True)
    parser.add_argument("--dest", type=str, help="The path to write the decoded file to", required=True)
    args = parser.parse_args()
    
    decode_file(args.source, args.dest)