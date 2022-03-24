import datetime
import os
import socket
import struct
import time

#-----------------------------------------------
def TSCapture(udp_ip, port, file_path, duration):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # listen on "port"
    sock.bind(('', port))

    try:
        timeout = time.time() + duration      # "duration" seconds

        # record to "file_path"
        f = open(file_path, 'wb')
        print('create file... done.')

        print('\ncapturing stream...')
        # capture from "udp_ip" stream
        mreq = struct.pack(">4sl", socket.inet_aton(udp_ip), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while True:
            data = sock.recv(1316)
            f.write(data)
            if time.time() > timeout:
                break

    except Exception as e:
        print('\nException: {0}\nArguments: {1}'.format(type(e).__name__, e.args))

    except KeyboardInterrupt as e:
        print('\nException: {0}\nArguments: {1}'.format(type(e).__name__, e.args))

    finally:
        sock.close()
        f.close()

        f_size = os.path.getsize(file_path)
        print('\n{0} bytes captured.'.format(f_size))
        print('Done.')
#-----------------------------------------------

# test
mcast_ip = '224.1.1.25'
port = 5000
file_path = 'C:/Users/NgocHung/Desktop/Work/DVB-T2/OTA/capture.ts'
seconds = 20

TSCapture(mcast_ip, port, file_path, seconds)