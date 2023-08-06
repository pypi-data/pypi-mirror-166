#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Security Groups rules management')
    parser.add_argument('-l', '--list',
                        help="Get the security groups list")

    arg = parser.parse_args()

    if arg.list:
       print('Security Groups List')

if __name__ == '__main__':
    sys.exit(main())
