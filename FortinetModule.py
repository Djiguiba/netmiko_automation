from netmiko import Netmiko

import re
import pandas as pd
import random
import requests

from DevicesModule import DevicesModule

class FortinetModule(DevicesModule):
    DEVICE_TYPE = 'fortinet'

    def __init__(self):
        DevicesModule.__init__(self)
    
    def get_attr(self):
       attr = DevicesModule.get_attr(self)
       attr['device_type'] = FortinetModule.DEVICE_TYPE

       return attr
    
    def set_hostname(self):
        hostname = input('Spécifiez un hostname: ')
        return  [
            'conf syst global',
            f'set hostname {hostname}',
            'end'
            ]
    
    def configure_ntp_server(self):
        conf_commands = ['conf syst ntp']
        conf_commands.append('set ntpsync enable')

        sync_interv = input('Indiquez une intervalle de synchronisation from <1> to <1440> (default = <60>): ')
        conf_commands.append(f'set syncinterval {sync_interv}')

        ntp_type = input('Veillez spécifier un type de ntp {fortiguard | custom}: ')
        conf_commands.append(f'set type {ntp_type}')

        if ntp_type == 'fortiguard':
            ip_source = input('Veillez indiquer l\'adresse IP source pour communiquer avec le serveur ntp: ')
            conf_commands.append(f'set source-ip {ip_source}')
        
            conf_commands.append('set server-mode enable')

            interface = input('Spécifiez l\'interface ou les interfaces d\'écoute: ')
            conf_commands.append(f'set interface {interface}')

            auth = input('Autorisez l\'authentification {en | di}: ')
            if auth == 'en' or auth == 'enable':
                conf_commands.append('set auth enable')
                key_type = input('Spécifiez le type de clé {MD5 | SHA1}: ')
                conf_commands.append(f'set key-type {key_type}')
                key = input('Spécifiez un mot de passe: ')
                conf_commands.append(f'set key {key}')
                conf_commands.append(f'set key-id {random.randint(0, 4294967295)}')

        elif ntp_type == 'custom':
            conf_commands.append('config ntpserver')
            conf_commands.append(f'edit {random.randint(1, 10)}')
            ip_address_or_hostname = input('Spécifiez le <ip_address or hostname>: ')
            conf_commands.append(f'set server {ip_address_or_hostname }')
            ntpv3_or_not = input('Autorisez le NTPv3 en lieu et place du NTPv4 {enable | disable}: ')
            conf_commands.append(f'set ntpv3 {ntpv3_or_not}')
            interface = input('Sélectionnez l\'interface de sortie pour atteindre le serveur {auto | sdwan | specify}: ')
            conf_commands.append(f'set interface-select-method {interface}')
            auth = input('Autorisez l\'authentification {en | di}: ')
            if auth == 'en' or auth == 'enable':
                key = input('Spécifiez un mot de passe: ')
                conf_commands.append(f'set key {key}')
                conf_commands.append(f'set key-id {random.randint(0, 4294967295)}')

        conf_commands.append('end')
        return conf_commands
    
    def configure_dns(self):
        conf_commands = ['conf syst dns']

        primary_ip_addr = input('Spécifiez l\'adresse IP primaire du serveur DNS: ')
        conf_commands.append(f'set primary {primary_ip_addr}')

        second_ip_addr = input('Spécifiez l\'adresse IP secondaire du serveur DNS: ')
        conf_commands.append(f'set secondary {second_ip_addr}')

        protocol = input('Spécifiez le proctocole {cleartext dot doh}: ')
        conf_commands.append(f'set protocol {protocol}')

        ssl_certificate = input('Spécifiez le ssl certificate: ')
        conf_commands.append(f'set ssl-certificate {ssl_certificate}')

        domains = input('Spécifiez le ou les nom(s) de domaine: ')
        conf_commands.append(f'set domain {domains}')

        outgoing_interface = input('Spécifiez l\'adresse IP utilisé par le serveur DNS comme IP source: ') 
        conf_commands.append(f'set source-ip {outgoing_interface}')

        interface = input('Spécifiez l\'interface de sortie pour atteindre le serveur: ')
        conf_commands.append(f'set interface-select-method {interface}')

        conf_commands.append('end')
        return conf_commands

    def configure_interfaces_manually(self):
        conf_commands = ['conf syst interf']
        pass
    
    def configure_interfaces_via_excel_file(self, df=None):
        conf_commands = ['conf syst interf']
        if df is None:
            file_name = input('Veillez spécifier le nom du fichier Excel sans l\'extension: ')
            try:
                df = pd.read_excel(f'templates\{file_name}.xlsx')

            except Exception as e:
                print('Le fichier que vous avez spécifié est incorrecte !\n')
                print(f'Erreur: {str(e)}')

        for row in df.iterrows():
            if row[1]['type'] == 'vlan':
                conf_commands.append(f"edit {row[1]['name']}")
                conf_commands.append('set vdom root')
                conf_commands.append(f"set interface {row[1]['interface']}")
                conf_commands.append(f"set type {row[1]['type']}")
                conf_commands.append(f"set vlanid {row[1]['vlanid']}")
                conf_commands.append(f"set mode {row[1]['mode']}")
                conf_commands.append(f"set status {row[1]['status']}")
                conf_commands.append(f"set ip {row[1]['ip']}")
                conf_commands.append(f"set allowaccess {row[1]['allowaccess']}")

                conf_commands.append('next')

            elif row[1]['type'] == 'physical':
                conf_commands.append(f"edit {row[1]['name']}")
                conf_commands.append(f"set mode {row[1]['mode']}")
                conf_commands.append(f"set status {row[1]['status']}")
                conf_commands.append(f"set ip {row[1]['ip']}")
                conf_commands.append(f"set allowaccess {row[1]['allowaccess']}")

                conf_commands.append('next')

            elif row[1]['type'] == 'aggregate':
                conf_commands.append(f"edit {row[1]['name']}")
                conf_commands.append('set vdom root')
                conf_commands.append(f"set ip {row[1]['ip']}")
                conf_commands.append(f"set allowaccess {row[1]['allowaccess']}")
                conf_commands.append(f"set type {row[1]['type']}")
                conf_commands.append(f"set member {row[1]['member']}")
                conf_commands.append(f"set snmp-index {random.randint(1, 2147483647)}")

                conf_commands.append('next')

            else:
                # row[1]['type'] == 'redundant'
                conf_commands.append(f"edit {row[1]['name']}")
                conf_commands.append('set vdom root')
                conf_commands.append(f"set ip {row[1]['ip']}")
                conf_commands.append(f"set allowaccess {row[1]['allowaccess']}")
                conf_commands.append(f"set type {row[1]['type']}")
                conf_commands.append(f"set member {row[1]['member']}")
                conf_commands.append(f"set snmp-index {random.randint(1, 2147483647)}")

                conf_commands.append('next')

            # secondary_ip_address_or_not = input(f'\nLe {interface} a t-il une seconde adresse ? si tel est le cas, spécifiez la ou ne spécifiez rien: ')
            # if secondary_ip_address_or_not != '':
            #     # Il faudrait que le format de l'addresse IP soit correcte, donc il faut faire une vérification
            #     conf_commands.append('set second enable')
            #     secondary_ip_address = secondary_ip_address_or_not
            #     num_seq = input('Spécifiez un numéro de séquence <1, 2, ...>: ')
            #     allow_access = input('Spécifiez les différents access séparés par un espace (comme X X) permis sur le {interface}: ')
            #     conf_commands.append('conf secondaryip')
            #     conf_commands.append(f'edit {num_seq}')
            #     conf_commands.append(f'set ip {secondary_ip_address}')
            #     conf_commands.append(f'set allow {allow_access}')
            #     conf_commands.append('end')

            # conf_commands.append('next')

        conf_commands.append('end')
        return conf_commands
    
    def configure_ha_manually(self):
        config_commands = ['config system ha']
        mode = input('\nSpécifiez le mode du ha {a-a, a-p, standalone}: ')
        config_commands.append(f"set mode {mode}")

        group_name = input('Spécifiez un nom de groupe de cluster: ')
        config_commands.append(f"set group-name {group_name}")

        print('\nAugmenter la priorité pour sélectionner l\'unité primaire (0 - 255)')
        priority = int(input('Indiquez une priorité: '))
        config_commands.append(f"set priority {priority}")

        monitor_interfaces = input('\nSpécifiez les interfaces de monitoring: ')
        config_commands.append(f"set monitor {monitor_interfaces}")

        heartbeat_interfaces = input('\nSpécifiez les heartbeat interfaces: ')
        heartbeat_interface_priority = []

        for interface in heartbeat_interfaces.split():
            priority = input(f"Spécifiez la priorité (0 - 512) du heartbeat {interface}: ")
            heartbeat_interface_priority.append(priority)
        
        config_commands.append(f"set hbdev {' '.join([interface +' '+ priority for interface, priority in ((zip(heartbeat_interfaces.split(), heartbeat_interface_priority)))])}")
        return config_commands
    
    def configure_ha_via_excel_file(self, df=None):
        config_commands_primary_device = ['config system ha']

        for row in df[df['priority'] == df['priority'].max()].iterrows():
            config_commands_primary_device.append(f"set mode {row[1]['mode']}")
            config_commands_primary_device.append(f"set group-name {row[1]['name_group_cluster']}")
            config_commands_primary_device.append(f"set priority {row[1]['priority']}")
            config_commands_primary_device.append(f"set monitor {row[1]['monitor_interfaces']}")
            config_commands_primary_device.append(f"set hbdev {' '.join([interface +' '+ priority for interface, priority in ((zip(row[1]['heartbeat_interfaces'].split(), row[1]['heartbeat_interfaces_priority'].split())))])}")

            config_commands_primary_device.append('end')
        return config_commands_primary_device
    
    def configure_ha_for_secondary_device_via_excel_file(self, df=None):
        config_commands_secondary_device = ['config system ha']

        for row in df[df['priority'] == df['priority'].min()].iterrows():
            config_commands_secondary_device.append(f"set mode {row[1]['mode']}")
            config_commands_secondary_device.append(f"set group-name {row[1]['name_group_cluster']}")
            config_commands_secondary_device.append(f"set priority {row[1]['priority']}")
            config_commands_secondary_device.append(f"set monitor {row[1]['monitor_interfaces']}")
            config_commands_secondary_device.append(f"set hbdev {' '.join([interface +' '+ priority for interface, priority in ((zip(row[1]['heartbeat_interfaces'].split(), row[1]['heartbeat_interfaces_priority'].split())))])}")

        config_commands_secondary_device.append('end')
        return config_commands_secondary_device

    def create_zones_via_excel_file(self, df=None):
        conf_commands = ['conf system zone']
        for row in df.iterrows():
            conf_commands.append(f"edit {row[1]['name']}")
            conf_commands.append(f"set inter {row[1]['members']}")
            conf_commands.append(f"set intra {row[1]['block intra-zone traffic']}")
            conf_commands.append('next')

        conf_commands.append('end')
        return conf_commands

    def create_local_users(self):
        conf_commands = ['conf user local']
        get_in_loop = True

        while get_in_loop:
            username = input('Entrez un nom d\'utilisateur: ')
            conf_commands.append(f'edit {username}')

            conf_commands.append('set status enable')
            conf_commands.append('set type password')

            passwd = input('Entrez un mot de passe: ')
            conf_commands.append(f'set passwd {passwd}')
            conf_commands.append('next')

            output = input('\nVoulez-vous créer un autre utilisateur local (O ou N): ')
            while output != 'N' and output != 'O':
                print('\nVotre choix est incorrecte !\n')
                output = input('Veillez en effectuer un autre entre (O ou N): ')
                print('\n')

            if output == 'N':
                get_in_loop = False
                
        conf_commands.append('end')
        return conf_commands

    def create_group_users(self):
        conf_commands = ['config user group']
        get_in_loop = True

        while get_in_loop:
            group_name = input('Entrez le nom du groupe: ')
            conf_commands.append(f'edit {group_name}')

            members = input('Entrez les membres du groupe en les séparant par un espace: ')
            conf_commands.append(f'set member {members}')

            conf_commands.append('next')

            output = input('\nVoulez-vous créer un autre groupe d\'utilisateurs (O ou N): ')
            while output != 'N' and output != 'O':
                print('\nVotre choix est incorrecte !\n')
                output = input('Veillez en effectuer un autre entre (O ou N): ')
                print('\n')

            if output == 'N':
                get_in_loop = False
                
        conf_commands.append('end')
        return conf_commands
    
    def create_group_users_via_excel_file(self, df=None):
        conf_commands = ['conf user group']
        for row in df.iterrows():
            if row[1]['type'] == 'ldap':
                conf_commands.append(f"edit {row[1]['user_group_name']}")
                conf_commands.append(f"set member {row[1]['remote_server']}")
                
                conf_commands.append("config match")
                conf_commands.append("edit 1")

                conf_commands.append(f"set server-name {row[1]['remote_server']}")
                conf_commands.append(f"set group-name {row[1]['group_name']}")
                conf_commands.append("next")

        conf_commands.append('end')
        conf_commands.append("end")
        return conf_commands
    
    def create_admin_account_ldap(self):
        conf_commands = ['conf system admin']
        conf_commands.append("edit remote_admin")
        conf_commands.append("set vdom root")
        conf_commands.append("set remote-auth enable")
        conf_commands.append("set accprofile super_admin")
        conf_commands.append("set wildcard enable")
        conf_commands.append("set remote-group Admin")

        conf_commands.append('end')
        return conf_commands

    
    def create_virtual_ips_via_excel_file(self, df=None):
        conf_commands = ['config firewall vip']
        for row in df.iterrows():
            conf_commands.append(f"edit {row[1]['name']}")
            conf_commands.append(f"set extip {row[1]['external IP address/range']}")
            conf_commands.append(f"set extintf {row[1]['interface']}")
            conf_commands.append(f"set mappedip {row[1]['map to IPv4 address/range']}")
            conf_commands.append('next')

        conf_commands.append('end')
        return conf_commands
    
    def create_antivirus_profiles_via_excel_file(self, df=None):
        conf_commands = ['config antivirus profile']
        for row in df.iterrows():
            conf_commands.append(f"edit {row[1]['name']}")
            conf_commands.append(f"set feature-set {row[1]['feature-set']}")
            if len(row[1]['inspected protocols'].split()) == 1:
                conf_commands.append(f"config {row[1]['inspected protocols']}")
                conf_commands.append(f"set av-scan {row[1]['antivirus scan service']}")
                conf_commands.append('end')
            else:
                protocols = row[1]['inspected protocols'].split()
                for protocol in protocols:
                    conf_commands.append(f"config {protocol}")
                    conf_commands.append(f"set av-scan {row[1]['antivirus scan service']}")
                    conf_commands.append('end')

        conf_commands.append('end')
        return conf_commands

    def create_object_addresses_manually(self):
        conf_commands = ['config firewall address']
        get_in_loop = True

        while get_in_loop:
            name_address = input('Spécifiez le nom de l\'objet d\'adresse à créer: ')
            ip_address = input('Spécifiez son adresse IP suivie du mask (/XX): ')

            conf_commands.append(f'edit {name_address}')
            conf_commands.append('set type ipmask')
            conf_commands.append(f'set subnet {ip_address}')
            conf_commands.append('next')

            output = input('\nVoulez-vous créer un autre objet d\'adresse (O ou N): ')
            while output != 'N' and output != 'O':
                print('\nVotre choix est incorrecte !\n')
                output = input('Veillez en effectuer un autre entre (O ou N): ')
                print('\n')

            if output == 'N':
                get_in_loop = False

        conf_commands.append('end')
        return conf_commands
    
    def create_object_addresses_via_excel_file(self, df=None):
        conf_commands = ['config firewall address']

        for row in df.iterrows():
            conf_commands.append(f"edit {row[1]['name']}")
            conf_commands.append('set type ipmask')
            conf_commands.append(f"set subnet {row[1]['IP']}")
            conf_commands.append('next')
        
        conf_commands.append('end')
        return conf_commands
    
    def create_group_addresses_via_excel_file(self, df=None):
        conf_commands = ['config firewall addrgrp']

        for row in df.iterrows():
            conf_commands.append(f"edit {row[1]['name']}")
            conf_commands.append(f"append member {row[1]['member']}")
            conf_commands.append('next')
        
        conf_commands.append('end')
        return conf_commands
    
    def create_group_addresses_manually(self):
        group_name = input('Spécifiez le nom du groupe à créer: ')
        output = input("L'adresse à ajouter existe t-elle déjà ? (O ou N): ")

        while output != 'O' and output != 'N':
            print('Votre choix est incorrecte !')
            output = input("Veillez en effectuer un autre: ")

        if output == 'O':
            name_address = input(f"\nSpécifiez le ou les nom(s) d'adresse(s) séparés par des virgules à ajouter au groupe {group_name}: ")

            return [
                'config firewall addrgrp',
                f'edit {group_name}',
                f'append member {name_address}',
                'end']
        else:
            commands_create_addresses = FortinetModule.create_object_addresses_manually(self)

            commands_create_addresses.append('config firewall addrgrp')
            commands_create_addresses.append(f'edit {group_name}')
            commands_create_addresses.append(f'append member {name_address}')
            commands_create_addresses.append('end')
            return commands_create_addresses
        
    def create_static_routes_manually(self):
        conf_commands = ['config router static']
        get_in_loop = True
        
        while get_in_loop:
            route_id = input('Spécifiez l\'id de la route: ')
            interface = input('Spécifiez l\'interface de sortie: ')
            gateway = input('Spécifiez la Gateway IP: ')
            ip_dest_addr = input('Spécifiez l\'adresse réseau de destination suivi du mask: ') 

            conf_commands.append(f'edit {route_id}')
            conf_commands.append('set status enable')
            conf_commands.append(f'set device {interface}')
            conf_commands.append(f'set gateway {gateway}')
            conf_commands.append(f'set dst {ip_dest_addr}')
            conf_commands.append('next')
            
            output = input('Voulez-vous créer une autre adresse statique (O ou N): ')

            while output != 'O' and output != 'N':
                print('Votre choix est incorrecte !')
                output = input("Veillez en effectuer un autre: ")

            if output == 'N':
                get_in_loop = False

        conf_commands.append('end')
        return conf_commands
    
    def create_static_routes_via_excel_file(self, df):
        conf_commands = ['config router static']
        for row in df.iterrows():
            conf_commands.append(f"edit {row[1]['seq-num']}")
            conf_commands.append(f"set dst {row[1]['destination']}")
            conf_commands.append(f"set gateway {row[1]['gateway']}")                    
            conf_commands.append(f"set device {row[1]['interface']}")
            conf_commands.append('set status enable')
            conf_commands.append('next')

        conf_commands.append('end')
        return conf_commands
    
    def create_ospf_routes_via_excel_file(self, df=None):
        conf_commands = ['config router ospf']

        # Configure Router ID and Areas table
        for row in df[df[['router-id', 'area-id']].duplicated()][['router-id', 'area-id']].iterrows():
            conf_commands.append(f"set router-id {row[1]['router-id']}")
            conf_commands.append('config area')
            conf_commands.append(f"edit {row[1]['area-id']}")

            conf_commands.append('next')
        conf_commands.append('end')

        # Configure networks table
        conf_commands.append('config network')
        for row in df[['network']].iterrows():
            conf_commands.append(f"edit {row[0]+1}")
            conf_commands.append(f"set prefix {row[1]['network']}")

            conf_commands.append('next')
        conf_commands.append('end')

        # Configure interfaces table
        conf_commands.append('config ospf-interface')
        for row in df[['name', 'interface', 'priority']].iterrows():
            conf_commands.append(f"edit {row[1]['name']}")
            conf_commands.append(f"set interface {row[1]['interface']}")
            conf_commands.append(f"set priority {row[1]['priority']}")
            conf_commands.append('set dead-interval 40')
            conf_commands.append('set hello-interval 10')

            conf_commands.append('next')
        conf_commands.append('end')

        return conf_commands
        
    def create_firewall_policy_via_excel_file(self, df=None):
        conf_commands = ['conf firewall policy']
        if df is None:
            file_name = input('Veillez spécifier le nom du fichier sans l\'extension: ')
            try:
                df = pd.read_excel(file_name)

            except Exception as e:
                print('Le fichier que vous avez spécifié est incorrecte !\n')
                print(f'Erreur: {str(e)}')
        
        for row in df.iterrows():
            conf_commands.append(f"edit {row[1]['policy-id']}")
            conf_commands.append(f"set name {row[1]['policy-name']}")
            conf_commands.append(f"set srcintf {row[1]['incoming-interface']}")
            conf_commands.append(f"set dstintf {row[1]['outgoing-interface']}")
            conf_commands.append(f"set srcaddr {row[1]['source']}")
            conf_commands.append(f"set dstaddr {row[1]['destination']}")
            conf_commands.append(f"set action {row[1]['action']}")
            conf_commands.append(f"set inspection-mode {row[1]['inspection-mode']}")
            conf_commands.append(f"set schedule {row[1]['schedule']}")
            conf_commands.append(f'set service {row[1]["service"].translate({ord(i): None for i in "[],"})}')
            conf_commands.append(f'set nat {row[1]["nat"]}')
            conf_commands.append(f'set status {row[1]["status"]}')
            conf_commands.append('next')

        conf_commands.append('end')
        return conf_commands
    
    def create_admin(self):
        conf_commands = ['conf syst acc']
        type_admin = input('Spécifiez le type d\'administrateur {Administrator, REST_API}: ')

        if type_admin == 'Administrator':
            pass
        elif type_admin == 'REST_API':
            pass
    
    def search_api_admin(self, response):
        match = False
        result = ''
        group_pattern = re.compile(r"edit (.+)")

        api_references = group_pattern.finditer(response)
        for api_reference in api_references:
            result = api_reference.group(1)

        if result == '"api-admin" <---':
            match = True
        return match

    def create_api_admin(self):
        return ['conf syst acc', 'edit api-admin-profile', 'set secfabgrp read-write',
                'set ftviewgrp read-write', 'set authgrp read-write', 'set sysgrp read-write', 'set netgrp read-write',
                'set loggrp read-write', 'set fwgrp read-write', 'set vpngrp read-write', 'set utmgrp read-write',
                'set wanoptgrp read-write', 'set wifi read-write', 'set admintimeout-override enable', 'set system-diagnostics enable',
                'end', 'conf syst api-user', 'edit api-admin', 'set accprofile api-admin-profile', 'set vdom root', 'end']   
    
    def generate_token(self):
        return ['execute api-user generate-key api-admin']
    
    def extract_token(self, response):
        token = response.split()[7]
        return token
    
    def get_static_routes(self, token):
        url = 'http://' + self.host + '/api/v2/cmdb/router/static'
        headers = {
                    'Authorization': f'Bearer {token}'
                }
        response = requests.request("GET", url, headers=headers)
        results = response.json()['results']

        static_routes = {
            'seq-num':[],
            'destination':[],
            'gateway':[],
            'interface':[],
            'status':[]
        }

        for i in range(0, len(results)):
            static_routes['seq-num'] += [results[i]['seq-num']]
            static_routes['destination'] += [results[i]['dst']]
            static_routes['gateway'] += [results[i]['gateway']]
            static_routes['interface'] += [results[i]['device']]
            static_routes['status'] += [results[i]['status']]

        df_static_routes = pd.DataFrame(static_routes)
        return df_static_routes
    
    def get_ospf_routes(self, token):
        url = 'http://' + self.host + '/api/v2/cmdb/router/ospf'
        headers = {
                    'Authorization': f'Bearer {token}'
                }
        response = requests.request("GET", url, headers=headers)
        results = response.json()['results']

        router_id_and_areas = {
            'router-id':[],
            'area-id':[],
            'type':[],
        }

        ospf_networks = {
            'network-id':[],
            'network-area':[],
            'network-prefix':[]
        }

        ospf_interfaces = {
            'name':[],
            'interface':[],
            'ip':[],
            'priority':[]
        }

        router_id_and_areas['router-id'] = results['router-id']
        router_id_and_areas['area-id'] += [area['id'] for area in results['area']]
        router_id_and_areas['type'] += [area['type'] for area in results['area']]

        ospf_interfaces['name'] += [[name['name'] for name in results['ospf-interface']]]
        ospf_interfaces['ip'] += [[ip['ip'] for ip in results['ospf-interface']]]
        ospf_interfaces['interface'] += [[interface['interface'] for interface in results['ospf-interface']]]
        ospf_interfaces['priority'] += [[priority['priority'] for priority in results['ospf-interface']]]

        ospf_networks['network-id'] += [[id['id'] for id in results['network']]]
        ospf_networks['network-prefix'] += [[prefix['prefix'] for prefix in results['network']]]
        ospf_networks['network-area'] += [[area['area'] for area in results['network']]]

        # df_ospf_routes = pd.DataFrame(ospf_routes)
        return ospf_networks

    def get_firewall_policy(self, token):
        url = 'http://'+ self.host + '/api/v2/cmdb/firewall/policy'
        headers = {
                    'Authorization': f'Bearer {token}'
                }
        response = requests.request("GET", url, headers=headers)
        results = response.json()['results']

        firewall_policy = {
            'policy-id':[],
            'status': [],
            'policy-name':[],
            'incoming-interface':[],
            'outgoing-interface':[],
            'source':[],
            'destination':[],
            'schedule':[],
            'service':[],
            'action':[],
            'inspection-mode':[],
            'nat':[]
            }

        for i in range(0, len(results)):
            firewall_policy['policy-id'] += [results[i]['policyid']]
            firewall_policy['status'] += [results[i]['status']]
            firewall_policy['policy-name'] += [results[i]['name']]
            firewall_policy['incoming-interface'] += [[srcintf['name'] for srcintf in results[i]['srcintf']]]
            firewall_policy['outgoing-interface'] += [[dstintf['name'] for dstintf in results[i]['dstintf']]]
            firewall_policy['source'] += [[srcaddr['name'] for srcaddr in results[i]['srcaddr']]]
            firewall_policy['destination'] += [[dstaddr['name'] for dstaddr in results[i]['dstaddr']]]
            firewall_policy['schedule'] += [results[i]['schedule']]
            firewall_policy['service'] += [[service['name'] for service in results[i]['service']]]
            firewall_policy['action'] += [results[i]['action']]
            firewall_policy['inspection-mode'] += [results[i]['inspection-mode']]
            firewall_policy['nat'] += [results[i]['nat']]
        
        df_firewall_policy = pd.DataFrame(firewall_policy)
        return df_firewall_policy
        # return df_policy.to_excel('Firewall_Policy.xlsx', index=False)

    def get_antivirus_profiles(self, token):

        url = "http://"+ self.host + "/api/v2/cmdb/antivirus/profile"
        headers = {
                    'Authorization': f'Bearer {token}'
                    }
        
        response = requests.request("GET", url, headers=headers)
        results = response.json()['results']
        antivirus_profiles = {
                                'name':[],
                                'comment':[],
                                'feature-set':[],
                                'inspected-protocols':[]
                                }
        for i in range(0, len(results)):
            antivirus_profiles['name'] += [results[i]['name']]
            antivirus_profiles['comment'] += [results[i]['comment']]
            antivirus_profiles['feature-set'] += [results[i]['feature-set']]
            antivirus_profiles['inspected-protocols'] += [[protocol for protocol in ('http', 'ftp', 'imap', 'pop3', 'smtp', 'mapi', 'nntp', 'cifs', 'ssh') 
                                                    if results[i][protocol]['av-scan'] == 'block']]
            
        df_antivirus_profiles = pd.DataFrame(antivirus_profiles)
        return df_antivirus_profiles

    def get_virtual_ips(self, token):

        url = "http://"+ self.host + "/api/v2/cmdb/firewall/vip"
        headers = {
                    'Authorization': f'Bearer {token}'
                    }
        
        response = requests.request("GET", url, headers=headers)
        results = response.json()['results']

        virtual_ips = {
            'name':[],
            'type':[],
            'external IP':[],
            'map-to':[],
            'external interface':[],
            'status':[]
        }

        for i in range(0, len(results)):
            virtual_ips['name'] += [results[i]['name']]
            virtual_ips['type'] += [results[i]['type']]
            virtual_ips['external IP'] += [results[i]['extip']]
            virtual_ips['map-to'] += [[mapped['range'] for mapped in results[i]['mappedip']]]
            virtual_ips['external interface'] += [results[i]['extintf']]
            virtual_ips['status'] += [results[i]['status']]
        
        df_virtual_ips = pd.DataFrame(virtual_ips)
        return df_virtual_ips
    
    def set_up_ldap_server(self):
        conf_commands = ['conf user ldap']
        ldap_name = input('\nSpécifiez un nom pour le serveur LDAP: ')
        conf_commands.append(f'edit {ldap_name}')

        domain_name_or_ip = input('Spécifiez l\'adresse IP ou le nom de domaine cn du server LDAP: ')
        conf_commands.append(f'set server {domain_name_or_ip}')

        # cn = input('Spécifiez l\'identifiant du nom commun du serveur LDAP (cn par défaut): ')
        # conf_commands.append(f'set cnid {cn}')

        dn = input('Spécifiez le nom distinctif utilisé pour rechercher des entrées sur le serveur LDAP sous la forme (dc=fortinet-fsso,dc=com): ')
        conf_commands.append(f'set dn {dn}')
        conf_commands.append('set type regular')

        username = input('Spécifiez le nom d\'utilisateur dn complet pour la liaison initiale sous la forme (cn=Administrator,cn=users,dc=fortinet-fsso,dc=com): ')
        conf_commands.append(f'set username {username}')

        passwd = input('Spécifiez le mot de passe pour la liaision initiale: ')
        conf_commands.append(f'set password {passwd}')
        # Tester la connectivité au serveur LDAP et renvoyé succeed si l'intégration a bien été effectué
        conf_commands.append('end')
        return conf_commands
    
    def set_up_ldap_server_via_excel_file(self, df=None):
        print('Intégration serveur LDAP')

        conf_commands = ['conf user ldap']
        for row in df.iterrows():
            conf_commands.append(f"edit {row[1]['name_server_ldap']}")
            conf_commands.append(f"set server {row[1]['domain_name_or_ip_address']}")
            conf_commands.append(f'set cnid cn')
            conf_commands.append(f"set dn {row[1]['distinguished_name']}")
            conf_commands.append('set type regular')
            conf_commands.append(f"set username {row[1]['username']}")
            conf_commands.append(f"set password {row[1]['password']}")

            conf_commands.append('end')

            print('Intégration serveur LDAP effectuée')
        return conf_commands

    def set_up_radius_server(self):
        pass

    def get_sdwan_rules(self):
        pass

    def get_object_addresses(self, token):
        url = 'http://'+ self.host + '/api/v2/cmdb/firewall/address'

        headers = {
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("GET", url, headers=headers)
        results = response.json()['results']

        object_addresses = {
            'name':[],
            'subnet':[],
            'type':[],
            'interface':[]
            }
        for i in range(0, len(results)):
            object_addresses['name'] += [results[i]['name']]
            object_addresses['subnet'] += [results[i]['subnet'] if 'subnet' in results[i].keys() else '']
            object_addresses['type'] += [results[i]['type']]
            object_addresses['interface'] += [results[i]['interface']]
        
        df_object_addresses = pd.DataFrame(object_addresses)
        return df_object_addresses
        
    def get_group_addresses(self, token):
        url = 'http://'+ self.host + '/api/v2/cmdb/firewall/addrgrp'
        headers = {
                    'Authorization': f'Bearer {token}'
                    }
        
        response = requests.request("GET", url, headers=headers)
        results = response.json()['results']

        group_addresses = {
            'name':[],
            'member':[],
            'exclude-member':[]
        }
        for i in range(0, len(results)):
            group_addresses['name'] += [results[i]['name']]
            group_addresses['member'] += [[member['name'] for member in results[i]['member']]]
            group_addresses['exclude-member'] += [[member['name'] for member in results[i]['exclude-member']]]

        df_group_addresses = pd.DataFrame(group_addresses)
        return df_group_addresses

    def get_backup(self, token):
        url = 'http://'+ self.host +'/api/v2/monitor/system/config/backup?destination=file&scope=global'

        headers = {
        'Authorization': f'Bearer {token}',
        'Cookie': 'FILE_DOWNLOADING_10657851028130304241="1"'
        }
        response = requests.request("GET", url, headers=headers)

        with open("Backup02.conf", 'wb') as f:
            f.write(response.content)

    def get_config_interfaces(self, token):
        url = 'http://'+ self.host +'/api/v2/cmdb/system/interface'

        headers = {
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("GET", url, headers=headers)
        results = response.json()['results']

        interfaces_states={
            'name':[],
            'type':[],
            'vlanid':[],
            'mode':[],
            'ip':[],
            'allowaccess':[],
            'interface':[],
            'member':[],
            'status':[],
            'secondaryip':[],
        }

        for j in range(0, len(results)):
            interfaces_states['name'] += [results[j]['name']]
            interfaces_states['type'] += [results[j]['type']]
            interfaces_states['vlanid'] += [results[j]['vlanid']]
            interfaces_states['mode'] += [results[j]['mode']]
            interfaces_states['ip'] += [results[j]['ip']]
            interfaces_states['allowaccess'] += [results[j]['allowaccess']]
            interfaces_states['interface'] += [results[j]['interface']]
            interfaces_states['member'] += [[member['interface-name'] for member in results[j]['member']]]
            interfaces_states['status'] += [results[j]['status']]
            interfaces_states['secondaryip'] += [results[j]['secondaryip']]
        
        df_interfaces = pd.DataFrame(interfaces_states)
        return df_interfaces
        # return df_interfaces.to_excel('firewall_forti_config_interfaces.xlsx', index=False)

    def get_zones(self, token):
        pass

    def get_policy_routes(self):
        pass

    def make_all_config(self):
        config_commands = {}
        file_name = input('\nVeillez spécifier le nom du fichier Excel sans l\'extension: ')
        f = pd.ExcelFile(f"templates\{file_name}.xlsx")
        try:
            for sheet in f.sheet_names:
                df = f.parse(sheet)
                
                if sheet == 'Object Addresses':
                    config_commands['config_object_addresses'] = FortinetModule.create_object_addresses_via_excel_file(self, df)
                
                elif sheet == 'Group Addresses':
                    config_commands['config_group_addresses'] = FortinetModule.create_group_addresses_via_excel_file(self, df)
                
                elif sheet == 'Interfaces':
                    config_commands['config_interfaces'] = FortinetModule.configure_interfaces_via_excel_file(self, df) 

                elif sheet == 'Zones':
                    config_commands['config_zones'] = FortinetModule.create_zones_via_excel_file(self, df)

                elif sheet == 'Virtual IPs':
                    config_commands['config_virtual_ips'] = FortinetModule.create_virtual_ips_via_excel_file(self, df)
                
                elif sheet == 'Firewall Policy':
                    config_commands['config_firewall_policy'] = FortinetModule.create_firewall_policy_via_excel_file(self, df)
            
                elif sheet == 'Policy routes':
                    pass

                elif sheet == 'Static routing':
                    config_commands['config_static_routes'] = FortinetModule.create_static_routes_via_excel_file(self, df)

                elif sheet == 'OSPF routing':
                    config_commands['config_ospf_routes'] = FortinetModule.create_ospf_routes_via_excel_file(self, df)

                elif sheet == 'BGP routing':
                    pass
                
                elif sheet == 'Antivirus Profiles':
                    config_commands['config_antivirus_profiles'] = FortinetModule.create_antivirus_profiles_via_excel_file(self, df)

                # elif sheet == 'IPS Sensor':
                #     pass

                # elif sheet == 'LDAP':
                #     config_commands['config_set_up_ldap_server'] = FortinetModule.set_up_ldap_server_via_excel_file(self, df)
                
                # if sheet == 'User Groups':
                #     config_commands['config_group_ldap_users'] = FortinetModule.create_group_users_via_excel_file(self, df)
                #     config_commands['config_admin_account_ldap'] = FortinetModule.create_admin_account_ldap(self)

                # elif sheet == 'HA':
                #     config_commands['config_ha_primary_device'] = FortinetModule.configure_ha_via_excel_file(self, df)
                #     config_commands['config_ha_secondary_device'] = FortinetModule.configure_ha_for_secondary_device_via_excel_file(self, df) 

        except Exception as e:
            print('Le fichier que vous avez spécifié est incorrecte !\n')
            print(f'Erreur: {str(e)}')

        return config_commands
    
    def get_all_config(self, token):
        df_object_addresses = FortinetModule.get_object_addresses(self, token=token)
        df_group_addresses = FortinetModule.get_group_addresses(self, token=token)
        df_interfaces = FortinetModule.get_config_interfaces(self, token=token)
        df_virtual_ips = FortinetModule.get_virtual_ips(self, token=token)
        df_firewall_policy = FortinetModule.get_firewall_policy(self, token=token)
        df_get_static_routes = FortinetModule.get_static_routes(self, token=token)
        # df_ospf_routes = FortinetModule.get_ospf_routes(self, token=token)
        # print(df_ospf_routes)
        df_antivirus_profiles = FortinetModule.get_antivirus_profiles(self, token=token)

        with pd.ExcelWriter('forti_all_config.xlsx') as writer:
            df_object_addresses.to_excel(writer, sheet_name='Object Addresses', index=False)
            df_group_addresses.to_excel(writer, sheet_name='Group Addresses', index=False)
            df_interfaces.to_excel(writer, sheet_name='Interfaces', index=False)
            df_virtual_ips.to_excel(writer, sheet_name='Virtual IPs', index=False)
            df_firewall_policy.to_excel(writer, sheet_name='Firewall Policy', index=False)
            df_get_static_routes.to_excel(writer, sheet_name='Static Routing', index=False)
            df_antivirus_profiles.to_excel(writer, sheet_name='Antivirus Profiles', index=False)

        
