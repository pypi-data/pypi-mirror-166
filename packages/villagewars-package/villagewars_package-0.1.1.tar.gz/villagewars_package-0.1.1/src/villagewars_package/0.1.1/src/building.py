import pygame
import toolbox as t
import math
from NPC import *

class Building(pygame.sprite.Sprite):
    def __init__(self, server, x, y, owner):
        '''
        owner must be client channel, not character.

        '''
        pygame.sprite.Sprite.__init__(self, self.gp)
        self.x = x
        self.y = y
        self.type = 'Please wait...'
        self.server = server
        self.level = 1
        self.owner = owner
        self.max_health = self.health = 50
        self.state = 'alive'
        self.dimensions = (675, 550)

        self.p = pygame.image.load('../assets/buildings/house.png')
        self.innerrect = self.p.get_rect(center=(x,y))
        self.rect = pygame.Surface((50, 50)).get_rect(midtop=(self.innerrect.midbottom[0], self.innerrect.midbottom[1] + 110))

        

    def post_init(self, rect):
        self.dim_rect = rect
        self.server.building_blocks.append(self.dim_rect)
        self.server.obs.append(self)
        

    def update(self):
        

        for p in self.server.players:
            if not p.pending:
                player = p.character
                angle = t.getAngle(self.rect.x, self.rect.y, player.x, player.y)
                
                p.Send({'action':'draw_building',
                        'image':'house',
                        'coords':(player.get_x(self), player.get_y(self)),
                        'health':self.health,
                        'max_health':self.max_health,
                        'angle':angle,
                        'color':self.owner.color,
                        'dimensions':self.dimensions,
                        'type':self.type,
                        'state':self.state,
                        'level':self.level})



    def getHurt(self, damage, attacker):
        
        if self.health > 0 and attacker != self.owner.character:
            self.health -= damage
            if self.health < 1:
                self.state = 'broken'
                self.owner.message = attacker.channel.username + ' has broken one of your ' + self.type + 's.'
                self.owner.message_count = 150
                self.owner.message_color = (255,0,0)
                self.health = 0
                attacker.destroyed += 1

    def isBuilding(self):
        return True


    def open_window(self, player):
        pass


    def Out(self, channel):
        
        channel.channel.in_window = False


    def heal(self, player):
        if player != self.owner.character:
            player.channel.message = "You can't heal someone else's building!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        
        elif player.food > 4:
            if self.health < self.max_health:
                self.health += 10
                if self.health > self.max_health:
                    self.health = self.max_health
                player.channel.message = 'You just healed this building 10 health for 5 food.'
                player.channel.message_count = 120
                player.channel.message_color = (255,205,0)
                player.food -= 5
            else:
                player.channel.message = 'This building is already at full health!'
                player.channel.message_count = 150
                player.channel.message_color = (50,50,255)
        else:
            player.channel.message = "You don't have enough food to heal this building!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False


    def clear(self, player):
        player.channel.in_window = False
        if player.gold > 1:
            player.channel.message = 'Cleared building for 2 gold'
            player.channel.message_count = 150
            player.channel.message_color = (255,205,0)
            player.gold -= 2

            self.server.building_blocks.remove(self.dim_rect)
            self.server.obs.remove(self)
            self.kill()
            
        else:
            player.channel.message = "You don't have enough food to clear this building!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        



class CentralBuilding(Building):
    dimensions = (675, 550)
    def __init__(self, server, x, y, owner):
        Building.__init__(self, server, x, y, owner)
        self.type = 'Central Building'
        self.max_health = self.health = 420
        self.dimensions = (675, 550)
        self.info = ('The Central Building is for buying other buildings.', 'If all your buildings are destroyed, you will not respawn.')

        rect = pygame.Rect(0, 0, 675, 550)
        rect.midtop = (x, y-round(self.p.get_height()/2))
        self.post_init(rect)


    def update(self):
        Building.update(self)



    
        
        
    def open_window(self, channel):
        if self.state == 'alive':
            channel.in_window = True
            channel.window = {'text':self.info,
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.heal), (1, self.buy_central_building), (2, self.buy_fitness_center), (3, self.buy_balloonist), (4, self.buy_farmers_guild), (5, self.buy_miners_guild), (6, self.buy_construction_site), (7, self.buy_restraunt), (8, self.Out)],
                              'simp':['Heal Building 10 health (5 food)', 'Portable Central Building (10 gold, 10 food)', 'Fitness Center (50 food)', 'Balloonist (30 gold)', "Farmer's Guild (25 food)", "Miner's Guild (25 gold)", 'Construction Site (60 gold)', 'Restoraunt (80 food)', 'Out']}
        elif self.state == 'broken':
            channel.in_window = True
            channel.window = {'text':('This building is broken.', ''),
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.clear), (1, self.Out)],
                              'simp':['Clear (2 gold)', 'Out']}

    def buy_central_building(self, player):
        if player.food > 9:
            if player.gold > 9:

                player.channel.text = 'Right click to place building'
                player.channel.build_to_place = PortableCentralBuilding
                player.channel.message = 'You just bought a Portable Central Building for 10 gold and 10 food.'
                player.channel.message_count = 150
                player.channel.message_color = (255,205,0)
                player.gold -= 10
                player.food -= 10
            else:
                player.channel.message = "You don't have enough gold to buy this!"
                player.channel.message_count = 150
                player.channel.message_color = (255,0,0)
        
        else:
            if player.gold > 9:
                player.channel.message = "You don't have enough food to buy this!"
            else:
                player.channel.message = "You can't afford this building!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False
        player.spence = 'gold'

    def buy_fitness_center(self, player):
        if player.food > 49:

            player.channel.text = 'Right click to place building'
            player.channel.build_to_place = FitnessCenter
            player.channel.message = 'You just bought a Fitness Center for 50 food.'
            player.channel.message_count = 150
            player.channel.message_color = (255,205,0)
            player.food -= 50
        else:
            player.channel.message = "You don't have enough food to buy this!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False
        player.spence = 'food'

    def buy_farmers_guild(self, player):
        if player.food > 24:

            player.channel.text = 'Right click to place building'
            player.channel.build_to_place = FarmersGuild
            player.channel.message = "You just bought a Farmer's Guild for 25 food."
            player.channel.message_count = 150
            player.channel.message_color = (255,205,0)
            player.food -= 25
        else:
            player.channel.message = "You don't have enough food to buy this!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False
        player.spence = 'food'

    def buy_miners_guild(self, player):
        if player.gold > 24:

            player.channel.text = 'Right click to place building'
            player.channel.build_to_place = MinersGuild
            player.channel.message = "You just bought a Miner's Guild for 25 gold."
            player.channel.message_count = 150
            player.channel.message_color = (255,205,0)
            player.gold -= 25
        else:
            player.channel.message = "You don't have enough gold to buy this!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False
        player.spence = 'gold'

    def buy_balloonist(self, player):
        if player.gold > 29:

            player.channel.text = 'Right click to place building'
            player.channel.build_to_place = Balloonist
            player.channel.message = 'You just bought a Balloonist for 30 gold.'
            player.channel.message_count = 150
            player.channel.message_color = (255,205,0)
            player.gold -= 30
        else:
            player.channel.message = "You don't have enough gold to buy this!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False
        player.spence = 'gold'

    def buy_construction_site(self, player):
        if player.gold > 59:

            player.channel.text = 'Right click to place building'
            player.channel.build_to_place = ConstructionSite
            player.channel.message = 'You just bought a Construction Site for 60 gold.'
            player.channel.message_count = 150
            player.channel.message_color = (255,205,0)
            player.gold -= 60
        else:
            player.channel.message = "You don't have enough gold to buy this!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False
        player.spence = 'gold'
    def buy_restraunt(self, player):
        if player.food > 79:

            player.channel.text = 'Right click to place building'
            player.channel.build_to_place = Restoraunt
            player.channel.message = 'You just bought a Restoraunt for 80 food.'
            player.channel.message_count = 150
            player.channel.message_color = (255,205,0)
            player.food -= 80
        else:
            player.channel.message = "You don't have enough food to buy this!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False
        player.spence = 'food'
    
        

class PortableCentralBuilding(CentralBuilding):
    dimensions = (585, 600)
    def __init__(self, server, x, y, owner, rect):
        CentralBuilding.__init__(self, server, x, y, owner)
        self.info = ('This building works the same way as the regular Central Building,', 'so you can use it as a portable central building.')
        self.type = 'Portable Central Building'
        self.health = self.max_health = 60
        self.dimensions = (585, 600)

        self.post_init(rect)


class RunningTrack(Building):
    dimensions = (800, 700)
    def __init__(self, server, x, y, owner, rect):
        Building.__init__(self, server, x, y, owner)
        self.info = ('This building increases your speed! Upgrade it to increase it', 'even more. (You can only have one Running Track at a time)')
        self.type = 'Running Track'
        self.health = self.max_health = 180
        self.dimensions = (800, 700)
        self.owner.character.speed += 3
        self.owner.character.moving += 3
        self.upgrade_cost = 90

        self.post_init(rect)

    def level_up(self, player):
        if player.food > 99:
            self.level += 1
            self.owner.character.speed += 3
            self.owner.character.moving += 3
            player.channel.message = 'You upgraded this Running Track to level ' + str(self.level) + ' for ' + str(self.upgrade_cost) + ' food.'
            player.channel.message_count = 150
            player.channel.message_color = (255,205,0)
            player.food -= self.upgrade_cost
            self.upgrade_cost += 30
            self.health = self.max_health = self.max_health + 40
            
        else:
            player.channel.message = "You don't have enough food to upgrade this building!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)

        
        player.channel.in_window = False

    def open_window(self, channel):
        if self.state == 'alive':
            channel.in_window = True
            if self.level < 3:
                channel.window = {'text':self.info,
                                  'upgradable':True,
                                  'health':(self.health, self.max_health),
                                  'building':self,
                                  'level':self.level,
                                  'options':[(0, self.level_up), (1, self.heal), (2, self.Out)],
                                  'simp':['Upgrade (' + str(self.upgrade_cost) + ' food)', 'Heal (5 food)', 'Out']}
            else:
                channel.window = {'text':self.info,
                                  'upgradable':False,
                                  'health':(self.health, self.max_health),
                                  'building':self,
                                  'level':self.level,
                                  'options':[(0, self.heal), (1, self.Out)],
                                  'simp':['Heal (10 food)', 'Out']}
        elif self.state == 'broken':
            channel.in_window = True
            channel.window = {'text':('This building is broken.', ''),
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.clear), (1, self.heal), (2, self.Out)],
                              'simp':['Clear (2 gold)', 'Out']}
            
    def getHurt(self, damage, attacker):
        
        if self.health > 0 and attacker != self.owner.character:
            self.health -= damage
            if self.health < 1:
                self.state = 'broken'
                self.owner.message = attacker.channel.username + ' has broken one of your ' + self.type + 's.'
                self.owner.message_count = 150
                self.owner.message_color = (255,0,0)
                self.health = 0
                self.owner.character.speed = 8
                self.owner.character.moving = 8
                attacker.destroyed += 1

class Gym(Building):
    dimensions = (800, 700)
    def __init__(self, server, x, y, owner, rect):
        Building.__init__(self, server, x, y, owner)
        self.info = ('This building increases your resistance! Upgrade it to increase it', 'even more. (You can only have one Gym at a time)')
        self.type = 'Gym'
        self.health = self.max_health = 180
        self.dimensions = (800, 700)
        self.owner.character.strength += 2
        
        self.upgrade_cost = 90

        self.post_init(rect)

    def level_up(self, player):
        if player.food > self.upgrade_cost - 1:
            self.level += 1
            self.owner.character.strength += 2
            
            player.channel.message = 'You upgraded this Gym to level ' + str(self.level) + ' for ' + str(self.upgrade_cost) + ' food.'
            player.channel.message_count = 150
            player.channel.message_color = (255,205,0)
            player.food -= self.upgrade_cost
            self.upgrade_cost += 30
            self.health = self.max_health = self.max_health + 40
            
        else:
            player.channel.message = "You don't have enough food to upgrade this building!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)

        
        player.channel.in_window = False

    def open_window(self, channel):
        if self.state == 'alive':
            channel.in_window = True
            if self.level < 3:
                channel.window = {'text':self.info,
                                  'upgradable':True,
                                  'health':(self.health, self.max_health),
                                  'building':self,
                                  'level':self.level,
                                  'options':[(0, self.level_up), (1, self.heal), (2, self.Out)],
                                  'simp':['Upgrade (' + str(self.upgrade_cost) + ' food)', 'Heal (5 food)', 'Out']}
            else:
                channel.window = {'text':self.info,
                                  'upgradable':False,
                                  'health':(self.health, self.max_health),
                                  'building':self,
                                  'level':self.level,
                                  'options':[(2, self.heal), (1, self.Out)],
                                  'simp':['Heal (5 food)', 'Out']}
        elif self.state == 'broken':
            channel.in_window = True
            channel.window = {'text':('This building is broken.', ''),
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.clear), (1, self.Out)],
                              'simp':['Clear (2 gold)', 'Out']}
            
    def getHurt(self, damage, attacker):
        
        if self.health > 0 and attacker != self.owner.character:
            self.health -= damage
            if self.health < 1:
                self.state = 'broken'
                self.owner.message = attacker.channel.username + ' has broken one of your ' + self.type + 's.'
                self.owner.message_count = 150
                self.owner.message_color = (255,0,0)
                self.health = 0
                self.owner.character.strength = 0
                attacker.destroyed += 1

class HealthCenter(Building):
    dimensions = (800, 700)
    def __init__(self, server, x, y, owner, rect):
        Building.__init__(self, server, x, y, owner)
        self.info = ('This building increases your maximum health! Upgrade it to increase it', 'even more. (You can only have one Health Center at a time)')
        self.type = 'Health Center'
        self.health = self.max_health = 180
        self.dimensions = (800, 700)
        self.owner.character.max_health += 30
        self.owner.character.health += 30
        
        self.upgrade_cost = 90

        self.post_init(rect)

    def level_up(self, player):
        if player.food > self.upgrade_cost - 1:
            self.level += 1
            self.owner.character.max_health += 30
            self.owner.character.health += 30
            
            player.channel.message = 'You upgraded this Health Center to level ' + str(self.level) + ' for ' + str(self.upgrade_cost) + ' food.'
            player.channel.message_count = 150
            player.channel.message_color = (255,205,0)
            player.food -= self.upgrade_cost
            self.upgrade_cost += 30
            self.health = self.max_health = self.max_health + 40
            
        else:
            player.channel.message = "You don't have enough food to upgrade this building!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)

        
        player.channel.in_window = False

    def open_window(self, channel):
        if self.state == 'alive':
            channel.in_window = True
            if self.level < 3:
                channel.window = {'text':self.info,
                                  'upgradable':True,
                                  'health':(self.health, self.max_health),
                                  'building':self,
                                  'level':self.level,
                                  'options':[(0, self.level_up), (1, self.heal), (2, self.Out)],
                                  'simp':['Upgrade (' + str(self.upgrade_cost) + ' food)', 'Heal (5 food)', 'Out']}
            else:
                channel.window = {'text':self.info,
                                  'upgradable':False,
                                  'health':(self.health, self.max_health),
                                  'building':self,
                                  'level':self.level,
                                  'options':[(2, self.heal), (1, self.Out)],
                                  'simp':['Heal (5 food)', 'Out']}
        elif self.state == 'broken':
            channel.in_window = True
            channel.window = {'text':('This building is broken.', ''),
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.clear), (1, self.Out)],
                              'simp':['Clear (2 gold)', 'Out']}
            
    def getHurt(self, damage, attacker):
        
        if self.health > 0 and attacker != self.owner.character:
            self.health -= damage
            if self.health < 1:
                self.state = 'broken'
                self.owner.message = attacker.channel.username + ' has broken one of your ' + self.type + 's.'
                self.owner.message_count = 150
                self.owner.message_color = (255,0,0)
                self.health = 0
                self.owner.character.max_health = 100
                if self.owner.character.health > 100:
                    self.owner.character.health = 100
                attacker.destroyed += 1




class FitnessCenter(Building):
    dimensions = (585, 600)
    def __init__(self, server, x, y, owner, rect):
        Building.__init__(self, server, x, y, owner)
        self.info = ('This building lets you buy the 3 fitness', 'buildings: Running Track, Gym and Health Center.')
        self.type = 'Fitness Center'
        self.health = self.max_health = 140
        self.dimensions = (585, 600)

        self.post_init(rect)

    def buy_running_track(self, player):
        yes = True
        for b in player.channel.get_buildings():
            if b.type == 'Running Track':
                yes = False
                player.channel.message = 'You already have a Running Track! You can only have one at a time.'
                player.channel.message_count = 150
                player.channel.message_color = (255,0,0)
                

        if yes:
            if player.gold > 74:

                player.channel.text = 'Right click to place building'
                player.channel.build_to_place = RunningTrack
                player.channel.message = 'You just bought a Running Track for 75 gold.'
                player.channel.message_count = 150
                player.channel.message_color = (255,205,0)
                player.gold -= 75
            else:
                player.channel.message = "You don't have enough gold to buy this!"
                player.channel.message_count = 150
                player.channel.message_color = (255,0,0)
        player.channel.in_window = False
        player.spence = 'gold'

    def buy_gym(self, player):
        yes = True
        for b in player.channel.get_buildings():
            if b.type == 'Gym':
                yes = False
                player.channel.message = 'You already have a Gym! You can only have one at a time.'
                player.channel.message_count = 150
                player.channel.message_color = (255,0,0)
                

        if yes:
            if player.gold > 74:

                player.channel.text = 'Right click to place building'
                player.channel.build_to_place = Gym
                player.channel.message = 'You just bought a Gym for 75 gold.'
                player.channel.message_count = 150
                player.channel.message_color = (255,205,0)
                player.gold -= 75
            else:
                player.channel.message = "You don't have enough gold to buy this!"
                player.channel.message_count = 150
                player.channel.message_color = (255,0,0)
        player.channel.in_window = False
        player.spence = 'gold'

    def buy_health_center(self, player):
        yes = True
        for b in player.channel.get_buildings():
            if b.type == 'Health Center':
                yes = False
                player.channel.message = 'You already have a Health Center! You can only have one at a time.'
                player.channel.message_count = 150
                player.channel.message_color = (255,0,0)
                

        if yes:
            if player.gold > 74:

                player.channel.text = 'Right click to place building'
                player.channel.build_to_place = HealthCenter
                player.channel.message = 'You just bought a Health Center for 75 gold.'
                player.channel.message_count = 150
                player.channel.message_color = (255,205,0)
                player.gold -= 75
            else:
                player.channel.message = "You don't have enough gold to buy this!"
                player.channel.message_count = 150
                player.channel.message_color = (255,0,0)
        player.channel.in_window = False
        player.spence = 'gold'


    def open_window(self, channel):
        if self.state == 'alive':
            channel.in_window = True
            channel.window = {'text':self.info,
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.heal), (1, self.buy_running_track), (2, self.buy_gym), (3, self.buy_health_center), (4, self.Out)],
                              'simp':['Heal (5 food)', 'Running Track (75 gold)', 'Gym (75 gold)', 'Health Center (75 gold)', 'Out']}
        elif self.state == 'broken':
            channel.in_window = True
            channel.window = {'text':('This building is broken.', ''),
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.clear), (1, self.Out)],
                              'simp':['Clear (2 gold)', 'Out']}


class Balloonist(Building):
    dimensions = (500, 495)
    def __init__(self, server, x, y, owner, rect):
        Building.__init__(self, server, x, y, owner)
        self.info = ('This building lets you upgrade your attack stat.', '')
        self.type = 'Balloonist'
        self.health = self.max_health = 120
        self.dimensions = (500, 495)
        self.upgrade_cost = 50


        self.post_init(rect)

    def level_up(self, player):
        if player.gold > self.upgrade_cost - 1:
            self.level += 1
            
            
            player.channel.message = 'You upgraded this Balloonist to level ' + str(self.level) + ' for ' + str(self.upgrade_cost) + ' gold.'
            player.channel.message_count = 150
            player.channel.message_color = (255,205,0)
            player.gold -= self.upgrade_cost
            self.upgrade_cost += 20
            self.health = self.max_health = self.max_health + 50
            
        else:
            player.channel.message = "You don't have enough gold to upgrade this building!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False

    def open_window(self, channel):
        if self.state == 'alive':
            channel.in_window = True
            channel.window = {'text':self.info,
                              'upgradable':True,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.level_up), (1, self.heal), (2, self.upgrade_balloon_damage), (3, self.upgrade_balloon_speed), (4, self.upgrade_balloon_knockback), (5, self.Out)],
                              'simp':['Upgrade ( ' + str(self.upgrade_cost) + ' food)', 'Heal (5 food)', ' + Balloon Attack (' + str(channel.character.damage_cost) + ' gold)', ' + Balloon Speed (' + str(channel.character.speed_cost) + ' gold)', ' + Balloon Knockback (' + str(channel.character.knockback_cost) + ' gold)', 'Out']}
        elif self.state == 'broken':
            channel.in_window = True
            channel.window = {'text':('This building is broken.', ''),
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.clear), (1, self.Out)],
                              'simp':['Clear (2 gold)', 'Out']}

    def upgrade_balloon_speed(self, player):
        if player.gold > player.speed_cost - 1:
            if player.balloon_speed == 18 and self.level == 1:
                player.channel.message = "You have to upgrade the building before upgrading this again."
                player.channel.message_count = 150
                player.channel.message_color = (255,0,0)
            else:
                
                player.balloon_speed += 1
            
                player.channel.message = "You upgraded your balloons' speed for " + str(self.owner.character.speed_cost) + " gold."
                player.channel.message_count = 150
                player.channel.message_color = (255,205,0)
                player.gold -= player.speed_cost

                player.speed_cost += 10

            
        else:
            player.channel.message = "You don't have enough gold to upgrade your balloons' speed!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False

    def upgrade_balloon_knockback(self, player):
        if player.gold > player.knockback_cost - 1:
            if player.knockback == 16 and self.level == 1:
                player.channel.message = "You have to upgrade the building before upgrading this again."
                player.channel.message_count = 150
                player.channel.message_color = (255,0,0)
            else:
                
                player.knockback += 3
            
                player.channel.message = "You upgraded your balloons' knockback for " + str(self.owner.character.knockback_cost) + " gold."
                player.channel.message_count = 150
                player.channel.message_color = (255,205,0)
                player.gold -= player.knockback_cost

                player.knockback_cost += 10

            
        else:
            player.channel.message = "You don't have enough gold to upgrade your balloons' knockback!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False

    def upgrade_balloon_damage(self, player):
        if player.gold > player.damage_cost - 1:
            if player.attack == 14 and self.level == 1:
                player.channel.message = "You have to upgrade the building before upgrading this again."
                player.channel.message_count = 150
                player.channel.message_color = (255,0,0)
            else:
                player.attack += 2
            
                player.channel.message = "You upgraded your attack for " + str(self.owner.character.damage_cost) + " gold."
                player.channel.message_count = 150
                player.channel.message_color = (255,205,0)
                player.gold -= player.damage_cost

                player.damage_cost += 10

            
        else:
            player.channel.message = "You don't have enough gold to upgrade your attack!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False




class FarmersGuild(Building):
    dimensions = (600, 500)
    def __init__(self, server, x, y, owner, rect):
        Building.__init__(self, server, x, y, owner)
        self.info = ('This building sends farmers out to collect wheat', 'for you.')
        self.type = "Farmer's Guild"
        self.health = self.max_health = 140
        self.dimensions = (600, 500)
        Farmer(self)

        self.post_init(rect)

    def getHurt(self, damage, attacker):
        
        if self.health > 0 and attacker != self.owner.character:
            self.health -= damage
            if self.health < 1:
                self.state = 'broken'
                self.owner.message = attacker.channel.username + ' has broken one of your ' + self.type + 's.'
                self.owner.message_count = 150
                self.owner.message_color = (255,0,0)
                self.health = 0
                attacker.destroyed += 1
                for farmer in self.server.NPCs:
                    if farmer.building == self:
                        farmer.kill()

    


    def open_window(self, channel):
        if self.state == 'alive':
            channel.in_window = True
            channel.window = {'text':self.info,
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.heal), (1, self.Out)],
                              'simp':['Heal (5 food)', 'Out']}
        elif self.state == 'broken':
            channel.in_window = True
            channel.window = {'text':('This building is broken.', ''),
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.clear), (1, self.Out)],
                              'simp':['Clear (2 gold)', 'Out']}

class MinersGuild(Building):
    dimensions = (500, 600)
    def __init__(self, server, x, y, owner, rect):
        Building.__init__(self, server, x, y, owner)
        self.info = ('This building sends miners out to mine gold', 'for you.')
        self.type = "Miner's Guild"
        self.health = self.max_health = 140
        self.dimensions = (500, 600)
        Miner(self)
        

        self.post_init(rect)

    def getHurt(self, damage, attacker):
        
        if self.health > 0 and attacker != self.owner.character:
            self.health -= damage
            if self.health < 1:
                self.state = 'broken'
                self.owner.message = attacker.channel.username + ' has broken one of your ' + self.type + 's.'
                self.owner.message_count = 150
                self.owner.message_color = (255,0,0)
                self.health = 0
                attacker.destroyed += 1
                for miner in self.server.NPCs:
                    if miner.building == self:
                        miner.kill()

    


    def open_window(self, channel):
        if self.state == 'alive':
            channel.in_window = True
            channel.window = {'text':self.info,
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.heal), (1, self.Out)],
                              'simp':['Heal (5 food)', 'Out']}
        elif self.state == 'broken':
            channel.in_window = True
            channel.window = {'text':('This building is broken.', ''),
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.clear), (1, self.Out)],
                              'simp':['Clear (2 gold)', 'Out']}










        



def builder(b, p):
    if b.isBuilding(object()):
        x, y = p.x, p.y - 140
        image = pygame.image.load('../assets/buildings/house.png')
        _rect = image.get_rect(center=(x, y))
        width, height = b.dimensions
        rect = pygame.Rect(0, 0, width, height)
        rect.midtop = (x, y-round(image.get_height()/2))

    else:
        x, y = p.x, p.y - 240
        surf = pygame.Surface((360, 360))
        rect = surf.get_rect(center=(x, y))

    if rect.left < 0 or rect.right > 6000 or rect.top < 0 or rect.bottom > 3900:
        return False, rect
    
    
    
    for obs in p.channel.server.building_blocks:
        if rect.colliderect(obs):
            return False, rect
    return True, rect



class ConstructionSite(Building):
    dimensions = (560, 560)
    def __init__(self, server, x, y, owner, rect):
        Building.__init__(self, server, x, y, owner)
        self.info = ('This building lets you buy defences for your village. Crates, Gates, Archery Towers, Robot Guards...', '')
        self.type = 'Construction Site'
        self.health = self.max_health = 160
        self.dimensions = (560, 560)
        self.upgradable = True

        self.post_init(rect)

    def buy_crate(self, player):
        if player.food > 1:
            player.channel.message = 'You bought a crate for 2 food.'
            player.channel.message_count = 150
            player.channel.message_color = (255,205,0)
            player.food -= 2
            player.crates += 1
        else:
            player.channel.message = "You don't have enough food for this!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        
        player.channel.in_window = False

    def buy_gate(self, player):
        if player.gold > 39:
            player.channel.message = 'You bought a gate for 40 gold.'
            player.channel.message_count = 150
            player.channel.message_color = (255,205,0)
            player.gold -= 40
            player.channel.text = 'Press x to place gate'
        else:
            player.channel.message = "You don't have enough gold for this!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        
        player.channel.in_window = False

    def buy_tnt(self, player):
        if player.gold > 99:
            if player.food > 99:
                player.channel.message = 'You bought TNT for 100 gold and 100 food.'
                player.channel.message_count = 150
                player.channel.message_color = (255,205,0)
                player.gold -= 100
                player.food -= 100
                player.channel.text = 'Press x to place TNT'
            else:
                player.channel.message = "You don't have enough food for this!"
                player.channel.message_count = 150
                player.channel.message_color = (255,0,0)
        else:
            if player.food > 99:
                player.channel.message = "You don't have enough gold for this!"
                player.channel.message_count = 150
                player.channel.message_color = (255,0,0)
            else:
                player.channel.message = "You can't afford this!"
                player.channel.message_count = 150
                player.channel.message_color = (255,0,0)
        
        player.channel.in_window = False

    def buy_archery_tower(self, player):
        if player.food > 19:
            if player.gold > 109:

                player.channel.text = 'Right click to place building'
                player.channel.build_to_place = ArcheryTower
                player.channel.message = 'You just bought an Archery Tower for 110 gold and 20 food.'
                player.channel.message_count = 150
                player.channel.message_color = (255,205,0)
                player.gold -= 110
                player.food -= 20
                player.spence = 'gold'
            else:
                player.channel.message = "You don't have enough gold to buy this!"
                player.channel.message_count = 150
                player.channel.message_color = (255,0,0)
        
        else:
            if player.gold > 9:
                player.channel.message = "You don't have enough food to buy this!"
            else:
                player.channel.message = "You can't afford an Archery Tower!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False

    def level_up(self, player):
        if player.gold > 29:
            self.level = 2
            
            
            player.channel.message = 'You upgraded this Balloonist to level 2 for 30 gold.'
            player.channel.message_count = 150
            player.channel.message_color = (255,205,0)
            player.gold -= 30
            self.upgradable = False
            self.health = self.max_health = 200
            
        else:
            player.channel.message = "You don't have enough gold to upgrade this building!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False
        



    def open_window(self, channel):
        if self.state == 'alive':
            if self.upgradable:
                channel.in_window = True
                channel.window = {'text':self.info,
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.level_up), (1, self.heal), (2, self.buy_crate), (3, self.buy_gate), (4, self.buy_tnt), (5, self.Out)],
                              'simp':['Upgrade', 'Heal (5 food)', 'Crate (2 food)', 'Gate (40 gold)', 'Tnt (100 gold, 100 food)', 'Out']}
            else:
                channel.in_window = True
                channel.window = {'text':self.info,
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.heal), (1, self.buy_crate), (2, self.buy_gate), (3, self.buy_tnt), (4, self.buy_archery_tower), (5, self.Out)],
                              'simp':['Heal (5 food)', 'Crate (2 food)', 'Gate (20 gold)', 'Tnt (100 gold, 100 food)', 'Archery Tower (110 gold, 20 food)', 'Out']}
        elif self.state == 'broken':
            channel.in_window = True
            channel.window = {'text':('This building is broken.', ''),
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.clear), (1, self.Out)],
                              'simp':['Clear (2 gold)', 'Out']}




class Restoraunt(Building):
    dimensions = (600, 580)
    def __init__(self, server, x, y, owner, rect):
        Building.__init__(self, server, x, y, owner)
        self.info = ('This building lets you buy meals, which heal you when you eat them.', '')
        self.type = 'Restoraunt'
        self.health = self.max_health = 220
        self.dimensions = (600, 580)

        self.post_init(rect)

    def buy_meal(self, player):

        if player.food > 11:
                if player.meal:
                    player.channel.message = "You already have a meal! Eat it before buying another one."
                    player.channel.message_count = 150
                    player.channel.message_color = (0,0,255)

                else:
                    player.meal = True
                    player.channel.message = "You bought a meal for 12 food."
                    player.channel.message_count = 150
                    player.channel.message_color = (255,205,0)
                    player.food -= 12



            
        else:
            player.channel.message = "You don't have enough food to buy a meal!"
            player.channel.message_count = 150
            player.channel.message_color = (255,0,0)
        player.channel.in_window = False



    def open_window(self, channel):
        if self.state == 'alive':
            channel.in_window = True
            channel.window = {'text':self.info,
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.heal), (1, self.buy_meal), (2, self.Out)],
                              'simp':['Heal (5 food)', 'Buy Meal (12 food)', 'Out']}
        elif self.state == 'broken':
            channel.in_window = True
            channel.window = {'text':('This building is broken.', ''),
                              'upgradable':False,
                              'health':(self.health, self.max_health),
                              'building':self,
                              'level':self.level,
                              'options':[(0, self.clear), (1, self.Out)],
                              'simp':['Clear (2 gold)', 'Out']}












                
            
