import napalm
import re
import json

# Входные данные для авторизации на сетевом оборудование
auth_user = {
    'login': 'admin',
    'password': 'admin'
}

def get_data_cisco(ip_address, login, password):
    # Select a software the network a device - Выбераем ПО для взаимодействие с устройством
    ios_device = napalm.get_network_driver('ios')
    cisco = ios_device(ip_address, login, password)
    # Открыть соединение на сетевом устройстве - Open connect at network device
    cisco.open()
    # Все интерфейсы на сетевом оборудование - All interface at the network device
    list_interface = cisco.get_facts()['interface_list']
    # Кол-во активных портов - Count active a ports
    count_up_port = 0
    # Кол-во выключеных портов - Count down a ports
    count_down_port = 0

    # Узнаем общее кол-во портов на устройстве
    for list in list_interface:
        # Находим все что связано с интерфейсом
        result = re.findall(r'Ethernet\d/', list)
        # Если мы находим интерфейс то выполним условие
        if len(result) > 0:
            # Выполним условие если порт активный
            if cisco.get_interfaces()[list]['is_up'] == True:
                # Подсчет активных портов
                count_up_port = count_up_port + 1
            # Выполним условие если порт не активный
            elif cisco.get_interfaces()[list]['is_up'] == False:
                # Подсчет не активных портов
                count_down_port = count_down_port + 1

    listing = ['show interface transceiver properties']
    # Кол-во встроенных портов
    count_media_type_port = 0
    # Кол-во модульных портов
    count_media_sfp_port = 0
    result = cisco.cli(listing)
    # Отправляем запрос для того чтобы получить Media port
    list_array = result['show interface transceiver properties'].split('\n')
    for list in list_array:
        # Находим все что связано с 'Media Type'
        temp = re.search(r'Media\sType.*', list)
        # Если нашли 'Media Type' тогда выполним условие
        if temp:
            try:
                # Находим все что связано с встроенными портами
                result = re.search(r'10/100/1000.*', temp[0].split(':')[1])
                if result:
                    # Введем подсчет встроенных портов
                    count_media_type_port = count_media_type_port + 1
                elif not result:
                    # Введем подсчет sfp портов
                    count_media_sfp_port = count_media_sfp_port + 1
            except IndexError:
                pass

    information_device = {'ip_address': ip_address, 'hostname': cisco.get_facts()['hostname'],
                          'model': cisco.get_facts()['model'], 'vendor': cisco.get_facts()['vendor'],
                          'port_rj': count_media_type_port, 'port_sfp': count_media_sfp_port,
                          'location': cisco.get_snmp_information()['location'], 'count_port': (count_media_type_port+count_media_sfp_port),
                          'count_port_up': count_up_port, 'count_port_down': count_down_port}

    cisco.close()
    return information_device


def program():
    data = {}

    # Читаем json файл с данными
    with open('ipaddress.json') as file:
        templates = json.load(file)

    for key in templates:
        for ip in templates[key]:
            result = get_data_cisco(ip, auth_user['login'], auth_user['password'])
            data[result['hostname']] = []
            data[result['hostname']].append({
                'IP-address': result['ip_address'],
                'Model device': result['model'],
                'Vendor': result['vendor'],
                'Port RJ45': result['port_rj'],
                'Port SFP': result['port_sfp'],
                'Location': result['location'],
                'Count port': result['count_port'],
                'Busy port': result['count_port_up'],
                'Free port': result['count_port_down']
            })
            print("ip:{0} | host:{1} | location:{2}".format(result['ip_address'], result['hostname'], result['location']))

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)

    print("Task win!")



if __name__ == '__main__':
     program()