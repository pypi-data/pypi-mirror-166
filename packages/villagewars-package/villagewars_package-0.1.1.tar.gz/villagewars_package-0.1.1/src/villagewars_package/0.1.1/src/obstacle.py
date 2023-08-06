import pygame
import toolbox as t

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, server, x, y):
        pygame.sprite.Sprite.__init__(self, self.gp)
        self.server = server
        self.image = None
        self.dimentions = (60, 60)
        self.x = x
        self.y = y
        self.max_health = self.health = 300
        self.owner = None

    def update(self):
        

        for p in self.server.players:
            if not p.pending:
                screen = pygame.Rect(0, 0, 1000, 650)
                rect = pygame.Rect(0, 0, 1, 1)
                rect.size = self.innerrect.size
                rect.topleft = (p.character.get_x(self.innerrect), p.character.get_y(self.innerrect))
                if screen.colliderect(rect):
                    p.Send({'action':'draw_obstacle',
                            'image':self.image,
                            'coords':(p.character.get_x(self), p.character.get_y(self)),
                            'health':self.health,
                            'max_health':self.max_health})

    def getHurt(self, damage, attacker):
        if self.health > 0:
            self.health -= damage
            if self.health < 1:
                self.server.building_blocks.remove(self.innerrect)
                self.server.obs.remove(self)
                self.kill()

    def isBuilding(self):
        return False


    def explode(self):
        self.getHurt(80, None)


class Tree(Obstacle):
    def __init__(self, server, x, y):
        Obstacle.__init__(self, server, x, y)
        self.image = 'tree'
        self.max_health = self.health = 300
        self.p = pygame.image.load('../assets/tree.png')
        self.innerrect = self.p.get_rect(center=(x,y))
        server.building_blocks.append(self.innerrect)
        server.obs.append(self)

        

class Boulder(Obstacle):
    def __init__(self, server, x, y):
        Obstacle.__init__(self, server, x, y)
        self.image = 'boulder'
        self.max_health = self.health = r.randint(18, 32) * 10
        self.p = pygame.image.load('../assets/boulder.png')
        self.innerrect = self.p.get_rect(center=(x,y))
        server.building_blocks.append(self.innerrect)
        server.obs.append(self)


class Crate(Obstacle):
    def __init__(self, player, x, y):
        Obstacle.__init__(self, player.channel.server, x, y)
        self.image = 'crate'
        self.max_health = self.health = 800
        self.p = pygame.Surface((50, 50))
        self.innerrect = self.p.get_rect(center=(x,y))
        self.server.building_blocks.append(self.innerrect)
        self.server.obs.append(self)
        self.owner = player

    def explode(self):
        self.server.building_blocks.remove(self.innerrect)
        self.server.obs.remove(self)
        self.kill()

    def update(self):
        
        

        for p in self.server.players:
            if not p.pending:
                p.Send({'action':'draw_obstacle',
                            'image':self.image,
                            'coords':(p.character.get_x(self), p.character.get_y(self)),
                            'health':self.health,
                            'max_health':self.max_health})

class Gate(Obstacle):
    def __init__(self, player, x, y, rot):
        Obstacle.__init__(self, player.channel.server, x, y)
        self.image = 'gate'
        self.max_health = self.health = 1000
        if rot == False:
            self.p = pygame.Surface((100, 200))
        else:
            self.p = pygame.Surface((200, 100))
        self.innerrect = self.p.get_rect(center=(x,y))
        self.server.building_blocks.append(self.innerrect)
        self.server.obs.append(self)
        self.owner = player
        self.rotated = rot

    def explode(self):
        self.getHurt(900, None)

    def update(self):

        

        for p in self.server.players:
            if not p.pending:
                p.Send({'action':'draw_obstacle',
                            'image':self.image,
                            'coords':(p.character.get_x(self), p.character.get_y(self)),
                            'health':self.health,
                            'max_health':self.max_health,
                            'rotated?':self.rotated})

class TNT(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        pygame.sprite.Sprite.__init__(self, self.gp)
        self.health = 130
        self.x = x
        self.y = y
        self.p = pygame.Surface((50, 50))
        self.innerrect = self.p.get_rect(center=(x,y))
        self.server = player.channel.server
        self.server.building_blocks.append(self.innerrect)
        self.server.obs.append(self)
        self.owner = player

    def update(self):
        self.health -= 1
        if self.health == 0:
            for p in self.server.players:
                screen = pygame.Rect(0, 0, 1000, 650)
                screen.center = p.character.rect.center
                if screen.colliderect(self.innerrect):
                    p.Send({'action':'sound', 'sound':'TNT'})
            self.server.building_blocks.remove(self.innerrect)
            self.server.obs.remove(self)

            ray = pygame.Rect(0, 0, 400, 400)
            ray.center = self.x, self.y
            for item in self.server.obstacles:
                if item != self and item.innerrect.colliderect(ray):
                    item.explode()
            for item in self.server.buildings:
                if item.innerrect.colliderect(ray):
                    item.getHurt(120, self.owner)
                elif item.rect.colliderect(ray):
                    item.getHurt(120, self.owner)
            for item in self.server.players:
                if item.character.rect.colliderect(ray):
                    item.character.getHurt(80, self.owner, t.getAngle(self.x, self.y, item.character.x, item.character.y), 120)
            for item in self.server.NPCs:
                if item.__class__.__name__ == 'ArcheryTower':
                    item.explode()
            
            self.kill()

        for p in self.server.players:
            if not p.pending:
                p.Send({'action':'draw_obstacle',
                            'image':'TNT',
                            'coords':(p.character.get_x(self), p.character.get_y(self))})
    def isBuilding(self):
        return False
    def getHurt(self, damage, attacker):
        pass
    def explode(self):
        ''' Ha! '''
        pass

class Block():
    def __init__(self, topleft, size):
        self.innerrect = pygame.Rect(topleft[0], topleft[1], size[0], size[1])
        self.owner = None
    def isBuilding(self):
        return False
    def getHurt(self, damage, attacker):
        pass
        
        
        
