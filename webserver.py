#!/usr/bin/env python
import cgi
import cgitb
import math

IP = '127.0.0.1'
buffer_size = 4000


def send_and_wait_for_socket(port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((IP, port))
		s.send(packet)

		while True:
			p = s.recv(buffer_size)

			if not p:
				break
			else:
				print lerPacote # todo : if checksum blablabla
	finally:
		s.close()

def lerPacote(p): #Fazer a leitura de cada parte do pacote
    Version =  p[0:4]
    IHL = p[4:8]
    TOS = p[8:16]
    Lenght = p[16:32]
    FragID = p[32:48]
    Flags = p[48:51]
    FragOffset = p[51:64]
    TTL = p[64:72]
    Protocol = p[72:80]
    HeaderChecksum = p[80:96]
    SourceAddr = p[96:128]
    DestinationAddr = p[128:160]
    Options = p[160:]



def montaPacote(cmd, Options='0'): # Montar o pacote juntando cada parte

    Version = '0010'
    IHL = '0101'
    Length = '0000000000000000'
    TOS = '00000000'
    FragID = '0000000000000000'
    Flags = '000'
    FragOffset = '0000000000000'
    TTL = '00001111'
    Protocol = cmd
    HeaderChecksum = '0000000000000000' #funcao_crc16

    # transformando um endereco de base 10 para base 2
    ip_bin = IP.split(".")
    for i in range(len(ip_bin)):
        ip_bin[i] = (bin(int(ip_bin[i]))) [2:].rjust(8, '0')

    SourceAddr = ''.join(ip_bin) # endereco em binario
    DestinationAddr = ''.join(ip_bin) # endereco em binario

    tamPacote = len(Version + IHL + TOS + Length + FragID + Flags + FragOffset + TTL + Protocol + HeaderChecksum \
    + SourceAddr + DestinationAddr + Options)

    word32 = int(math.ceil(float(tamPacote) / 32.0))
    Length = ''.join(bin(word32 * 32)) [2:].rjust(16, '0')


    p = (Version + IHL + TOS + Length + FragID  + Flags + FragOffset + TTL + Protocol + HeaderChecksum \
    + SourceAddr + DestinationAddr + Options)

    return p



cgitb.enable()    

print("Content-Type: text/html;charset=utf-8\r\n\r\n")
print("Hello World!</br>")

form = cgi.FieldStorage()
print(form)

packet_list_maq1 = []
packet_list_maq2 = []
packet_list_maq3 = []

try:
	if form["maq1_ps"].value == 'ps':
		print ("</br> maq 1 ps entrou")
		packet_list_maq1.append(montaPacote('0001'))
except Exception:
	pass

try:
	if form["maq1_df"].value == 'df':
		print ("</br> maq 1 df entrou")
		packet_list_maq1.append(montaPacote('0010'))
except Exception:
	pass

try:
	if form["maq1_finger"] == 'finger':
		packet_list_maq1.push(montaPacote('0011'))
except Exception:
	pass


try:
	if form["maq1_uptime"] == 'uptime':
		packet_list_maq1.push(montaPacote('0100'))
except Exception:
	pass

try:
	if form["maq2_ps"] == 'ps':
		packet_list_maq2.push(montaPacote('0001'))
except Exception:
	pass

try:
	if form["maq2_df"] == 'df':
		packet_list_maq2.push(montaPacote('0010'))
except Exception:
	pass

try:
	if form["maq2_finger"] == 'finger':
		packet_list_maq2.push(montaPacote('0011'))
except Exception:
	pass

try:
	if form["maq2_uptime"] == 'uptime':
		packet_list_maq2.push(montaPacote('0100'))
except Exception:
	pass

try:
	if form["maq3_ps"] == 'ps':
		packet_list_maq3.push(montaPacote('0001'))
except Exception:
	pass

try: 
	if form["maq3_df"] == 'df':
		packet_list_maq3.push(montaPacote('0010'))
except Exception:
	pass

try:
	if form["maq3_finger"] == 'finger':
		packet_list_maq3.push(montaPacote('0011'))
except Exception:
	pass

try:
	if form["maq3_uptime"] == 'uptime':
		packet_list_maq3.push(montaPacote('0100'))
except Exception:
	pass


print ("</br>packet_list_maq1: " + str(packet_list_maq1))
print ("</br>packet_list_maq2: " + str(packet_list_maq2))
print ("</br>packet_list_maq3: " + str(packet_list_maq3))

# for que vai fazer as conexoes socket
for packet in packet_list_maq1:
	send_and_wait_for_socket(9001)

for packet in packet_list_maq2:
	send_and_wait_for_socket(9002)

for packet in packet_list_maq3:
	send_and_wait_for_socket(9003)

