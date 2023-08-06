import pygame
import toolbox as t


class Balloon(pygame.sprite.Sprite):
    def __init__(self, server, owner):
        pygame.sprite.Sprite.__init__(self, self.gp)
        self.server = server
        self.owner = owner
        self.speed = owner.balloon_speed
        self.x = owner.x
        self.y = owner.y
        self.angle = owner.angle
        self.damage = owner.attack
        self.knockback = owner.knockback

        self.image = pygame.image.load('../assets/balloon.png')


    def update(self, obstacles):
        self.move()

        for p in self.server.players:
            if not p.pending:
                p.Send({'action':'draw_balloon',
                    'coords':(p.character.get_x(self), p.character.get_y(self)),
                    'angle':self.angle})

        if self.x > 7000 or self.x < -1000 or self.y > 4400 or self.y < -500:
            self.kill()

        self.rect = self.image.get_rect(center=(self.x, self.y))

        for item in obstacles:
            if self.rect.colliderect(item.innerrect) and not (self.__class__ == Arrow  and item.__class__.__name__ == 'ArcheryTower') and not (self.__class__ == Arrow  and item.owner == self.owner):
                #Splash(self)
                for p in self.server.players:
                    if not p.pending:
                        screen = pygame.Rect(0, 0, 1000, 650)
                        screen.center = p.character.rect.center
                        if screen.colliderect(self.rect):
                            p.Send({'action':'sound', 'sound':'splash'})
                    item.getHurt(self.damage, self.owner)
                self.kill()
            elif item.isBuilding():
                if self.rect.colliderect(item.rect) and item.owner != self.owner.channel:
                    for p in self.server.players:
                        if not p.pending:
                            screen = pygame.Rect(0, 0, 1000, 650)
                            screen.center = p.character.rect.center
                            if screen.colliderect(self.rect):
                                p.Send({'action':'sound', 'sound':'splash'})
                    #Splash(self)
                    item.getHurt(self.damage, self.owner)
                    self.kill()
        for p in self.server.players:
            if not p.pending:
                if self.rect.colliderect(p.character.rect) and p != self.owner.channel and p.character.dead == False:
                    for p2 in self.server.players:
                        if not p2.pending:
                            screen = pygame.Rect(0, 0, 1000, 650)
                            screen.center = p2.character.rect.center
                            if screen.colliderect(self.rect):
                                p2.Send({'action':'sound', 'sound':'splash'})
                    #Splash(self)
                    p.character.getHurt(self.damage, self.owner, self.angle, self.knockback)
                    self.kill()


    def move(self):

        x, y = t.getDir(self.angle, self.speed)
        self.x += x
        self.y += y




class Arrow(Balloon):
    def __init__(self, tower):
        Balloon.__init__(self, tower.server, tower.owner)
        self.x = tower.innerrect.center[0]
        self.y = tower.innerrect.center[1]
        self.speed = tower.balloon_speed
        self.angle = tower.angle
        self.damage = tower.attack
        self.knockback = tower.knockback










        
