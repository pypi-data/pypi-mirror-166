import pygame
import random as r
import toolbox as t
from balloon import Arrow


class Farmer(pygame.sprite.Sprite):
    def __init__(self, building):
        pygame.sprite.Sprite.__init__(self, self.gp)
        self.building = building
        self.x, self.y = building.rect.x, building.rect.y
        self.setout()
        self.speed = 2
        self.food = 0

    def setout(self):
        self.status = 'Going to Farms'
        sm_dist = 8000
        for farm in self.building.server.resources:
            if farm.__class__.__name__ == 'Farm':
                dx, dy = r.randint(farm.x + 90, farm.x + 310), r.randint(farm.y + 50, farm.y + 95)
                dist = t.getDist(self.x, self.y, dx, dy)
                if dist < sm_dist:
                    sm_dist = dist
                    x, y = dx, dy
                    self.farm = farm
        self.dest_x = x
        self.dest_y = y
        self.angle = t.getAngle(self.x, self.y, x, y)

    def start_gather(self):
        self.status = 'Gathering Food'
        sm_dist = 1000
        for food in self.farm.foods:
            if food.image == 'good':
                dist = t.getDist(self.x, self.y, food.x, food.y)
                if dist < sm_dist:
                    sm_dist = dist
                    self.the_food = food
                    self.dest_x = food.x
                    self.dest_y = food.y

    def mine(self):
        try:
            self.the_food.mine(self)
            if self.the_food.image == 'used':
                self.start_gather()
        except:
            self.start_gather()

    def at_dest(self):
        return t.getDist(self.x, self.y, self.dest_x, self.dest_y) < 10

    def go_back(self):
        self.status = 'Returning to Guild'
        self.dest_x, self.dest_y = self.building.rect.center

    def update(self, obs):
        
        self.angle = t.getAngle(self.x, self.y, self.dest_x, self.dest_y)
        x, y = t.getDir(self.angle, self.speed)
        
        lx, ly = self.x, self.y
        if self.status != 'Gathering Food':
            self.x += x
            self.rect = pygame.Rect(self.x, self.y, 50, 50)
            for ob in obs:
                if self.rect.colliderect(ob.innerrect):
                    self.x -= x
            
            self.y += y
            self.rect = pygame.Rect(self.x, self.y, 50, 50)
            for ob in obs:
                if self.rect.colliderect(ob.innerrect):
                    self.y -= y
            if round(lx) == round(self.x) and round(ly) == round(self.y) and self.status != 'Gathering Food':
                blocked = True
                while blocked:
                    blocked = False
                    
                    self.x += x
                    self.rect = pygame.Rect(self.x, self.y, 50, 50)
                    for ob in obs:
                        if self.rect.colliderect(ob.innerrect):
                            blocked = True
            
                    self.y += y
                    self.rect = pygame.Rect(self.x, self.y, 50, 50)
                    for ob in obs:
                        if self.rect.colliderect(ob.innerrect):
                            blocked = True
                

        if self.status == 'Gathering Food':
            if self.food < 20:
                self.mine()
            else:
                self.go_back()
            

        if self.at_dest():
            if self.status == 'Going to Farms':
                self.start_gather()
            elif self.status == 'Returning to Guild':
                self.food = 0
                self.building.owner.character.food += 20
                self.setout()
        
        for p in self.building.server.players:
            if not p.pending:
                if self.status == 'Gathering Food':
                    p.Send({'action':'draw_NPC',
                        'coords':(p.character.get_x(self), p.character.get_y(self)),
                        'image':'farmer',
                        'status':'Gathering Food : ' + str(self.food) + '/20',
                        'color':self.building.owner.color,
                        'angle':self.angle})
                else:
                    p.Send({'action':'draw_NPC',
                        'coords':(p.character.get_x(self), p.character.get_y(self)),
                        'image':'farmer',
                        'status':self.status,
                        'color':self.building.owner.color,
                        'angle':self.angle})


class Miner(pygame.sprite.Sprite):
    def __init__(self, building):
        pygame.sprite.Sprite.__init__(self, self.gp)
        self.building = building
        self.x, self.y = building.rect.x, building.rect.y
        self.setout()
        self.speed = 2
        self.gold = 0
        

    def setout(self):
        self.status = 'Heading to Mines'
        sm_dist = 8000
        for farm in self.building.server.resources:
            if farm.__class__.__name__ == 'Mine':
                dx, dy = farm.x+100, r.randint(farm.y + 50, farm.y + 400)
                dist = t.getDist(self.x, self.y, dx, dy)
                if dist < sm_dist:
                    sm_dist = dist
                    x, y = dx, dy
                    self.farm = farm
        self.dest_x = x
        self.dest_y = y
        self.angle = t.getAngle(self.x, self.y, x, y)

    def start_gather(self):
        self.status = 'Mining'
        sm_dist = 1000
        for food in self.farm.golds:
            if food.image == 'good':
                dist = t.getDist(self.x, self.y, food.x, food.y)
                if dist < sm_dist:
                    sm_dist = dist
                    self.the_food = food
                    self.dest_x = food.x
                    self.dest_y = food.y

    def mine(self):
        try:
            self.the_food.collect(self)
            if self.the_food.image == 'used':
                self.start_gather()
        except:
            self.start_gather()

    def at_dest(self):
        return t.getDist(self.x, self.y, self.dest_x, self.dest_y) < 10

    def go_back(self):
        self.status = 'Returning to Guild'
        self.dest_x, self.dest_y = self.building.rect.center

    def update(self, obs):
        
        self.angle = t.getAngle(self.x, self.y, self.dest_x, self.dest_y)
        x, y = t.getDir(self.angle, self.speed)
        
        lx, ly = self.x, self.y
        if self.status != 'Mining':
            self.x += x
            self.rect = pygame.Rect(self.x, self.y, 50, 50)
            for ob in obs:
                if self.rect.colliderect(ob.innerrect):
                    self.x -= x
            
            self.y += y
            self.rect = pygame.Rect(self.x, self.y, 50, 50)
            for ob in obs:
                if self.rect.colliderect(ob.innerrect):
                    self.y -= y
            if round(lx) == round(self.x) and round(ly) == round(self.y) and self.status != 'Mining':
                blocked = True
                while blocked:
                    blocked = False
                    
                    self.x += x
                    self.rect = pygame.Rect(self.x, self.y, 50, 50)
                    for ob in obs:
                        if self.rect.colliderect(ob.innerrect):
                            blocked = True
            
                    self.y += y
                    self.rect = pygame.Rect(self.x, self.y, 50, 50)
                    for ob in obs:
                        if self.rect.colliderect(ob.innerrect):
                            blocked = True
                

        if self.status == 'Mining':
            if self.gold < 20:
                self.mine()
            else:
                self.go_back()
            

        if self.at_dest():
            if self.status == 'Heading to Mines':
                self.start_gather()
            elif self.status == 'Returning to Guild':
                self.gold = 0
                self.building.owner.character.gold += 20
                self.setout()
        
        for p in self.building.server.players:
            if self.status == 'Mining':
                p.Send({'action':'draw_NPC',
                    'coords':(p.character.get_x(self), p.character.get_y(self)),
                    'image':'miner',
                    'status':'Mining : ' + str(self.gold) + '/20',
                    'color':self.building.owner.color,
                    'angle':self.angle})
            else:
                p.Send({'action':'draw_NPC',
                    'coords':(p.character.get_x(self), p.character.get_y(self)),
                    'image':'miner',
                    'status':self.status,
                    'color':self.building.owner.color,
                    'angle':self.angle})


class ArcheryTower(pygame.sprite.Sprite):
    dimensions = (360, 360)
    def __init__(self, server, x, y, channel, rect):
        pygame.sprite.Sprite.__init__(self, self.gp)
        self.building = self
        
        self.server = server
        self.x, self.y = x, y - 100
        self.owner = channel.character
        self.health = 300
        self.dimensions = (360, 360)
        
        self.innerrect = rect
        self.server.building_blocks.append(self.innerrect)
        self.server.obs.append(self)

        self.balloon_speed = 20
        self.attack = 24
        self.knockback = 32

        self.shoot_cooldown = 60
        self.state = 'alive'

        self.attacking = False

    def update(self, obs):
        self.lookx = self.owner.x
        self.looky = self.owner.y
        self.attacking = False
        for player in self.server.players:
            if t.getDist(self.x, self.y, player.character.x, player.character.y) < 800 and player != self.owner.channel:
                self.lookx = player.character.x
                self.looky = player.character.y
                self.attacking = True

        self.angle = t.getAngle(self.x, self.y, self.lookx, self.looky)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.shoot_cooldown < 1 and self.attacking and self.state == 'alive':
            Arrow(self)
            self.shoot_cooldown = 60


        for p in self.server.players:
            p.Send({'action':'archery_tower',
                    'coords':(p.character.get_x(self), p.character.get_y(self)),
                    'angle':self.angle,
                    'color':self.owner.channel.color,
                    'health':self.health,
                    'state':self.state})


    def isBuilding(self):
        return False
    def getHurt(self, damage, attacker):
        if attacker != self.owner:
            self.health -= damage
            if self.health < 1:
                self.state = 'broken'
                attacker.destroyed += 1
                self.owner.channel.message = attacker.channel.username + ' has broken one of your Archery Towers.'
                self.owner.channel.message_count = 150
                self.owner.channel.message_color = (255,0,0)
                self.server.obs.remove(self)

    def explode(self):
        if self.state == 'broken':
            self.server.building_blocks.remove(self.innerrect)
            self.kill()
        else:
            self.getHurt(80, None)
            if self.state == 'broken':
                self.server.building_blocks.remove(self.innerrect)
                self.kill()
















                
        
