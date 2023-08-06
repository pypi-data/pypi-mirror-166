from PodSixNet.Connection import ConnectionListener, connection
import toolbox

class CreateAccount(ConnectionListener):

    def __init__(self, host, port, username):
        ConnectionListener.__init__(self)
        self.Connect((host, port))
        self.username = username
        self.pswd = input('Please enter your password: ')

    def Network_created(self, data):
        global running
        running = False

    
    def Network_connected(self, data):
        """
        Network_connected runs when you successfully connect to the server
        """
        connection.Send({'action':'init', 'username':self.username, 'pswd':self.pswd, 'status':'CA'})
        self.connected = True
        print("Connection succesful!")

    def update(self):
        connection.Pump()
        self.Pump()


running = True
username = input('Please enter your usename: ')

ip = toolbox.getMyIP() # input("Please enter the host's IP address: ")
port = 5555
main = CreateAccount(ip, port, username)
while running:
    main.update()
