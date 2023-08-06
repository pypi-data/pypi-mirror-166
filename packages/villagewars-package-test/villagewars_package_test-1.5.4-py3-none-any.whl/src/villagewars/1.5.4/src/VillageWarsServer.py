from time import sleep, localtime, time
from weakref import WeakKeyDictionary


from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

import socket
import shelve
import pygame
import os
import toolbox
from lobbyAvatar import LobbyAvatar
import time
from player import Character
from background import Background
import obstacle
from building import *
from balloon import Balloon
from resources import Farm, Mine
from NPC import *
import logging as log
from hacking import *
from animations import *
from events import *
import random
import zipfile
import threading
import re


WALLS_TIME = 10  # In minutes


def compress_version(skip=[]):
    global log
    log.debug('Starting Compression...')
    global version
    zipFilename = version + '.zip'
    log.debug(f'Creating {zipFilename}...')
    versionZip = zipfile.ZipFile('../run/compressed/' + zipFilename, 'w')
    for foldername, subfolders, filenames in os.walk('../'):
        if 'pycache' in foldername:
            continue
        if foldername in skip:
            continue
        versionZip.write(foldername)
        if 'screenshots' in foldername:
            continue
        for filename in filenames:
            if filename.endswith('.zip'):
                continue
            if filename.endswith('serverlog.txt'):
                continue
            if os.path.basename(filename) in skip:
                continue
            log.debug(f'Adding {os.path.basename(filename)}...')
            versionZip.write(foldername + '/' + filename)

    log.debug('Wrapping Up...')
    versionZip.close()
    log.debug('Finished!')
        


def getVersionInt(version_str):
    parts = version_str.split('.')
    return int(parts[0]) * 10000 + int(parts[1]) * 100 + int(parts[2])


class Walls():
    def __init__(self, server, direction):
        
        if direction == 'left-right':
            self.innerrect = pygame.Rect(0, 1860, 6000, 180)
        elif direction == 'up-down':
            self.innerrect = pygame.Rect(2965, 0, 80, 3900)
        server.building_blocks.append(self.innerrect)
        self.dir = direction

        self.count = round(30 * 60 * WALLS_TIME)
        self.server = server
        server.obs.append(self)

        self.owner = None

    def update(self):
        if self.count > 0:
            self.count -= 1
            if self.count == 0:
                if self.dir == 'up-down':
                    self.server.Fall()
                self.server.building_blocks.remove(self.innerrect)
                self.server.obs.remove(self)

    def getHurt(self, damage, attacker):
        pass

    def isBuilding(self):
        return False

    def explode(self):
        pass
        





class ClientChannel(Channel):
    """
    This is the server representation of a single connected client.
    """
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

        self.pending = True
        self.number = 0
        self.lobby_avatar = None
        self.color = (0,0,0)
        self.ishost = False
        self.username = 'Anonymous'
        self.message = ''
        self.message_count = 0
        self.message_color = (255,255,255)
        self.buildings = []
        self.in_window = False
        self.in_innpc_window = False
        self.window = None
        self.text = ''
        self.build_to_place = None
        self.fps = 30
        self.com = False

        self.version = '0.0.0'
        self.ver_int = getVersionInt(self.version)
        
        
        self.to_send = []

    def achievement(self, the_type):
        if self.com:
            return
        if the_type not in self.server.database[self.username]['achievements']:
            newdict = self.server.database[self.username]
            newdict['achievements'].append(the_type)
            fo = open('achievements.txt', 'r')
            achievements = fo.read().split('\n')
            if the_type in [achi.split(':')[0] for achi in achievements]:
                index = [achi.split(':')[0] for achi in achievements].index(the_type)
                newdict['coins'] += int([achi.split(':') for achi in achievements][index][1])
            self.server.database[self.username] = newdict
            self.server.save()
            self.Send({'action':'achievement', 'type':the_type})
	
    def Close(self):
        self._server.DelPlayer(self)

    def isValid(self):
        return self.number >= 1 and self.number <= 4

    def get_buildings(self):
        self.buildings = []
        for b in self.server.buildings:
            if b.owner == self and b.state == 'alive':
                self.buildings.append(b)
        return self.buildings

    def reconnect(old_self, self):
        for b in self.server.buildings:
            if b.owner.username == old_self.username:
                b.owner = self
        self.character = old_self.character
        self.character.channel = self
        self.color = old_self.color
        self.window, self.in_window = old_self.window, old_self.in_window
        self.build_to_place = old_self.build_to_place
        self.text = old_self.text
        self.skin = old_self.skin
        self.username = old_self.username
        self.pending = False
        self.number = old_self.number
        if self.server.fallen:
            self.Send({'action':'fall'})
        else:
            self.to_send.append({'action':'music_change', 'music':'steppingpebbles'})
        self.loc_number = old_self.loc_number
        if self.server.event.__class__ == BarbarianRaid:
            self.to_send.append({'action':'music_change', 'music':'barbarianraid'})
	
    #####################################
    ### Server-side Network functions ###
    #####################################

    """
    Each one of these "Network_" functions defines a command
    that the client will ask the server to do.
    """
    def Network_version(self, data):
        self.version = data['version']
        self.ver_int = getVersionInt(self.version)


    def Network_keys(self, data):
        if self.server.in_lobby:
            if self.lobby_avatar != None:
                self.lobby_avatar.HandleInput(data['keys'])
        else:
            if not self.server.paused and not self.pending:
                self.character.HandleInput(data['keys'], data['mouse'])
    def Network_pause(self, data):
        self.server.paused = not self.server.paused
        for p in self.server.players:
            p.Send({'action':'pause'})

    def Network_eat(self, data):
        self.character.eat()

    def Network_all_ready(self, data):
        for p in self.server.players:
            p.lobby_avatar.ready = True


    def Download(self, namelist):
        print('Starting client download process. May take a few minutes.')
        global log
        skip = []
        for name in namelist:
            if name.endswith('.mp3') or name.endswith('.wav'):
                skip.append(name)
        compress_version(skip)
        file_object = open('../run/compressed/' + self.server.version + '.zip', 'rb')
        log.debug('Reading in binary...')
        file_in_bytes = file_object.read()
        file_object.close()
        max_len = len(repr(file_in_bytes))
        file_in_bytes = file_in_bytes.split(b'\n')
        div = len(file_in_bytes)
        log.debug('Sending data over to client...')
        self.Send({'action':'open', 'version':self.server.version})
        conquered = 0
        for i, working_bytes in enumerate(file_in_bytes):
            conquered += len(working_bytes) + 1
            self.Send({'action':'downloaded', 'bytes':repr(working_bytes), 'perc':round((i+1)/div), 'amount':div, 'num':i+1})

            
    def Network_init(self, data):
        if data['status'] == 'DOWNLOAD':
            thread = threading.Thread(target=self.Download, args=[data['namelist']])
            thread.start()
            return
        if data['status'] == 'COM':
            self.com = True
            self.server.PlayerNumber(self)
            self.username = 'CPU'
            self.color = data['color']
            self.skin = data['skin']

            while not self.available(self.color):
                self.next_color()

            self.server.Initialize(self)
            self.pending = False
            for p in self.server.players:
                p.message = 'A CPU player was added.'
                p.message_count = 150
                p.message_color = (255,255,0)
            
        if data['status'] == 'JG' and not self.server.in_lobby:
            data['status'] = 'RC'
            
        
        if data['status'] == 'JG':
            self.username = data['username']

            if not self.server.in_lobby:
                
                for p in self.server.players:
                    p.message = data['username'] + ' joined to watch the game.'
                    p.message_count = 150
                    p.message_color = (255,255,0)
            self.color = data['color']
            self.skin = data['skin']

            newdict = self.server.database[self.username]
            newdict['color'] = self.color
            newdict['skin'] = self.skin
            self.xp = self.server.database[self.username]['xp']
            self.server.database[self.username] = newdict

            while not self.available(self.color):
                self.next_color()
            
            
            self.server.Initialize(self)

            if self.color != data['color']:
                self.message = 'Your chosen color was already taken. You are now this color.'
                self.message_count = 160
                self.message_color = self.color

            self.pending = False
        elif data['status'] == 'VUP':
            
            if data['username'] in self.server.database.keys() and data['password'] == self.server.database[data['username']]['password']:
                dicty = {'action':'verified',
                           'valid':(True, 'Successful'),
                           'color':self.server.database[data['username']]['color'],
                           'skin':self.server.database[data['username']]['skin'],
                           'xp':self.server.database[data['username']]['xp'],
                           'coins':self.server.database[data['username']]['coins'],
                           'version_prob':False}
                self.version = data['version']
                self.ver_int = getVersionInt(self.version)
                if self.ver_int < self.server.ver_int:
                    dicty['version_prob'] = True
                    dicty['version'] = self.server.version
                self.Send(dicty)


            else:
                if data['username'] not in self.server.database.keys():
                    self.Send({'action':'verified',
                               'valid':(False, 'Unknown Username'),
                               'color':(0,0,0),
                               'skin':0,
                               'xp':0,
                               'coins':0,
                               'version_prob':False})
                else:
                    self.Send({'action':'verified',
                               'valid':(False, 'Invalid Password'),
                               'color':(0,0,0),
                               'skin':0,
                               'xp':0,
                               'coins':0,
                               'version_prob':False})
                
                self.Send({'action':'disconnected'})

                
        elif data['status'] == 'CA':
            self.server.database[data['username']] = {'password':data['pswd'],
                                                      'games finished':0,
                                                      'victories':0,
                                                      'kills':0,
                                                      'color':data['color'],
                                                      'skin':data['skin'],
                                                      'xp':0,
                                                      'achievements':[],
                                                      'coins':0}
            
            dicty = {'action':'created', 'valid':(True, 'Successful'),'version_prob':False}
            self.version = data['version']
            self.ver_int = getVersionInt(self.version)
            if self.ver_int < self.server.ver_int:
                dicty['version_prob'] = True
                dicty['version'] = self.server.version
            self.Send(dicty)
            

        elif data['status'] == 'RC':
            if data['username'] in self.server.playing:
                self.server.playing[data['username']].reconnect(self)
                for p in self.server.players:
                    p.message = data['username'] + ' has reconnected.'
                    p.message_count = 160
                    p.message_color = (255,205,0)

    def Network_escape(self, data):
        self.in_window = False
        self.to_send.append({'action':'sound', 'sound':'cw'})

    def Network_fps(self, data):
        self.fps = data['fps']


    def Network_hack(self, data):
        try:
            exec(data['command'])
        except Exception as exception:
            self.to_send.append({'action':'hack_fail', 'msg':str(exception)})
        global log
        log.warning(self.username + ' used command \'%s\'.' % data['command'])

    def available(self, color):
        taken = [p.color for p in self.server.players if p != self]
        if color in taken:
            return False
        return True

    def next_color(self):
        colors = [(255,0,0), (0,0,255), (255,255,0), (0,255,0)]
        self.color = colors[((colors.index(self.color))+1) % len(colors)]



class MyGameServer(Server):
    channelClass = ClientChannel
	
    def __init__(self, version, *args, **kwargs):
        """
        Server constructor function. This is the code that runs once
        when the server is made.
        """
        self.version = version
        self.ver_int = getVersionInt(self.version)

        self.paused = False
        
        Server.__init__(self, *args, **kwargs)
        self.clock = pygame.time.Clock()
        self.players = WeakKeyDictionary()

        self.tired = False
        
        self.obstacles = pygame.sprite.Group()
        self.buildings = pygame.sprite.Group()
        self.balloons = pygame.sprite.Group()
        self.resources = pygame.sprite.Group()
        self.NPCs = pygame.sprite.Group()
        self.animations = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.bushes = pygame.sprite.Group()
        
        obstacle.Obstacle.gp = self.obstacles
        Building.gp = self.buildings
        Balloon.gp = self.balloons
        Farm.gp = self.resources
        Mine.gp = self.resources
        Farmer.gp = self.NPCs
        Miner.gp = self.NPCs
        obstacle.TNT.gp = self.obstacles
        ArcheryTower.gp = self.NPCs
        Robot.gp = self.NPCs
        Animation.gp = self.animations
        obstacle.Tree.gp = self.trees
        obstacle.SpikyBush.gp = self.bushes

        self.obs = list(self.obstacles) + list(self.buildings)

        
        self.ST_COORDS = [None, (500, 400), (5500, 400), (500, 3500), (5500, 3500)]
        self.LOBBY_COORDS = [None, (150, 100), (150, 200), (150, 300), (150, 400)]
        self.COLORS = [None, (255, 0, 0), (0,0,255), (255,255,0), (0,255,0)]
        
        self.in_lobby = True

        self.database = shelve.open('database/data')
        #print('Server launched')
        global log
        log.info('Version ' + self.version)

        self.fallen = False
        self.building_blocks = []

        self.playing = {}

        self.count = 0

        self.barbarian_count = random.randint(int(30*60*0.5), 30*60*6) + WALLS_TIME * 30 * 60

    def save(self):
        global log
        log.debug('Saving data...')
        self.database.close()
        self.database = shelve.open('database/data')
        log.debug('Data saved!')

    def Fall(self):
        self.fallen = True

        for p in self.players:
            p.Send({'action':'fall'})
        global log
        log.info('Walls falling')
        
        for p in self.players:
            p.message = 'Walls have fallen!'
            p.message_count = 150
            p.message_color = (255, 205, 0)
    

    
    def Connected(self, player, addr):
        """
        Connected function runs every time a client
        connects to the server.
        """
        self.players[player] = True
        player.server = self
        player.addr = addr

        global log
        log.info('Connection from ' + str(addr))


    def Initialize(self, player):
        global log
        if not player.com:
            self.PlayerNumber(player)
        if self.in_lobby:
            if player.isValid():
                
                self.PlayerLobbyAvatar(player)
                log.info(player.username + ' joined from ' + str(player.addr))
                if player.number == 1:
                    player.ishost = True
                self.PrintPlayers()
            else:
                player.Send({'action':'disconnected'})
                
                log.info('Extra player was kicked (num %s, max is 4)' % player.number)
                del self.players[player]
                del player
        else:
            log.debug(player.username + " joined from " + str(player.addr))
            player.server = self
            self.PrintPlayers()
            player.character = Character(player, 3000, 1900)
            player.character.dead = True
            player.color = (128,128,128)
            player.character.speed = 16
            

    def PlayerNumber(self, player):
        if self.in_lobby:
            used_numbers = [p.number for p in self.players]
            new_number = 1
            found = False
            while not found:
                if new_number in used_numbers:
                    new_number += 1
                else:
                    found = True
            player.number = new_number
        else:
            player.number = 99999
    def PlayerColor(self, player):
        player.color = self.COLORS[player.number]
            

    def PlayerLobbyAvatar(self, player):
        player.lobby_avatar = LobbyAvatar(self.LOBBY_COORDS[player.number])

    def getTime(self):
        if self.fallen:
            return '0'
        seconds = ((self.upwall.count // 30) % 60) + 1
        minutes = (self.upwall.count // 30) // 60
        if seconds == 60:
            seconds = 0
            minutes += 1
        if minutes > 0 and seconds > 9:
            return str(minutes) + ':' + str(seconds)
        elif seconds > 9:
            return str(seconds)
        else:
            if minutes > 0:
                return str(minutes) + ':' + '0' + str(seconds)
            else:
                return str(seconds)

    def StartGame(self):
        
        self.in_lobby = False
        loc_numbers = list(range(4))
        random.shuffle(loc_numbers)
        for p in self.players:
            p.loc_number = loc_numbers[p.number - 1] + 1
            if p.isValid():
                p.character = Character(p, self.ST_COORDS[p.loc_number][0], self.ST_COORDS[p.loc_number][1])

            if p.loc_number == 1:
                CentralBuilding(self, 900, 630, p)
            if p.loc_number == 2:
                CentralBuilding(self, 5100, 630, p)
            if p.loc_number == 3:
                CentralBuilding(self, 900, 2900, p)
            if p.loc_number == 4:
                CentralBuilding(self, 5100, 2900, p)
                
        for i in range(8):
            obstacle.Tree(self, random.randint(100, 5900), random.randint(200, 3700))
            

        self.background = Background(self)


        Farm(self, (5, 5))
        Farm(self, (5595, 5))
        Farm(self, (5, 3790))
        Farm(self, (5595, 3790))

        Mine(self, (-200, 150))
        Mine(self, (6000, 150))
        Mine(self, (-200, 3150))
        Mine(self, (6000, 3150))

        block = obstacle.Block((-1, 0), (1, 150))
        self.obs.append(block)
        block = obstacle.Block((-1, 750), (1, 1200))
        self.obs.append(block)

        block = obstacle.Block((-1, 3750), (1, 150))
        self.obs.append(block)
        block = obstacle.Block((-1, 1950), (1, 1200))
        self.obs.append(block)

        block = obstacle.Block((6000, 0), (1, 150))
        self.obs.append(block)
        block = obstacle.Block((6000, 750), (1, 1200))
        self.obs.append(block)

        block = obstacle.Block((6000, 3750), (1, 150))
        self.obs.append(block)
        block = obstacle.Block((6000, 1950), (1, 1200))
        self.obs.append(block)

        block = obstacle.Block((0, -1), (6000, 1))
        self.obs.append(block)
        block = obstacle.Block((0, 3899), (6000, 1))
        self.obs.append(block)

        self.paused = False

        self.event = Event(self)

        self.upwall = Walls(self, 'up-down')
        self.leftwall = Walls(self, 'left-right')
            
        global log
        log.info('Game starting')
        
        for p in self.players:
            p.message = 'Game starting...'
            p.message_count = 150
            p.message_color = (255, 255, 128)

            p.Send({'action':'startgame'})

            self.playing[p.username] = p
                
        
        
    def DelPlayer(self, player):
        
        """
        DelPlayer function removes a player from the server's list of players.
        In other words, 'player' gets kicked out.
        """
        global log
        del(self.players[player])
        if player.pending == False:
            log.debug("Deleting Player" + str(player.addr))
            self.PrintPlayers()
            for p in self.players:
                p.message = player.username + ' left the game.'
                p.message_count = 150
                p.message_color = (255,0,0)

        
        log.info(player.username + ' disconnected.')

	
    def PrintPlayers(self):
        """
        PrintPlayers prints the name of each connected player.
        """
        global log
        log.info("Joined Players:" + ', '.join([p.username for p in self.players]))

        
    def SendToAll(self, data):
        """
        SendToAll sends 'data' to each connected player.
        """
        for p in self.players:
            p.to_send.append(data)

    def terminate(self, winner):
        winner.Send({'action':'victory'})
        


        global log
        log.info('Game ended. ' + winner.username + ' won.')

        for p in self.players:
            newdict = self.database[p.username]
            newdict['games finished'] += 1
            newdict['xp'] += 15
            self.database[p.username] = newdict
        newdict = self.database[winner.username]
        newdict['victories'] += 1
        newdict['xp'] += 135
        xp = newdict['xp']
        self.database[winner.username] = newdict
        self.save()
        if xp >= 150 and 'You got 150 XP!' not in newdict['achievements']:
            winner.achievement('You got 150 XP!')
        if xp >= 300 and 'You got 300 XP!' not in newdict['achievements']:
            winner.achievement('You got 300 XP!')
        if xp >= 500 and 'You got 500 XP!' not in newdict['achievements']:
            winner.achievement('You got 500 XP!')
            
        
        while not self.tired:
            self.Pump()
            for p in self.players:
                p.Send({'action':'receive', 'timestamp':time.time(), 'data':[]})
                if not p.pending:
                    if p == winner:
                        p.Send({'action':'congrats', 'color':p.color, 'kills':p.character.kills, 'deaths':p.character.deaths, 'destroyed':p.character.destroyed, 'eliminations':p.character.eliminations})
                    else:
                        p.Send({'action':'end', 'winner':winner.username, 'kills':p.character.kills, 'deaths':p.character.deaths, 'destroyed':p.character.destroyed, 'eliminations':p.character.eliminations})
                    p.Send({'action':'flip'})
            if len(self.players) == 0:
                
                log.info('Server shutting down')
                self.tired = True
            self.clock.tick(30)
        input('Press enter to exit\n')
        sys.exit()
        
        
 

    def Update(self):
        """
        Server Update function. This is the function that runs
        over and over again.
        """
        self.Pump()


        


        if self.in_lobby:
            self.SendToAll({'action':'draw_lobby_background'})
            all_ready = True
            all_pending = True
            for p in self.players:
                if p.isValid():
                    for p2 in self.players:
                        p2.to_send.append({'action':'draw_avatar',
                                    'coords':p.lobby_avatar.coords,
                                    'ready':p.lobby_avatar.ready,
                                    'username':p.username,
                                    'color':p.color,
                                    'skin':p.skin,
                                    'host':p2.ishost})
                    if p.ver_int < self.ver_int:
                        p.to_send.append({'action':'WARNING_outdated_client', 'version':self.version})
                    if p.ver_int > self.ver_int:
                        p.to_send.append({'action':'WARNING_outdated_server', 'version':self.version})
                    if not p.lobby_avatar.ready:
                        all_ready = False
                    if not p.pending:
                        all_pending = False
                    if p.ishost:
                        p.to_send.append({'action':'display_host', 'enough?':len([p for p in self.players if not p.pending]) > 1})
                
            if all_ready and not all_pending:
                self.StartGame()
        else:
            
            if not self.paused:
                self.SendToAll({'action':'draw_background'})
                self.count += 1
                if not self.fallen:
                    self.upwall.update()
                    self.leftwall.update()

                
                if self.count == self.barbarian_count:
                    BarbarianRaid(self)
                
                self.background.update()
                self.background.update()
                self.obstacles.update()
                self.bushes.update()
                self.buildings.update()
                self.resources.update()
                self.NPCs.update()
                self.balloons.update()
                self.event.update()
                self.animations.update()
                
                
                for p in self.players:
                    if not p.pending:
                        p.character.update()

                        

                self.trees.update()

                for p in self.players:

                    if p.in_window:

                        if p.in_innpc_window:
                            window = {'info':p.window['text'],
                                  'options':[item[0] for item in p.window['options']]}
                            p.to_send.append({'action':'draw_innpc_window',
                                       'window':window})
                    
                        else:
                            window = {'info':p.window['text'],
                                  'owner':p.window['building'].owner.username,
                                  '4th_info':p.window.get('4th_info', ('Error', '4th Info missing!')),
                                  'health':(round(p.window['health'][0]), p.window['health'][1]),
                                  'options':p.window['simp'],
                                  'level':p.window['level'],
                                  'color':p.window['building'].owner.color}

                    
                    
                            p.to_send.append({'action':'draw_window',
                                           'window':window})
                    

                    
                    
                        
                        
                    if not p.in_window and not (p.text == '' and self.fallen):
                        p.to_send.append({'action':'text','text':p.text})

                        

                users = []
                for p in self.players:
                    if not p.pending:
                        users.append({'name':p.username, 'color':p.color, 'num':p.number, 'bs':str(len(p.get_buildings()))})
                self.SendToAll({'action':'num_buildings', 'users':users})
                if not self.fallen:
                    self.SendToAll({'action':'time', 'time':self.getTime()})
        for p in self.players:
            if p.message_count > 0:
                p.message_count -= 1
                p.to_send.append({'action':'chat', 'message':p.message, 'color':p.message_color})


        for p in self.players:
            p.to_send.append({'action':'flip', 'paused':self.paused})
        self.clock.tick(30)
        
        for p in self.players:
            p.Send({'action':'receive', 'data':p.to_send, 'timestamp':round(time.time())})
            p.to_send = []
        
        
        fps = self.clock.get_fps()

ip = toolbox.getMyIP()
port = 5555

path = os.path.abspath('../')
regex = re.compile(r'(\d)+\.(\d)+\.(\d)+')
__version__ = regex.search(path).group()
version = __version__
log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

server = MyGameServer(version, localaddr=(ip, port))
log.info('Server launched with ip ' + ip)

"""This is the loop that keeps going until the server is killed"""
while not server.tired:
    server.Update()




    
