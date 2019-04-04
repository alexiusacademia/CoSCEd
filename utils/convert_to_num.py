def convert_to_int(str):
    num = 0
    msg = ''
    try:
        num = int(str)
        msg = ''
    except ValueError:
        num = 0
        msg = 'Value must be numeric instead of ' + str + '.'
    except:
        num = 0
        msg = 'Unknown error has occurred.'

    return num, msg

def convert_to_float(str):
    num = 0.0
    msg = ''
    try:
        num = float(str)
        msg = ''
    except ValueError:
        num = 0.0
        msg = 'Value must be numeric instead of ' + str + '.'
    except:
        num = 0.0
        msg = 'Unknown error has occurred.'

    return num, msg
