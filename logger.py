import termcolor

def colorConsoleLog(type,message=None):
    if message is None:
        message=type
    if type == "[ERROR]":
        termcolor.cprint(type+message,"red")
    elif type == "[WARN]":
        termcolor.cprint(type+message,"orange")
    elif type == "[LOG]":
        termcolor.cprint(type+message,"white")
    else:
        termcolor.cprint(type+message)