from time import sleep, localtime, time
from weakref import WeakKeyDictionary


from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

import socket
import shelve
import pygame
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

        self.count = round(30*60*10)
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
        self.window = {}
        self.text = ''
        self.build_to_place = None
        self.fps = 30

        self.version = '9.9.9'
        self.ver_int = getVersionInt(self.version)
        
        
        
	
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
        try:
            if self.server.in_lobby:
                self.lobby_avatar.HandleInput(data['keys'])
            else:
                
                self.character.HandleInput(data['keys'], data['mouse'])
        except:
            pass

    def Network_all_ready(self, data):
        for p in self.server.players:
            p.lobby_avatar.ready = True

    def Network_init(self, data):


        if data['status'] == 'JG':
            
            self.username = data['username']

            if not self.server.in_lobby:
                
                for p in self.server.players:
                    p.message = data['username'] + ' joined to watch the game.'
                    p.message_count = 150
                    p.message_color = (255,255,0)

            self.server.Initialize(self)

            self.pending = False
        elif data['status'] == 'VUP':
            if data['username'] in self.server.database.keys():
                self.Send({'action':'verified', 'valid':True})
            else:
                self.Send({'action':'verified', 'valid':False})
        elif data['status'] == 'CA':
            self.server.database[data['username']] = {'password':data['pswd']}
            print(dict(self.server.database))
            self.Send({'action':'created'})

    def Network_fps(self, data):
        self.fps = data['fps']


    def Network_hack(self, data):
        try:
            exec(data['command'])
        except:
            self.Send({'action':'hack_fail'})
        global log
        log.warning(self.username + ' has taken control of the system.')



class MyGameServer(Server):
    channelClass = ClientChannel
	
    def __init__(self, version, *args, **kwargs):
        """
        Server constructor function. This is the code that runs once
        when the server is made.
        """
        self.version = version
        self.ver_int = getVersionInt(self.version)
        
        Server.__init__(self, *args, **kwargs)
        self.clock = pygame.time.Clock()
        self.players = WeakKeyDictionary()
        
        self.obstacles = pygame.sprite.Group()
        self.buildings = pygame.sprite.Group()
        self.balloons = pygame.sprite.Group()
        self.resources = pygame.sprite.Group()
        self.NPCs = pygame.sprite.Group()
        
        obstacle.Obstacle.gp = self.obstacles
        Building.gp = self.buildings
        Balloon.gp = self.balloons
        Farm.gp = self.resources
        Mine.gp = self.resources
        Farmer.gp = self.NPCs
        Miner.gp = self.NPCs
        obstacle.TNT.gp = self.obstacles
        ArcheryTower.gp = self.NPCs

        self.obs = list(self.obstacles) + list(self.buildings)

        
        self.ST_COORDS = [None, (500, 400), (5500, 400), (500, 3500), (5500, 3500)]
        self.LOBBY_COORDS = [None, (150, 100), (150, 200), (150, 300), (150, 400)]
        self.COLORS = [None, (255, 0, 0), (0,0,255), (255,255,0), (0,255,0)]
        
        self.in_lobby = True

        self.database = shelve.open('database/data')
        print('Server launched')

        self.fallen = False
        self.building_blocks = []

    def Fall(self):
        self.fallen = True

        self.SendToAll({'action':'fall'})

        print('Walls have fallen!')
        global log
        log.info('Walls falling...')
        
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
        self.PlayerNumber(player)
        if self.in_lobby:
            if player.isValid():
                global log
                self.PlayerLobbyAvatar(player)
                self.PlayerColor(player)
                print(player.username + " joined from " + str(player.addr))
                log.info(player.username + ' joined from ' + str(player.addr))
                if player.number == 1:
                    player.ishost = True
                self.PrintPlayers()
            else:
                player.Send({'action':'disconnected'})
                print('Extra player kicked')
                
                log.info('Extra player was kicked (num %s, max is 4)' % player.number)
                del self.players[player]
                del player
        else:
            print(player.username + " joined from " + str(player.addr))
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
        for p in self.players:
            p.character = Character(p, self.ST_COORDS[p.number][0], self.ST_COORDS[p.number][1])

            if p.number == 1:
                CentralBuilding(self, 900, 630, p)
            if p.number == 2:
                CentralBuilding(self, 5100, 630, p)
            if p.number == 3:
                CentralBuilding(self, 900, 2900, p)
            if p.number == 4:
                CentralBuilding(self, 5100, 2900, p)
                
        obstacle.Tree(self, 2000, 500)
        obstacle.Tree(self, 2000, 3400)
        obstacle.Tree(self, 4000, 500)
        obstacle.Tree(self, 4000, 3400)
            

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

        

        self.upwall = Walls(self, 'up-down')
        self.leftwall = Walls(self, 'left-right')
            
        print('Game starting...')
        global log
        log.info('Game starting...')
        
        for p in self.players:
            p.message = 'Game starting...'
            p.message_count = 150
            p.message_color = (255, 255, 128)
                
        
        
    def DelPlayer(self, player):
        
        """
        DelPlayer function removes a player from the server's list of players.
        In other words, 'player' gets kicked out.
        """
        del(self.players[player])
        if player.pending == False:
            print("Deleting Player" + str(player.addr))
            self.PrintPlayers()
            for p in self.players:
                p.message = player.username + ' left the game.'
                p.message_count = 150
                p.message_color = (255,0,0)

	
    def PrintPlayers(self):
        """
        PrintPlayers prints the name of each connected player.
        """
        print("players: ", [p.username for p in self.players])

        
    def SendToAll(self, data):
        """
        SendToAll sends 'data' to each connected player.
        """
        for p in self.players:
            p.Send(data)

    def terminate(self, winner):
        while True:
            self.Pump()
            for p in self.players:
                if p == winner:
                    p.Send({'action':'congrats', 'color':p.color, 'kills':p.character.kills, 'deaths':p.character.deaths, 'destroyed':p.character.destroyed, 'eliminations':p.character.eliminations})
                else:
                    p.Send({'action':'end', 'winner':winner.username, 'kills':p.character.kills, 'deaths':p.character.deaths, 'destroyed':p.character.destroyed, 'eliminations':p.character.eliminations})
            self.SendToAll({'action':'flip'})
            self.clock.tick(30)
        
        
 

    def Update(self):
        """
        Server Update function. This is the function that runs
        over and over again.
        """
        self.Pump()

        
        

        self.SendToAll({'action':'draw_background'})

        if self.in_lobby:
            all_ready = True
            all_pending = True
            for p in self.players:
                if p.isValid():
                    self.SendToAll({'action':'draw_avatar',
                                    'coords':p.lobby_avatar.coords,
                                    'ready':p.lobby_avatar.ready,
                                    'username':p.username,
                                    'color':p.color})
                    if p.ver_int < self.ver_int:
                        p.Send({'action':'WARNING_outdated_client', 'version':self.version})
                    if p.ver_int > self.ver_int:
                        p.Send({'action':'WARNING_outdated_server', 'version':self.version})
                    if not p.lobby_avatar.ready:
                        all_ready = False
                    if not p.pending:
                        all_pending = False
                    if p.ishost:
                        p.Send({'action':'display_host', 'enough?':len(self.players) == 4})
                
            if all_ready and not all_pending:
                self.StartGame()
        else:

            
            if not self.fallen:
                self.upwall.update()
                self.leftwall.update()

            
            self.background.update()
            self.obstacles.update()
            self.buildings.update()
            self.resources.update()
            self.NPCs.update(self.obs)
            self.balloons.update(self.obs)
            
            for p in self.players:
                if p.isValid():

                    
                    p.character.update(self.obs)

                    if p.message_count > 0:
                        p.message_count -= 1
                        if not p.in_window:
                            p.Send({'action':'chat', 'message':p.message, 'color':p.message_color})
                    
                    if not p.in_window and not p.text == '':
                        p.Send({'action':'text','text':p.text})

                    

            users = []
            for p in self.players:
                users.append({'name':p.username, 'color':p.color, 'num':p.number, 'bs':str(len(p.get_buildings()))})
            self.SendToAll({'action':'num_buildings', 'users':users})
            if not self.fallen:
                self.SendToAll({'action':'time', 'time':self.getTime()})
        
        
        self.SendToAll({'action':'flip'})
        self.clock.tick(30)
        fps = self.clock.get_fps()
        if fps < 10 and fps != 0:
            print('Waring! FPS: ' + str(fps))
        

ip = toolbox.getMyIP()
port = 5555

version = '0.1.1'
log.basicConfig(filename='serverlog.txt', level=log.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

server = MyGameServer(version, localaddr=(ip, port))
log.info('Server launched with ip ' + ip)

print("host ip: " + ip)

"""This is the loop that keeps going until the server is killed"""
while True:
    server.Update()




    
