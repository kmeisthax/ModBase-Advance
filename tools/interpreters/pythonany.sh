#!/bin/bash

# Some platforms install Python as "python3", others install it as "python".
# And someone might have stuck Python in "python2" if they're really pedantic.
# This script just tries to find any working Python version.

for current_command in python python3 python2
do
    if [[ $($current_command --version 2> /dev/null | grep "^Python") ]]; then
        echo $current_command
        exit 0
    fi
done

exit 1
