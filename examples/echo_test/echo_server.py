# Echo server program, stolen from https://docs.python.org/2/library/socket.html, and add CmdHandler
import socket
import subprocess

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

class CmdHandler(object):
    def __init__(self, conn, cmd):
        self._conn = conn
        self._cmd = cmd.strip()

    def __call__(self):
        try:
            return getattr(self, self._cmd)()
        except AttributeError:
            return self._send(self._cmd)

    def __getattr__(self, attr):
        if attr.startswith('!'):
            return lambda : self._run_system_cmd(attr.strip('!'))
        raise AttributeError

    def quit(self):
        self._send('got quit command, stop service')
        raise QuitError

    def showdate(self):
        from datetime import datetime
        self._send(str(datetime.now()))

    def _run_system_cmd(self, cmd):
        try:
            cmd_result = subprocess.check_output(cmd)
        except subprocess.CalledProcessError, err:
            cmd_result = 'ERROR: %s' % err
        self._send(cmd_result)

    def _send(self, data):
        self._conn.sendall(data + '\n')


class QuitError(Exception):
    pass


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print 'Connected by', addr
    while 1:
        data = conn.recv(1024)
        if not data: break
        try:
            CmdHandler(conn, data)()
        except QuitError:
            break
    conn.close()


