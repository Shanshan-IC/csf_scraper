# -*- encoding: utf-8 -*-

from time import strftime, sleep
from sha_executives import ShaExecutives
from szx_executives import SzxExecutives


def spider():
    SzxExecutives().main()
    ShaExecutives().main()

if __name__ == '__main__':
    while 1:
        if strftime('%H%M') not in ['9010', '1420']:
            print strftime('%Y-%m-%d %H:%M:%S %A')
            sleep(20.0)
            continue

        try:
            spider()
        except Exception as e:
            print 'Exception class: {0}, Error: {1}'.format(e.__class__, e.message)
    # spider()
