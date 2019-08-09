#!/usr/bin/env python
import argparse
from   process_ni_io_trace.method import Method
from   process_ni_io_trace.status import Status
import sys

def main():
    parser = argparse.ArgumentParser(description='Convert NI IO Trace Capture.txt files into easier to parse SCPI list files')
    parser.add_argument('--write-only',            action='store_true')
    parser.add_argument('--read-write-only',       action='store_true')
    parser.add_argument('--exclude-open-close',    action='store_true')
    parser.add_argument('--exclude-read-response', action='store_true')
    parser.add_argument('--exclude-read-stb',      action='store_true')
    parser.add_argument('--exclude-visa-status',   action='store_true')
    parser.add_argument('--debug',                 action='store_true')
    parser.add_argument('capture_text_filename')
    parser.add_argument('output_filename')
    cli_args = parser.parse_args()

    # cannot --write-only and --read-write-only!
    if cli_args.write_only and cli_args.read_write_only:
        parser.print_help()
        sys.exit(1)

    # write only and/or read write only
    if cli_args.write_only or cli_args.read_write_only:
        cli_args.exclude_open_close    = True
        cli_args.exclude_read_stb      = True
        cli_args.exclude_visa_status   = True
    if cli_args.write_only:
        cli_args.exclude_read_response = True

    # methods
    open_method     = Method(name='Open',          args=['rm', 'address', 'arg3', 'arg4', 'instr'])
    open_rm_method  = Method(name='OpenDefaultRM', args=['rm'])
    close_method    = Method(name='Close',         args=['instr'])
    write_method    = Method(name='WriteAsync',    args=['instr', 'written',  'count', 'callback'])
    read_method     = Method(name='ReadAsync',     args=['instr', 'callback', 'read',  'size'], completing=True)
    read_stb_method = Method(name="ReadSTB",       args=['instr', 'status'])

    with open(cli_args.capture_text_filename, 'rb') as f_in:
        with open(cli_args.output_filename,   'w')  as f_out:
            stb        = None
            visa_error = None

            # match line
            for line in f_in:
                # visa status
                if not cli_args.exclude_visa_status:
                    if Status.is_match(line):
                        if cli_args.debug:
                            print(f'Processing status line: {line}')
                        if Status.is_error(line):
                            visa_error = Status.enum(line)
                            if cli_args.debug:
                                print(f'  updating visa_error: {visa_error}')
                        elif visa_error:
                            if cli_args.debug:
                                print(f'  outputting last visa_error: {visa_error}')
                            f_out.write(f'VISA ERROR: {visa_error}\n')
                            visa_error = None
                        continue

                # methods
                if Method.is_method(line):
                    # read stb
                    if not cli_args.exclude_read_stb:
                        if read_stb_method.is_match(line):
                            if cli_args.debug:
                                print(f'Processing read stb line: {line}')
                            id, args = read_stb_method.id_args(line)
                            stb = args['status']
                            continue
                        elif stb:
                            if cli_args.debug:
                                print(f'Writing last read stb: {stb}')
                            f_out.write(f'=> {stb}\n')
                            stb = None

                    # open close
                    if not cli_args.exclude_open_close:
                        if open_rm_method.is_match(line):
                            if cli_args.debug:
                                print(f'Processing open rm line: {line}')
                            id, args = open_rm_method.id_args(line)
                            f_out.write(f'Opening RM:    {args["rm"]}\n')
                            continue
                        elif open_method.is_match(line):
                            if cli_args.debug:
                                print(f'Processing open line: {line}')
                            id, args = open_method.id_args(line)
                            f_out.write(f'Opening instr: {args["instr"]}\n')
                            continue
                        elif close_method.is_match(line):
                            if cli_args.debug:
                                print(f'Processing close line: {line}')
                            id, args = close_method.id_args(line)
                            if not 'Event' in args['instr']:
                                f_out.write(f'Closing:       {args["instr"]} (line {id})\n')
                            continue

                    # read
                    if not cli_args.exclude_read_response:
                        if read_method.is_match(line):
                            if cli_args.debug:
                                print(f'Processing read line: {line}')
                            id, args = read_method.id_args(line)
                            f_out.write(f'=> {args["read"]}\n')
                            continue

                    # write
                    if write_method.is_match(line):
                        if cli_args.debug:
                            print(f'Processing write line: {line}')
                        id, args = write_method.id_args(line)
                        f_out.write(f'{args["written"]}\n')
                        continue

if __name__ == '__main__':
    main()
    sys.exit(0)
