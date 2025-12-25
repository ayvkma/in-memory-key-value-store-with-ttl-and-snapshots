import copy
import json
import time
import uuid
import threading
from datetime import datetime, timedelta
from pathlib import Path

CLEAN_UP_INTERVAL_IN_SECONDS = 60
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

def convert_iso_to_datetime(store):
    for key in store:
        if not store[key]['expire_at']:
            store[key]['expire_at'] = None
        else:
            expire_at_iso = datetime.fromisoformat(store[key]['expire_at'])
            store[key]['expire_at'] = expire_at_iso
    return store
    
def clean_up():
    while True:
        now = datetime.now()
        keys = list(STORE.keys())
        
        for key in keys:
            if STORE[key]['expire_at'] and STORE[key]['expire_at'] <= datetime.now():
                del STORE[key]

        try:
            if STORE != {}:
                store = convert_datetime_to_iso(store=copy.deepcopy(STORE))
                lines = None
                with open(FILE, 'r') as file:
                    lines = file.readlines()
                new_file = Path(str(uuid.uuid4()) + '.log')
                with open(new_file, 'w') as file:
                    for line in lines:
                        file.write(line)
                    file.write(json.dumps(store) + '\n')
                new_file.replace(FILE)

        except Exception as e:
            print('Error: ', e)

        time.sleep(CLEAN_UP_INTERVAL_IN_SECONDS)
        
def load_data(FILE) -> dict:
    with open(FILE, '+a') as file:
        # Move the file pointer to the beginning to read all contents
        file.seek(0)
        lines = file.readlines()
        if len(lines) < 1:
            return {}
        last_recorded_snapshot = lines[-1].strip('\n\r')
        store = json.loads(last_recorded_snapshot)
        store = convert_iso_to_datetime(store)
        return store
    
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
    # Load on start
    STORE = load_data(FILE)
    main()