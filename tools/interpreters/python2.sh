#!/bin/bash

# Some platforms install Python3 as "python3", others install it as "python".
# This script finds which one is Python 2.
# I know of no platform which installs Python 2 as "python2", but I'm checking
# it just in case.

for current_command in python2 python
do
    if [[ $($current_command --version 2> /dev/null | grep "^Python 2\.") ]]; then
        echo $current_command
        exit 0
    fi
done

exit 1
