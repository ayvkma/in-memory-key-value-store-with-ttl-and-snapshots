import copy
import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path

CLEAN_UP_INTERVAL_IN_SECONDS = 5
EXPIRATION_TIME_IN_SECONDS = 10
FILE = Path('snapshots.log')
STORE = {}

def convert_datetime_to_iso(store):
    for key in store:
        if not store[key]['expire_at']:
            store[key]['expire_at'] = ''
        else:
            expire_at_iso = store[key]['expire_at'].isoformat()
            store[key]['expire_at'] = expire_at_iso
    return store

# def load_data():
    
def clean_up():
    while True:
        now = datetime.now()
        keys = list(STORE.keys())
        
        for key in keys:
            if STORE[key]['expire_at'] and STORE[key]['expire_at'] <= datetime.now():
                del STORE[key]
    
        store = convert_datetime_to_iso(store=copy.deepcopy(STORE))
        with open(FILE, 'a') as file:
            file.write(json.dumps(store) + '\n')

        time.sleep(CLEAN_UP_INTERVAL_IN_SECONDS)
        

# TODO - LOADING PERSISTED DATA ON LOAD
                    
def main():
    thread = threading.Thread(target=clean_up, daemon=True)
    thread.start()
    
    while True:
        command = input('Enter Command: ')
        key = input('Key: ') 
        if command == 'SET':
            value = input('Value: ')
            set_expiry = input('Want to set expire time? Y/n: ')
            try:
                if set_expiry == "Y":
                    expire_at = int(input('Enter time in minutes for expiry: '))
                    expire_at = datetime.now() + timedelta(minutes=expire_at)
                    STORE[key] = {
                        "value": value,
                        "expire_at": expire_at
                    }
                elif set_expiry == "n":
                    STORE[key] = {
                        "value": value,
                        "expire_at": None
                    }
                else:
                    print('Only Y/n are supported.')
            except Exception as e:
                print('Error: ', e)
        elif command == 'GET':
            if key not in STORE or (STORE[key]['expire_at'] and STORE[key]['expire_at'] <= datetime.now()):
                print('Key Not Found.')
            else:
                print(STORE[key]['value'])
        elif command == 'DELETE':
            if key not in STORE:
                print('Key Not Found.')
            else:
                del STORE[key]
        elif command == 'EXPIRE':
            if key not in STORE:
                print('Key Not Found.')
            else:
                STORE[key]['expire_at'] = datetime.now() + timedelta(seconds=EXPIRATION_TIME_IN_SECONDS)
        elif command == 'EXIT':
            break          
        else:
            print(f'{command} command is not supported.')
        
if __name__ == '__main__':
    main()