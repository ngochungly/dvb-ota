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

        print('\ncapture stream on IP', udp_ip, 'port', port)
        # capture from "udp_ip" stream
        mreq = struct.pack(">4sl", socket.inet_aton(udp_ip), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        print('loop...')
        while True:
            data = sock.recv(1316)
            f.write(data)
            print(len(data), 'bytes')
            if time.time() > timeout:
                print('timeout.')
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
mcast_ip = '229.10.10.1'
port = 5001
file_path = 'capture.ts'
seconds = 30

TSCapture(mcast_ip, port, file_path, seconds)