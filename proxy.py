import socket, sys
from thread import *


LISTEN_PORT = 10080

MAX_CONN = 5
BUF_SIZE = 4096

TARGET_HOST = 'alpha-cab.cloud.toast.com'
TARGET_PORT = 80


def init():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', LISTEN_PORT))
        s.listen(MAX_CONN)
    except Exception as e:
        print e
        sys.exit(2)

    while 1:
        try:
            conn, addr = s.accept()
            data = conn.recv(BUF_SIZE)
            start_new_thread(deliver, (conm, data, addr))
        except KeyboardInterrupt:
            s.close()
            sys.exit(1)

    s.close()


def deliver(conn, data, addr):
    try:
        first = data.split('\n')[0]
        url = first.split(' ')[1]

        http_pos = url.find('://')
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos+3):]
        port_pos = temp.find(':')

        webserver_pos = temp.find('/')
        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver = ''
        port = -1
        if port_pos==-1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_post-port_pos-1])
            webserver = temp[:port_pos]

        proxy_server(webserver, port, conn, addr, data)
    except Exception:
        pass


def proxy_server(webserver, prot, conn, data, addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(data)

        while 1:
            reply = s.recv(BUF_SIZE)

            if (len(reply) > 0):
                conn.send(reply)

                dar = float(len(reply))
                dar = float(dar / 1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)
                print '[*] Request Done: %s -> %s <=' % (str(addr[9]), str(dar))
            else:
                break

            s.close()
            conn.close()
    except socket.error, (value, message):
        s.close()
        conn.close()
        sys.exit()

init()
