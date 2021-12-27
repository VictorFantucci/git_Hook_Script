#!/usr/bin/env python
import re
import os
import sys
from collections import defaultdict
from pylint.lint import Run

detect_print=True
detect_pdb=True
linter_limit=8.5

errors = defaultdict(list)
file_inspected = sys.argv[1]

try:
    with open(file_inspected, 'r') as file_readed:
        for position, line in enumerate(file_readed):
            if re.findall(r'print\(.*\)',  line) and detect_print:
                msg = 'print at line {position} - > {code}'
                msg = msg.format(position=position, code=line)
                errors[position].append(msg)
            if re.findall(r'pdb', line) and detect_pdb:
                msg = 'pdb at line {position} - > {code}'
                msg = msg.format(position=position, code=line)
                errors[position].append(msg)

    results = Run([file_inspected, '-d R'], do_exit=False)
    linter_value = results.linter.stats['global_note']
    linter_ok = linter_value > linter_limit
    n_errors = len(errors)
    if not n_errors and linter_ok:
        sys.exit(0)
    else:
        print('-----------------------------------------------------')
        print('                COMMIT NOT ALLOWED!                ')
        print('                  ERRORS FOUND {}                '.format(n_errors))
        print('-----------------------------------------------------')
        print('                                                     ')
        for position, item in errors.items():
            print('               ')
            print('***************')
            msg = '{file_name}: {msg_error}'
            msg = msg.format(file_name=file_inspected, msg_error=item)
            print(msg)
            print('                                                     ')
            print('-----------------------------------------------------')

        if not linter_ok:
            linter_value = round(linter_value, 2)
            msg = 'Linter value of {} above the limit of {}'.format(linter_value,
                                                                    linter_limit)
            print(msg)
        sys.exit(1)
except Exception as e:
    print("{} No such file or directory".format(file_inspected))
