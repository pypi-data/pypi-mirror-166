import platform
import diagnostics

def get_python_command():
    python_command = ""
    if platform.system().lower() == "windows":
        python_command = "python "
    else:
        python_command = "python3 "

    return python_command

def get_shell_extension():
    extension = ""
    if platform.system().lower() == "windows":
        extension = ".bat"
    else:
        extension = ".sh"

    return extension

def evaluate_statuscode(statusCode):
    log = diagnostics.StreamLogger()
    if platform.system().lower() == "windows":
        log.debug("Status Code:" + str(statusCode))
        if statusCode != 0:
            log.error("Error Code:" + str(statusCode))
            return False
    else:
        log.debug("Status Code:" + str(statusCode))
        if not os.WIFEXITED(statusCode):
            log.error("Error Code: " + os.WEXITSTATUS(statusCode))
            return False
    
    return True