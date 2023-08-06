
class Background():

    def __init__(self, server):
        self.server = server
        self.x = 0
        self.y = 0
        

    def update(self):

        for p in self.server.players:
            if not p.pending:
                p.Send({'action':'ingame', 'coords':(p.character.get_x(self), p.character.get_y(self))})
