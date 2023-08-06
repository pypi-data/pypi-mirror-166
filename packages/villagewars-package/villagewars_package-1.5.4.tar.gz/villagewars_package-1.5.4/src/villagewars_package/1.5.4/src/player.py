import pygame
import toolbox as t
from balloon import Balloon, Bolt
from obstacle import *
from building import *
from animations import *
from NPC import ArcheryTower

class Character():



    def __init__(self, channel, x, y):

        self.channel = channel
        self.image = pygame.Surface((50, 50))
        self.x = x
        self.y = y
        self.x_flip = 500-x
        self.y_flip = 325-y
        self.angle = 0
        self.speed = self.moving = 8
        
        self.health = self.max_health = 100
        self.hurt_count = 1
        self.dead = False

        if self.channel.username == 'ModestNoob' or self.channel.username == 'f':
            self.gold = 100000
            self.food = 100000
        else:
            self.gold = 0
            self.food = 0
        
        self.strength = 0
        self.obs = []
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.shoot_cooldown = 0
        self.barbshoot_cooldown = -1
        self.shot_speed = 15
        self.crate_cooldown = 0

        self.respawn_count = 0
        self.meal = False
        self.meal_type = 0

        self.crates = 0
        self.spiky_bushes = 0
        self.spence = 'gold'

        self.garden_xp = 0

        self.shield_count = 0
        self.shield_angle = 0
        self.has_shield = False


        ### Stat Side ###

        
        self.attack = 10
        self.damage_cost = 30
        
        self.balloon_speed = 16
        self.speed_cost = 10
        
        self.knockback = 10
        self.knockback_cost = 10


        ### Info Side ###

        self.kills = 0
        self.destroyed = 0
        self.deaths = 0
        self.eliminations = 0

    @property
    def have_builder(self):
        true = False
        for inn in self.channel.get_buildings():
            if inn.__class__.__name__ == 'Inn':
                if inn.NPC.__class__.__name__ == 'Builder':
                    true = True
                    break
            if inn.type == 'Builder\'s':
                true = True
                break
        return true
        

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

    def move_x(self, a, type_=None):
        
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

                
                    

    def move_y(self, a, type_=None):
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
            for item in self.channel.server.bushes:
                if self.rect.colliderect(item.innerrect) and type_ != 'hurt':
                    if item.__class__.__name__ == 'SpikyBush':
                        self.getHurt(1, 'a spiky bush', self.angle + 180, 4, msg='<Victim> fell in <Attacker>.')
                    else:
                        self.getHurt(0, '', self.angle + 180, 4)
             
                    
        
    def move(self, angle):
        x, y = t.getDir(angle, self.get_speed())
        self.move_x(round(x))
        self.move_y(round(y))

    def update(self):
        
        if self.channel.build_to_place:

            self.channel.to_send.append({'action':'preview', 'dimensions':((self.channel.build_to_place.dimensions[0]*0.8, self.channel.build_to_place.dimensions[1]*0.8) if self.have_builder else self.channel.build_to_place.dimensions), 'ArcheryTower?':self.channel.build_to_place==ArcheryTower})
        
        self.rect = self.image.get_rect(center=(self.x, self.y))
        if not self.dead:
            for item in self.obs:
                if item.__class__ == Crate and self.rect.colliderect(item.innerrect):
                    x, y = t.getDir(self.angle + 180, 40)
                    self.x += x
                    self.x_flip -= x
                    self.y += y
                    self.y_flip -= y
                else:
                    thr = False
                    if item.__class__ == Gate and item.owner == self:
                        thr = True
                    if self.rect.colliderect(item.innerrect) and not thr:
                        self.suffocate()


        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.crate_cooldown > 0:
            self.crate_cooldown -= 1
        if self.hurt_count > 1:
            self.hurt_count -= 1
        if self.shield_count:
            self.shield_count -= 1
        if self.barbshoot_cooldown:
            self.barbshoot_cooldown -= 1

        if not self.barbshoot_cooldown:
            self.barbshoot()

        if self.respawn_count > 0:
            self.respawn_count -= 1
            if self.respawn_count == 0:
                self.respawn()
        
        self.obs = self.channel.server.obs
        
        
        if not self.dead:
            for p in self.channel.server.players:
            
                if p != self.channel:
                    if not p.pending:
                        
                    
                        p.to_send.append({'action':'draw_player',
                                'hurt':int(bool(self.hurt_count - 1)),
                                'coords':(p.character.get_x(self), p.character.get_y(self)),
                                'angle':self.angle,
                                'color':self.channel.color,
                                'username':self.channel.username,
                                'health':self.health,
                                'max_health':self.max_health,
                                'skin':self.channel.skin,
                                'shield':(self.shield_angle if self.shield_count else None)})
                else:
                    p.to_send.append({'action':'draw_player',
                            'hurt':int(bool(self.hurt_count - 1)),
                            'coords':(p.character.get_x(self), p.character.get_y(self)),
                            'angle':self.angle,
                            'color':self.channel.color,
                            'username':self.channel.username,
                            'health':self.health,
                            'gold':self.gold,
                            'food':self.food,
                            'max_health':self.max_health,
                            'skin':self.channel.skin,
                            'shield':(self.shield_angle if self.shield_count else None)})
                    
                    p.to_send.append({'action':'meal',
                            'food?':self.meal,
                                      'type':self.meal_type})
                    
                    if self.crates:
                        p.to_send.append({'action':'crates',
                            'crates':self.crates})
                    if self.spiky_bushes:
                        p.to_send.append({'action':'spiky_bushes',
                            'num':self.spiky_bushes})

    def barbshoot(self):
        
        dire = 650
        player = None
        for p in self.channel.server.players:
            if t.getDist(self.x, self.y, p.character.x, p.character.y) < dire and p != self.channel:
                player = p.character
                dire = t.getDist(self.x, self.y, p.character.x, p.character.y)
        if player:
            self.angle = t.getAngle(self.x, self.y, player.x, player.y)
            Bolt(self)
            self.barbshoot_cooldown = 50
        

    def HandleInput(self, keys, mouse):
        if not self.channel.in_window:
            self.angle = t.getAngle(500, 325, mouse[0], mouse[1])

            if keys[pygame.K_a]:
                self.channel.achievement('You pressed the A button!')
            if keys[pygame.K_8]:
                self.channel.achievement('You pressed the 8 button!')
                
            if keys[pygame.K_SPACE]:
                self.move(self.angle)

            if keys[pygame.K_c] and not self.dead:
                if self.channel.text == 'Press c to place sappling':
                    Sappling(self.channel.server, self.x, self.y)
                    self.channel.text = ''
                    self.crate_cooldown = 30
                elif self.channel.text == 'Press c to place invasive vine':
                    Vine(self, self.x, self.y + 60)
                    self.channel.text = ''
                    self.crate_cooldown = 30
                elif self.crate_cooldown == 0 and self.spiky_bushes > 0:
                    x, y = self.x, self.y
                    move = t.getDir(self.angle, 80)
                    x += move[0]
                    y += move[1]
                        
                    SpikyBush(self, x, y)
                    self.crate_cooldown = 30
                    self.spiky_bushes -= 1

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

            
            if mouse[2] and not self.dead:

                not_shoot = False
                if self.dead == False:
                    for farm in self.channel.server.resources:
                        if farm.HandleInput(mouse, self):
                            not_shoot = True

                if not not_shoot:
                    self.shoot()

        if self.channel.in_window and mouse[2] and not self.dead and not self.channel.in_innpc_window:
            not_farm = True
            not_shoot = True
            for option in self.channel.window['options']:
                
                x = 200
                y = 200 + option[0] * 40
                rect = pygame.Rect(x, y, 600, 50)

                if rect.collidepoint((mouse[0], mouse[1])):
                    option[1](self)
                    if self.channel.message == 'The Gold Discovery Rate is at its maximum!' and len([b for b in self.channel.get_buildings() if b.type == 'Miner\'s Guild']) == 0:
                        self.channel.message = 'Get a Miner\'s Guild first.'
                    if self.channel.message == 'The Food Production Rate is at its maximum!' and len([b for b in self.channel.get_buildings() if b.type == 'Farmer\'s Guild']) == 0:
                        self.channel.message = 'Get a Farmer\'s Guild first.'
                    break
                
        if self.channel.in_window and mouse[2] and not self.dead and self.channel.in_innpc_window:
            for i, option in enumerate(self.channel.window['options']):
                
                x = 200
                y = 200 + i * 40
                rect = pygame.Rect(x, y, 600, 50)

                if rect.collidepoint((mouse[0], mouse[1])):
                    option[1](self.channel)
                    if self.channel.message == 'The Gold Discovery Rate is at its maximum!' and len([b for b in self.channel.get_buildings() if b.type == 'Miner\'s Guild']) == 0:
                        self.channel.message = 'Get a Miner\'s Guild first.'
                    if self.channel.message == 'The Food Production Rate is at its maximum!' and len([b for b in self.channel.get_buildings() if b.type == 'Farmer\'s Guild']) == 0:
                        self.channel.message = 'Get a Farmer\'s Guild first.'
                    break


        if mouse[4] and not self.dead:
            
            if self.channel.build_to_place != None:
                result = builder(self.channel.build_to_place, self, self.have_builder)
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
            elif not self.channel.in_window and not self.channel.in_innpc_window:
                for b in self.channel.server.buildings:
                    rect = b.p.get_rect(center=(self.get_x(b), self.get_y(b)))
                    if rect.collidepoint((mouse[0], mouse[1])):
                        b.open_window(self.channel)
                        self.channel.to_send.append({'action':'sound', 'sound':'ow'})

                    else:
                        rect = b.rect.copy()
                        rect.x, rect.y = self.get_x(rect), self.get_y(rect)
                        if rect.collidepoint((mouse[0], mouse[1])):
                            b.open_window(self.channel)
                            self.channel.to_send.append({'action':'sound', 'sound':'ow'})

                    if b.__class__ == Inn and b.NPC != None and b.owner == self.channel:
                        rect = pygame.Rect(0, 0, 0, 0)
                        rect.topleft = self.get_x(b.NPC.rect), self.get_y(b.NPC.rect)
                        rect.size = b.NPC.rect.size
                        if rect.collidepoint((mouse[0], mouse[1])):
                            self.channel.in_window = True
                            self.channel.in_innpc_window = True
                            self.channel.window = b.NPC.window
                            self.channel.to_send.append({'action':'sound', 'sound':'ow'})



    def eat(self):
        if not self.dead:
            self.meal = False
            self.health = self.max_health
            self.channel.message = 'You ate your meal, your health bar is now full again.'
            self.channel.message_count = 150
            self.channel.message_color = (255,205,0)
            
        
    def getHurt(self, damage, attacker, angle, knockback, msg='<Attacker> killed <Victim>.'):
        if randint(0, 2) == 0 and self.has_shield:
            self.shield_angle = angle + 180
            self.shield_count = 20
            for p in self.channel.server.players:
                if not p.pending:
                    screen = pygame.Rect(0, 0, 1000, 650)
                    rect = pygame.Rect(0, 0, 1, 1)
                    rect.size = self.rect.size
                    rect.topleft = (p.character.get_x(self), p.character.get_y(self))
                    if screen.colliderect(rect):
                        p.to_send.append({'action':'sound','sound':'bump'})
            return 'repelled'
        final_damage = (damage - self.strength)
        if final_damage < 0:
            final_damage = 0
        self.health -= final_damage
        x, y = t.getDir(angle, knockback)
        self.move_x(x, 'hurt')
        self.move_y(y, 'hurt')
        self.hurt_count = 8
        if not self.health > 0:
            Explosion(self)
            for p in self.channel.server.players:
                screen = pygame.Rect(0, 0, 1000, 650)
                screen.center = p.character.rect.center
                if screen.colliderect(self.rect):
                    p.to_send.append({'action':'sound', 'sound':'die'})
            self.channel.text = ''
            self.channel.build_to_place = None
            self.dead = True
            
            self.deaths += 1
            self.crates = 0
            self.meal = False
            self.moving = 16
            if not isinstance(attacker, str):
                attacker.kills += 1
                newdict = self.channel.server.database[attacker.channel.username]
                newdict['kills'] += 1
                self.channel.server.database[attacker.channel.username] = newdict
                username = attacker.channel.username
            else:
                username = attacker

            msg = msg.replace('<Attacker>', username).replace('<Victim>', self.channel.username)
            for channel in self.channel.server.players:
                channel.message = msg
                channel.message_count = 150
                channel.message_color = (255,205,0)
                if channel == self.channel:
                    channel.message_color = (255,0,0)
            if len(self.channel.get_buildings()) != 0:
                self.respawn_count = 200
            else:
                if not isinstance(attacker, str):
                    attacker.eliminations += 1
                guys = []
                for channel in self.channel.server.players:
                    channel.message = username + ' has eliminated ' + self.channel.username + ' from the game.'
                    channel.message_count = 150
                    channel.message_color = (255,205,0)
                    if channel == self.channel:
                        channel.message = username + ' has eliminated you from the game!'
                        channel.message_color = (255,0,0)
                    if channel.character.dead == False:
                        guys.append(channel)
                    elif channel.character.respawn_count > 0:
                        guys.append(channel)
                if len(guys) == 1:
                    self.channel.server.terminate(guys[0])

        self.channel.in_window = False
        self.channel.window = None

    def suffocate(self):
        Explosion(self)
        for p in self.channel.server.players:
            screen = pygame.Rect(0, 0, 1000, 650)
            screen.center = p.character.rect.center
            if screen.colliderect(self.rect):
                p.to_send.append({'action':'sound', 'sound':'die'})
        self.channel.text = ''
        self.channel.build_to_place = None
        self.dead = True
            
        self.deaths += 1
        self.crates = 0
        self.meal = False
        self.moving = 16

        for channel in self.channel.server.players:
            channel.message = self.channel.username + ' suffocated.'
            channel.message_count = 150
            channel.message_color = (255,205,0)
            if channel == self.channel:
                channel.message_color = (255,0,0)

        if len(self.channel.get_buildings()) != 0:
            self.respawn_count = 200
        else:
            guys = []
            for channel in self.channel.server.players:
                channel.message = self.channel.username + ' has been eliminated from the game by suffocation.'
                channel.message_count = 150
                channel.message_color = (255,205,0)
                if channel == self.channel:
                    channel.message = 'You suffocated and were eliminated from the game!'
                    channel.message_color = (255,0,0)
                if channel.character.dead == False:
                    guys.append(channel)
                elif channel.character.respawn_count > 0:
                    guys.append(channel)
            if len(guys) == 1:
                self.channel.server.terminate(guys[0])



    def shoot(self):
        if self.shoot_cooldown == 0:
            Balloon(self.channel.server, self)
            self.shoot_cooldown = self.shot_speed
            for p in self.channel.server.players:
                if not p.pending:
                    screen = pygame.Rect(0, 0, 1000, 650)
                    screen.center = p.character.rect.center
                    if screen.colliderect(self.rect):
                        p.to_send.append({'action':'sound', 'sound':'shot'})


    def respawn(self):
        self.dead = False
        self.x, self.y = self.channel.server.ST_COORDS[self.channel.loc_number]
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
        



    

    









            
