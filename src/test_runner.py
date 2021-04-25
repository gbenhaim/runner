from commands import Command
from termcolor import colored


def test_init():
    """ Test should check that the init works correctly"""
    
    command = Command("cd ./home")
    assert command.command_to_exe == "cd ./home "
    assert command.original_command == "cd ./home"
    assert len(command.return_codes) == 0


def test_run_c(capsys):
    """ Test should check that the option --c COUNT works correctly + capture its output and compare it to
                   the expected output"""
    command = Command("cd ./home -c 10")
    command.exe()
    out, err = capsys.readouterr()
    expected_output = "An exception occurred\n" * 10
    assert expected_output == out
    command.print_return_codes()
    out, err = capsys.readouterr()
    assert "return code: 512 accord 10 times.\n" + "The most frequent return code is: 512\n" == out


def test_run_failed_count(capsys):
    """ Test should check that the option --failed-count N works correctly + capture its output and compare it to
                   the expected output"""
    command = Command("cd ./home -c 12 --failed-count 10")
    command.exe()
    out, err = capsys.readouterr()
    expected_output = "An exception occurred\n" * 10 + "cd ./home -c 12 --failed-count 10 got failed count limit\n"
    assert expected_output == out
    command.print_return_codes()
    out, err = capsys.readouterr()
    assert "return code: 512 accord 10 times.\n" + "The most frequent return code is: 512\n" == out


def test_run_sys_trace(capsys):
    """ Test should check that the option --sys-trace works correctly + capture its output and compare it to
                   the expected output"""
    command = Command("cd ./home --sys-trace")
    command.exe()
    out, err = capsys.readouterr()
    assert "Disk IO:" in out
    assert "Memory:" in out
    assert "Processes/threads and cpu usage:" in out
    assert "Network card package counters:" in out
    command.print_return_codes()
    out, err = capsys.readouterr()
    assert "return code: 512 accord 1 times.\n" + "The most frequent return code is: 512\n" == out


def test_run_call_trace(capsys):
    """ Test should check that the option --call-trace works correctly + capture its output and compare it to
                   the expected output"""
    command = Command("cd ./home --call-trace")
    command.exe()
    out, err = capsys.readouterr()
    expected_output = "An exception occurred\n" + "All the syscalls: \n"
    assert expected_output == out
    command.print_return_codes()
    out, err = capsys.readouterr()
    assert "return code: 256 accord 1 times.\n" + "The most frequent return code is: 256\n" == out


def test_run_log_trace(capsys):
    """ Test should check that the option --log-trace works correctly + capture its output and compare it to
                   the expected output"""
    command = Command("cd ./home --log-trace")
    command.exe()
    out, err = capsys.readouterr()
    expected_output = "An exception occurred\n" + colored("sh: 1: cd: can't cd to ./home\n", 'red') + "\n"
    assert expected_output == out
    command.print_return_codes()
    out, err = capsys.readouterr()
    assert "return code: 512 accord 1 times.\n" + "The most frequent return code is: 512\n" == out


def test_run_debug(capsys):
    """ Test should check that the option --debug works correctly + capture its output and compare it to
                   the expected output"""
    command = Command("cd ./home --debug")
    command.exe()
    out, err = capsys.readouterr()
    expected_output = colored("cd ./home ", 'blue') + "\nAn exception occurred\n"
    assert expected_output == out
    command.print_return_codes()
    out, err = capsys.readouterr()
    assert "return code: 512 accord 1 times.\n" + "The most frequent return code is: 512\n" == out


def test_run_help(capsys):
    """ Test should check that the option --help works correctly + capture its output and compare it to
                the expected output"""
    command = Command("cd ./home --help")
    command.exe()
    out, err = capsys.readouterr()
    assert "usage: [COMMAND] [OPTION]" in out
    assert "Options:" in out
    assert "-c [count]" in out
    assert "--failed-count [N]" in out
    assert "--sys-trace" in out
    assert "--call-trace" in out
    assert "--log-trace" in out
    assert "--debug" in out
    assert "--help" in out
    assert "Exit status:" in out


def test_run_c_negative_count(capsys):
    """ Test should command with option --c COUNT, when COUNT < 0 and failed + capture its output and compare it to
                the expected output"""
    command = Command("cd ./home -c -4")
    command.exe()
    out, err = capsys.readouterr()
    expected_output = "-c should have a zero or positive number after\n"
    assert expected_output == out


def test_run_invalid_command(capsys):
    """ Test should run invalid command with option --c COUNT and failed + capture its output and compare it to
                the expected output"""
    command = Command("cd fdnmfsdmn ./home -c 5")
    command.exe()
    out, err = capsys.readouterr()
    expected_output = "An exception occurred\n" * 5
    assert expected_output == out
    command.print_return_codes()
    out, err = capsys.readouterr()
    assert "return code: 512 accord 5 times.\n" + "The most frequent return code is: 512\n" == out


def test_run_valid_command_call(capsys):
    """ Test should run valid command with option --call-trace successfully and capture its output and compare it to
                the expected output"""
    command = Command("ls -c 5 --call-trace")
    command.exe()
    out, err = capsys.readouterr()
    expected_output = ""
    assert expected_output == out
    command.print_return_codes()
    out, err = capsys.readouterr()
    assert "return code: 0 accord 5 times.\n" + "The most frequent return code is: 0\n" == out


def test_run_valid_command_log(capsys):
    """ Test should run valid command with option --log-trace successfully and capture its output and compare it to
            the expected output"""
    command = Command("ls -c 5 --log-trace")
    command.exe()
    out, err = capsys.readouterr()
    expected_output = ""
    assert expected_output == out
    command.print_return_codes()
    out, err = capsys.readouterr()
    assert "return code: 0 accord 5 times.\n" + "The most frequent return code is: 0\n" == out
