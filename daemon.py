import socket
import sys
import thread
import math
import subprocess

BUFFER_SIZE = 4096
IP = 127.0.0.1
if len(sys.argv) < 2:
  print "Porta não encontrada"
else:
    PORT = int(sys.argv[1])

def lerPacote(p):
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

    return Protocol, TTL

def montaPacote(cmd, t):
    Version =  '0010'
    IHL = '0101'
    TOS = '00000000'
    Lenght = '0000000000000000'
    FragID = '0000000000000000'
    Flags = '111'
    FragOffset = '0000000000000'
    TTL = p[64:72]
    Protocol = '00000000'
    HeaderChecksum = '0000000000000000'
    SourceAddr = p[96:128]
    DestinationAddr = p[128:160]
    Options = p[160:]


def execute(cmd):
        if(cmd == 1):
            return subprocess.check_output(['ps'])
        elif(cmd == 2):
            return subprocess.check_output(['df'])
        elif(cmd == 3):
            return subprocess.check_output(['finger'])
        else:
            return subprocess.check_output(['uptime'])
