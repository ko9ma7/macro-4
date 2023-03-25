import configparser
from SRT import SRT
import time

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

username = config['login']['username']
password = config['login']['password']
reservation_date = config['reservation']['date']
reservation_time = config['reservation']['time']
departure = config['reservation']['departure']
destination = config['reservation']['destination']
train_kind = config['reservation']['train_kind']

# Create an SRT instance
srt = SRT(username, password)

# Search for SRT train schedules
trains = srt.search_train(departure, destination, reservation_date)

# Reserve an SRT train
while True:
    try:
        res = srt.reserve(trains[0])
        break
    except Exception as e:
        print(e)
        print("Retrying...")
        time.sleep(0.2)

# Print the reservation information
print(res)