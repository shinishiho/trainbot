import configparser
import subprocess

def connect():
    config = configparser.ConfigParser()
    config.read('config.ini')
    addr = config.get('Connection', 'address')
    port = config.get('Connection', 'port')
    output = subprocess.check_output(['adb', 'connect', addr + ':' + port])
    if output.decode('utf-8').find('connected') == -1:
        print('Failed to connect to device')
        return 1
    return 0

def startup():
    output = subprocess.check_output(['adb', 'shell', 'monkey', '-p', 'air.com.pixelfederation.TrainStationGame', '-c', 'android.intent.category.LAUNCHER', '1'])
    if output.decode('utf-8').find('Error') != -1:
        print('Failed to start app')
        return 2
    return 0