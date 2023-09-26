import pandas as pd
import re

from DevicesModule import DevicesModule
from FortinetModule import FortinetModule

class PaloAltoModule(DevicesModule):

    DEVICE_TYPE = 'paloalto_panos'

    def __init__(self):
        DevicesModule.__init__(self)

    def get_attr(self):
        attr = DevicesModule.get_attr(self)
        attr['device_type'] = PaloAltoModule.DEVICE_TYPE

        return attr


    def match_interfaces_fortigate(self, df):
        physical_interfaces = df[df['type'] == 'physical']['name'].unique()
        match_interf_palo = {}

        for physical_interface in physical_interfaces:
            interface = input(f'A quoi correspond le {physical_interface} du fortigate sur le palo alto: ')
            match_interf_palo[f'{physical_interface}'] = interface

        for key, value in match_interf_palo.items():
            match = re.search(r'eth(?:er)?(\d+)/(\d+)', value)
            if match:
                part1_port = match.group(1)
                part2_port = match.group(2)
                replaced_value = re.sub(r'eth(?:er)?(\d+)/(\d+)', 'ethernet' + part1_port + "/" + part2_port, value)
                match_interf_palo[f'{key}'] = replaced_value
        
        for inter in physical_interfaces:
            df.loc[df['name'] == inter, 'name'] = match_interf_palo[f'{inter}']
            df.loc[df['interface'] == inter, 'interface'] = match_interf_palo[f'{inter}']
        
        return df

    def config_interfaces_via_sheet(self, df=None):

        # if df is None:
        #     file_name = input('Veillez spécifier le nom du fichier Excel sans l\'extension: ')
        #     try:
        #         df = pd.read_excel(f'{file_name}.xlsx')

        #     except Exception as e:
        #         print('Le fichier que vous avez spécifié est incorrecte !\n')
        #         print(f'Erreur: {str(e)}')

        df_matched = PaloAltoModule.match_interfaces_fortigate(self, df=df)

        # Configuration des interfaces
        conf_commands = []
        for row in df_matched.iterrows():
            if row[1]['type'] == 'physical':
                # Création du profil de management
                conf_commands.append(f"set network profiles interface-management-profile access_{row[1]['name'].replace('/', '-')} {' '.join([access+' yes' for access in row[1]['allowaccess'].split()])}")

                # Configuration des interfaces ethernet
                conf_commands.append(f"set network interface ethernet {row[1]['name']} layer3 interface-management-profile access_{row[1]['name'].replace('/', '-')} ip {row[1]['ip']}")

            elif row[1]['type'] == 'vlan':
                # Création des sous interfaces VLANs
                conf_commands.append(f"set network interface ethernet {row[1]['interface']} layer3 units {row[1]['interface']}.{row[1]['vlanid']} tag {row[1]['vlanid']} ip {row[1]['ip']}")

            elif row[1]['type'] == 'aggregate':
                pass

            else:
                pass

        # conf_commands.append('commit')
        return conf_commands
    
    def create_object_addresses_via_sheet(self, df=None):
        
        conf_commands = []
        for row in df.iterrows():
            conf_commands.append(f"set address {row[1]['name']} ip-netmask {row[1]['IP']}")

        return conf_commands
    
    def attribute_object_addresses_into_group(self, df=None):

        conf_commands = []
        for row in df.iterrows():
            members = row[1]['member'].split()
            for member in members:
                conf_commands.append(f"set address-group {row[1]['name']} static {member}")
        
        return conf_commands
    
    def create_firewall_policy_via_sheet(self, df=None):
        conf_commands = []
        return conf_commands
        
    def make_all_config(self):
        config_commands = {}
        file_name = input('\nVeillez spécifier le fichier de configuration Excel sans l\'extension: ')
        f = pd.ExcelFile(f"{file_name}.xlsx")
        try:
            for sheet in f.sheet_names:
                df = f.parse(sheet)
                df = df.fillna('None')

                if sheet == 'Object Addresses':
                    config_commands['config_object_addresses'] = PaloAltoModule.create_object_addresses_via_sheet(self, df)
                
                elif sheet == 'Group Addresses':
                    config_commands['config_attrib_obj_addr_into_group'] = PaloAltoModule.attribute_object_addresses_into_group(self, df)

                elif sheet == 'Interfaces':
                    print('\n')
                    config_commands['config_interfaces'] = PaloAltoModule.config_interfaces_via_sheet(self, df)


                elif sheet == 'Firewall Policy':
                    config_commands['confif_firewall_policy'] = PaloAltoModule.create_firewall_policy_via_sheet(self, df)
                
        except Exception as e:
            print('Le fichier que vous avez spécifié est incorrecte !\n')
            print(f'Erreur: {str(e)}')

        return config_commands