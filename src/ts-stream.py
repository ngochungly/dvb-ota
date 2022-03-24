#import datetime
import os
import socket
import time

# delay
def tsdelay(begin_time):
    delay = 0.00052632
    
    while True:
        end_time = time.perf_counter()
        delta_time = end_time - begin_time
        if delta_time >= delay:
            break

file_path = 'C:/Users/ADMIN/Desktop/Le travail/SCTV/DVB-T2/OTA/ts-bin/ota.ts'

MCAST_GRP = '224.1.1.25'
MCAST_PORT = 5000

HOST = '10.192.34.114'
PORT = 10253

# regarding socket.IP_MULTICAST_TTL
# ---------------------------------
# for all packets sent, after seven hops on the network the packet will not 
# be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
MULTICAST_TTL = 7

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.bind((HOST, PORT))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

try:
    f_size = os.path.getsize(file_path)
    f = open(file_path, 'rb')
    print('reading file...')
    print('{0} bytes.'.format(f_size))

    n_byte = 0
    n_pkt = 0
    #t_interval = 5

    print('\nsending data...')
    while True:
        data = f.read(1316)     # 7 TS packets, 188 bytes/packet
        while data:
            send_last_time = time.perf_counter()
            sock.sendto(data, (MCAST_GRP, MCAST_PORT))
            
            #n_byte += len(data)
            #n_pkt += 1
            data = f.read(1316)     # 7 TS packets, 188 bytes/packet
            tsdelay(send_last_time)
            #time.sleep(0.004)
        f.seek(0)
        #break
    
    
    # print('{0} bytes sent.'.format(n_byte))
    # print('{0} packets sent.'.format(n_pkt))
    #print('{0} total seconds.'.format(delta_time.total_seconds()))
    
    print('Done.')

except Exception as e:
    print('\nException: {0}\nArguments: {1}'.format(type(e).__name__, e.args))

finally:
    sock.close()
    f.close()
