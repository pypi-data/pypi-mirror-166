#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import timeit

import httpx

from rich import print


start_time = timeit.default_timer()

parser = argparse.ArgumentParser(description='Check Status of Web Pages.')
parser.add_argument('url', type=str, nargs='?', help='Input URL to check.')
parser.add_argument('--input-file', '-i', type=argparse.FileType('r'), default=sys.stdin,
                    help='Read URLs from a local text file.')
parser.add_argument('--verbose', '-v', action='store_true', help='Turn on verbose output.')
cli_args = parser.parse_args()


def check(url):
    try:
        cli_args.verbose and print(f'Check: {url}')
        resp = httpx.head(url)
    except Exception as err:
        print(f'Exception: {url} - {err}')
        return

    if resp.is_success:
        cli_args.verbose and print(f'Success: {url}')
    elif resp.is_redirect:
        print(f'Redirect: {url} -> {resp.headers["location"]}')
    else:
        print(f'Not OK: {url} - {resp.status_code}')


if cli_args.url:
    check(cli_args.url)
elif cli_args.input_file:
    for line in cli_args.input_file.readlines():
        check(line.strip())


cli_args.verbose and print('Script runtime: ', timeit.default_timer() - start_time)
