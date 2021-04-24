from myShell import MyShell


def receiveSignal(signalNumber, frame):
    """The handler for ctrl c signal.
    Print the return codes and the most frequent return code in case the script was interrupted"""

    print("received signal number: " + str(signalNumber))
    ms = MyShell.getInstance()
    if ms.com:
        ms.com.print_return_codes()
    exit(0)
