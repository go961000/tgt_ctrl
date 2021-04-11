import threading

import serial


__all__ = ['TargetConsole']


class TargetConsole(object):
    '''
    TargetConsole is controller for target's console.
    '''

    def __init__(self, *args, **kwargs):
        self.serial: serial.Serial = serial.Serial(*args, **kwargs)
        self.wait_str: str = ''
        self.thread: threading.Thread = \
            threading.Thread(target=self.read_thread)
        self.thread.start()

    def read_thread(self):
        output_buf: str = ''

        while True:
            output_str: str = self.serial.read().decode()
            if output_str:
                print(output_str, end='')
                if self.wait_str:
                    output_buf += output_str
                    if self.wait_str in output_buf:
                        self.wait_str = None
                        output_buf = ''
                    else:
                        output_buf = output_buf[-(len(self.wait_str) - 1):]

    def write_console(self, input_str: str):
        self.serial.write(input_str.encode())

    def output_wait(self, wait_str: str):
        self.wait_str: str = wait_str

        while self.wait_str:
            pass
