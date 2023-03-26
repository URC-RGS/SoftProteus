from socket import *
import sys

host = 'localhost'
port = 777
addr = (host,port)

udp_socket = socket(AF_INET, SOCK_DGRAM)


data = input('write to server: ')
if not data : 
    udp_socket.close() 
    sys.exit(1)

#encode - перекодирует введенные данные в байты, decode - обратно
data = str.encode(data)
udp_socket.sendto(data, addr)
data = bytes.decode(data)
data = udp_socket.recvfrom(1024)
print(data)


udp_socket.close()


class RovClient:
    def __init__(self, server_config: dict):
        '''Класс ответсвенный за связь с постом'''
        self.logi = server_config['logger']
        
        if server_config['local_host_start']:
            self.host = server_config['local_host']
            self.port = server_config['port_local_host']

        else:
            self.host = server_config['real_host']
            self.port = server_config['port_real_host']

        self.check_connect = True      

        # Настройки клиента 
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM,)
        self.client.connect((self.host, self.port))

    def receiver_data(self):
        #Прием информации с поста управления 
        if self.check_connect:
            data = self.client.recv(512).decode('utf-8')

            if len(data) == 0:
                self.check_connect = False
                self.logi.info('Rov disconect')
                self.client.close()
                return None

            data = dict(literal_eval(str(data)))
            self.logi.debug(f'Receiver data : {str(data)}')
            return data

    def send_data(self, data:dict):
        #Функция для  отправки пакетов на пульт 
        if self.check_connect:
            data['time'] = str(datetime.now())

            self.logi.debug(f'Send data : {str(data)}')

            data_output = str(data).encode("utf-8")
            self.client.send(data_output)
