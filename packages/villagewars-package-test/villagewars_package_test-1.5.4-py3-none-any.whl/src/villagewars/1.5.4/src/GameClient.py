import pygame
import pygame as p
from pygame.locals import *

import random
import time
import threading
import re
import sys
import os
from pymsgbox import alert, confirm, prompt, password

try:
    from PodSixNet.Connection import ConnectionListener, connection
    import toolbox as t
except:
    from src.PodSixNet.Connection import ConnectionListener, connection
    from src import toolbox as t

toolbox = t

answer = ''

def hack():
    command = prompt('Enter the command:', title='VillageWars Console')
    if command is not None:
        connection.Send({'action':'hack', 'command':command})

def find_cursor(cursor_param):
    regex = re.compile(r'constant: SYSTEM_CURSOR_(.*)\)>')
    res = regex.search(repr(cursor_param))
    return res.group(1)


class MyGameClient(ConnectionListener):
    def __init__(self, host, port, screen, clock, username, version, color, skin):

        """
        Client constructor function. This is the code that runs once
        when a new client is made.
        """
        ConnectionListener.__init__(self)

        self.color = color
        # Start the game
        pygame.init()
        pygame.mixer.pre_init(buffer=64)
        game_width = 1000
        game_height = 650
        self.started = False
        self.screen = screen
        self.clock = clock
        self.skin = skin

        self.fps_expected = 30

        self.toDraw = []
        self.toDrawNext = []

        self.disconnected = 0

        self.back_pic = p.image.load('../assets/BG_SciFi.png')
        self.ocean_pics = [p.transform.scale(p.image.load('../assets/ocean/' + i), (1000, 1000)) for i in os.listdir('../assets/ocean/')]
        self.ocean_frame = 0
        self.players = [(p.transform.scale(p.image.load('../assets/Skins/%s.png' % (i)), (50, 50)), p.transform.scale(p.image.load('../assets/Skins/%sh.png' % (i)), (50, 50))) for i in range(len(os.listdir('../assets/Skins'))//2)]
        self.archer = p.transform.scale(p.image.load('../assets/Enemy_04.png'), (50, 50))

        self.bolt = p.image.load('../assets/barbarians/bolt.png')

        self.startgame_icon = p.image.load('../assets/Startgame_btn.png')
        self.startgame_icon_over = p.image.load('../assets/Startgame_btn_over.png')
        self.startgame_icon_locked = p.image.load('../assets/Startgame_btn_locked.png')

        self.balloon = p.image.load('../assets/balloon.png')
        self.op_balloon = p.image.load('../assets/balloon2.png')
        self.speedy_plus_op = p.image.load('../assets/Drop.png')
        self.speedy_balloon = p.image.load('../assets/DropSmall.png')
        self.robot = p.transform.scale(p.image.load('../assets/Enemy_05.png'), (50, 50))
        self.robot_hurt = p.transform.scale(p.image.load('../assets/Enemy_05_hurt.png'), (50, 50))

        self.animations = {
            'Splash':(p.image.load('../assets/splash1.png'), p.image.load('../assets/splash2.png'), p.image.load('../assets/splash3.png')),
            'Explosion':(p.image.load('../assets/explode1.png'), p.image.load('../assets/explode2.png'), p.image.load('../assets/explode3.png')),
            'BAM':(p.transform.scale(p.image.load('../assets/LargeExplosion1.png'), (360, 360)), p.transform.scale(p.image.load('../assets/LargeExplosion1.png'), (360, 360)), p.transform.scale(p.image.load('../assets/LargeExplosion2.png'), (360, 360)), p.transform.scale(p.image.load('../assets/LargeExplosion2.png'), (360, 360)), p.transform.scale(p.image.load('../assets/LargeExplosion3.png'), (360, 360)), p.transform.scale(p.image.load('../assets/LargeExplosion3.png'), (360, 360)))
            }

        self.paused_image = p.image.load('../assets/paused.png')
        
        self.red = p.image.load('../assets/buildings/red.png')
        self.blue = p.image.load('../assets/buildings/blue.png')
        self.green = p.image.load('../assets/buildings/green.png')
        self.yellow = p.image.load('../assets/buildings/yellow.png')
        self.preview = p.image.load('../assets/buildings/preview.png')

        self.house = p.image.load('../assets/buildings/House.png')
        self.house_burnt = p.image.load('../assets/buildings/House_burnt.png')

        self.building_person = p.transform.scale(p.image.load('../assets/Skins/4.png'), (50, 50))
  
        self.miner = p.transform.scale(p.image.load('../assets/Skins/2.png'), (50, 50))
        self.farmer = p.transform.scale(p.image.load('../assets/Skins/4.png'), (50, 50))

        self.barbarians = {
            'leader':[p.image.load('../assets/barbarians/leader.png'), p.image.load('../assets/barbarians/leaderh.png'), p.image.load('../assets/barbarians/leaderm.png')],
            'archer':[p.image.load('../assets/barbarians/archer.png'), p.image.load('../assets/barbarians/archerh.png')],
            'swordsman':[p.image.load('../assets/barbarians/swordsman.png'), p.image.load('../assets/barbarians/swordsmanh.png')]
            }
        self.shield = p.image.load('../assets/barbarians/shield.png')
        self.barbarian_banner = p.transform.scale(p.image.load('../assets/barbarians/banner.png'), (45, 90))

        for i, b in enumerate(self.barbarians['leader']):
            self.barbarians['leader'][i] = p.transform.scale(b, (50, 50))
        for i, b in enumerate(self.barbarians['archer']):
            self.barbarians['archer'][i] = p.transform.scale(b, (50, 50))
        for i, b in enumerate(self.barbarians['swordsman']):
            self.barbarians['swordsman'][i] = p.transform.scale(b, (50, 50))
        
        self.startgame_rect = self.startgame_icon.get_rect(topleft=(445, 400))

        self.Setting = p.image.load('../assets/Setting_walls.png')

        self.food_image = p.image.load('../assets/food.png')
        self.food_used = p.image.load('../assets/food_used.png')
        self.food_mine = p.image.load('../assets/food_mine.png')

        self.plate = p.transform.scale(p.image.load('../assets/meals/plate.png'), (100, 100))
        self.meals = [
            p.transform.scale(p.image.load('../assets/meals/meal1.png'), (100, 100)),
            p.transform.scale(p.image.load('../assets/meals/meal2.png'), (100, 100)),
            p.transform.scale(p.image.load('../assets/meals/meal3.png'), (100, 100)),
            p.transform.scale(p.image.load('../assets/meals/meal4.png'), (100, 100)),
                     ]
        self.meals = [p.transform.scale(p.image.load('../assets/meals/meal%s.png' % (num - 1)), (100, 100)) for num in range(len(os.listdir('../assets/meals'))) if num not in (0, 1)]

        self.gold_image = p.transform.scale(p.image.load('../assets/gold.png'), (45, 45))
        self.gold_mine = p.transform.scale(p.image.load('../assets/gold_mine.png'), (45, 45))

        self.mine = p.image.load('../assets/mine.png')

        self.x = p.image.load('../assets/x.png')
        self.x_hov = p.image.load('../assets/x_hov.png')

        self.tree = p.transform.scale(p.image.load('../assets/trees/tree1.png'), (200, 280))
        self.sappling = p.image.load('../assets/trees/sappling.png')

        self.large_font = p.font.SysFont('default', 80)
        self.medium_font = p.font.SysFont('default', 40)
        self.small_font = p.font.SysFont('default', 20)

        self.crate = p.transform.scale(p.image.load('../assets/crate.png'), (50, 50))
        
        self.tnt = p.transform.scale(p.image.load('../assets/TNT.png'), (50, 50))
        self.gate = p.image.load('../assets/gate.png')
        self.spiky_bush = p.image.load('../assets/spiky_bush.png')

        self.ready_text = self.small_font.render('READY', True, (0,255,0))
        self.not_ready_text = self.small_font.render('NOT READY', True, (255,0,0))

        self.host_text = self.small_font.render('host', True, (255,0,0))
        self.escape_count = 0
        self.connected = False
        self.username = username

        p.mixer.init()
        self.sound_be = pygame.mixer.Sound('../assets/sfx/explosion-big.wav')
        self.sound_se = pygame.mixer.Sound('../assets/sfx/explosion-small.wav')
        self.sound_sp = pygame.mixer.Sound('../assets/sfx/splash.wav')
        self.sound_sh = pygame.mixer.Sound('../assets/sfx/splash-heavy.wav')
        self.sound_shot = pygame.mixer.Sound('../assets/sfx/shot.wav')
        self.sound_bump = pygame.mixer.Sound('../assets/sfx/bump.wav')
        self.sound_bb = pygame.mixer.Sound('../assets/sfx/building.wav')
        self.sound_ow = pygame.mixer.Sound('../assets/sfx/open_window.wav')
        self.sound_cw = pygame.mixer.Sound('../assets/sfx/close_window.wav')

        self.musics = {
            'steppingpebbles':'../assets/sfx/stepPebblesLoop.mp3',
            'village':'../assets/sfx/villageLoop.mp3',
            'barbarianraid':'../assets/sfx/War song.mp3'
            }

        self.paused = False

        with open('tips.txt') as tipfile:
            self.tips = [line.replace('\n', '') for line in tipfile]
        self.tip_frame = 0
        self.tip = 0


        self.achievement_pic = p.transform.scale(p.image.load('../assets/achievement.png'), (225, 50))
        
        self.achievement = [0, 'None']
        

        self.Connect((host, port))

        self.version = version
        connection.Send({'action':'version', 'version':self.version})

    def update(self):
        """
        Client update function. This is the function that runs over and
        over again, once every frame of the game.
        """
        self._connected = False
        connection.Pump()
        self.Pump()
        global running

        if answer == 'OK':
            self.connected = False
            connection.Close()
            p.quit()
            exit()

        global cursor
        old_cursor = p.mouse.get_cursor()
        if not find_cursor(cursor) == find_cursor(old_cursor):
            p.mouse.set_cursor(cursor)
        cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)

        if self.achievement[0]:
            self.achievement[0] -= 1
            if self.achievement[0] >= 90:
                x = (225/30) * (120-self.achievement[0])
            elif self.achievement[0] <= 30:
                x = (225/30) * self.achievement[0]
            else:
                x = 225
            self.toDraw.append((self.achievement_pic, (1000-x, 55)))
            text = self.small_font.render(self.achievement[1], True, (0,0,0))
            text_rect = text.get_rect(midtop = (1120-x, 85))
            self.toDraw.append([text, text_rect])

        if not self._connected:
            self.disconnected += 1
        else:
            self.disconnected = 0

        if self.escape_count:
            self.escape_count -= 1

        if self.disconnected == 50:
            p.mixer.music.stop()
            self.screen.blit(p.image.load('../assets/Disconnected.png'), (0, 0))
            pygame.display.flip()
            
            while True:                
                for e in p.event.get():
                    if e.type == QUIT:
                        p.quit()
                        sys.exit()
                        
                fps = self.clock.get_fps()
                self.clock.tick(30)
                pygame.display.set_caption("SuperShooterWar fps: " + str(fps))
        
        self.tip_frame += 1
        if self.tip_frame == 250:
            self.tip_frame = 0
            self.tip += 1
            if self.tip == len(self.tips):
                self.tip = 0
                random.shuffle(self.tips)
                if 'Always get a Miner\'s Guild and a Farmer\'s Guild first!' in self.tips:
                    self.tips.remove('Always get a Miner\'s Guild and a Farmer\'s Guild first!')

        
        # Set running to False if the player clicks the X
        global music_playing
        for event in pygame.event.get():
            if event.type == QUIT:
                def confirm_exit():
                    global answer
                    answer = confirm('The game is still going. Are you sure you want to quit?')
                thread = threading.Thread(target=confirm_exit)
                thread.start()
                
            if event.type == KEYUP and event.key == K_F1 and self.started:
                music_playing = not music_playing
                if music_playing:
                    p.mixer.music.pause()
                else:
                    p.mixer.music.play(-1, 0.0)
            if event.type == KEYUP and event.key == K_ESCAPE:
                connection.Send({'action':'escape'})
            if event.type == KEYUP and event.key == K_F2:
                num = len(os.listdir('../run/screenshots')) + 1
                name = 'sreenshot' + str(num)
                p.image.save(self.screen, '../run/screenshots/%s.png' % (name))
                alert('Screenshot saved as %s.png' % (name))
            if event.type == KEYUP and event.key == K_F10:
                hack()
                
            if event.type == KEYUP and event.key == K_ESCAPE:
                if not self.escape_count:
                    connection.Send({'action':'pause'})
                    self.escape_count = 30
            if event.type == MOUSEMOTION:
                self.mouseX = event.pos[0]
                self.mouseY = event.pos[1]
        _keys = p.key.get_pressed()
        keys = []
        for i in range(len(list(_keys))):
            keys.append(_keys[i])
        mouse = list(p.mouse.get_pos())
        mouse_click = p.mouse.get_pressed()
        mouse.append(mouse_click[0])
        mouse.append(mouse_click[1])
        mouse.append(mouse_click[2])

        connection.Send({'action': 'keys', 'keys': keys, 'mouse':mouse})

        
        
        
        _screen = p.Surface((1000, 650))
        for image in self.toDraw:
            _screen.blit(image[0], image[1])
        if self.paused:
            _screen.blit(self.paused_image, (0, 0))
        
        self.screen.blit(_screen, (0, 0))
        
        
            
        # Tell pygame to update the screen
        pygame.display.flip()

        fps = self.clock.get_fps()
        connection.Send({'action':'fps', 'fps':fps})
        self.clock.tick(self.fps_expected)
        pygame.display.set_caption("VillageWars " + self.version + " fps: " + str(fps))


    def ShutDown(self):
        """
        Client ShutDown function. Disconnects and closes the game.
        """
        self.connected = False
        connection.Close()
        
                
    #####################################
    ### Client-side Network functions ###
    #####################################
    """
    Each one of these "Network_" functions defines a command
    that the server will tell you (the client) to do.
    """
    def Network_hack_fail(self, data):
        print('Exception:', data['msg'])


    def Network_receive(self, data):
        #print(time.time() - data['timestamp'])
        self.diconnected = 0
        self._connected = True
        if time.time() - data['timestamp'] < 0.5:
            self.fps_expected = 30
            for i in data['data']:
                exec('self.Network_' + i['action'] + '(' + repr(i) + ')')
        else:
            self.fps_expected = 60
    

    def Network_fall(self, data):
        
        self.Setting = p.image.load('../assets/Setting.png')
        p.mixer.music.stop()
        p.mixer.music.load('../assets/sfx/villageLoop.mp3')
        global music_playing
        if music_playing:
            p.mixer.music.play(-1, 0.0)

    def Network_achievement(self, data):
        self.achievement = [120, data['type']]

    def Network_pause(self, data):
        self.paused = not self.paused

    def Network_flip(self, data):
        if not self.paused:           
            self.toDraw.clear()
            self.toDraw = self.toDrawNext[:]
            self.toDrawNext.clear()
        
        
    def Network_draw_setting(self, data):
        self.toDrawNext.append([self.Setting, data['coords']])

        
    def Network_draw_lobby_background(self, data):
        self.toDrawNext.append([self.back_pic, (0, 0)])

    def Network_draw_background(self, data):
        self.toDrawNext.append([self.ocean_pics[self.ocean_frame], (0, 0)])
        self.ocean_frame += 1
        self.ocean_frame %= 40

    def Network_preview(self, data):

        if not data['ArcheryTower?']:
            image = self.house
            rect = image.get_rect(center=(500, 185))
            cage = self.preview

            cage = p.transform.scale(cage, data['dimensions'])
            cage_rect = cage.get_rect(midtop=rect.midtop)
            self.toDrawNext.append([cage, cage_rect])
        else:
            cage = p.transform.scale(self.preview, (360, 360))
            cage_rect = cage.get_rect(center=(500, 85))
            self.toDrawNext.append([cage, cage_rect])


    def Network_draw_avatar(self, data):
        avatar_pic = self.players[data['skin']][0]
        avatar_rect = avatar_pic.get_rect(center=data['coords'])
        self.toDrawNext.append([avatar_pic, avatar_rect])

        if data['ready']:
            text_to_draw = self.ready_text
        else:
            text_to_draw = self.not_ready_text

        text_rect = text_to_draw.get_rect(midtop = avatar_rect.midbottom)
        text_rect.y += 4
        self.toDrawNext.append([text_to_draw, text_rect])

        num_text = self.medium_font.render(data['username'], True, data['color'])
        text_rect = num_text.get_rect(midbottom = avatar_rect.midtop)
        text_rect.y -= 4
        self.toDrawNext.append([num_text, text_rect])

        if data['host']:
            mouse = p.mouse.get_pos()
            click = p.mouse.get_pressed()

            image = self.x
            rect = image.get_rect(center=avatar_rect.topright)
            if rect.collidepoint(mouse):
                global cursor
                cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                image = self.x_hov
                if click[0]:
                    connection.Send({'action':'hack', 'command':'kick(self, "%s")' % (data['username'])})

            self.toDrawNext.append((image, rect))
        

    def Network_victory(self, data):
        p.mixer.music.stop()
        victory = p.mixer.Sound('../assets/sfx/victory.mp3')
        victory.play()

    def Network_animation(self, data):
        image = self.animations[data['name']][data['frame']]
        rect = image.get_rect(center=data['coords'])
        self.toDrawNext.append((image, rect))

    def Network_congrats(self, data):
        screen = p.Surface((1000, 650))
        screen.fill((255,255,0))
        self.toDrawNext.append([screen, (0, 0)])
        if data['color'] == (255,255,0): data['color'] = (0,0,0)
        name = self.large_font.render('You won the game!', True, data['color'])
        text_rect = name.get_rect(midtop=(500, 30))
        self.toDrawNext.append([name, text_rect])

        name = self.medium_font.render('Kills: ' + str(data['kills']), True, (0,0,0))
        text_rect = name.get_rect(topleft=(400, 200))
        self.toDrawNext.append([name, text_rect])
        name = self.medium_font.render('Eliminations: ' + str(data['eliminations']), True, (0,0,0))
        text_rect = name.get_rect(topleft=(400, 320))
        self.toDrawNext.append([name, text_rect])
        name = self.medium_font.render('Buildings Destroyed: ' + str(data['destroyed']), True, (0,0,0))
        text_rect = name.get_rect(topleft=(400, 440))
        self.toDrawNext.append([name, text_rect])
        name = self.medium_font.render('Deaths: ' + str(data['deaths']), True, (255,0,0))
        text_rect = name.get_rect(topleft=(400, 560))
        self.toDrawNext.append([name, text_rect])

        keys = p.key.get_pressed()
        if keys[K_ESCAPE]:
            global running
            running = False

    def Network_end(self, data):
        p.mixer.music.stop()
        screen = p.Surface((1000, 650))
        screen.fill((128, 128, 128))
        self.toDrawNext.append([screen, (0, 0)])
        name = self.large_font.render(data['winner'] + ' won the game.', True, (0,0,0))
        text_rect = name.get_rect(midtop=(500, 30))
        self.toDrawNext.append([name, text_rect])

        name = self.medium_font.render('Kills: ' + str(data['kills']), True, (0,0,0))
        text_rect = name.get_rect(topleft=(400, 200))
        self.toDrawNext.append([name, text_rect])
        name = self.medium_font.render('Eliminations: ' + str(data['eliminations']), True, (0,0,0))
        text_rect = name.get_rect(topleft=(400, 320))
        self.toDrawNext.append([name, text_rect])
        name = self.medium_font.render('Buildings Destroyed: ' + str(data['destroyed']), True, (0,0,0))
        text_rect = name.get_rect(topleft=(400, 440))
        self.toDrawNext.append([name, text_rect])
        name = self.medium_font.render('Deaths: ' + str(data['deaths']), True, (255,0,0))
        text_rect = name.get_rect(topleft=(400, 560))
        self.toDrawNext.append([name, text_rect])
        
    def Network_ingame(self, data):
        self.toDrawNext.append([self.Setting, data['coords']])

    def Network_music_change(self, data):
        p.mixer.music.stop()
        p.mixer.music.load(self.musics[data['music']])
        global music_playing
        if music_playing:
            p.mixer.music.play(-1, 0.0)


    def Network_draw_barbarian(self, data):
        image = self.barbarians[data['type']][bool(data['hurt'])]
        rect = image.get_rect(center=data['coords'])
        image, rect = t.rotate(image, rect, data['angle'])

        if data['type'] == 'leader':
            banner = self.barbarian_banner
            banner_rect = banner.get_rect(bottomleft=rect.center)
            self.toDrawNext.append((banner, banner_rect))
        
        self.toDrawNext.append((image, rect))

        username_text = self.small_font.render('Barbarian ' + data['type'].title(), True, (0,0,0))
        text_rect = username_text.get_rect(midbottom = (rect.midtop[0], rect.midtop[1] - 15))
        self.toDrawNext.append([username_text, text_rect])


        if data['shield'] != None:
            image = self.shield
            rect = image.get_rect(center=data['coords'])
            image, rect = t.rotate(image, rect, data['shield'])
            self.toDrawNext.append((image, rect))
            
        

        
        health_bar = p.Surface((50, 10))
        health_bar.fill((255, 0, 0))
        health_rect = health_bar.get_rect(midbottom=rect.midtop)
        
        green_bar = p.Surface((int(data['health']/2), 10))
        green_bar.fill((0,255,0))
        health_bar.blit(green_bar, (0, 0))
        
        self.toDrawNext.append([health_bar, health_rect])


    def Network_draw_player(self, data):
        global cursor
        cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        image = self.players[data['skin']][data['hurt']]
        rect = image.get_rect(center=(data['coords']))
        image, rect = t.rotate(image, rect, data['angle'])
        self.toDrawNext.append([image, rect])


        
        username_text = self.small_font.render(data['username'], True, data['color'])
        text_rect = username_text.get_rect(midbottom = (rect.midtop[0], rect.midtop[1] - 15))
        self.toDrawNext.append([username_text, text_rect])

        
        health_bar = p.Surface((int(data['max_health'] / 2), 10))
        health_bar.fill((255, 0, 0))
        health_rect = health_bar.get_rect(midbottom=rect.midtop)
        
        green_bar = p.Surface((int(data['health']/2), 10))
        green_bar.fill((0,255,0))
        health_bar.blit(green_bar, (0, 0))
        
        self.toDrawNext.append([health_bar, health_rect])

    

        try:
            
            gold = self.medium_font.render('Gold: ' + str(data['gold']), True, (255,205,0))
            gold_rect = gold.get_rect(topright = (950,260))
            self.toDrawNext.append([gold, gold_rect])
            
            food = self.medium_font.render('Food: ' + str(data['food']), True, (5,255,5))
            food_rect = food.get_rect(topright = (950,300))
            self.toDrawNext.append([food, food_rect])
        except:
            pass

        if data['shield'] != None:
            image = self.shield
            rect = image.get_rect(center=data['coords'])
            image, rect = t.rotate(image, rect, data['shield'])
            self.toDrawNext.append((image, rect))


    def Network_draw_NPC(self, data):
        if data['image'] == 'farmer':
            image = self.farmer
            name = 'Farmer'
        elif data['image'] == 'miner':
            image = self.miner
            name = 'Miner'
        rect = image.get_rect(topleft=(data['coords']))
        image, rect = t.rotate(image, rect, data['angle'])
        self.toDrawNext.append([image, rect])


        
        username_text = self.small_font.render(name, True, data['color'])
        text_rect = username_text.get_rect(midbottom = (rect.midtop[0], rect.midtop[1] - 15))
        self.toDrawNext.append([username_text, text_rect])

        status_text = self.small_font.render(data['status'], True, (0,0,0))
        text_rect = status_text.get_rect(midbottom = (rect.midtop[0], rect.midtop[1] + 5))
        self.toDrawNext.append([status_text, text_rect])

    def Network_draw_InnPC(self, data):
        
        image = self.players[0][0]
        rect = image.get_rect(center=(data['coords']))
        image, rect = t.rotate(image, rect, data['angle'])
        self.toDrawNext.append([image, rect])
        
        username_text = self.small_font.render(data['type'], True, data['color'])
        text_rect = username_text.get_rect(midbottom = (rect.midtop[0], rect.midtop[1] - 15))
        self.toDrawNext.append([username_text, text_rect])

        health_bar = p.Surface((50, 10))
        health_bar.fill((255,0,0))
        health_rect = health_bar.get_rect(midbottom=rect.midtop)
        
        green_bar = p.Surface((round(data['health'] / 2), 10))
        green_bar.fill((0,255,0))
        health_bar.blit(green_bar, (0, 0))
        
        self.toDrawNext.append([health_bar, health_rect])
    def Network_draw_robot(self, data):
        if data['image'] == 'regular':
            image = self.robot
        elif data['image'] == 'hurt':
            image = self.robot_hurt
        
        rect = image.get_rect(center=(data['coords']))
        image, rect = t.rotate(image, rect, data['angle'])
        self.toDrawNext.append([image, rect])


        
        username_text = self.small_font.render(data['name'], True, data['color'])
        text_rect = username_text.get_rect(midbottom = (rect.midtop[0], rect.midtop[1] - 15))
        self.toDrawNext.append([username_text, text_rect])


        health_bar = p.Surface((50, 10))
        health_bar.fill((255,0,0))
        health_rect = health_bar.get_rect(midbottom=rect.midtop)
        
        green_bar = p.Surface((round(data['health'] / 2), 10))
        green_bar.fill((0,255,0))
        health_bar.blit(green_bar, (0, 0))
        
        self.toDrawNext.append([health_bar, health_rect])


    def Network_draw_farm(self, data):
        if data['state'] == 'good':
            image = self.food_image
        elif data['state'] == 'mine':
            image = self.food_mine
        else:
            image = self.food_used
        self.toDrawNext.append([image, data['coords']])

    def Network_draw_gold(self, data):
        image = None
        if data['state'] == 'good':
            image = self.gold_image
        elif data['state'] == 'mine':
            image = self.gold_mine
        if image != None:
            self.toDrawNext.append([image, data['coords']])

    def Network_draw_mine(self, data):
        image = self.mine
        if data['right'] == True:
            image = p.transform.flip(image, True, False)
        self.toDrawNext.append([image, data['coords']])
    

    def Network_draw_balloon(self, data):
        balloon_type = data.get('type', 'normal')
        image = self.balloon
        if balloon_type == 'bolt':
            image = self.bolt
        if balloon_type == 'op':
            image = self.op_balloon
        if balloon_type == 'speedy':
            image = self.speedy_balloon
        if balloon_type == 'speedy+op':
            image = self.speedy_plus_op
        rect = image.get_rect(center=(data['coords']))
        image, rect = t.rotate(image, rect, data['angle'])
        self.toDrawNext.append([image, rect])

        
    def Network_draw_building(self, data):
        
        if data['image'] == 'house':
            if data['state'] == 'alive':
                image = self.house
            else:
                image = self.house_burnt
        rect = image.get_rect(center=data['coords'])
        

        color = data['color']
        if color == (255,0,0):
            cage = self.red
        elif color == (0,255,0):
            cage = self.green
        elif color == (0,0,255):
            cage = self.blue
        elif color == (255,255,0):
            cage = self.yellow

        cage = p.transform.scale(cage, data['dimensions'])
        cage_rect = cage.get_rect(midtop=rect.midtop)
        self.toDrawNext.append([cage, cage_rect])

        self.toDrawNext.append([image, rect])

        if data['state'] == 'alive':
            person = self.building_person
            person_rect = image.get_rect(midtop=(rect.midbottom[0], rect.midbottom[1] + 50))
            person, person_rect = t.rotate(person, person_rect, data['angle'])

            self.toDrawNext.append([person, person_rect])

            name = self.small_font.render(data['type'], True, data['color'])
            text_rect = name.get_rect(midbottom = (person_rect.midtop[0], person_rect.midtop[1] - 30))
            self.toDrawNext.append([name, text_rect])

            name = self.small_font.render('(Level ' + str(data['level']) + ')', True, data['color'])
            text_rect = name.get_rect(midbottom = (person_rect.midtop[0], person_rect.midtop[1] - 15))
            self.toDrawNext.append([name, text_rect])

            health_bar = p.Surface((int(data['max_health'] / 2), 10))
            health_bar.fill((255, 0, 0))
            health_rect = health_bar.get_rect(midbottom=person_rect.midtop)
            
            green_bar = p.Surface((int(data['health']/2), 10))
            green_bar.fill((0,255,0))
            health_bar.blit(green_bar, (0, 0))
            
            self.toDrawNext.append([health_bar, health_rect])

    def Network_archery_tower(self, data):
        

        color = data['color']
        if color == (255,0,0):
            cage = self.red
        elif color == (0,255,0):
            cage = self.green
        elif color == (0,0,255):
            cage = self.blue
        elif color == (255,255,0):
            cage = self.yellow

        cage = p.transform.scale(cage, (360, 360))
        cage_rect = cage.get_rect(center=data['coords'])
        self.toDrawNext.append([cage, cage_rect])

        
        
        person = self.archer
        person_rect = person.get_rect(midtop=(data['coords']))
        person, person_rect = t.rotate(person, person_rect, data['angle'])
        if data['state'] == 'alive':
            self.toDrawNext.append([person, person_rect])

        if data['state'] == 'alive':
            name = self.small_font.render('Archery Tower', True, data['color'])
        else:
            name = self.small_font.render('Archery Tower (Broken)', True, data['color'])
        text_rect = name.get_rect(midbottom = (person_rect.midtop[0], person_rect.midtop[1] - 15))
        self.toDrawNext.append([name, text_rect])

        if data['state'] == 'alive':
            health_bar = p.Surface((150, 10))
            health_rect = health_bar.get_rect(midbottom=person_rect.midtop)
            health_bar.fill((255,0,0))
            
            green_bar = p.Surface((int(data['health']/2), 10))
            green_bar.fill((0,255,0))
            health_bar.blit(green_bar, (0, 0))
            
            self.toDrawNext.append([health_bar, health_rect])

    def Network_sound(self, data):
        if data['sound'] == 'TNT':
            self.sound_be.play()
        if data['sound'] == 'shot':
            self.sound_shot.play()
        if data['sound'] == 'die':
            self.sound_se.play()
        if data['sound'] == 'splash':
            self.sound_sp.play()
        if data['sound'] == 'opsplash':
            self.sound_sh.play()
        if data['sound'] == 'bump':
            self.sound_bump.play()
        if data['sound'] == 'building':
            self.sound_bb.play()
        if data['sound'] == 'ow':
            self.sound_ow.play()
        if data['sound'] == 'cw':
            self.sound_cw.play()


    def Network_num_buildings(self, data):
        y = 500
        x = 990
        for user in data['users']:
            username = self.small_font.render(user['name'] + ' has ' + str(user['bs']) + ' buildings.', True, user['color'])
            text_rect = username.get_rect(topright=(x, y+user['num']*30))
            self.toDrawNext.append([username, text_rect])
    

    def Network_chat(self, data):

        name = self.medium_font.render(data['message'], True, data['color'])
        text_rect = name.get_rect(topleft=(20, 20))
        self.toDrawNext.append([name, text_rect])

    def Network_startgame(self, data):
        p.mixer.music.stop()
        p.mixer.music.load('../assets/sfx/stepPebblesLoop.mp3')
        self.started = True
        global music_playing
        if music_playing:
            p.mixer.music.play(-1, 0.00)

    def Network_text(self, data):

        if data['text']:
            name = self.medium_font.render(data['text'], True, (0,0,255))
        else:
            name = self.medium_font.render('TIP: ' + self.tips[self.tip], True, (255,205,0))            
        text_rect = name.get_rect(midbottom=(500, 500))
        self.toDrawNext.append([name, text_rect])
    
    def Network_crates(self, data):
        self.toDrawNext.append([p.transform.scale(self.crate, (30, 30)), (900, 5)])
        
        text = self.medium_font.render('x ' + str(data['crates']), True, (0,0,0))
        text_rect = text.get_rect(midleft=(940, 20))
        self.toDrawNext.append([text, text_rect])

    def Network_spiky_bushes(self, data):
        self.toDrawNext.append([p.transform.scale(self.spiky_bush, (30, 30)), (900, 60)])
        
        text = self.medium_font.render('x ' + str(data['num']), True, (0,0,0))
        text_rect = text.get_rect(midleft=(940, 75))
        self.toDrawNext.append([text, text_rect])

    def Network_time(self, data):
        text = self.medium_font.render(data['time'], True, (0,0,0))
        text_rect = text.get_rect(midbottom=(500, 640))
        self.toDrawNext.append([text, text_rect])

    def Network_draw_obstacle(self, data):
        if data['image'] == 'tree':
            image = self.tree
        if data['image'] == 'sappling':
            image = self.sappling
        if data['image'] == 'crate':
            image = self.crate
        if data['image'] == 'vine':
            image = self.vine
        if data['image'] == 'gate':
            if data['rotated?']:
                image = p.transform.rotate(self.gate, 90)
            else:
                image = self.gate
        if data['image'] == 'spiky bush':
            image = self.spiky_bush
        if data['image'] == 'TNT':
            image = self.tnt
        rect = image.get_rect(center=data['coords'])
        self.toDrawNext.append([image, rect])

        if data['image'] != 'crate' and data['image'] != 'gate' and data['image'] != 'TNT' and data['image'] != 'spiky bush' and data['image'] != 'vine':
            health_bar = p.Surface((int(data['max_health']/2), 12))
            health_bar.fill((255, 0, 0))
            health_rect = health_bar.get_rect(midbottom=rect.midtop)
        
            green_bar = p.Surface((int(data['health']/2), 12))
        
            green_bar.fill((0,255,0))
            health_bar.blit(green_bar, (0, 0))
        
            self.toDrawNext.append([health_bar, health_rect])

    def Network_meal(self, data):
        if data['food?']:
            image = self.meals[data['type']]
        else:
            image = self.plate

        mouse = p.mouse.get_pos()

        rect = image.get_rect(center=(890, 130))
        if rect.collidepoint(mouse) and image != self.plate:
            image = p.transform.scale(image, (110, 110))
            rect = image.get_rect(center=(890, 130))
            pressed = p.mouse.get_pressed()
            if pressed[0]:
                connection.Send({'action':'eat'})

        self.toDrawNext.append([image, rect])


    def Network_draw_window(self, data):
        grey = p.Surface((610, 618))
        large_rect = grey.get_rect(topleft=(195, 4))
        grey.fill((128,128,128))
        self.toDrawNext.append([grey, large_rect])

        if large_rect.collidepoint(p.mouse.get_pos()):
            global cursor
            cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)

        dark_grey = p.Surface((600, 606))
        rect = dark_grey.get_rect(topleft=(200, 10))
        dark_grey.fill((95,95,95))
        self.toDrawNext.append([dark_grey, rect])

        x = 200
        y = 200

        info = self.small_font.render(data['window']['info'][0], True, (0,0,0))
        text_rect = info.get_rect(topleft=(210,30))
        self.toDrawNext.append([info, text_rect])
        info = self.small_font.render(data['window']['info'][1], True, (0,0,0))
        text_rect = info.get_rect(topleft=(210,55))
        self.toDrawNext.append([info, text_rect])

        info = self.small_font.render('Owner:', True, (255,0,255))
        text_rect = info.get_rect(topleft=(210,90))
        self.toDrawNext.append([info, text_rect])
        info = self.small_font.render('Health:', True, (255,0,255))
        text_rect = info.get_rect(topleft=(210,110))
        self.toDrawNext.append([info, text_rect])
        info = self.small_font.render('Level:', True, (255,0,255))
        text_rect = info.get_rect(topleft=(210,130))
        self.toDrawNext.append([info, text_rect])
        info = self.small_font.render(data['window']['4th_info'][0] + ':', True, (255,0,255))
        big_text_rect = info.get_rect(topleft=(210,150))
        self.toDrawNext.append([info, big_text_rect])
        right = big_text_rect.topright[0] + 30

        info = self.small_font.render(data['window']['owner'], True, data['window']['color'])
        text_rect = info.get_rect(topleft=(right,90))
        self.toDrawNext.append([info, text_rect])

        info = self.small_font.render(str(data['window']['health'][0]) + '/' + str(data['window']['health'][1]), True, (0,0,0))
        text_rect = info.get_rect(topleft=(right,110))
        self.toDrawNext.append([info, text_rect])

        info = self.small_font.render(str(data['window']['level']), True, (0,0,0))
        text_rect = info.get_rect(topleft=(right,130))
        self.toDrawNext.append([info, text_rect])

        info = self.small_font.render(data['window']['4th_info'][1], True, (0,0,0))
        text_rect = info.get_rect(topleft=(right,150))
        self.toDrawNext.append([info, text_rect])

        for Y in range(len(data['window']['options'])):
            black = p.Surface((600, 2))
            black_rect = black.get_rect(topleft=(200,y+Y*40))
            grey = p.Surface((600, 44))
            rect = grey.get_rect(topleft=(200, y+Y*40))
            grey.fill((155,155,155))
            mouse = p.mouse.get_pos()
            if rect.collidepoint(mouse):
                grey.fill((250, 250, 255))
            self.toDrawNext.append([grey, rect])
            self.toDrawNext.append([black, black_rect])

            name = self.medium_font.render(data['window']['options'][Y], True, (0,0,0))
            text_rect = name.get_rect(midtop=(500, y+Y*40+5))
            self.toDrawNext.append([name, text_rect])


    def Network_draw_innpc_window(self, data):
        grey = p.Surface((610, 618))
        large_rect = grey.get_rect(topleft=(195, 4))
        grey.fill((128,128,128))
        self.toDrawNext.append([grey, large_rect])

        dark_grey = p.Surface((600, 606))
        rect = dark_grey.get_rect(topleft=(200, 10))
        dark_grey.fill((95,95,95))
        self.toDrawNext.append([dark_grey, rect])

        x = 210
        y = 30

        for Y, thing in enumerate(data['window']['info']):
            info = self.small_font.render(thing, True, (0,0,0))
            text_rect = info.get_rect(topleft=(x, y + Y*15))
            self.toDrawNext.append([info, text_rect])

        x = 200
        y = 200
        for Y in range(len(data['window']['options'])):
            black = p.Surface((600, 2))
            black_rect = black.get_rect(topleft=(200,y+Y*40))
            grey = p.Surface((600, 44))
            rect = grey.get_rect(topleft=(200, y+Y*40))
            grey.fill((155,155,155))
            mouse = p.mouse.get_pos()
            if rect.collidepoint(mouse):
                grey.fill((250, 250, 255))
            self.toDrawNext.append([grey, rect])
            self.toDrawNext.append([black, black_rect])

            name = self.medium_font.render(data['window']['options'][Y], True, (0,0,0))
            text_rect = name.get_rect(midtop=(500, y+Y*40+5))
            self.toDrawNext.append([name, text_rect])

    def Network_WARNING_outdated_client(self, data):
        info = self.medium_font.render('WARNING: Outdated Client', True, (255,0,0))
        text_rect = info.get_rect(midbottom=(400,600))

        box = p.Surface((text_rect.width + 10, 85))
        box.fill((255,255,255))
        rect = box.get_rect(midbottom=(400, 650))
        self.toDrawNext.append([box, rect])

        self.toDrawNext.append([info, text_rect])
        info = self.medium_font.render('Server: %s - Client: %s' % (data['version'], self.version), True, (255,0,0))
        text_rect = info.get_rect(midbottom=(400,635))
        self.toDrawNext.append([info, text_rect])

    


    def Network_WARNING_outdated_server(self, data):
        info = self.medium_font.render('WARNING: Outdated Server', True, (255,0,0))
        text_rect = info.get_rect(midbottom=(400,600))

        box = p.Surface((text_rect.width + 10, 85))
        box.fill((255,255,255))
        rect = box.get_rect(midbottom=(400, 650))
        self.toDrawNext.append([box, rect])

        self.toDrawNext.append([info, text_rect])
        info = self.medium_font.render('Server: %s - Client: %s' % (data['version'], self.version), True, (255,0,0))
        text_rect = info.get_rect(midbottom=(400,635))
        self.toDrawNext.append([info, text_rect])

        
        

    def Network_display_host(self, data):
        self.toDrawNext.append([self.host_text, (480, 20)])

        if data['enough?']:
            if self.startgame_rect.collidepoint((self.mouseX, self.mouseY)):
                image = self.startgame_icon_over
                if p.mouse.get_pressed()[0]:
                    print(p.mouse.get_pressed()[0])
                    connection.Send({'action':'all_ready'})
            else:
                image = self.startgame_icon
        else:
            image = self.startgame_icon_locked

        self.toDrawNext.append([image, self.startgame_rect])


        

    def Network_connected(self, data):
        """
        Network_connected runs when you successfully connect to the server
        """
        
        connection.Send({'action':'init', 'username':self.username, 'status':'JG', 'color':self.color, 'skin':self.skin})
        self.connected = True
        print("Joined game")

        p.mixer.music.stop()
        
    
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

    def Network_kicked(self, data):
        self.ShutDown()
        p.quit()
        exit()






    
def main(screen, clock, username, version, userInfo, ip, port=5555, musicPlaying=True):
    global running, cursor, music_playing
    running = True
    cursor = p.cursors.Cursor(p.SYSTEM_CURSOR_ARROW)
    music_playing = musicPlaying
    print(ip)
    cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
    client = MyGameClient(ip, port, screen, clock, username, version, userInfo['color'], userInfo['skin'])
    while running:
        client.update()
    client.ShutDown()
    p.mixer.music.stop()
    return music_playing


if __name__ == '__main__':
    import VillageWarsClient
    VillageWarsClient.main()
                   

















