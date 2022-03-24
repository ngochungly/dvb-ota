import datetime
import os
import socket
import struct
import time

#-----------------------------------------------
def TSParse(file_in, pid_list, file_out):

    try:

        # 
        f_in = open(file_in, 'rb')
        f_out = open(file_out, 'wb')
        print('create file... done.')

        print('\nreading file', file_in)
        pid_list_in_file = []
        null_int = int.from_bytes(b'\x1F\xFF', 'big')
        # 
        while True:
            data = f_in.read(188)
            while data:
                p_byte = data[1:3]
                p_int = int.from_bytes(p_byte, 'big')
                pid_int = p_int & null_int
                pid = pid_int.to_bytes(2, 'big')

                pid_str = '0x' + pid.hex().upper()
                if pid_str not in pid_list_in_file:
                    pid_list_in_file.append(pid_str)

                if pid in pid_list:
                    f_out.write(data)
                data = f_in.read(188)
            break

    except Exception as e:
        print('\nException: {0}\nArguments: {1}'.format(type(e).__name__, e.args))

    except KeyboardInterrupt as e:
        print('\nException: {0}\nArguments: {1}'.format(type(e).__name__, e.args))

    finally:
        f_in.close()
        f_out.close()

        f_size = os.path.getsize(file_out)
        pid_list_in_file.sort()
        print('\n{0} bytes parsed.'.format(f_size))
        print('\nPID list in file:', pid_list_in_file)
#-----------------------------------------------

# test
file_in = 'C:/Users/NgocHung/Desktop/Work/DVB-T2/CAS/Gospell/File capture after mux/capture_30s_cas_scramble.ts'
pid_list = [ b'\x00\x4E', b'\x00\x54', ]
file_out = 'C:/Users/NgocHung/Desktop/Work/DVB-T2/CAS/Gospell/File capture after mux/output_cas_scr_S5.ts'

TSParse(file_in, pid_list, file_out)