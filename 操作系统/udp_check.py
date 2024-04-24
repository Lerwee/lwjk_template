#!/usr/bin/python
#-* encoding=utf-8 *-
import socket
import threading
import time
import struct
import sys
if sys.version_info[0] < 3: # 判断python版本，加载对应“队列”模块
    from Queue import Queue
else:
    from queue import Queue
queue = Queue()
def udp_sender(ip,port):
    try:
        ADDR = (ip,port)
        sock_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        if sys.version_info[0] < 3: # 判断python版本，定义发送内容
            sock_udp.sendto("abcd...",ADDR)
        else:
            sock_udp.sendto(b'\x61\x62\x63\x64\x2e\x2e\x2e',ADDR)
        sock_udp.close()
    except:
        pass
def icmp_receiver(ip,port):
    icmp = socket.getprotobyname("icmp")
    try:
        sock_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error as e:
        errno, msg = e.args
        if errno == 1:
            # Operation not permitted
            msg = msg + (
            " - 请注意，ICMP消息只能从以root身份运行的进程中发送。"
            )
            raise socket.error(msg)
        raise # 抛出原始错误
    sock_icmp.settimeout(2)
    try:
        recPacket,addr = sock_icmp.recvfrom(64)
    except Exception as e:
        # print(e)
        queue.put(True)
        return
    icmpHeader = recPacket[20:28]
    if sys.version_info[0] < 3: # 判断python版本，转义字符recPacket为16进制编码
        icmpPort = int(recPacket.encode('hex')[100:104],16)
    else:
        import binascii
        icmpPort = int(binascii.hexlify(recPacket)[100:104], 16)

    head_type, code, checksum, packetID, sequence = struct.unpack(
    "bbHHh", icmpHeader
    )
    sock_icmp.close()
    # print(head_type, code, checksum, packetID, sequence,addr)
    if code == 3 and icmpPort == port and addr[0] == ip:
        queue.put(False)
        return
    else:
        queue.put('unknown')
        return
def checker_udp(ip,port):
    thread_udp = threading.Thread(target=udp_sender,args=(ip,port))
    thread_icmp = threading.Thread(target=icmp_receiver,args=(ip,port))
    thread_udp.daemon= True
    thread_icmp.daemon = True
    thread_icmp.start()
    # time.sleep(0.1)
    thread_udp.start()
    thread_icmp.join()
    thread_udp.join()
    try:
        return queue.get(False)
    except:
        return False
if __name__ == '__main__':
    import sys
    ip,port = sys.argv[1],int(sys.argv[2])
    ip = socket.gethostbyname(ip) # 域名转IP
    for_num = 2
    count = []
    total_time = 0
    for i in range(for_num): # 重复执行检查，提高准确率
        start_at = time.time()
        result = checker_udp(ip,port)
        # print(result)
        if result == True:
            result = 1
        elif result == 'unknown':
            result = 2
        elif result == False:
            result = 0
        time_used = time.time() - start_at
        total_time += time_used
        count.append(result)
    # print(count)
    if 0 in count:
        print ('{"status":0}')
    elif 1 in count:
        run_time = total_time / for_num
        print ('{"status":1,"runtime":%s}'% run_time)
    else:
        print ('{"status":2}')
