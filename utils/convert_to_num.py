def convert_to_int(str1):
    num = 0
    msg = ''
    try:
        num = int(str1)
        msg = ''
    except ValueError:
        num = 0
        msg = 'Value must be numeric instead of ' + str1 + '.'
    except:
        num = 0
        msg = 'Unknown error has occurred.'

    return num, msg


def convert_to_float(str1):
    num = 0.0
    msg = ''
    try:
        num = float(str1)
        msg = ''
    except ValueError:
        num = 0.0
        msg = 'Value must be numeric instead of ' + str1 + '.'
    except:
        num = 0.0
        msg = 'Unknown error has occurred.'

    return num, msg
