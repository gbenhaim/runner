from commands import Command


class MyShell:
    class __MyShell:
        def __init__(self):
            """The constructor for __MyShell.
                    :field com: The Command object, init to None."""
            self.com = None

        def run_command(self, cmd_line):
            """ Get the user input and create + execute the command and prints a summary"""
            self.com = Command(cmd_line=cmd_line)
            self.com.exe()
            self.com.print_return_codes()
            self.com = None

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if MyShell.__instance == None:
            MyShell.__instance = MyShell.__MyShell()
        return MyShell.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if MyShell.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            MyShell.__instance = MyShell.__MyShell()
