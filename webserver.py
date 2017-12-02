#!/usr/bin/env python
import cgi
import cgitb
import math
import socket
from struct import *

IP = '127.0.0.1'
buffer_size = 4096


def send_and_wait_for_socket(port, packet):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#print("</br> socket recebeu,  s = " + s.getsockname())

		s.connect((IP, port))

		s.send(packet)

		while True:
			p = s.recv(buffer_size)
			#print("</br> dentro do while true,  p = " + str(p))
			if not p:
				break
			else:
				print lerPacote(p)
	except Exception as e:
		print (e)
	finally:
		s.close()

def lerPacote(p): #Fazer a leitura de cada parte do pacote
    pac_list = p.split("|||")
    cabecalho = unpack('!BBHHHBBHII', pac_list[0])
    soma_checksum = 0
    bytes_pack = unpack('!BBBBBBBBBBBBBBBBBBBB', pac_list[0])
    for i in range(len(bytes_pack)):
        if i not in (10,11):
            #print("</br>i="+str(i))
            #print ("</br>"+str(bytes_pack[i]))
            #print ("</br>soma_checksum anterior: " + str(soma_checksum))
            soma_checksum = soma_checksum ^ bytes_pack[i]
            #print ("</br>novo soma_checksum : " + str(soma_checksum))
        
    checksum = cabecalho[7]
    #print("</br> checksum="+str(checksum))
    if soma_checksum == checksum:
        return pac_list[1]
    else:
        return "Erro"


def montaPacote(cmd, opt): # Montar o pacote juntando cada parte

    soma_checksum = 0
    Version = '0010'
    IHL = '0101'
    soma_checksum = soma_checksum ^ int(Version+IHL,2)

    TOS = '00000000'

    tamPacote = 24
    bytes_tam = unpack('BB', pack('H', tamPacote))
    soma_checksum = soma_checksum ^ bytes_tam[0]
    soma_checksum = soma_checksum ^ bytes_tam[1]

    #Length = '0000000000000000'
    FragID = '0000000000000000'
    soma_checksum = soma_checksum ^ int(FragID[0:8], 2)
    soma_checksum = soma_checksum ^ int(FragID[8:16], 2)

    Flags = '000'
    FragOffset = '0000000000000'
    TTL = '00001111'
    soma_checksum = soma_checksum ^ int(TTL, 2)

    Protocol = cmd
    soma_checksum = soma_checksum ^ int(Protocol, 2)
    
    # transformando um endereco de base 10 para base 2
    ip_bin = IP.split(".")
    for i in range(len(ip_bin)):
        ip_bin[i] = (bin(int(ip_bin[i]))) [2:].rjust(8, '0')

    SourceAddr = ''.join(ip_bin) # endereco em binario
    soma_checksum = soma_checksum ^ int(SourceAddr[0:8],2)
    soma_checksum = soma_checksum ^ int(SourceAddr[8:16],2)
    soma_checksum = soma_checksum ^ int(SourceAddr[16:24],2)
    soma_checksum = soma_checksum ^ int(SourceAddr[24:32],2)

    DestinationAddr = ''.join(ip_bin) # endereco em binario
    soma_checksum = soma_checksum ^ int(DestinationAddr[0:8],2)
    soma_checksum = soma_checksum ^ int(DestinationAddr[8:16],2)
    soma_checksum = soma_checksum ^ int(DestinationAddr[16:24],2)
    soma_checksum = soma_checksum ^ int(DestinationAddr[24:32],2)


    bytes_opt = unpack('BBBB', pack('I', opt))
    
    soma_checksum = soma_checksum ^ bytes_opt[0]
    soma_checksum = soma_checksum ^ bytes_opt[1]
    soma_checksum = soma_checksum ^ bytes_opt[2]
    soma_checksum = soma_checksum ^ bytes_opt[3]

    pacote = pack('!BBHHHBBHIII',int(Version+IHL, 2) \
                     , int(TOS, 2) \
                     , tamPacote \
                     , int(FragID, 2) \
                     , int((Flags+FragOffset),2) \
                     , int(TTL, 2) \
                     , int(Protocol, 2) \
                     , soma_checksum \
                     , int(SourceAddr, 2) \
                     , int(DestinationAddr, 2) \
                     , int(opt))

    
    return pacote

def converteOption(s):
    if s == '':
        return 0
    if s == '-ef':
        return 1
    elif s == 'ax':
        return 2
    elif s == '-s':
        return 3
    elif s == '-l':
        return 4
    elif s == '-a':
        return 5
    elif s == '-h':
        return 6
    elif s == '-p':
        return 7
    elif s == '-V':
        return 8
    else:
    	return 0

cgitb.enable()    

print("Content-Type: text/html;charset=utf-8\r\n\r\n")
print("<pre>")

form = cgi.FieldStorage()


packet_list_maq1 = []
packet_list_maq2 = []
packet_list_maq3 = []

try:
	if form["maq1_ps"].value == 'ps':
		try:
			texto = form["maq1-ps"].value
		except KeyError:
			texto = ''
		packet_list_maq1.append(montaPacote('0001', \
		converteOption(texto)))
except KeyError:
	pass

try:
	if form["maq1_df"].value == 'df':
		try:
			texto = form["maq1-df"].value
		except KeyError:
			texto = ''
		packet_list_maq1.append(montaPacote('0010', \
		converteOption(texto)))
except KeyError:
	pass

try:
	if form["maq1_finger"].value == 'finger':
		try:
			texto = form["maq1-finger"].value
		except KeyError:
			texto = ''
		packet_list_maq1.append(montaPacote('0011', \
			converteOption(texto)))
except KeyError:
	pass


try:
	if form["maq1_uptime"].value == 'uptime':
		try:
			texto = form["maq1-uptime"].value
		except KeyError:
			texto = ''
		packet_list_maq1.append(montaPacote('0100', \
			converteOption(texto)))
except KeyError:
	pass

try:
	if form["maq2_ps"].value == 'ps':
		try:
			texto = form["maq2-ps"].value
		except KeyError:
			texto = ''
		packet_list_maq2.append(montaPacote('0001', \
			converteOption(texto)))
except KeyError:
	pass

try:
	if form["maq2_df"].value == 'df':
		try:
			texto = form["maq2-df"].value
		except KeyError:
			texto = ''
		packet_list_maq2.append(montaPacote('0010', \
			converteOption(texto)))
except KeyError:
	pass

try:
	if form["maq2_finger"].value == 'finger':
		try:
			texto = form["maq2-finger"].value
		except KeyError:
			texto = ''
		packet_list_maq2.append(montaPacote('0011', \
			converteOption(texto)))
except KeyError:
	pass

try:
	if form["maq2_uptime"].value == 'uptime':
		try:
			texto = form["maq2-uptime"].value
		except KeyError:
			texto = ''
		packet_list_maq2.append(montaPacote('0100', \
			converteOption(texto)))
except KeyError:
	pass

try:
	if form["maq3_ps"].value == 'ps':
		try:
			texto = form["maq3-ps"].value
		except KeyError:
			texto = ''
		packet_list_maq3.append(montaPacote('0001', \
			converteOption(texto)))
except KeyError:
	pass

try: 
	if form["maq3_df"].value == 'df':
		try:
			texto = form["maq3-df"].value
		except KeyError:
			texto = ''
		packet_list_maq3.append(montaPacote('0010', \
			converteOption(texto)))
except KeyError:
	pass

try:
	if form["maq3_finger"].value == 'finger':
		try:
			texto = form["maq3-finger"].value
		except KeyError:
			texto = ''
		packet_list_maq3.append(montaPacote('0011', \
			converteOption(texto)))
except KeyError:
	pass

try:
	if form["maq3_uptime"].value == 'uptime':
		try:
			texto = form["maq3-uptime"].value
		except KeyError:
			texto = ''
		packet_list_maq3.append(montaPacote('0100', \
			converteOption(texto)))
except KeyError:
	pass


# for que vai fazer as conexoes socket
for packet in packet_list_maq1:
	send_and_wait_for_socket(9001, packet)

for packet in packet_list_maq2:
	send_and_wait_for_socket(9002, packet)

for packet in packet_list_maq3:
	send_and_wait_for_socket(9003, packet)
