import shelve
import os
import sys

import pygame
import threading
import os
import re
try:
    import mygmail
    mygmail.PATH = 'gmail_files/'
    #mygmail.get_creds('send')
except ModuleNotFoundError:
    print('MyGmail module not found.')


import pygame as p
from pygame.locals import *
from pymsgbox import *


try:
    import toolbox
    import toolbox as t
    import typer
    import GameClient
    import VillageWarsDownload
    from PodSixNet.Connection import ConnectionListener, connection

except:
    from src import toolbox
    from src import toolbox as t
    from src import typer
    from src import GameClient
    from src import VillageWarsDownload
    from src.PodSixNet.Connection import ConnectionListener, connection

path = os.path.abspath('.')

if not path.endswith('src'):
    os.chdir('src/')


regex = re.compile(r'(\d)+\.(\d)+\.(\d)+')
__version__ = regex.search(path).group()
print('Running VillageWars version', __version__)

#print()
#sys.stderr.write('VillageWars Program started.')
#print()

music_playing = True

p.mixer.pre_init(buffer=5)
p.mixer.init()
p.mixer.music.load('../assets/sfx/menu.mp3')
p.mixer.music.play(-1, 0.0)

DOWNLOAD = False
p.font.init()
background = p.image.load('../assets/BG_Sand.png')
play = p.image.load('../assets/play.png')
play_hov = p.image.load('../assets/play_hov.png')
play_rect = play.get_rect(center=(330, 250))
shop = p.image.load('../assets/shop.png')
shop_hov = p.image.load('../assets/shop_hov.png')
shop_no = p.image.load('../assets/shop_no.png')
shop_rect = shop.get_rect(center=(330, 350))
right = p.image.load('../assets/right.png')
right, right_hov = p.transform.scale(right, (45, 45)), p.transform.scale(right, (60, 60))
right_rect = right.get_rect(topleft=(500, 155))
right_hov_rect = right_hov.get_rect(center=right_rect.center)
left = p.image.load('../assets/left.png')
left, left_hov = p.transform.scale(left, (45, 45)), p.transform.scale(left, (60, 60))
left_rect = left.get_rect(topright=(500, 155))
left_hov_rect = left_hov.get_rect(center=left_rect.center)
icon = p.image.load('../assets/Skins/0.png')
skins = [p.transform.scale(p.image.load('../assets/Skins/%s.png' % (i)), (280, 280)) for i in range(len(os.listdir('../assets/Skins')) // 2)]
skin_rect = skins[0].get_rect(topright=(900, 250))
skin_prime = skins[0].get_rect(center=(500, 360))
bright = p.image.load('../assets/right.png')
bright, bright_hov = p.transform.scale(bright, (74, 74)), p.transform.scale(bright, (98, 98))
bright_rect = bright.get_rect(midleft=skin_prime.midright)
bright_rect.left += 100
bright_hov_rect = bright_hov.get_rect(center=bright_rect.center)
bleft = p.image.load('../assets/left.png')
bleft, bleft_hov = p.transform.scale(left, (74, 74)), p.transform.scale(bleft, (98, 98))
bleft_rect = bleft.get_rect(midright=skin_prime.midleft)
bleft_rect.right -= 100
bleft_hov_rect = bleft_hov.get_rect(center=bleft_rect.center)
edit = p.transform.scale(p.image.load('../assets/Edit.png'), (175, 65))
edit_rect = edit.get_rect(midtop=(skin_rect.midbottom[0], skin_rect.midbottom[1] + 30))
bigedit = p.transform.scale(edit, (190, 90))
bigedit_rect = bigedit.get_rect(center=(edit_rect.center))
done = p.transform.scale(p.image.load('../assets/Done.png'), (175, 75))
done_rect = done.get_rect(midbottom=(500, 600))
done_rect2 = done.get_rect(topleft=(12, 12))
bigdone = p.transform.scale(done, (190, 90))
bigdone_rect = bigdone.get_rect(center=(done_rect.center))
bigdone_rect2 = bigdone.get_rect(center=done_rect2.center)
click_sound = p.mixer.Sound('../assets/sfx/click.wav')
ximg = p.image.load('../assets/x.png')
x_hov = p.image.load('../assets/x_hov.png')
title = p.font.SysFont('default', 140).render('VillageWars', True, (100,2,100))
text_rect = title.get_rect(midtop=(500, 30))
image = p.font.SysFont('default', 120).render('Shop', True, (100,2,100))
shop_title = p.transform.scale(image, (image.get_width() * 1.6, image.get_height()))
shop_title_rect = shop_title.get_rect(midtop=(500, 20))
servertext = p.font.SysFont('default', 40).render('Connecting to server: ' + 'Localhost', True, (0,0,130))
servertext_rect = servertext.get_rect(midtop=(text_rect.center[0], text_rect.midbottom[1] + 45))
diffserver = p.image.load('../assets/diffserver.png')
diffserver_hov = p.image.load('../assets/diffserver_hov.png')
diffserver_rect = diffserver.get_rect(midtop=(500, 213))
addserverimg = p.image.load('../assets/addserver.png')
addserverimg_hov = p.image.load('../assets/addserver_hov.png')
addserver_rect = addserverimg.get_rect(center=(500, 600))
signin = p.image.load('../assets/BtnSignin.png')
sIn_rect = signin.get_rect(topright=(400, 425))
bsignin = p.transform.scale(signin, (270, 137))
bsIn_rect = bsignin.get_rect(center=sIn_rect.center)
signup = p.image.load('../assets/BtnSignup.png')
sUp_rect = signup.get_rect(topleft=(600, 425))
bsignup = p.transform.scale(signup, (270, 137))
bsUp_rect = bsignup.get_rect(center=sUp_rect.center)
cancel = p.image.load('../assets/cancel.png')
cancel_rect = cancel.get_rect(topleft=(12, 12))
bcancel = p.transform.scale(cancel, (170, 82))
bcancel_rect = bcancel.get_rect(center=cancel_rect.center)
SigningIn = p.image.load('../assets/SigningIn.png')
CreatingAcount = p.image.load('../assets/CreatingAcount.png')
Connecting = SigningIn
cursor = p.cursors.Cursor(p.SYSTEM_CURSOR_ARROW)
grey_bar = p.Surface((800, 50))
grey_bar.fill((95, 95, 95))
grey_bar_rect = grey_bar.get_rect(center=(500, 300))
blue_bar_pos = grey_bar_rect.topleft

def get_uns(username):
    font = p.font.SysFont('default', 90)
    return font.render(username, True, (255, 0, 0)), font.render(username, True, (0, 0, 255)), font.render(username, True, (255, 255, 0)), font.render(username, True, (0, 255, 0))


def update(screen, clock, ip, port, username, userInfo):
    while True:
        for e in p.event.get():
            if e.type == QUIT and confirm('Are you sure you want to cancel this update?', buttons=['Yes', 'No']) == 'Yes':
                p.quit()
                sys.exit()
        screen.fill((255,255,255))

            
        try:
            blue_bar = p.Surface((VillageWarsDownload.perc()/100*800, 50))
        except:
            blue_bar = p.Surface((0, 50))
        blue_bar.fill((10, 10, 250))

            
        screen.blit(title, text_rect)
        screen.blit(grey_bar, blue_bar_pos)
        screen.blit(blue_bar, blue_bar_pos)
        try:
            perctext = p.font.SysFont('default', 40).render(str(round(VillageWarsDownload.perc(), 1)) + ' %', True, (255,128,0))
        except:
            perctext = p.font.SysFont('default', 40).render('0 %', True, (255,128,0));

        perctextrect = perctext.get_rect(midtop=(500, 330))
        screen.blit(perctext, perctextrect)
            
        p.display.set_caption('VillageWars Update: ' + str(VillageWarsDownload.num()) + '/' + str(VillageWarsDownload.amount()))
        p.display.update()
        clock.tick(6)

        if VillageWarsDownload.FINISHED:
            if VillageWarsDownload.FINISHED == True:
                alert('The Update has been finished successfuly.')
                os.chdir('../../%s/src/' % (VillageWarsDownload.client.version))
                import VillageWarsClient
                VillageWarsClient.startFromTitle(screen, clock, ip, port, username, userInfo)
            break



def getScreen():
    p.init()
    screen = p.display.set_mode((1000, 650))
    p.display.set_icon(icon)
    clock = p.time.Clock()
    return screen, clock

def getServer(screen, clock):
    global music_playing
    choose_server = False
    addserver = False
    server = 'Localhost'
    serverlist = shelve.open('database/serverlist')
    servernames = serverlist['0']
    servers = serverlist['1']
    serverlist.close()
    servers['Localhost'] = toolbox.getMyIP()
    servernames.append('Add Server')
    while True:
        screen.blit(background, (0, 0))
        screen.blit(title, text_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                p.quit()
                sys.exit()
            if event.type == KEYUP and event.key == K_TAB and addserver:
                if addservertyping == 'name':
                    addservertyping = 'ip'
                else:
                    addservertyping = 'name'
                
            if (event.type == KEYUP or event.type == KEYDOWN) and (event.key == K_LSHIFT or event.key == K_RSHIFT):
                servernametext.shift()
                serveriptext.shift()
            if (event.type == KEYUP or event.type == KEYDOWN) and (event.key == K_LCTRL or event.key == K_RCTRL):
                servernametext.ctrl()
                serveriptext.ctrl()
            if event.type == KEYUP and event.key == K_F1:
                music_playing = not music_playing
                if music_playing:
                    p.mixer.music.play(-1, 0.0)
                else:
                    p.mixer.music.pause()
            if event.type == KEYUP and addserver:
                if addservertyping == 'name':
                    servernametext.type(event)
                elif addservertyping == 'ip':
                    serveriptext.type(event)
        click = p.mouse.get_pressed()
        mouse = p.mouse.get_pos()
        if not choose_server:
                
            global servertext
            global servertext_rect
            screen.blit(servertext, servertext_rect)

            if diffserver_rect.collidepoint(mouse):
                cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                screen.blit(diffserver_hov, diffserver_rect)
                if click[0]:
                    click_sound.play()
                    choose_server = True
                    p.mouse.set_pos((mouse[0], 150))
                        
            else:
                screen.blit(diffserver, diffserver_rect)
                
           

            if sIn_rect.collidepoint(mouse):
                cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                screen.blit(bsignin, bsIn_rect)
                if click[0]:
                    click_sound.play()
                    logInType = 'sign in'
                    ip = servers[server]
                    port = 5555
                    break
            else:
                screen.blit(signin, sIn_rect)

            if sUp_rect.collidepoint(mouse):
                cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                screen.blit(bsignup, bsUp_rect)
                if click[0]:
                    click_sound.play()
                    logInType = 'sign up'
                    ip = servers[server]
                    port = 5555
                    break
            else:
                screen.blit(signup, sUp_rect)
        else:
            click = p.mouse.get_pressed()
            mouse = p.mouse.get_pos()

            if addserver:
                    

                    
                if cancel_rect.collidepoint(mouse):
                    cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                    screen.blit(bcancel, bcancel_rect)
                    if click[0]:
                        click_sound.play()
                        addserver = False
                        p.mouse.set_pos((200, mouse[1]))
                else:
                    screen.blit(cancel, cancel_rect)

                grey1 = p.Surface((400, 40))
                grey2 = p.Surface((400, 40))
                    
                rect1 = grey1.get_rect(center=(500, 280))
                rect2 = grey2.get_rect(center=(500, 380))

                if rect1.collidepoint(mouse) or rect2.collidepoint(mouse):
                    cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_IBEAM)
                if click[0]:
                    if rect1.collidepoint(mouse):
                        addservertyping = 'name'
                    elif rect2.collidepoint(mouse):
                        addservertyping = 'ip'
                    else:
                        addservertyping = None

                grey1.fill((190, 190, 188))
                grey2.fill((190, 190, 188))
                    
                if addservertyping == 'name':
                    grey1.fill((255, 255, 255))
                elif addservertyping == 'ip':
                    grey2.fill((255, 255, 255))

                screen.blit(grey1, rect1)
                screen.blit(grey2, rect2)
                black = p.Surface((400, 2))
                outline1 = black.get_rect(topleft=rect1.topleft)
                outline2 = black.get_rect(topleft=rect1.bottomleft)
                outline3 = black.get_rect(topleft=rect2.topleft)
                outline4 = black.get_rect(topleft=rect2.bottomleft)
                black2 = p.Surface((2, 40))
                outline5 = black.get_rect(topleft=rect1.topleft)
                outline6 = black.get_rect(topleft=rect1.topright)
                outline7 = black.get_rect(topleft=rect2.topleft)
                outline8 = black.get_rect(topleft=rect2.topright)

                screen.blit(black, outline1)
                screen.blit(black, outline2)
                screen.blit(black, outline3)
                screen.blit(black, outline4)
                screen.blit(black2, outline5)
                screen.blit(black2, outline6)
                screen.blit(black2, outline7)
                screen.blit(black2, outline8)

                font = p.font.SysFont('default', 40)

                if addservertyping == 'name':
                    name = font.render(' ' + servernametext.text(), True, (0,0,0))
                    ipimg = font.render((' ' + serveriptext.result if serveriptext.result != '' else ' Server IP'), True, (0,0,0))

                    name_rect = name.get_rect(midleft=rect1.midleft)
                    ip_rect = ipimg.get_rect(midleft=rect2.midleft)

                    screen.blit(name, name_rect)
                    screen.blit(ipimg, ip_rect)
                        
                elif addservertyping == 'ip':
                    name = font.render((' ' + servernametext.result if servernametext.result != '' else ' Server Name'), True, (0,0,0))
                    ipimg = font.render(' ' + serveriptext.text(), True, (0,0,0))

                    name_rect = name.get_rect(midleft=rect1.midleft)
                    ip_rect = ipimg.get_rect(midleft=rect2.midleft)

                    screen.blit(name, name_rect)
                    screen.blit(ipimg, ip_rect)

                else:
                    name = font.render((' ' + servernametext.result if servernametext.result != '' else ' Server Name'), True, (0,0,0))
                    ipimg = font.render((' ' + serveriptext.result if serveriptext.result != '' else ' Server IP'), True, (0,0,0))

                    name_rect = name.get_rect(midleft=rect1.midleft)
                    ip_rect = ipimg.get_rect(midleft=rect2.midleft)

                    screen.blit(name, name_rect)
                    screen.blit(ipimg, ip_rect)

                if addserver_rect.collidepoint(mouse):
                    cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                    screen.blit(addserverimg_hov, addserver_rect)
                    if click[0]:
                        click_sound.play()
                        addserver = False
                        p.mouse.set_pos((200, mouse[1]))
                        servernames.insert(len(servernames) - 1, servernametext.result)
                        servers[servernametext.result] = serveriptext.result
                        serverlist = shelve.open('database/serverlist')
                        serverlist['0'] = servernames[:len(servernames) - 1]
                        serverlist['1'] = servers
                        serverlist.close()
                else:
                    screen.blit(addserverimg, addserver_rect)
                        
                    
                        
            else:    
                if done_rect2.collidepoint(mouse):
                    cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                    screen.blit(bigdone, bigdone_rect2)
                    if click[0]:
                        click_sound.play()
                        choose_server = False
                else:
                    screen.blit(done, done_rect2)


                font = p.font.SysFont('default', 40)
                x = 100
                y = 200
                black = p.Surface((801, 2))
                grey = p.Surface((800, 41))

                loopservernames = servernames[:]
                for Y in range(len(loopservernames)):
                    black_rect = black.get_rect(topleft=(x,y+Y*40))
                    rect = grey.get_rect(topleft=(x, y+Y*40))

                    if loopservernames[Y] not in ('Add Server', 'Localhost'):
                        x_rect = ximg.get_rect(midleft=rect.midright)
                        image = ximg
                        if x_rect.collidepoint(mouse):
                            cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                            image = x_hov
                            if click[0]:
                                answer = confirm('Are you sure you want to delete this server?', title='VillageWars')
                                if answer == 'OK':
                                    servernames.remove(servernames[Y])
                                    serverlist = shelve.open('database/serverlist')
                                    serverlist['0'] = servernames[:len(servernames) - 1]
                                    serverlist['1'] = servers
                                    serverlist.close()
                                    p.mouse.set_pos(950, mouse[1])
                        screen.blit(image, x_rect)
                        
                    if rect.collidepoint(mouse):
                        cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                        if server == servernames[Y]:
                            grey.fill((85,85,160))
                        else:
                            grey.fill((95,95,95))
                                
                        if click[0]:
                            if server != servernames[Y]:
                                click_sound.play()
                            if servernames[Y] != 'Add Server':
                                server = loopservernames[Y]
                                servertext = font.render('Connecting to server: ' + server, True, (0,0,130))
                                servertext_rect = servertext.get_rect(midtop=(text_rect.center[0], text_rect.midbottom[1] + 45))
                            else:
                                addserver = True
                                servernametext = typer.Typing()
                                serveriptext = typer.Typing()
                    else:
                        if server == loopservernames[Y]:
                            grey.fill((85,85,160))
                        else:    
                            grey.fill((155,155,155))
                    screen.blit(grey, rect)
                    screen.blit(black, black_rect)
                        
                    if loopservernames[Y] != 'Add Server':
                        name = font.render(loopservernames[Y], True, (0,0,0))
                        rect = name.get_rect(topleft=(x+12, y+Y*40+5))
                        screen.blit(name, rect)
                        name = font.render(servers[loopservernames[Y]], True, (35,35,35))
                        rect = name.get_rect(topright=(x+788,y+Y*40+5))
                        screen.blit(name, rect)
                    else:
                        name = font.render('Add Server', True, (11,0,0))
                        rect = name.get_rect(midtop=(500, y+Y*40+5))
                        screen.blit(name, rect)
                        
                black_rect = black.get_rect(topleft=(x, black_rect.y + 41))
                screen.blit(black, black_rect)
                        
                black = p.Surface((2, len(servernames)*40))
                black_rect = black.get_rect(topleft=(x,y))
                screen.blit(black, black_rect)
                black_rect = black.get_rect(topleft=(x+800,y))
                screen.blit(black, black_rect)


        p.display.update()
        global __version__
        p.display.set_caption('VillageWars ' + __version__)
        clock.tick(60)
        

            
            
    return servers[server], 5555, logInType
def GetUsernamePassword(screen, clock, username_prompt, password_prompt):
    myText = typer.Typing()
    testing = 'username'

    username_prompt_surf = p.font.SysFont('default', 45).render(username_prompt, True, (0,0,0))
    username_prompt_rect = username_prompt_surf.get_rect(center=(500, 250))
    password_prompt_surf = p.font.SysFont('default', 45).render(password_prompt, True, (0,0,0))
    password_prompt_rect = username_prompt_surf.get_rect(center=(500, 250))
    Break = False
    while True:
        screen.blit(background, (0, 0))
        screen.blit(title, text_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                p.quit()
                sys.exit()
                
            if (event.type == KEYUP or event.type == KEYDOWN) and (event.key == K_LSHIFT or event.key == K_RSHIFT):
                myText.shift()
            if (event.type == KEYUP or event.type == KEYDOWN) and (event.key == K_LCTRL or event.key == K_RCTRL):
                myText.ctrl()

            if event.type == KEYUP and event.key == K_F1:
                music_playing = not music_playing
                if music_playing:
                    p.mixer.music.play(-1, 0.0)
                else:
                    p.mixer.music.pause()
            
            if event.type == KEYUP:
                myText.type(event)
                
                if event.key == K_RETURN:

                    if testing == 'password':
                        password = myText.result
                        Break = True
                    else:
                        username = myText.result
                        testing = 'password'
                        myText = typer.Typing()

                        
        username_surf = p.font.SysFont('default', 40).render(myText.text(), True, (0,0,0))
        username_rect = username_surf.get_rect(center=(500, 325))
        screen.blit(username_surf, username_rect)
        if testing == 'password':
            screen.blit(password_prompt_surf, password_prompt_rect)
        else:
            screen.blit(username_prompt_surf, username_prompt_rect)

        p.display.update()
        clock.tick(60)
        p.display.set_caption('VillageWars ' + __version__)

        if Break:
            break
    
    return username, password
def logIn(screen, clock, ip, port, logInType, username, password):

    class CheckValidUser(ConnectionListener):

        def __init__(self, host, port, username, pswd):
            ConnectionListener.__init__(self)
            self.Connect((host, port))
            self.username = username
            self.pswd = pswd
            self.host_ip = host
            self.userInfo = {'received':False, 'valid':False, 'username_prompt':'Enter your username:', 'password_prompt':'Enter your password'}

        def Network_verified(self, data):
            self.userInfo = {'received':True,
                         'valid':data['valid'][0],
                         'username_prompt':'Enter your username:',
                         'password_prompt':'Enter your password',
                         'color':data['color'],
                         'skin':data['skin'],
                         'xp':data['xp'],
                         'coins':data['coins']}
            if not self.userInfo['valid']:
                if data['valid'][1] == 'Unknown Username':
                    self.userInfo['username_prompt'] = data['valid'][1]
                elif data['valid'][1] == 'Invalid Password':
                    self.userInfo['password_prompt'] = data['valid'][1] 

            if data['version_prob']:
                response = confirm('Server:\t%s\tClient:\t%s\n\tUpdate?' % (data['version'], __version__), title='VillageWars: Outdated Client')
                if response == 'OK':
                    global DOWNLOAD
                    DOWNLOAD = True
                    global servers
                    print('Downloading from server:', self.host_ip)
                    VillageWarsDownload.init(self.host_ip)
                    obj = threading.Thread(target=VillageWarsDownload.main)
                    obj.start()

        
        def Network_connected(self, data):
            """
            Network_connected runs when you successfully connect to the server
            """
            global version
            connection.Send({'action':'init', 'username':self.username, 'password':self.pswd, 'status':'VUP', 'version':__version__})
            self.connected = True
            print("Connection succesful!")


        def update(self):
            connection.Pump()
            self.Pump()

    class CreateAccount(ConnectionListener):

        def __init__(self, host, port, username, pswd):
            ConnectionListener.__init__(self)
            self.Connect((host, port))
            self.username = username
            self.pswd = pswd
            self.color = (255,0,0)
            self.skin = 0
            self.host_ip = host
            self.userInfo = {'received':False, 'valid':False, 'username_prompt':'Enter your username:', 'password_prompt':'Enter your password'}

        def Network_created(self, data):
            
            self.userInfo = {'received':True,
                         'valid':data['valid'][0],
                         'username_prompt':'Enter your username:',
                         'password_prompt':'Enter your password',
                         'color':(255,0,0),
                         'skin':0,
                         'xp':0,
                         'coins':0}
            if not self.userInfo['valid']:
                self.userInfo['username_prompt'] = data['valid'][1]
                    
            if data['version_prob']:
                response = confirm('Server:\t%s\tClient:\t%s\n\tUpdate?' % (data['version'], __version__), title='VillageWars: Outdated Client')
                if response == 'OK':
                    
                    global DOWNLOAD
                    DOWNLOAD = True
                    global servers
                    VillageWarsDownload.init(self.host_ip)
                    obj = threading.Thread(target=VillageWarsDownload.main)
                    obj.start()
            else:
                alert('Acount Creation Successful!', 'VillageWars')
                

        
        def Network_connected(self, data):
            """
            Network_connected runs when you successfully connect to the server
            """
            global version
            connection.Send({'action':'init', 'username':self.username, 'pswd':self.pswd, 'status':'CA', 'color':self.color, 'skin':self.skin, 'version':__version__})
            self.connected = True
            print("Connection succesful!")

        def update(self):
            connection.Pump()
            self.Pump()

    if logInType == 'sign in':
        client = CheckValidUser(ip, port, username, password)
    elif logInType == 'sign up':
        client = CreateAccount(ip, port, username, password)
    
    

    while not client.userInfo['received']:
        client.update()
        for ev in pygame.event.get():
            if ev.type == QUIT:
                p.quit()
                sys.exit()
            if ev.type == KEYUP:
                if logInType == 'sign in':
                    client = CheckValidUser(ip, port, username, password)
                elif logInType == 'sign up':
                    client = CreateAccount(ip, port, username, password)
                    
            screen.blit((SigningIn if logInType == 'sign in' else CreatingAcount), (0, 0))
            p.display.update()
            clock.tick(60)

    return client.userInfo
    
def titlePage(screen, clock, ip, port, username, userInfo):
    in_title = True
    in_shop = False
    un_sf = p.font.SysFont('default', 100).render(username, True, userInfo['color'])
    color = userInfo['color']
    xp = userInfo['xp']
    XP = p.font.SysFont('default', 50).render(str(xp) + ' xp', True, (128,0,128))
    XP_rect = XP.get_rect(midbottom=(350, 600))
    un_rt = un_sf.get_rect(midbottom=skin_rect.midtop)
    un_red, un_blue, un_yellow, un_green = get_uns(username)
    skin_num = userInfo['skin']
    coins = userInfo['coins']
    coin = [p.transform.scale(p.image.load('../assets/coin/%s.png' % (i)), (50, 32*(50/18))) for i in range(8)]
    coin_frame = 0
    coin_rect = coin[0].get_rect(bottomleft=(20, 650))
    coin_rect2 = coin[0].get_rect(topright=(980, 2))
    un_prime = un_red.get_rect(midtop=(500, 155))
    color_change_cooldown = 0
    skin_change_cooldown = 0
    right_rect.left = un_prime.right + 90
    right_hov_rect = right_hov.get_rect(center=right_rect.center)
    left_rect.right = un_prime.left - 90
    left_hov_rect = left_hov.get_rect(center=left_rect.center)
    
    while True:
        skin = skins[skin_num]
        mouse = p.mouse.get_pos()
        click = p.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                p.quit()
                sys.exit()
                
        if in_shop:
            screen.fill((180, 180, 180))
            screen.blit(shop_title, shop_title_rect)
            if done_rect2.collidepoint(mouse):
                cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                screen.blit(bigdone, bigdone_rect2)
                if click[0]:
                    click_sound.play()
                    in_shop = False
            else:
                screen.blit(done, done_rect2)

            

            sf = p.font.SysFont('default', 70).render(str(coins), True, (255,235,0))
            rect = sf.get_rect(topright=(980, 20))
            screen.blit(sf, rect)
            

            coin_frame += 1
            coin_frame %= 24

            coin_rect2 = coin[coin_frame//3].get_rect(midright=(rect.left - 10, rect.midleft[1] + 12))
            screen.blit(coin[coin_frame//3], coin_rect2)
            
            
        else:
            screen.blit(background, (0, 0))
            screen.blit(title, text_rect)
            if in_title:
                if play_rect.collidepoint(mouse):
                    cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                    screen.blit(play_hov, play_rect)
                    if click[0]:
                        click_sound.play()
                        break
                else:
                    screen.blit(play, play_rect)


                if username == 'f' or username == 'ModestNoob': # Only for testing right now
                    if shop_rect.collidepoint(mouse):
                        cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                        screen.blit(shop_hov, shop_rect)
                        if click[0]:
                            click_sound.play()
                            in_shop = True
                    else:
                        screen.blit(shop, shop_rect)
                else:
                    screen.blit(shop_no, shop_rect)
                    if shop_rect.collidepoint(mouse):
                        cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_NO)
                                
                angle = t.getAngle(skin_rect.center[0], skin_rect.center[1], mouse[0], mouse[1])
                skin_surf, skin_rt = t.rotate(skin, skin_rect, angle)
                screen.blit(skin_surf, skin_rt)

                un_rt = un_sf.get_rect(midbottom=skin_rt.midtop)
                screen.blit(un_sf, un_rt)


                if edit_rect.collidepoint(mouse):
                    cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                    screen.blit(bigedit, bigedit_rect)
                    if click[0]:
                        click_sound.play()
                        in_title = False
                    
                else:
                    screen.blit(edit, edit_rect)

                        
                screen.blit(XP, XP_rect)

                sf = p.font.SysFont('default', 70).render(str(coins), True, (255,235,0))
                rect = sf.get_rect(bottomleft=(90, 620))
                screen.blit(sf, rect)

                coin_frame += 1
                coin_frame %= 24

                screen.blit(coin[coin_frame//3], coin_rect)
            else:
                skin = skins[skin_num]
                screen.blit(skin, skin_prime)
                if color == (255, 0, 0):
                    sf = un_red
                if color == (0, 0, 255):
                    sf = un_blue
                if color == (255, 255, 0):
                    sf = un_yellow
                if color == (0, 255, 0):
                    sf = un_green

                screen.blit(sf, un_prime)

                if color_change_cooldown > 0:
                    color_change_cooldown -= 1
                if skin_change_cooldown > 0:
                    skin_change_cooldown -= 1
                    
                click = p.mouse.get_pressed()
                mouse = p.mouse.get_pos()

                if right_rect.collidepoint(mouse) and color_change_cooldown == 0:
                    cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                    screen.blit(right_hov, right_hov_rect)
                    if click[0]:
                        click_sound.play()
                        color_change_cooldown = 10
                        if color == (255, 0, 0):
                            color = (0, 0, 255)
                        elif color == (0, 0, 255):
                            color = (255, 255, 0)
                        elif color == (255, 255, 0):
                            color = (0, 255, 0)
                        else:
                            color = (255, 0, 0)
                else:
                    screen.blit(right, right_rect)
                    

                if left_rect.collidepoint(mouse) and color_change_cooldown== 0:
                    cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                    screen.blit(left_hov, left_hov_rect)
                    if click[0]:
                        click_sound.play()
                        color_change_cooldown = 10
                        if color == (255, 0, 0):
                            color = (0, 255, 0)
                        elif color == (0, 0, 255):
                            color = (255, 0, 0)
                        elif color == (255, 255, 0):
                            color = (0, 0, 255)
                        else:
                            color = (255, 255, 0)
                else:
                    screen.blit(left, left_rect)

                if bright_rect.collidepoint(mouse) and skin_change_cooldown == 0:
                    cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                    screen.blit(bright_hov, bright_hov_rect)
                    if click[0]:
                        click_sound.play()
                        skin_change_cooldown = 10
                        skin_num += 1
                        skin_num = skin_num % len(skins)
                        skin = skins[skin_num]
                        
                else:
                    screen.blit(bright, bright_rect)
                    

                if bleft_rect.collidepoint(mouse) and skin_change_cooldown== 0:
                    cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                    screen.blit(bleft_hov, bleft_hov_rect)
                    if click[0]:
                        click_sound.play()
                        skin_change_cooldown = 10
                        skin_num -= 1
                        skin_num = skin_num % len(skins)
                        skin = skins[skin_num]
                else:
                    screen.blit(bleft, bleft_rect)

                if done_rect.collidepoint(mouse):
                    cursor = p.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
                    screen.blit(bigdone, bigdone_rect)
                    if click[0]:
                        click_sound.play()
                        in_title = True
                        un_sf = p.font.SysFont('default', 100).render(username, True, color)
            
                else:
                    screen.blit(done, done_rect)
                    

    
        p.display.update()
        clock.tick(60)
        p.display.set_caption('VillageWars ' + __version__)
    
    return {'color':color,
            'skin':skin_num,
            'xp':userInfo['xp'],
            'coins':userInfo['coins']}
def joinGame(screen, clock, ip, port, username, newUserInfo):
    global music_playing
    music_playing = GameClient.main(screen, clock, username, __version__, newUserInfo, ip, port=port, musicPlaying=music_playing)
    if music_playing:
        p.mixer.music.load('../assets/sfx/menu.wav')
        p.mixer.music.play(-1, 0.0)
    

def startFromTitle(screen, clock, ip, port, username, userInfo):
    newUserInfo = titlePage(screen, clock, ip, port, username, userInfo)
    screen.blit(Connecting, (0, 0))
    p.display.update()
    joinGame(screen, clock, ip, port, username, newUserInfo)
    startFromTitle(screen, clock, ip, port, username, newUserInfo)

def main():
    screen, clock = getScreen()    
    ip, port, logInType = getServer(screen, clock)
    userInfo = {'valid':False, 'username_prompt':'Enter your username:', 'password_prompt':'Enter your password'}
    while not userInfo['valid']:
        username, password = GetUsernamePassword(screen, clock, userInfo['username_prompt'], userInfo['password_prompt'])
        userInfo = logIn(screen, clock, ip, port, logInType, username, password)
    global DOWNLOAD
    if DOWNLOAD:
        update(screen, clock, ip, port, username, userInfo)
    newUserInfo = titlePage(screen, clock, ip, port, username, userInfo)
    screen.blit(Connecting, (0, 0))
    p.display.update()
    joinGame(screen, clock, ip, port, username, newUserInfo)
    startFromTitle(screen, clock, ip, port, username, newUserInfo)





    


if __name__ == '__main__':
    main()

