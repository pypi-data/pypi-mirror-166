from building import *

def kick(self, playername):
    for p in self.server.players:
        if p.username == playername:
            p.Send({'action':'disconnected'})
    
    print('Kicked ' + playername)


def makeWallsFall(self):
    self.server.upwall.count = 10
    self.server.leftwall.count = 10
