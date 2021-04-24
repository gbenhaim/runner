from myShell import MyShell
import signal
from signals_handlers import receiveSignal
import sys

if __name__ == "__main__":

    # create a singleton instance
    ms = MyShell.getInstance()
    signal.signal(signal.SIGINT, receiveSignal)

    #while 1:
    cmd_line = ' '.join(sys.argv[1:])
    ms.run_command(cmd_line=cmd_line)
