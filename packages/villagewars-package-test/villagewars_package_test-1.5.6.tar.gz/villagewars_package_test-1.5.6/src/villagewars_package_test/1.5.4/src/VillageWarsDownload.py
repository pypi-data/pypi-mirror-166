try:
    from PodSixNet.Connection import ConnectionListener, connection
    import toolbox
except:
    from src.PodSixNet.Connection import ConnectionListener, connection
    from src import toolbox
import os
import zipfile
import sys

import pymsgbox

print_output = True
ip = 'NOT_INITIALIZED'
FINISHED = False

def init(IP, printOutput=False):
    global print_output
    print_output = printOutput
    global ip
    ip = IP



class DownloadClient(ConnectionListener):

    def __init__(self, host, port):
        self.last_perc = 0
        self.num = 0
        self.amount = 0
        self.namelist = []
        self.running = True
        for foldername, subfolders, filenames in os.walk('../'):
            self.namelist.append(foldername)
            self.namelist.extend(filenames)
        
        ConnectionListener.__init__(self)
        self.Connect((host, port))
        
        

    def Network_open(self, data):

        self.file = open('../run/downloads/' + data['version'] + '.zip', 'wb')
        self.version = data['version']
        

    def update(self):
        connection.Pump()
        self.Pump()

    def ShutDown(self):
        self.connected = False
        connection.Close()

    def Network_downloaded(self, data):
        perc = data['num'] / data['amount'] * 100
        global print_output
        if print_output and perc != self.last_perc:
            print('Downloading - ' + str(round(perc)) + '%', data['amount'])
        self.last_perc = perc
        self.file.write(eval(data['bytes']))

        if data['num'] == data['amount']:
            self.file.close()
            if print_output:
                print('Downloaded VillageWars version ' + self.version + '!')
            self.running = False
        else:
            self.file.write(b'\n')

        self.num = data['num']
        self.amount = data['amount']
            

    def Network_connected(self, data):
        print('Connection succesful!')
        print('Updating VillageWars...')
        
        self.connected = True
        connection.Send({'action':'init', 'status':'DOWNLOAD', 'namelist':self.namelist})
        
        
        

        

    def Network_error(self, data):
        """
        Network_error runs when there is a server error
        """
        print('error:', data['error'][1])
        self.ShutDown()

    def Network_disconnected(self, data):
        """
        Network_disconnected runs when you disconnect from the server
        """
        self.ShutDown()

def main():
    global print_output, FINISHED, ip
    if print_output:
        input('This is the VillageWars updating and downloading system! Press enter to start.')
        if ip == 'NOT_INITIALIZED':
            ip = input('Enter the host\'s IP address: ')
        print('Connecting to host server...')



    port = 5555
    global client
    try:
        client = DownloadClient(ip, port)

    
        while client.running:
            client.update()
        print('Adding extra files...')

        file = zipfile.ZipFile(f'../run/downloads/{client.version}.zip', 'a')
        for name in client.namelist:
            if name.endswith('.mp3') or name.endswith('.wav'):
                file.write('../assets/sfx/' + name)
        file.close()

        if print_output:
            print('Extracting...')
            
        file = zipfile.ZipFile(f'../run/downloads/{client.version}.zip', 'r')

        os.makedirs('../../%s' % (client.version), exist_ok=True)
        file.extractall('../../%s' % (client.version))
        if print_output:
            print('Extraction Successful!')
            print('Finalizing...')
        file.close()
        if print_output:
            input(f'Downloaded VillageWars Version {client.version} Successfully, press enter to exit.')
        FINISHED = True
    except OSError as exc:
        answ = pymsgbox.confirm('An error occured while updating. Click OK to restart.')
        if answ == 'OK':
            main()
        else:
            
            FINISHED = 'failed'

if __name__ == '__main__':
    main()


def perc():
    global client
    try:
        return client.last_perc
    except NameError:
        return 0

def amount():
    global client
    try:
        return client.amount
    except NameError:
        return 1

def num():
    global client
    try:
        return client.num
    except NameError:
        return 0
