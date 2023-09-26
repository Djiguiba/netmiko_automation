import pandas as pd

from DevicesModule import DevicesModule
from getpass import getpass

class CiscoIosModule(DevicesModule):
    DEVICE_TYPE = 'cisco_ios'

    def __init__(self):
        DevicesModule.__init__(self)
        self.enable_password = getpass('Indiquez le enable password: ')

    def get_attr(self):
        attr = DevicesModule.get_attr(self)
        attr['device_type'] = CiscoIosModule.DEVICE_TYPE
        attr['secret'] = self.enable_password
        return attr
    
    def create_user(self):
        username = input("Entrer le nom d'utilisateur: ")
        password = input("Entrer le mot de passe: ")
        return f"username {username} password {password}"

    def modify_hostname(self):
        hostname = input("Indiquez le nom de l'hostname: ")
        return f'hostname {hostname}'
    
    def create_loopback_interfaces(self):
        # nb_interf_loopback = int(input("Combien d'interfaces loopback voulez-vous: "))
        pass

    def config_interfaces(self):
        # input_value = True
        config_command = []
        # Precisez dans le main que 'exit' permet d'indiquer qu'il n'y a plus d'interfaces à configurer
        interf = input("Indiquez l'interface à configurer: ")
        
        while interf != 'exit':
            config_command.append(f'inter {interf}')
            ip_address = input("Indiquez l'adresse IP suivi du mask: ")
            config_command.append(f'ip address {ip_address}')
            config_command.append('no sh')

            # print(f"Configuration de l'interface {interf} effectuee.\n")
            print(f"{'#'*50}")
            interf = input("Indiquez l'interface suivante: ")
        return config_command
    
    def config_interfaces_via_excel_file(self, df=None):
        config_command = []
        for row in df.iterrows():
            config_command.append(f"inter {row[1]['interfaces']}")
            # config_command.append(f"ip addr {row[1]['ip_address']}")
            if row[1]['description'] != "None":
                config_command.append(f"descr {row[1]['description']}")
            config_command.append(f"swi mode {row[1]['trunk']}")
            if row[1]['channel_group'] != 0:
                config_command.append(f"channel-group {row[1]['channel_group']} mode {row[1]['mode_channel']}")

            config_command.append('no sh')
        return config_command
    
    def config_management_interface(self):
        pass

    def create_vlan_interfaces(self):
        config_commands = []
        # Precisez dans le main que 'exit' permet d'indiquer qu'il n'y a plus de VLANs à créer
        num_inter_vlan = input(f"Indiquez le numero de l'interface VLAN: ")

        while num_inter_vlan != 'exit':
            config_commands.append(f'inter vlan {num_inter_vlan}')

            descr = input("Description du VLAN: ")
            config_commands.append(f'des {descr}')

            ip_vlan = input("Indiquez l'adresse du VLAN ainsi que son mask: ")
            config_commands.append(f'ip address {ip_vlan}')

            config_commands.append('no sh')
            print(f"{'#'*100}")
            num_inter_vlan = input("Indiquez le numero de l'interface VLAN suivante: ")

        return config_commands
    
    def create_vlan_interfaces_via_excel_file(self, df=None):
        config_commands = []
        for row in df.iterrows():
            config_commands.append(f"inter vlan {row[1]['num_vlan_interface']}")
            if row[1]['description'] != 'None':
                config_commands.append(f"des {row[1]['description']}")
            config_commands.append(f"ip addr {row[1]['ip_vlan_address']}")

            config_commands.append('no sh')
        return config_commands
    
    def modify_vlan_interface(self):
        config_commands = []
        num_inter_vlan = input("Indiquez le numero de l'interface VLAN a modifier: ")

        # Verification si l'interface existe 
        pass

    def drop_vlan_interface(self):
        config_commands = []
        num_inter_vlan = input("Indiquez le numero de l'interface VLAN a supprimer: ")

        # Verification si l'interface existe ensuite effectuer le script suivant
        config_commands.append(f'no inter vlan {num_inter_vlan}')

        return config_commands

    def create_vlans(self):
        config_commands = []
        num_vlan = input(f"Indiquez le numero du VLAN: ")

        while num_vlan != 'exit':
            config_commands.append(f'vlan {num_vlan}')

            name = input("Indiquez le nom du VLAN: ")
            config_commands.append(f'name {name}')

            print(f"{'#'*100}")
            num_vlan = input("Indiquez le numero du VLAN suivant: ")

        return config_commands

    def create_vlans_via_excel_file(self, df=None):
        config_commands = []
        for row in df.iterrows():
            config_commands.append(f"vlan {row[1]['num_vlan']}")
            config_commands.append(f"name {row[1]['name_vlan']}")
        
        return config_commands

    def modify_vlan(self):
        config_commands = []
        num_vlan = input('Indiquez le numero du VLAN à modifier: ')
        pass

    def drop_vlan(self):
        num_vlan = input("Quel est le numéro du VLAN à supprimer: ")
        return f'no inter vlan {num_vlan}'
    
    def add_interfaces_to_vlan(self):
        config_command = []
        vlan_id = input('Indiquez le numero du VLAN: ')
        print('\n')

        while vlan_id != 'exit':
            range_or_not = input('Voulez-vous y ajouter un range d\'interfaces (O ou N): ')
            
            if range_or_not == 'O':
                interface_range = input('Spécifiez le range d\'interfaces: ')
                config_command.append(f'inter range {interface_range}')
                config_command.append('switchport mode access')
                config_command.append(f'switchport access vlan {vlan_id}') 

            else:
                interface = input('Spécifiez l\'interface: ')
                config_command.append(f'inter {interface}')
                config_command.append('switchport mode access')
                config_command.append(f'switchport access vlan {vlan_id}')
            print('\n')
            print('Voulez-vous y attribuer à un autre VLAN ?\n')
            vlan_id = input('Spécifiez le numero du VLAN, si c\'est le cas: ')

        return config_command
    
    def add_interfaces_to_vlan_via_excel_file(self, df=None):
        pass
    
    def add_vlan_to_trunk_port(self):
        config_command = []
        interface = input('\nSpécifiez ledit port: ')
        config_command.append(f'interface {interface}')

        vlans = input(f'\nSpécifiez les VLANs à attribuer au port {interface}: ')
        config_command.append(f"switchport trunk allowed vlan add {','.join([vlan for vlan in vlans.split()])}")
        return config_command
    
    def switch_port_to_trunk(self):
        config_command = []
        interfaces = input('Spécifiez le ou les ports à mettre en mode trunk: ')
        if len(interfaces.split()) == 1:
            config_command.append(f'interface {interfaces}')
            config_command.append('switchport trunk encapsulation dot1q')
            config_command.append('switchport mode trunk')
        else:
            for interface in interfaces.split():
                config_command.append(f'interface {interface}') 
                config_command.append('switchport trunk encapsulation dot1q')
                config_command.append('switchport mode trunk')

        # config_command.append('do wr')
        return config_command

    def switch_port_to_access(self):
        config_command = []
        interfaces = input('Spécifiez le ou les ports à mettre en mode access: ')
        if len(interfaces.split()) == 1:
            config_command.append(f'interface {interfaces}')
            config_command.append('switchport mode access')
        else:
            for interface in interfaces.split():
                config_command.append(f'interface {interface}')
                config_command.append('switchport mode access')

        # config_command.append('do wr')
        return config_command
    
    def config_link_aggregation(self):
        config_command = []

        interfaces = input('Spécifiez soit le range ou les ports à regrouper: ')
        if len(interfaces.split()) == 1:
            config_command.append(f'interface range {interfaces}')
            config_command.append('switchport trunk encapsulation dot1q')
            config_command.append('switchport mode trunk')
        else:
            config_command.append(f"interface range {', '.join([interface for interface in interfaces.split()])}")
            config_command.append('switchport trunk encapsulation dot1q')
            config_command.append('switchport mode trunk')
        
        num_port_channel = input('\nSpécifiez un numéro de port channel: ')
        config_command.append(f'channel-group {num_port_channel} mode active')
        config_command.append('channel-protocol lacp')

        # config_command.append('do wr')
        return config_command
    
    def config_link_aggregation_via_excel_file(self, df=None):
        pass

    def add_static_routes(self):
        config_commands = []
        input_route = input('Indiquez le réseau de destination suivie du mask et de la gateway: ')
        while input_route != 'exit':
            config_commands.append(f'ip route {input_route}')
            input_route = input('Indiquez la route suivante: ')

        return config_commands
    
    def add_static_routes_via_excel_file(self, df=None):
        config_commands = []
        for row in df.iterrows():
            config_commands.append(f"ip route {row[1]['network']} {row[1]['mask']} {row[1]['gateway']}")
        
        return config_commands

    def add_dynamic_routes(self):
        config_commands = []

        protocol = input('Indiquez le protocole de routage (ospf ou bgp): ')
        id = input('Indiquez le process id (<1-65535>): ')
        print('\n')
        config_commands.append(f'router {protocol} {id}')

        print(f"{'#'*50} Veillez indiquer les differents network {'#'*50}")
        if protocol == 'ospf':
            input_network = input("Indiquez la route: ")
            wild_card = input('Indiquez le wild card: ')
            area = input("Indiquez le numéro de l'area: ")

            while input_network != 'exit':
                config_commands.append(f'network {input_network} {wild_card} area {area}')
                config_commands.append('no shut')
                input_network = input('Indiquez la route suivante: ')
            
        elif protocol == 'bgp':
            input_network = input("Indiquez la route suivie du mask: ")

            while input_network != 'exit':
                config_commands.append(f'network {input_network}')
                input_network = input('Indiquez la route suivante: ')

        return config_commands
    
    def add_dynamic_routes_via_excel_file(self, df=None):
        config_commands = []
        for row in df.iterrows():
            if row[1]['routing_protocol'] == 'ospf':
                config_commands.append(f"router {row[1]['routing_protocol']} {row[1]['process_id']}")
                config_commands.append(f"network ")

    def config_load_balancing(self):
        pass

    def activate_dchp_relay(self):
        pass

    def activate_dhcp_protocol(self):
        pass

    def get_backup(self):
        return 'show run'
    
    def make_all_config(self):
        config_commands = {}
        file_name = input('\nVeillez spécifier le nom du fichier Excel sans l\'extension: ')
        f = pd.ExcelFile(f"templates\{file_name}.xlsx")
        try:
            for sheet in f.sheet_names:
                df = f.parse(sheet)

                if sheet == 'Interfaces':
                    config_commands['config_interfaces'] = CiscoIosModule.config_interfaces_via_excel_file(self, df)

                elif sheet == 'VLAN Interfaces':
                    config_commands['config_vlan_interfaces'] = CiscoIosModule.create_vlan_interfaces_via_excel_file(self, df)
                
                elif sheet == 'VLAN':
                    config_commands['config_vlans'] = CiscoIosModule.create_vlans_via_excel_file(self, df)

                elif sheet == 'Static Routes':
                    config_commands['config_static_routes'] = CiscoIosModule.add_static_routes_via_excel_file(self, df)
                
                elif sheet == 'Dynamic Routes':
                    pass

                elif sheet == 'Link Aggregation':
                    pass

        except Exception as e:
            print('Le fichier que vous avez spécifié est incorrecte !\n')
            print(f'Erreur: {str(e)}')
        
        return config_commands
