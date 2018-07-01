#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Get all the dependencies of armips assembly files recursively,
and output them using Make dependency syntax.
"""

# This approach adapted from nowhere - 95% artisanal @obskyr solution 😎👌

from __future__ import print_function
from __future__ import unicode_literals

import os
import re
import sys
if sys.version_info[0] < 3:
    from codecs import open

INCLUDE_RE = re.compile(r"^\s*\.(loadtable|table|importobj|importlib|open|include|incbin|import)", re.IGNORECASE)

def dependencies_in(asm_file_paths):
    asm_file_paths = list(asm_file_paths)
    dependencies = {}
    
    for path in asm_file_paths:
        if path not in dependencies:
            asm_dependencies, bin_dependencies = shallow_dependencies_of(path)
            dependencies[path] = asm_dependencies | bin_dependencies
            asm_file_paths += asm_dependencies
    
    return dependencies

def shallow_dependencies_of(asm_file_path):
    asm_dependencies = set()
    bin_dependencies = set()

    with open(asm_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = INCLUDE_RE.match(line)
            if m is None:
                continue
            
            keyword = m.group(1).upper()
            line = line.split(';', 1)[0]
            first_quote = line.index('"') + 1
            second_quote = line.index('"', first_quote)
            path = line[first_quote:second_quote]
            if keyword == 'INCLUDE':
                asm_dependencies.add(path)
            else:
                bin_dependencies.add(path)
    
    return asm_dependencies, bin_dependencies

def main():
    if not len(sys.argv) > 1:
        print(sys.argv)
        print("Usage: {} <paths to assembly files...>".format(os.path.basename(__file__)))
        sys.exit(1)
    
    for path, dependencies in dependencies_in(sys.argv[1:]).items():
        # It seems that if A depends on B which depends on C, and
        # C is modified, Make needs you to change the modification
        # time of B too. That's the reason for the "@touch $@".
        if dependencies:
            print("{}: {}\n\t@touch $@".format(path, ' '.join(dependencies)))

if __name__ == '__main__':
    main()
