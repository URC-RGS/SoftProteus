#Модуль socket для сетевого программирования
from socket import *

#данные сервера
host = 'localhost'
port = 777
addr = (host,port)

#socket - функция создания сокета 
#первый параметр socket_family может быть AF_INET или AF_UNIX
#второй параметр socket_type может быть SOCK_STREAM(для TCP) или SOCK_DGRAM(для UDP)
udp_socket = socket(AF_INET, SOCK_DGRAM)
#bind - связывает адрес и порт с сокетом
udp_socket.bind(addr)

#Бесконечный цикл работы программы
while True:
    
    #Если мы захотели выйти из программы
    question = input('Do you want to quit? y\\n: ')
    if question == 'y': break
    
    print('wait data...')
    
    #recvfrom - получает UDP сообщения
    conn, addr = udp_socket.recvfrom(1024)
    print('client addr: ', addr)
    print(conn)
    
    #sendto - передача сообщения UDP
    udp_socket.sendto(b'message received by the server', addr)
    
  
udp_socket.close()


class RovServer:
    def __init__(self, server_config: dict):
        '''Класс отвечающий за создание сервера'''

        self.logi = server_config['logger']
        
        # выбор режима: Отладка\Запуск на реальном аппарате
        if server_config['local_host_start']:
            self.host = server_config['local_host']
            self.port = server_config['port_local_host']
        else:
            self.host = server_config['real_host']
            self.port = server_config['port_real_host']
            
            
        # настройка сервера
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM,)
        self.server.bind((self.host, self.port))
        self.logi.info('ROV waiting for connection')
        self.server.listen(1)
        self.user_socket, self.address = self.server.accept()
        self.check_connect = True

        self.logi.info(f'ROV Connected {self.user_socket}')

    def receiver_data(self):
        #Прием информации с аппарата
        if self.check_connect:
            data = self.user_socket.recv(512)
            if len(data) == 0:
                self.server.close()
                self.check_connect = False
                self.logi.info(f'ROV disconnection {self.user_socket}')
                return None

            data = dict(literal_eval(str(data.decode('utf-8'))))
            self.logi.debug(f'Receiver data : {str(data)}')
            return data

    def send_data(self, data: dict):
        #Отправка массива на аппарат
        if self.check_connect:
            self.user_socket.send(str(data).encode('utf-8'))
            self.logi.debug(f'Send data : {str(data)}')