#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
sys.path.append('/home/xutaoding/autumn/')

from time import strftime, sleep
from east_report.er_update import ErUpdate


if __name__ == '__main__':
    update_time = ['0130', '0300', '0430', '0600', '0800', '0930']
    query_date = ['2015-09-27']
    while 1:
        if strftime('%H%M') not in update_time:
            print strftime('%Y-%m-%d %H:%M:%S %A')
            sleep(20.0)
        else:
            try:
                ErUpdate().main()
            except:
                pass
    # ErUpdate().main(query_date)
