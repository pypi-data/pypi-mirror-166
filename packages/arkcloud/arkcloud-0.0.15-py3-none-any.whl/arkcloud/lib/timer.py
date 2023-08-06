from time import sleep, time


def countdown(seconds: int, message=None):
    start = 0
    end = seconds
    progress(start, end, prefix=f"\rWaiting {end - start}", suffix=message or '', color='white')
    while start < end:
        sleep(1)
        start += 1
        progress(start, end, prefix=f"\rWaiting {end - start}", suffix=message or '', color='white')


def progress(iteration, total, prefix='', suffix='', color_temp=False, decimals=1, length=50, fill='█',
                     color=''):
    colors = {'': '30m', 'gray': '90m', 'red': '31m', 'green': '92m', 'yellow': '93m', 'purple': '35m',
              'orange': '33m', 'blue': '34m', 'pink': '95m', 'cyan': '96m', 'black': '97m', 'white': '38m'}
    if int(iteration % (total / 100)) == 0 or iteration == total or prefix != '' or suffix != '':
        # calculated percentage of completeness
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        # modifies the bar
        bar = fill * filledLength + '-' * (length - filledLength)
        # Creates the bar
        if color_temp:
            temp = {0.0: 'red', 35.0: 'orange', 65.0: 'yellow', 100.0: 'green'}
            color = temp[min([0.0, 35.0, 65.0, 100.0], key=lambda x: abs(x - float(percent)))]
        print(f'\r\033[{colors[color]}\t\t{prefix} |{bar}| {percent}% {suffix}', end='\033[0m')
        # Print New Line on Complete
        if iteration == total:
            print()


class Timer:
    def __init__(self):
        pass

