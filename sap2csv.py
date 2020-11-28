#!/usr/bin/env python3
import argparse
import os

def sap2csv(args):
    def read_cols(f, line):
        return [ i.strip() for i in line.split("|")[1:][:-1] ]

    def write_cols(f, fields):
        print("|".join(fields), file=f)

    have_header=False
    last_values = None

    for f in args.infiles:

        fo = args.outfile

        if fo is None:
            name, _ = os.path.splitext(f.name)
            outfile_name = name + '.csv'
            fo = open(outfile_name, 'wt')
            have_header = False
            last_values = False

        f.readline() # Dispose date
        f.readline() # Dispose bar
        f.readline() # Dispose bar
        header=read_cols(f, f.readline())
        f.readline() # Dispose bar
        if not have_header:
            field_count=len(header)
            write_cols(fo, header)
            have_header=True
        else:
            if field_count != len(header):
                raise Exception(f"Field-count mismatch reading: {f.name}")
        line = ""
        lines = 0
        values = []

        for part in f:
            part = part.strip()
            if len(values) == len(header):
                if len(part) <= 0:
                    print(f'when adding to: {line}')
                    print(f'got: {part}')
                if part[0] == "|":
                    write_cols(fo, values)
                    last_values = values
                    line = ""
                    lines += 1
                    values=[]
            line += part
            try:
                values=read_cols(f, line)
            except Exception as e:
                print(f"Last good line in {f.name}:")
                print(last_values)
                raise e
            if len(values) < len(header):
                line += " "
                continue
            if len(values) > len(header):
                print(f'headers ({len(header)}): {header}')
                print(f'values ({len(values)}: {values}')
                raise Exception(f"Too many values writing to {fo.name}:{lines}")
        if len(values) != 0:
            if len(values) < len(header):
                print(f'headers ({len(header)}): {header}')
                print(f'values ({len(values)}: {values}')
                raise Exception(f"Insufficient values writing to {fo.name}:{lines}")
            write_cols(fo, values)
            lines += 1

        print(f'Wrote {lines} lines to {fo.name}')

def main():
    parser = argparse.ArgumentParser(
        description='SAP to CSV converter',
    )
    parser.add_argument(
        dest='infiles',
        help='SAP txt dump files to read',
        type=argparse.FileType('rt', errors='ignore'),
        nargs='+',
    )
    parser.add_argument(
        '--out',
        '-O',
        dest='outfile',
        help='CSV file to write',
        type=argparse.FileType('wt'),
        required=False,
    )
    args = parser.parse_args()
    sap2csv(args)

if __name__ == '__main__':
    main()

