import os

import getpass
import requests as r
from tqdm import tqdm
import configparser
import ast
import traceback
import time

import subprocess

def play_mp3(file_path):
    process = subprocess.run(['start', file_path], shell=True)
    return process
# Example usage
mp3_file = "hacky_song.mp3"

import urllib3

# Disable the SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


config = configparser.ConfigParser()
config.read('config.ini')
url = config['SETTINGS']['url']
processable_files = ast.literal_eval(config['SETTINGS']['processable_files'])
play_mp3_file = ast.literal_eval(config['SETTINGS']['play_mp3'])

print('play_mp3: ' + str(play_mp3))


if bool(play_mp3_file):
    try:
        process = play_mp3(mp3_file)
    except:
        print("Error playing mp3 file")
        print(traceback.format_exc())


print(f'SETTINGS: Processable files: {processable_files}, url: {url}' )

loading_animation = '''
     ________________        Excel File       ________________
    |                |    ---------------->  |                |
    |    Computer    |                       |     FastAPI    |
    |                |                       |                |
    |     _______    |                       |     _______    |
    |    |_______|   |                       |    |_______|   |
    |________________|                       |________________|
'''

def show_onedrive_files():
    username = getpass.getuser()
    dir_path = f'C:\\Users\\{username}\\OneDrive - Siemens Energy\\EXCEL_FILES_FROM _SAP'
    for filename in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, filename)):
            print(filename)


def parse_sap_excel_to_dict():
    username = getpass.getuser()
    excel_file_path = f'C:\\Users\\{username}\\OneDrive - Siemens Energy\\EXCEL_FILES_FROM _SAP\\'
  
    print('Files that will be processed:')
    for file in processable_files:
        print(file)

    for file in tqdm(processable_files):
        excel_file_path = excel_file_path + file
        # print(' Trying to upload file: ' + excel_file_path)

        try:
            with open(excel_file_path, 'rb') as file:
                response = r.post(url, files={'file': file}, verify=False)
                # Check the response status code for success
                if response.status_code == 200:
                    print('Excel file uploaded successfully: ', response.text)
                    pass
                else:
                    print(f'Error uploading Excel file. Status code: {response.status_code}')

        except IOError as e:
            print(f'Error opening the file: {e}')


        

    
print('\n' * 1)
print('Available Excel files in OneDrive folder:')
print('-----------------------------------------')
print('''
 ___________________
 | _______________ |
 | |             | |
 | |             | |
 | |   ONEDRIVE  | |
 | |    FILES:   | |
 | |             | |
 |_________________|
     _[_______]_
 ___[___________]___
|         [_____] []|
|         [_____] []| 
L___________________J     

''')

show_onedrive_files()
print('\n' * 1)
username = getpass.getuser()    
print(f'Uploading Excel files to FastAPI from folder:' + f'C:\\Users\\{username}\\OneDrive - Siemens Energy\\EXCEL_FILES_FROM _SAP\\')
print('--------------------------------------------------------------------------------------------------------------------------------------')
print(loading_animation)

while True:
    parse_sap_excel_to_dict()
    print('\n' * 1)
    print('------------------------------------- TRANSFER FINISHED -------------------------------------')
    time.sleep(200)


