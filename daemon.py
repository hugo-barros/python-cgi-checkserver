import socket
import sys
import thread
import math
import subprocess
from struct import *


'''

lista de options - codigo
se quiser adicionar mais um codigo eh necessario colocar dentro do "if op" no execute aqui e tambem 
no webserver.py (codificador e decodificador)

sem options = 0
-ef = 1
ax = 2
-s = 3
-l = 4
-a = 5
-h = 6
-p = 7
-V = 8

'''

BUFFER_SIZE = 4096
IP = '127.0.0.1'
PORT = 9001
if len(sys.argv) < 2:
  print ("Porta nao encontrada")
else:
    PORT = int(sys.argv[1])

def execute(cmd, op): # Execucao dos comandos
    #op eh int
    cmd_list = []

    if(cmd == 1):
        cmd_list.append('ps')
        
    elif(cmd == 2):
        cmd_list.append('df')
        
    elif(cmd == 3):
        cmd_list.append('finger')
        
    elif(cmd == 4):
        cmd_list.append('uptime')
    else:
        return 'Erro'

    if op == 1:
        cmd_list.append('-ef')
    elif op == 2:
        cmd_list.append('ax')
    elif op == 3:
        cmd_list.append('-s')
    elif op == 4:
        cmd_list.append('-l')
    elif op == 5:
        cmd_list.append('-a')
    elif op == 6:
        cmd_list.append('-h')
    elif op == 7:
        cmd_list.append('-p')
    elif op == 8:
        cmd_list.append('-V')
    

    return subprocess.check_output(cmd_list)

def lerPacote(p): #Fazer a leitura de cada parte do pacote
    print("Lendo pacote data")
    cabecalho = unpack('!BBHHHBBHIII', p)
    soma_checksum = 0
    bytes_pack = unpack('!BBBBBBBBBBBBBBBBBBBBBBBB', p)
    # dividindo o pacote em bytes para conseguirmos checar o checksum
    # utilizamos da operacao XOR (como explicado em aula) para fazer o processo
    # nao "somamos" o byte 10 e 11 pois eles sao o checksum
    for i in range(len(bytes_pack)):
        if i not in (10,11):
            print(str(i))
            print (bytes_pack[i])
            print ("soma_checksum anterior: " + str(soma_checksum))
            soma_checksum = soma_checksum ^ bytes_pack[i]
            print ("novo soma_checksum : " + str(soma_checksum))
        
    checksum = cabecalho[7]
    print(cabecalho)
    print("SomaChecksum = " + str(soma_checksum))
    print("Checksum = " + str(checksum))
    Protocol = cabecalho[6]
    TTL = cabecalho[5]
    opt = cabecalho[-1]

    if soma_checksum == checksum:
        return Protocol, TTL, opt
    else:
        return "Erro", TTL, opt

def montaPacote(cmd, t, opt): # Montar o pacote juntando cada parte
    if t > 1:
        soma_checksum = 0
        # 1st byte:
        Version =  '0010'
        IHL = '0101'
        soma_checksum = soma_checksum ^ int(Version+IHL,2)

        TOS = '00000000'
        soma_checksum = soma_checksum ^ int(TOS, 2)

        Dat = execute(cmd, opt) # devolve string de resultado do comando
        print("dat == " + Dat)

        tamPacote = 20 + len(Dat) # tamanho contado em bytes
        bytes_tam = unpack('!BB', pack('H', tamPacote))
        soma_checksum = soma_checksum ^ bytes_tam[0]
        soma_checksum = soma_checksum ^ bytes_tam[1]


        FragID = '0000000000000000'
        soma_checksum = soma_checksum ^ int(FragID[0:8], 2)
        soma_checksum = soma_checksum ^ int(FragID[8:16], 2)

        Flags = '111'
        FragOffset = '0000000000000'
        soma_checksum = soma_checksum ^ int((Flags+FragOffset)[0:8],2)
        soma_checksum = soma_checksum ^ int((Flags+FragOffset)[8:16],2)

        TTL = t-1 #parametro t eh um int 
        soma_checksum = soma_checksum ^ TTL

        Protocol = '00000000'


        t = IP.split(".")
        for i in range(len(t)):
            t[i] = (bin(int(t[i]))) [2:].rjust(8, '0')

        SourceAddr = ''.join(t)
        soma_checksum = soma_checksum ^ int(SourceAddr[0:8],2)
        soma_checksum = soma_checksum ^ int(SourceAddr[8:16],2)
        soma_checksum = soma_checksum ^ int(SourceAddr[16:24],2)
        soma_checksum = soma_checksum ^ int(SourceAddr[24:32],2)

        DestinationAddr = ''.join(t)

        soma_checksum = soma_checksum ^ int(DestinationAddr[0:8],2)
        soma_checksum = soma_checksum ^ int(DestinationAddr[8:16],2)
        soma_checksum = soma_checksum ^ int(DestinationAddr[16:24],2)
        soma_checksum = soma_checksum ^ int(DestinationAddr[24:32],2)


        
        print ("checksum: " + str(soma_checksum))
        cabecalho = pack('!BBHHHBBHII', int(Version+IHL, 2) \
                                     , int(TOS, 2) \
                                     , tamPacote
                                     , int(FragID, 2) \
                                     , int((Flags+FragOffset),2) \
                                     , TTL \
                                     , int(Protocol, 2) \
                                     , soma_checksum \
                                     , int(SourceAddr, 2) \
                                     , int(DestinationAddr, 2)
                                     )
        return cabecalho + "|||" + Dat # ||| para conseguir dar o split mais tarde, porque 
                                        # o socket soh pode enviar uma string ou buffer
                                        # optamos por enviar uma string no formato:
                                        # "Cabecalho|||Dados"


def func(connection):
    data = connection.recv(BUFFER_SIZE)
    print("data: " + str(data))
    if data:
        comando, aux_t, opt = lerPacote(data)
        if comando != 'Erro':
            pacote = montaPacote(comando, aux_t, opt)
            print ("OK")
            connection.send(pacote)
        else:
            print ("ERROR")

    connection.close()

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind((IP, PORT))
c.listen(50)

while True:
        connect, addr = c.accept()
        print 'Address = ', addr
        thread.start_new_thread(func, (connect,))
