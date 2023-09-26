from getpass import getpass

class DevicesModule:
    def __init__(self):
        self.host = input('Veillez indiquer l\'adresse IP de management de l\'équipement: ')
        self.username = input('Veillez spécifier le nom d\'utilisateur: ')
        self.password = getpass('Spécifiez le mot de passe: ')

    def get_attr(self):
        return {
            'host': self.host,
            'username': self.username,
            'password': self.password
        }