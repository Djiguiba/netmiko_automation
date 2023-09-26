from DevicesModule import DevicesModule

class CiscoAsaModule(DevicesModule):
    DEVICE_TYPE = 'cisco_asa'

    def __init__(self, host='', username='', password=''):
        DevicesModule.__init__(self, host, username, password)

    def get_attr(self):
        attr = DevicesModule.get_attr(self)
        attr['device_type'] = CiscoAsaModule.DEVICE_TYPE

        return attr
        