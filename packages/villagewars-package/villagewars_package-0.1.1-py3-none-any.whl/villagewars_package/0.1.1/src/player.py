import pygame
import toolbox as t
from balloon import Balloon
from obstacle import Crate, Gate, TNT
from building import *
class Character():



    def __init__(self, channel, x, y):

        self.channel = channel
        self.image = pygame.image.load('../assets/Player_01.png')
        self.x = x
        self.y = y
        self.x_flip = 500-x
        self.y_flip = 325-y
        self.angle = 0
        self.speed = self.moving = 8
        
        self.health = self.max_health = 100
        self.hurt_count = 1
        self.dead = False
        self.gold = 0
        self.food = 0
        
        self.strength = 0
        self.obs = []
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.shoot_cooldown = 0
        self.crate_cooldown = 0

        self.respawn_count = 0
        self.meal = False

        self.crates = 0
        self.spence = 'gold'


        ### Stat Side ###

        
        self.attack = 10
        self.damage_cost = 30
        
        self.balloon_speed = 16
        self.speed_cost = 30
        
        self.knockback = 10
        self.knockback_cost = 30


        ### Info Side ###

        self.kills = 0
        self.destroyed = 0
        self.deaths = 0
        self.eliminations = 0
        
        

    def get_x(self, item):

        try:
            return item.x + self.x_flip
        except:
            return item + self.x_flip
        

    def get_y(self, item):

        try:
            return item.y + self.y_flip
        except:
            return item + self.y_flip

    def move_x(self, a):
        
        self.x += a
        self.x_flip -= a

        self.rect = self.image.get_rect(center=(self.x, self.y))


        if not self.dead:
            for item in self.obs:
                thr = False
                if item.__class__ == Gate and item.owner == self:
                    thr = True
                if self.rect.colliderect(item.innerrect) and not thr:
                    self.x -= a
                    self.x_flip += a

                
                    

    def move_y(self, a):
        self.y += a
        self.y_flip -= a

        self.rect = self.image.get_rect(center=(self.x, self.y))

        if not self.dead:
            for item in self.obs:
                thr = False
                if item.__class__ == Gate and item.owner == self:
                    thr = True
                if self.rect.colliderect(item.innerrect) and not thr:
                    self.y -= a
                    self.y_flip += a
             
                    
        
    def move(self, angle):
        x, y = t.getDir(angle, self.get_speed())
        self.move_x(round(x))
        self.move_y(round(y))

    def update(self, obs):

        if self.hurt_count > 0:
            self.hurt_count -= 1
            image = 'default_hurt'
        else:
            image = 'default'

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.crate_cooldown > 0:
            self.crate_cooldown -= 1

        if self.respawn_count > 0:
            self.respawn_count -= 1
            if self.respawn_count == 0:
                self.respawn()
        
        self.obs = obs[:]
        
        
        if not self.dead:
            for p in self.channel.server.players:
            
                if p != self.channel:
                    if not p.pending:
                    
                        p.Send({'action':'draw_player',
                                'image':image,
                                'coords':(p.character.get_x(self), p.character.get_y(self)),
                                'angle':self.angle,
                                'color':self.channel.color,
                                'username':self.channel.username,
                                'health':self.health,
                                'max_health':self.max_health})
                else:
                    
                    p.Send({'action':'draw_player',
                            'image':image,
                            'coords':(p.character.get_x(self), p.character.get_y(self)),
                            'angle':self.angle,
                            'color':self.channel.color,
                            'username':self.channel.username,
                            'health':self.health,
                            'gold':self.gold,
                            'food':self.food,
                            'max_health':self.max_health})
                    
                    p.Send({'action':'meal',
                            'food?':self.meal})
                    p.Send({'action':'crates',
                            'crates':self.crates})


            if self.channel.in_window:
                
                window = {'info':self.channel.window['text'],
                              'owner':self.channel.window['building'].owner.username,
                              'upgradable':self.channel.window['upgradable'],
                              'health':self.channel.window['health'],
                              'options':self.channel.window['simp'],
                              'level':self.channel.window['level'],
                              'color':self.channel.window['building'].owner.color}

                
                
                self.channel.Send({'action':'draw_window',
                                   'window':window})
        

    def HandleInput(self, keys, mouse):
        if not self.channel.in_window:
            self.angle = t.getAngle(500, 325, mouse[0], mouse[1])
            
            if keys[pygame.K_SPACE]:
                self.move(self.angle)

            if keys[pygame.K_x]:
                if self.channel.text == 'Press x to place gate':
                    self.channel.text = ''
                    x, y = self.x, self.y
                    move = t.getDir(self.angle, 100)
                    x += move[0]
                    y += move[1]
                    rotated = False
                    if 45 < self.angle < 135 or -45 > self.angle > -135:
                        rotated = True
                    
                    Gate(self, x, y, rotated)
                    self.crate_cooldown = 40

                elif self.channel.text == 'Press x to place TNT':
                    self.channel.text = ''
                    x, y = self.x, self.y
                    move = t.getDir(self.angle, 80)
                    x += move[0]
                    y += move[1]
                    
                    TNT(self, x, y)
                    self.crate_cooldown = 40
                    
                elif not self.dead and self.crate_cooldown == 0 and self.crates > 0:
                    x, y = self.x, self.y
                    move = t.getDir(self.angle, 80)
                    x += move[0]
                    y += move[1]
                    
                    Crate(self, x, y)
                    self.crate_cooldown = 30
                    self.crates -= 1

            if keys[pygame.K_DELETE] and self.channel.build_to_place != None:
                self.channel.build_to_place = None
                self.channel.text = ''
                if self.spence == 'gold':
                    self.channel.message = 'You deleted the building, you gain 10 gold.'
                    self.gold += 10
                else:
                    self.channel.message = 'You deleted the building, you gain 10 food.'
                    self.food += 10
                self.channel.message_count = 150
                self.channel.message_color = (255,100,0)

            if keys[pygame.K_c]:
                if self.meal and not self.dead:
                    self.meal = False
                    self.health = self.max_health
                    self.channel.message = 'You ate your meal, your health bar is now full again.'
                    self.channel.message_count = 150
                    self.channel.message_color = (255,205,0)

            if mouse[2] and not self.dead:

                not_shoot = False
                if self.dead == False:
                    for farm in self.channel.server.resources:
                        if farm.HandleInput(mouse, self):
                            not_shoot = True

                if not not_shoot:
                    self.shoot()

            if mouse[3]:
                print(round(self.x), round(self.y))
        if self.channel.in_window and mouse[2]:
            not_farm = True
            not_shoot = True
            for option in self.channel.window['options']:
                
                x = 250
                y = 200 + option[0] * 40
                rect = pygame.Rect(x, y, 500, 50)

                if rect.collidepoint((mouse[0], mouse[1])):
                    option[1](self)

        if mouse[4]:
            
            if self.channel.build_to_place != None:
                result = builder(self.channel.build_to_place, self)
                to_build = result[0]
                if to_build:
                    b = self.channel.build_to_place(self.channel.server, self.x, self.y - 140, self.channel, result[1])

                    self.channel.text = ''
                    self.channel.build_to_place = None
                    try:
                        self.channel.message = 'You have placed a ' + b.type + '.'
                    except:
                        self.channel.message = 'You have placed an Archery Tower.'
                    self.channel.message_count = 150
                    self.channel.message_color = (255,205,0)
                else:
                    
                    self.channel.message = 'You cannot place this building here.'
                    self.channel.message_count = 100
                    self.channel.message_color = (255,0,0)
            else:
                for b in self.channel.server.buildings:
                    rect = b.p.get_rect(center=(self.get_x(b), self.get_y(b)))
                    if rect.collidepoint((mouse[0], mouse[1])):
                        b.open_window(self.channel)
                    else:
                        rect = b.rect.copy()
                        rect.x, rect.y = self.get_x(rect), self.get_y(rect)
                        if rect.collidepoint((mouse[0], mouse[1])):
                            b.open_window(self.channel)
            
        
    def getHurt(self, damage, attacker, angle, knockback):
        self.health -= (damage - self.strength)
        x, y = t.getDir(angle, knockback)
        self.move_x(x)
        self.move_y(y)
        self.hurt_count = 8
        if not self.health > 0:
            for p in self.channel.server.players:
                screen = pygame.Rect(0, 0, 1000, 650)
                screen.center = p.character.rect.center
                if screen.colliderect(self.rect):
                    p.Send({'action':'sound', 'sound':'die'})
            self.channel.text = ''
            self.channel.build_to_place = None
            self.dead = True
            attacker.kills += 1
            self.deaths += 1
            self.crates = 0
            self.meal = False
            self.moving = 16
            for channel in self.channel.server.players:
                channel.message = attacker.channel.username + ' has exploded ' + self.channel.username + '.'
                channel.message_count = 150
                channel.message_color = (255,205,0)
                if channel == self.channel:
                    channel.message_color = (255,0,0)
            if len(self.channel.get_buildings()) != 0:
                self.respawn_count = 200
            else:
                attacker.eliminations += 1
                guys = []
                for channel in self.channel.server.players:
                    channel.message = attacker.channel.username + ' has eliminated ' + self.channel.username + ' from the game.'
                    channel.message_count = 150
                    channel.message_color = (255,205,0)
                    if channel == self.channel:
                        channel.message = attacker.channel.username + ' has eliminated you. You may stay to watch, or leave.'
                        channel.message_color = (255,0,0)
                    if channel.character.dead == False:
                        guys.append(channel)
                    elif channel.character.respawn_count > 0:
                        guys.append(channel)
                if len(guys) == 1:
                    self.channel.server.terminate(guys[0])

        self.channel.in_window = False
        self.channel.window = None
                


    def shoot(self):
        if self.shoot_cooldown == 0:
            Balloon(self.channel.server, self)
            self.shoot_cooldown = 15
            for p in self.channel.server.players:
                screen = pygame.Rect(0, 0, 1000, 650)
                screen.center = p.character.rect.center
                if screen.colliderect(self.rect):
                    p.Send({'action':'sound', 'sound':'shot'})


    def respawn(self):
        self.dead = False
        self.x, self.y = self.channel.server.ST_COORDS[self.channel.number]
        self.x_flip = 500-self.x
        self.y_flip = 325-self.y
        self.moving = self.speed
        self.channel.message = 'You respawned. You respawn as long as you have buildings alive.'
        self.channel.message_count = 150
        self.channel.message_color = (128,255,5)
        self.health = self.max_health


    def get_speed(self):
        speed = self.moving
        speed /= self.channel.fps
        speed *= 30

        return speed
        



    

    









            
