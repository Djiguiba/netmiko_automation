from netmiko import Netmiko

from CiscoIosModule import CiscoIosModule
from FortinetModule import FortinetModule
from PaloAltoModule import PaloAltoModule

print('\n')
print(f"{'*'*50} CONFIGURATION DES EQUIPEMENTS DE RESEAU ET DE SECURITE {'*'*50}\n")
print(f"{'*'*48} Faites un choix en sélectionnant le nombre correspondant {'*'*48}\n")
print(f"{'*'*40} Pour sortir du programme ou d'une configuration, entrez la commande: exit {'*'*40}")
print('\n')

run_program = True
while run_program:
    print(f"{'*'*160}\n")
    print(f"{' '*70} PROGRAMME PRINCIPAL {' '*70}\n")
    print(f"{'*'*160}\n")
    print("1. Configuration d'un routeur\n")
    print("2. Configuration d'un switch\n")
    print("3. Configuration d'un firewall\n")

    choice_input = True
    inp = input("Quel est votre choix: ")

    while choice_input:
        if inp == '1':
            print('\n')
            print(f"{'*'*55} MODELES DE ROUTEUR {'*'*55}\n")

            print("1. Cisco 4300 series\n")
            # print("2. Cisco 9300 series\n")
            # print("3. Nexus")

            choice = input('Veillez effectuer une selection du routeur: ')
            if choice == '1':
                print('\n')
                cisco_ios = CiscoIosModule()
                print('\n')

                try:
                    print(f"{'*'*50} Connection à l'équipement réseau {'*'*50}\n")
                    net_connect = Netmiko(**cisco_ios.get_attr())
                    print(f"{'*'*58} Connection effectuée {'*'*58}\n")

                except Exception as e:
                    print(f"Erreur : {str(e)}")
                    print('\n')
                    break
                
                run_sub_routine = True
                while run_sub_routine:

                    print(f"{'*'*48} Veillez selectionner une configuration {'*'*48}\n")

                    print("1. Modification du hostname\n")
                    print("2. Création d'utilisateurs\n")
                    print("3. Configuration des interfaces\n")
                    print("4. Configuration de routes statiques\n")
                    print("5. Configuration du routage dynamique\n")
                    print("6. Routage Inter-VLAN\n")

                    choice = input("Quel est votre choix: ")
                    print('\n')
                    if choice == '1':
                        config_command = cisco_ios.modify_hostname()
                        net_connect.enable()
                        modif_done = net_connect.send_config_set(config_command)

                        # print(modif_host)
                    elif choice == '2':
                        config_command = cisco_ios.create_user()
                        net_connect.enable()
                        user_created = net_connect.send_config_set(config_command)

                        # print(user_created)
                    elif choice == '3':
                        config_command = cisco_ios.config_interfaces()
                        net_connect.enable()
                        conf_interfaces_done = net_connect.send_config_set(config_command)
                        
                        # print(conf_interfaces_done)
                    elif choice == '4':
                        print('Veillez respecter le format suivant -> X.X.X.X X.X.X.X X.X.X.X\n')
                        config_command = cisco_ios.add_static_routes()
                        net_connect.enable()
                        conf_static_route_done = net_connect.send_config_set(config_command)

                        # print(conf_static_route_done)
                    elif choice == '5':
                        config_command = cisco_ios.add_dynamic_routes()
                        net_connect.enable()
                        conf_dynamic_route_done = net_connect.send_config_set(config_command)

                        # print(conf_dynamic_route_done)
                    elif choice == 'exit':
                        break

                net_connect.disconnect()

            elif choice == 'exit':
                print('\n')
                break

            else:
                print('\n')
                print("Votre selection est incorrecte, veillez en effectuer une autre.\n")

        elif inp == '2':
            print('\n')
            print(f"{'*'*55} MODELES DE SWITCH {'*'*55}\n")

            print("1. Cisco 9000 series\n")
            print("2. Nexus 9000 series\n")
            print("3. Nexus 3000 series\n")
            
            choice = input('Veillez effectuer une sélection du Switch: ')
            if choice in('1', '2', '3'):
                print('\n')
                cisco_ios = CiscoIosModule()
                print('\n')

                try:
                    print(f"{'*'*50} Connection à l'équipement réseau {'*'*50}\n")
                    net_connect = Netmiko(**cisco_ios.get_attr())
                    print(f"{'*'*58} Connection effectuée {'*'*58}\n")

                except Exception as e:
                    print(f"Erreur : {str(e)}")
                    print('\n')
                    break

                run_sub_routine = True
                while run_sub_routine:

                    print(f"{'*'*50} Veillez sélectionner une configuration {'*'*50}\n")
                    print("1. Modifier du hostname\n")
                    print("2. Créer un utilisateur\n")
                    print("3. Configurer des VLANs\n")
                    print("4. Configurer des interfaces VLAN\n")
                    print("5. Affecter des interfaces à un VLAN spécifique\n")
                    print("6. Switcher des ports en mode trunk\n")
                    print("7. Switcher des ports en mode access\n")
                    print("8. Ajouter des VLANs à un port trunk spécifique\n")
                    print("9. Configurer le LACP\n")
                    print("10. Effectuer les configurations à partir d'un seul fichier\n")

                    choice = input("Quel est votre choix: ")

                    print('\n')
                    if choice == '1':
                        net_connect.enable()
                        net_connect.send_config_set(cisco_ios.modify_hostname())

                    elif choice == '2':
                        net_connect.enable()
                        net_connect.send_config_set(cisco_ios.create_user())

                    elif choice == '3':
                        net_connect.enable()
                        net_connect.send_config_set(cisco_ios.create_vlans())

                    elif choice == '4':
                        net_connect.enable()
                        net_connect.send_config_set(cisco_ios.create_vlan_interfaces())
                    
                    elif choice == '5':
                        net_connect.enable()
                        net_connect.send_config_set(cisco_ios.add_interfaces_to_vlan())

                    elif choice == '6':
                        net_connect.enable()
                        net_connect.send_config_set(cisco_ios.switch_port_to_trunk())

                    elif choice == '7':
                        net_connect.enable()
                        net_connect.send_config_set(cisco_ios.switch_port_to_access())

                    elif choice == '8':
                        net_connect.enable()
                        net_connect.send_config_set(cisco_ios.add_vlan_to_trunk_port())

                    elif choice == '9':
                        net_connect.enable()
                        net_connect.send_config_set(cisco_ios.config_link_aggregation())
                    
                    elif choice == '10':
                        net_connect.enable()
                        for config_command in cisco_ios.make_all_config().items():
                            net_connect.send_config_set(config_command[1])

                    elif choice == 'exit':
                        break

                    else:
                        print('Vous avez effectué une mauvaise selection, veillez en effectuer une autre!\n')

                net_connect.disconnect()

            elif choice == 'exit':
                print('\n')
                break

            else:
                print('\n')
                print("Votre selection est incorrecte, veillez en effectuer une autre.\n")

        elif inp == '3':
            print('\n')
            print(f"{'*'*55} Veillez effectuer une sélection du Firewall {'*'*55}\n")

            print("1. FortiGate\n")
            print("2. Palo Alto\n")
            print("3. Juniper\n")
            print("4. Cisco ASA\n")
            
            choice = input('Veillez effectuer la sélection du Firewall: ')
            if choice == '1':
                print('\n')
                fortinet = FortinetModule()
                print('\n')

                try:
                    print(f"{'*'*20} Connection à l'équipement réseau {'*'*20}\n")
                    net_connect = Netmiko(**fortinet.get_attr())
                    print(f"{'*'*28} Connection effectuée {'*'*28}\n")

                except Exception as e:
                    print(f"Erreur : {str(e)}")
                    print('\n')
                    break
                
                run_sub_routine = True
                while run_sub_routine:
                    print(f"{'*'*28} Veillez selectionner une configuration {'*'*28}\n")

                    print("1. Configuration des paramètres généraux\n")
                    print("2. Configuration des paramètres avancés\n")

                    select = input(f"{'*'*10} Veillez effectuer votre sélection: ")

                    print('\n')
                    if select == '1':
                        into_loop = True
                        while into_loop:
                            
                            print(f"{'*'*28} Veillez effectuer une sélection {'*'*28}\n")

                            print("1. Configurer le Hostname\n")
                            print("2. Configurer le NTP\n")
                            print("3. Configurer le DNS\n")
                            print("4. Création d'utilisateurs locaux\n")
                            print("5. Création de groupes d'utilisateurs\n")

                            choice = input("Veillez effectuer votre sélection: ")
                            print('\n')
                            if choice == '1':
                                net_connect.send_config_set(fortinet.set_hostname())
                                print('\n')

                            elif choice == '2':
                                net_connect.send_config_set(fortinet.configure_ntp_server())
                                print('\n')

                            elif choice == '3':
                                net_connect.send_config_set(fortinet.configure_dns())
                                print('\n')

                            elif choice == '4':
                                net_connect.send_config_set(fortinet.create_local_users())
                                print('\n')

                            elif choice == '5':
                                net_connect.send_config_set(fortinet.create_group_users())
                                print('\n')

                            elif choice == 'exit':
                                into_loop = False
                                print('\n')
                            
                            else:
                                print('Votre sélection est incorrecte, veillez en effectuer une autre!\n')

                    elif select == '2':
                        into_loop = True
                        while into_loop:
                            
                            print(f"{'*'*48} Veillez effectuer une sélection {'*'*48}\n")

                            print("1. Interfaces\n")
                            print("2. Adresses\n")
                            print("3. Politiques de Firewall\n")
                            print("4. Routage\n")
                            print("5. Profils de sécurité\n")
                            print("6. Intégration serveur\n")
                            print("7. High Availability (HA)\n")
                            print("8. Effectuer les configurations à partir d'un seul fichier\n")
                            print("9. Récupérer les configurations effectuées via un fichier Excel\n")

                            choice = input(f"{'*'*10} Veillez effectuer une sélection: ")
                            if choice == '1':
                                enter=True
                                while enter:
                                    print("\n1. Configurer via un fichier Excel\n")
                                    print("2. Configurer manuellement\n")

                                    input_value = input(f"{'*'*5} Veillez sélectionner une option: ")
                                    if input_value == '1':
                                        # Status ---> 01/02 achieved
                                        net_connect.send_config_set(fortinet.configure_interfaces_via_excel_file())
                                        
                                    elif input_value == '2':
                                        # A implémenter la méthode configure_interfaces_manually() 
                                        net_connect.send_config_set(fortinet.configure_interfaces_manually())

                                    elif input_value == 'exit':
                                        enter=False
                                        print('\n')

                                    else:
                                        enter_input = False 
                                        while not enter_input:
                                            print('Votre sélection est incorrecte, veillez en effectuer une autre!\n')
                                            input_value = input("Quel est votre choix: ")
                                            if enter_input in ('1', '2', 'exit'):
                                                enter_input = True

                            elif choice == '2':
                                # Status ---> 03/04
                                print('\n1. Créer des objets d\'adresses\n')
                                print('2. Créer des groupes d\'adresses\n')

                                input_value = input(f"{'*'*5} Veillez sélectionner une option: ")
                                if input_value == '1':
                                    print("\n1. Via un fichier Excel\n")
                                    print("2. Manuellement\n")

                                    opt = input(f"{'*'*10} Quel est votre choix: ")
                                    if opt == '1':
                                        net_connect.send_config_set(fortinet.create_object_addresses_via_excel_file())
                                        print('\n')

                                    elif opt == '2':
                                       net_connect.send_config_set(fortinet.create_object_addresses_manually())
                                       print('\n')
                                        
                                    elif opt == 'exit':
                                        pass

                                    else:
                                        opt_input = False
                                        while not opt_input:
                                            print("Votre choix est incorrecte, veillez en effectuer un nouveau.\n")
                                            opt_input = input("Quel est votre choix: ")
                                            if opt_input in ('1', '2', 'exit'):
                                                opt_input = True

                                elif input_value == '2':
                                    print("\n1. Via un fichier Excel\n")
                                    print("2. Manuellement\n")

                                    opt = input(f"{'*'*10} Quel est votre choix: ")
                                    if opt == '1':
                                        # A implémenter la méthode create_group_addresses_via_excel_file()
                                        net_connect.send_config_set(fortinet.create_group_addresses_via_excel_file())
                                        print('\n')

                                    elif opt == '2':
                                        net_connect.send_config_set(fortinet.create_group_addresses_manually())

                                    elif opt == 'exit':
                                        pass

                                    else:
                                        opt_input = False
                                        while not opt_input:
                                            print("Votre choix est incorrecte, veillez en effectuer un nouveau.\n")
                                            opt_input = input("Quel est votre choix: ")
                                            if opt_input in ('1', '2', 'exit'):
                                                opt_input = True

                            elif choice == '3':
                                # Status ---> OK
                                print('\n1. Configurer les politiques du firewall via un fichier Excel\n')
                                print('2. Récupérer les politiques du firewall via un fichier Excel\n')

                                input_value = input(f"{'*'*10} Veillez sélectionner une option: ")
                                if input_value == '1':
                                    net_connect.send_config_set(fortinet.create_firewall_policy_via_excel_file())
                                    print('\n')

                                elif input_value == '2':
                                    api_admin_is_created_or_not = net_connect.send_config_set(['show syst api-user | grep -f api-admin'])
                                    result = fortinet.search_api_admin(api_admin_is_created_or_not)
                                                                                    
                                    if result == False:
                                        # Création de l'administrateur REST API "api-admin"
                                        conf_create_api_admin_profile = fortinet.create_api_admin()
                                        net_connect.send_config_set(conf_create_api_admin_profile)

                                    # Générer le token puis l'extraire à travers "response" et le passer à l'API                           
                                    response = net_connect.send_config_set(fortinet.generate_token())
                                    fortinet.get_firewall_policy(fortinet.extract_token(response))
                                    print('\n')

                                elif input_value == 'exit':
                                    pass

                                else:
                                    opt_input = False
                                    while not opt_input:
                                        print("Votre choix est incorrecte, veillez en effectuer un nouveau.\n")
                                        opt_input = input("Quel est votre choix: ")
                                        if opt_input in ('1', '2', 'exit'):
                                            opt_input = True

                            elif choice == '4':
                                print('\n1. Configurer les routes statiques\n')
                                print('2. Configurer les routes dynamiques\n')

                            elif choice == '5':
                                pass

                            elif choice == '6':
                                pass

                            elif choice == '7':
                                # config_commands = fortinet.configure_ha_manually()
                                net_connect.send_config_set(fortinet.configure_ha_manually())

                                # net_connect.disconnect()

                                print(f"\n{'*'*10} Établissement de la connexion pour le HA {'*'*10}\n")
                                fortinet_to_connect = FortinetModule()
                                forti_to_connect_net_connect = Netmiko(**fortinet_to_connect.get_attr())
                                print(f"\n{'*'*15} Connexion établie {'*'*15}")

                                print(forti_to_connect_net_connect.send_config_set(fortinet_to_connect.configure_ha_manually()))
                                forti_to_connect_net_connect.disconnect()

                            elif choice == '8':
                                for key_command, config_command in fortinet.make_all_config().items():

                                    if key_command == 'config_ha_secondary_device':
                                        print(f"\n{'*'*10} Connexion à l'équipement secondaire {'*'*10}\n")
                                        fortinet_to_connect = FortinetModule()
                                        forti_to_connect_net_connect = Netmiko(**fortinet_to_connect.get_attr())
                                        print(f"\n{'*'*15} Connexion établie {'*'*15}")

                                        print(f"\n{'*'*10} Configuration du HA en cours{'*'*10}")
                                        forti_to_connect_net_connect.send_config_set(config_command)
                                        print(f"\n{'*'*10} Configuration du HA effectuée{'*'*10}\n")

                                        # forti_to_connect_net_connect.disconnect()
                                    else:
                                        print(net_connect.send_config_set(config_command))
                                        print('\n')

                            elif choice == '9':
                                api_admin_is_created_or_not = net_connect.send_config_set(['show syst api-user | grep -f api-admin'])
                                result = fortinet.search_api_admin(api_admin_is_created_or_not)

                                if result == False:
                                # Création de l'administrateur REST API "api-admin"
                                    conf_create_api_admin_profile = fortinet.create_api_admin()
                                    net_connect.send_config_set(conf_create_api_admin_profile)

                                response = net_connect.send_config_set(fortinet.generate_token())
                                fortinet.get_all_config(fortinet.extract_token(response))

                            elif choice == 'exit':
                                into_loop = False
                                print('\n')

                            else:
                                print('Votre sélection est incorrecte, veillez en effectuer une autre!\n')
                    
                    elif select == 'exit':
                        run_sub_routine = False
                        print('\n')

                    else:
                        print('\n')
                        print("Votre selection est incorrecte, veillez en effectuer une autre.\n")

                net_connect.disconnect()
            
            elif choice == '2':
                print('\n')
                palo_alto = PaloAltoModule()
                print('\n')

                try:
                    print(f"{'*'*50} Connection à l'équipement {'*'*50}\n")
                    net_connect = Netmiko(**palo_alto.get_attr())
                    print(f"{'*'*58} Connection effectuée {'*'*58}\n")

                except Exception as e:
                    print(f"Erreur : {str(e)}")
                    print('\n')
                    break
                run_sub_routine = True
                while run_sub_routine:
                    
                    print(f"{'*'*48} Veillez selectionner une configuration {'*'*48}\n")
                    print('1. Configuration des paramètres généraux\n')
                    print('2. Configuration des paramètres avancés\n')

                    select = input(f"{'*'*10} Veillez effectuer votre sélection: ")

                    print('\n')
                    if select == '1':
                        into_loop = True
                        while into_loop:
                            print(f"{'*'*48} Veillez effectuer une sélection {'*'*48}\n")
                    
                    elif select == '2':
                        into_loop = True
                        while into_loop:

                            print(f"{'*'*48} Veillez effectuer une sélection {'*'*48}\n")
                            print('\n1. Interfaces\n')
                            # print('')
                            # print('')
                            print('4. Rétranscrire les configurations d\'un autre équipement\n')

                            choice = input(f"{'*'*10} Veillez effectuer une sélection: ")
                            if choice == '1':
                                enter=True
                                while enter:
                                    print("\n1. Configurer les interfaces\n")
                                    print("2. Récupérer la configuration des interfaces via un fichier Excel\n")

                                    input_value = input(f"{'*'*10} Veillez sélectionner une option: ")
                                    if input_value == '1':
                                        pass

                                    elif input_value == '2':
                                        pass

                            elif choice == 'exit':
                                into_loop = False
                                print('\n')

                            elif choice == '4':
                                for config_command in palo_alto.make_all_config().values():
                                    net_connect.send_config_set(config_command)

                net_connect.disconnect()
                
            elif choice == '3':
                pass

            elif choice == '4':
                pass

            else:
                break

        elif inp == 'exit':
            run_program = False
            print('\n')
            print(f"{'*'*65} Sortie du programme {'*'*65}")
            break

        else:
            choice_input = False
            while not choice_input:
                print("Votre choix est incorrecte, veillez en effectuer un nouveau.\n")
                inp = input("Quel est votre choix: ")
                if inp in ('1', '2', '3', 'exit'):
                    choice_input = True