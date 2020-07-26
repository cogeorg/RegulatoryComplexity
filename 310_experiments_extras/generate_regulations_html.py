#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2020-07-26

@author: cogeorg@protonmail.com
"""
import sys
import os


# ===========================================================================
# MAIN
# ===========================================================================
if __name__ == "__main__":
    input_directory_name = sys.argv[1]
    output_directory_name = sys.argv[2]

    for filename in os.listdir(input_directory_name):
        if filename.endswith(".tex"):
            print(os.path.join(input_directory_name, filename))
