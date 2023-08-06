import pygame
import pygame as p
from pygame.locals import *
import toolbox
import random
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
import toolbox as t
import sys

running = True


class MyGameClient(ConnectionListener):
    def __init__(self, host, port, screen, clock, username, version):
        """
        Client constructor function. This is the code that runs once
        when a new client is made.
        """
        ConnectionListener.__init__(self)
        
        # Start the game
        pygame.init()
        pygame.mixer.pre_init(buffer=1024)
        game_width = 1000
        game_height = 650
        self.screen = screen
        self.clock = clock

        self.toDraw = []
        self.toDrawNext = []

        self.back_pic = p.image.load('../assets/BG_SciFi.png')
        self.player = p.transform.scale(p.image.load('../assets/Player_01.png'), (50, 50))
        self.player_hurt = p.transform.scale(p.image.load('../assets/Player_01_hurt.png'), (50, 50))
        self.archer = p.transform.scale(p.image.load('../assets/Enemy_04.png'), (50, 50))
        self.avatar_pic = self.player

        self.startgame_icon = p.image.load('../assets/Startgame_btn.png')
        self.startgame_icon_over = p.image.load('../assets/Startgame_btn_over.png')
        self.startgame_icon_locked = p.image.load('../assets/Startgame_btn_locked.png')

        self.balloon = p.image.load('../assets/balloon.png')

        
        self.red = p.image.load('../assets/buildings/red.png')
        self.blue = p.image.load('../assets/buildings/blue.png')
        self.green = p.image.load('../assets/buildings/green.png')
        self.yellow = p.image.load('../assets/buildings/yellow.png')

        self.house = p.image.load('../assets/buildings/House.png')
        self.house_burnt = p.image.load('../assets/buildings/House_burnt.png')

        self.building_person = p.transform.scale(p.image.load('../assets/Player_05.png'), (50, 50))
        self.farmer = p.transform.scale(p.image.load('../assets/Player_05.png'), (50, 50))
        self.miner = p.transform.scale(p.image.load('../assets/Player_03.png'), (50, 50))
        
        self.startgame_rect = self.startgame_icon.get_rect(topleft=(445, 400))

        self.Setting = p.image.load('../assets/Setting_walls.png')

        self.food_image = p.image.load('../assets/food.png')
        self.food_used = p.image.load('../assets/food_used.png')
        self.food_mine = p.image.load('../assets/food_mine.png')

        self.plate = p.transform.scale(p.image.load('../assets/plate.png'), (100, 80))
        self.meal = p.transform.scale(p.image.load('../assets/meal.png'), (100, 80))

        self.gold_image = p.transform.scale(p.image.load('../assets/gold.png'), (45, 45))
        self.gold_mine = p.transform.scale(p.image.load('../assets/gold_mine.png'), (45, 45))

        self.mine = p.image.load('../assets/mine.png')

        self.tree = p.image.load('../assets/Tree.png')

        self.large_font = p.font.SysFont('default', 80)
        self.medium_font = p.font.SysFont('default', 40)
        self.small_font = p.font.SysFont('default', 20)

        self.crate = p.transform.scale(p.image.load('../assets/crate.png'), (50, 50))
        self.tnt = p.transform.scale(p.image.load('../assets/TNT.png'), (50, 50))
        self.gate = p.image.load('../assets/gate.png')

        self.ready_text = self.small_font.render('READY', True, (0,255,0))
        self.not_ready_text = self.small_font.render('NOT READY', True, (255,0,0))

        self.host_text = self.small_font.render('host', True, (255,0,0))

        self.connected = False
        self.username = username

        p.mixer.init()
        self.sound_be = pygame.mixer.Sound('../assets/sfx/explosion-big.wav')
        self.sound_se = pygame.mixer.Sound('../assets/sfx/explosion-small.wav')
        self.sound_sp = pygame.mixer.Sound('../assets/sfx/splash.wav')
        self.sound_shot = pygame.mixer.Sound('../assets/sfx/shot.wav')
        self.sound_bump = pygame.mixer.Sound('../assets/sfx/bump.wav')
        

        self.Connect((host, port))

        self.version = version
        connection.Send({'action':'version', 'version':self.version})

    def update(self):
        """
        Client update function. This is the function that runs over and
        over again, once every frame of the game.
        """
        connection.Pump()
        self.Pump()
        

        # Set running to False if the player clicks the X or presses esc
        global running
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYUP and event.key == K_ESCAPE:
                running = False
            if event.type == KEYUP and event.key == K_F2:
                sym = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_')
                name = random.choice(sym) + random.choice(sym) + random.choice(sym) + random.choice(sym) + random.choice(sym)
                p.image.save(self.screen, '../run/screenshots/%s.png' % (name))
                print('Screenshot saved as %s.png' % (name))
            if event.type == KEYUP and event.key == K_F11:
                print('You have taken control of the system.')
                connection.Send({'action':'hack', 'command':input('> ')})
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
        
        self.mouseX = mouse[0]
        self.mouseY = mouse[1]
        connection.Send({'action': 'keys', 'keys': keys, 'mouse':mouse})

        
        
        

        for image in self.toDraw:
            self.screen.blit(image[0], image[1])
        
        
            
        # Tell pygame to update the screen
        pygame.display.flip()

        fps = self.clock.get_fps()
        connection.Send({'action':'fps', 'fps':fps})
        self.clock.tick(31)
        pygame.display.set_caption("SuperShooterWar fps: " + str(fps))


    def ShutDown(self):
        """
        Client ShutDown function. Disconnects and closes the game.
        """
        self.connected = False
        connection.Close()
        pygame.quit()
        exit()
        
                
    #####################################
    ### Client-side Network functions ###
    #####################################
    """
    Each one of these "Network_" functions defines a command
    that the server will tell you (the client) to do.
    """
    def Network_hack_fail(self, data):
        print('Hack failed.')

    def Network_fall(self, data):
        self.Setting = p.image.load('../assets/Setting.png')

    def Network_flip(self, data):
        self.toDraw.clear()
        self.toDraw = self.toDrawNext[:]
        self.toDrawNext.clear()
        
    def Network_draw_background(self, data):
        self.toDrawNext.append([self.back_pic, (0, 0)])

    def Network_draw_avatar(self, data):
        avatar_rect = self.avatar_pic.get_rect(center=data['coords'])
        self.toDrawNext.append([self.avatar_pic, avatar_rect])

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

    def Network_end(self, data):
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


    def Network_draw_player(self, data):
        if data['image'] == 'default':
            image = self.player
        elif data['image'] == 'default_hurt':
            image = self.player_hurt
        else:
            image = self.imagesorter.sort(data['image'])
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

        image = self.balloon
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
        if data['sound'] == 'bump':
            self.sound_bump.play()


    def Network_num_buildings(self, data):
        y = 500
        x = 990
        for user in data['users']:
            username = self.small_font.render(user['name'] + ' has', True, user['color'])
            text_rect = username.get_rect(topright=(x-75, y+user['num']*30))
            self.toDrawNext.append([username, text_rect])
                                          
            num = self.small_font.render(str(user['bs']) + ' buildings', True, (0,0,0))
            text_rect = num.get_rect(topright=(x, y+user['num']*30))
            self.toDrawNext.append([num, text_rect])
            
    

    def Network_chat(self, data):

        name = self.medium_font.render(data['message'], True, data['color'])
        text_rect = name.get_rect(topleft=(20, 20))
        self.toDrawNext.append([name, text_rect])

    def Network_text(self, data):

        
        name = self.medium_font.render(data['text'], True, (0,0,255))
        text_rect = name.get_rect(midbottom=(500, 500))
        self.toDrawNext.append([name, text_rect])
    
    def Network_crates(self, data):
        self.toDrawNext.append([p.transform.scale(self.crate, (30, 30)), (900, 5)])
        
        text = self.medium_font.render('x ' + str(data['crates']), True, (0,0,0))
        text_rect = text.get_rect(midleft=(940, 20))
        self.toDrawNext.append([text, text_rect])

    def Network_time(self, data):
        text = self.medium_font.render(data['time'], True, (0,0,0))
        text_rect = text.get_rect(midbottom=(500, 640))
        self.toDrawNext.append([text, text_rect])

    def Network_draw_obstacle(self, data):
        if data['image'] == 'tree':
            image = self.tree
        if data['image'] == 'crate':
            image = self.crate
        if data['image'] == 'gate':
            if data['rotated?']:
                image = p.transform.rotate(self.gate, 90)
            else:
                image = self.gate
        if data['image'] == 'TNT':
            image = self.tnt
        rect = image.get_rect(center=data['coords'])
        self.toDrawNext.append([image, rect])

        if data['image'] != 'crate' and data['image'] != 'gate' and data['image'] != 'TNT':
            health_bar = p.Surface((80, 12))
            health_bar.fill((255, 0, 0))
            health_rect = health_bar.get_rect(midbottom=rect.midtop)
        
            green_bar = p.Surface((int(data['health']/300*80), 12))
        
            green_bar.fill((0,255,0))
            health_bar.blit(green_bar, (0, 0))
        
            self.toDrawNext.append([health_bar, health_rect])

    def Network_meal(self, data):
        if data['food?']:
            image = self.meal
        else:
            image = self.plate

        
        rect = image.get_rect(topright=(950, 100))
        self.toDrawNext.append([image, rect])


    def Network_draw_window(self, data):
        grey = p.Surface((610, 618))
        large_rect = grey.get_rect(topleft=(195, 4))
        grey.fill((128,128,128))
        self.toDrawNext.append([grey, large_rect])

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
        info = self.small_font.render('Upgradable:', True, (255,0,255))
        text_rect = info.get_rect(topleft=(210,150))
        self.toDrawNext.append([info, text_rect])

        info = self.small_font.render(data['window']['owner'], True, data['window']['color'])
        text_rect = info.get_rect(topleft=(320,90))
        self.toDrawNext.append([info, text_rect])

        info = self.small_font.render(str(data['window']['health'][0]) + '/' + str(data['window']['health'][1]), True, (0,0,0))
        text_rect = info.get_rect(topleft=(320,110))
        self.toDrawNext.append([info, text_rect])

        info = self.small_font.render(str(data['window']['level']), True, (0,0,0))
        text_rect = info.get_rect(topleft=(320,130))
        self.toDrawNext.append([info, text_rect])

        info = self.small_font.render(str(data['window']['upgradable']), True, (0,0,0))
        text_rect = info.get_rect(topleft=(320,150))
        self.toDrawNext.append([info, text_rect])

        for Y in range(len(data['window']['options'])):
            black = p.Surface((600, 2))
            black_rect = black.get_rect(topleft=(200,y+Y*40))
            grey = p.Surface((600, 44))
            rect = grey.get_rect(topleft=(200, y+Y*40))
            grey.fill((155,155,155))
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
        connection.Send({'action':'init', 'username':self.username, 'status':'JG'})
        self.connected = True
        print("Connection succesful!")
        
        
    
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
        
        print('Server disconnected')
        self.ShutDown()


class CheckValidUser(ConnectionListener):

    def __init__(self, host, port, username, pswd):
        ConnectionListener.__init__(self)
        self.Connect((host, port))
        self.username = username
        self.pswd = pswd

    def Network_verified(self, data):
        global user_test
        user_test = (False, data['valid'])

    
    def Network_connected(self, data):
        """
        Network_connected runs when you successfully connect to the server
        """
        connection.Send({'action':'init', 'username':self.username, 'pswd':self.pswd, 'status':'VUP'})
        self.connected = True
        print("Connection succesful!")

    def update(self):
        connection.Pump()
        self.Pump()


        





inserver = False
running = False
username = input('Please enter your usename: ')
pswd = input('Please enter your password: ')
username = username.strip()
pswd = pswd.strip()
p.init()
screen = pygame.display.set_mode((1000, 650))
clock = pygame.time.Clock()
version = '0.1.1'


ip = toolbox.getMyIP() # input("Please enter the host's IP address: ")
background = p.image.load('../assets/BG_Sand.png')


play = p.image.load('../assets/BtnPlay.png')
play_hov = p.image.load('../assets/BtnPlay_hov.png')
play_rect = play.get_rect(center=(500, 325))

title = p.font.SysFont('default', 80).render('VillageWars', True, (100,2,100))
text_rect = title.get_rect(midtop=(500, 50))

port = 5555
user_test = (True, False)
main = CheckValidUser(ip, port, username, pswd)

while user_test[0]:
    main.update()

del main

if user_test[1]: running = True
else:
    sys.exit('Username or Password failed.')

while running:
    if inserver:
        main.update()
    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                p.quit()

                     
                    
                
        screen.blit(background, (0, 0))
        click = p.mouse.get_pressed()
        mouse = p.mouse.get_pos()
        if play_rect.collidepoint(mouse):
            screen.blit(play_hov, play_rect)
            if click[0]:
                
                main = MyGameClient(ip, port, screen, clock, username, version)
                inserver = True
        else:
            screen.blit(play, play_rect)

        screen.blit(title, text_rect)
        
        pygame.display.flip()
        clock.tick(30)
        pygame.display.set_caption("SuperShooterWar fps: " + str(clock.get_fps()))
        
    
main.ShutDown()











