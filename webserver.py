#!/usr/bin/env python
import cgi
import cgitb

IP = '127.0.0.1'

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

    Version =  '0010'
    IHL = '0101'
    TOS = '00000000'
    FragID = '0000000000000000'
    Flags = '000'
    FragOffset = '0000000000000'
    TTL = '00001111'
    Protocol = cmd
    HeaderChecksum = funcao_crc16

    # transformando um endereço de base 10 para base 2
    ip_bin = IP.split(".")
    for i in range(len(ip_bin)):
        ip_bin[i] = (bin(int(ip_bin[i]))) [2:].rjust(8, '0')

    SourceAddr = ''.join(ip_bin) # endereço em binario
    DestinationAddr = ''.join(ip_bin) # endereço em binario


    tamPacote = len(Version + IHL + TOS + Length + FragID + Flags + FragOffset + TTL + Protocol + HeaderChecksum \
    + SourceAddr + DestinationAddr + Dat)

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

if form["maq1_ps"] == 'ps':
	packet_list_maq1.push(montaPacote('0001'))


if form["maq1_df"] == 'df':
	packet_list_maq1.push(montaPacote('0010'))


if form["maq1_finger"] == 'finger':
	packet_list_maq1.push(montaPacote('0011'))


if form["maq1_uptime"] == 'uptime':
	packet_list_maq1.push(montaPacote('0100'))


if form["maq2_ps"] == 'ps':
	packet_list_maq2.push(montaPacote('0001'))


if form["maq2_df"] == 'df':
	packet_list_maq2.push(montaPacote('0010'))


if form["maq2_finger"] == 'finger':
	packet_list_maq2.push(montaPacote('0011'))


if form["maq2_uptime"] == 'uptime':
	packet_list_maq2.push(montaPacote('0100'))


if form["maq3_ps"] == 'ps':
	packet_list_maq3.push(montaPacote('0001'))


if form["maq3_df"] == 'df':
	packet_list_maq3.push(montaPacote('0010'))


if form["maq3_finger"] == 'finger':
	packet_list_maq3.push(montaPacote('0011'))


if form["maq3_uptime"] == 'uptime':
	packet_list_maq3.push(montaPacote('0100'))


# for que vai fazer as conexoes socket