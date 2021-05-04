import string
import os
import psutil
from termcolor import colored


class Command:
    """The constructor for Command.
            :param cmd_line: The full input of the user.
            :field original_command: The full input of the user.
            :field command_to_exe: The external command with the outer options.
            :field options: A dict such that keys = options and values = count or a flag that represents
                            if we should be considered ot not.
            :field return_codes: A dict such that keys =  return code num and values = num of times they accord.
            :field valid_command: True if the command is valid according to the script's options"""

    def __init__(self, cmd_line: string):
        self.original_command = cmd_line
        self.command_to_exe = ""
        self.options = {
            "-c": 1,
            "--failed-count": float('inf'),
            "--sys-trace": False,
            "--call-trace": False,
            "--log-trace": False,
            "--debug": False,
            "--help": False,
            "--net-trace": False
        }
        self.return_codes = dict()
        self.valid_command = True

        # splits (according to whitespace) the cmd line into a list
        args = cmd_line.split()

        # sets the options and build the command
        i = 0
        while i < len(args):
            if args[i] in self.options:
                if args[i] == "-c" or args[i] == "--failed-count":
                    i += 1
                    if i < len(args) and args[i].isnumeric():
                        self.options[args[i - 1]] = int(args[i])
                    else:
                        print("-c should have a zero or positive number after")
                        self.valid_command = False
                else:
                    # set the flag
                    self.options[args[i]] = True
            # not one of our options - it's part of the command to execute
            else:
                self.command_to_exe += args[i] + " "
            i += 1

    def exe(self):
        """Execute the command according to it's options.
                    input:
                        -self - The command.
            """

        if not self.valid_command:
            return

        count_failed = 0

        # check options and act accordingly
        for i in range(self.options.get("-c")):

            # --help
            if self.options.get("--help"):
                self.help_message()
            else:
                # --call-trace
                if self.options.get("--call-trace"):
                    self.command_to_exe = "strace -c -o sys.txt " + self.command_to_exe

                # run the command
                return_value = os.system(self.command_to_exe + " > out.txt 2> err.txt")

                # updates return codes of needed
                self.return_codes[return_value] = self.return_codes[
                                                      return_value] + 1 if return_value in self.return_codes else 1
                # --debug
                if self.options.get("--debug"):
                    self.debug()

                # in case the run failed, check options and act accordingly
                if return_value != 0:
                    print("An exception occurred")
                    count_failed += 1

                    # --sys-trace
                    if self.options.get("--sys-trace"):
                        self.sys_trace()

                    # --call-trace
                    if self.options.get("--call-trace"):
                        sys_file = open("sys.txt", "r")
                        self.call_trace(sys_file)
                        sys_file.close()

                    # --log-trace
                    if self.options.get("--log-trace"):
                        out_file = open("out.txt", "r")
                        err_file = open("err.txt", "r")
                        self.log_trace(out_file, err_file)
                        out_file.close()
                        err_file.close()

                    # --count-failed
                    if count_failed >= self.options.get("--failed-count"):
                        print(self.original_command + " got failed count limit")
                        return

    def sys_trace(self):
        """For each failed execution, create a log for each of the following values, measured during command execution:
                    * Disk IO
                    * Memory
                    * Processes/threads and cpu usage of the command
                    * Network card package counters
                    input:
                        -self - The command.
            """
        # Disk IO info
        print("Disk IO: " + str(psutil.disk_io_counters()))

        # Memory
        print("Memory: " + str(psutil.virtual_memory()))

        # Processes/threads and cpu usage of the command
        print("Processes/threads and cpu usage: " + str(psutil.cpu_percent(1)))

        # Network card package counters
        print("Network card package counters: " + str(psutil.net_io_counters()))

    def call_trace(self, sys_file):
        """Print a log with all the system calls ran by the command. """

        print("All the syscalls: ")
        for line in sys_file:
            print(line)

    def log_trace(self, output, err):
        """For each failed execution, add also the command output logs (stdout, stderr)"""
        for line in output:
            print(line)
        for line in err:
            print(colored(line, 'red'))

    def print_return_codes(self):
        """Print a summary of the command return codes (how many times each return code happened) and the most
                frequent return code."""

        max_frequent_return_code = None
        max_frequency = 0
        for return_code in self.return_codes.keys():
            max_frequency = max(max_frequency, self.return_codes.get(return_code))
            max_frequent_return_code = return_code if max_frequency == self.return_codes.get(
                return_code) else max_frequent_return_code
            print("return code: " + str(return_code) + " accord " + str(self.return_codes.get(return_code)) + " times.")
        if max_frequent_return_code != None:
            print("The most frequent return code is: " + str(max_frequent_return_code))

    def debug(self):
        """Debug mode, show each instruction executed by the script"""
        print(colored(self.command_to_exe, 'blue'))

    def help_message(self):
        '''Print a usage message to STDERR explaining how the script should be used.'''

        print("usage: [COMMAND] [OPTION]")
        print()
        print("Options:")
        print("      -c [count]               Number of times to run the given command.")
        print("      --failed-count [N]       Number of times to run the given command.")
        print("      --sys-trace              For each failed execution, create a log for each of the following values,"
              "measured during command execution: * Disk IO * Memory * Processes/threads and cpu usage of the command"
              " * Network card package counters")
        print("      --call-trace             For each failed execution, add also a log with all the system calls ran"
              " by the command.")
        print("      --log-trace              For each failed execution, add also the command output logs"
              " (stdout,stderr)")
        print("      --debug                  Debug mode, show each instruction executed by the script")
        print(
            "      --help                   Print a usage message to STDERR explaining how the script should be used.")

        print("Exit status:")
        print("0  if OK,")
        print("1  if the command failed")
