#!/usr/bin/python3
"""Module for log parsing script.

This script reads stdin line by line and computes metrics:
- Total file size
- Number of lines by status code

The input format:
<IP Address> - [<date>] "GET /projects/260 HTTP/1.1" <status code> <file size>
If the format is not this one, the line must be skipped.
"""

import sys
import re

def extract_input(input_line):
    '''Extracts sections of a line of an HTTP request log.'''
    log_pattern = (
        r'(?P<ip>\S+) - \[(?P<date>.*?)\] "GET /projects/260 HTTP/1.1" '
        r'(?P<status_code>\d{3}) (?P<file_size>\d+)'
    )
    match = re.match(log_pattern, input_line)
    if match:
        return match.group('status_code'), int(match.group('file_size'))
    return None, None

def print_statistics(total_file_size, status_codes_stats):
    '''Prints the accumulated statistics of the HTTP request log.'''
    print(f"File size: {total_file_size}")
    for status_code in sorted(status_codes_stats):
        if status_codes_stats[status_code] > 0:
            print(f"{status_code}: {status_codes_stats[status_code]}")

def run():
    '''Starts the log parser.'''
    line_num = 0
    total_file_size = 0
    status_codes_stats = {str(code): 0 for code in [
        200, 301, 400, 401, 403, 404, 405, 500]}

    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            status_code, file_size = extract_input(line)
            if status_code and file_size:
                total_file_size += file_size
                if status_code in status_codes_stats:
                    status_codes_stats[status_code] += 1
                line_num += 1
                if line_num % 10 == 0:
                    print_statistics(total_file_size, status_codes_stats)
    except KeyboardInterrupt:
        print_statistics(total_file_size, status_codes_stats)
        raise
    except EOFError:
        print_statistics(total_file_size, status_codes_stats)
    finally:
        print_statistics(total_file_size, status_codes_stats)

if __name__ == '__main__':
    run()
