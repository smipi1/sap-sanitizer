#!/usr/bin/env python3
import argparse
import csv
import os

def splitcsv(args):
    
    infiles = [ f.name for f in args.infiles]
    max_record_count = args.max_record_count

    for infile in [ f.name for f in args.infiles]:

        infile_base, infile_ext = os.path.splitext(infile)
        outfile_count = 0
        outfile = None
        outfile_record_count = 0
        total_record_count = 0

        def next_outfile():
            nonlocal outfile_count, outfile, outfile_record_count
            outfile_count += 1
            outfile = infile_base + '.%03d'%(outfile_count) + infile_ext
            outfile_record_count = 0
        
        next_outfile()

        with open(infile, 'rt', newline='') as f_in:

            reader = csv.DictReader(f_in, delimiter='|')
            f_out = None
            writer = None

            def next_writer():
                nonlocal f_out, writer
                next_outfile()
                f_out = open(outfile, 'w', newline='')
                writer = csv.DictWriter(f_out, reader.fieldnames, delimiter='|')
            
            next_writer()

            try:
                for record in reader:
                    writer.writerow(record)
                    total_record_count += 1
                    outfile_record_count += 1
                    if outfile_record_count >= max_record_count:
                        print(f'Wrote {outfile_record_count} records to {outfile}, totalling {total_record_count}')
                        next_writer()
            except Exception as e:
                raise type(e)(str(e) + f' reading line {total_record_count-1} from {infile}')
            
            print(f'Wrote {outfile_record_count} records to {outfile}, totalling {total_record_count}')

def main():
    parser = argparse.ArgumentParser(
        description='CSV splitter',
    )
    parser.add_argument(
        dest='max_record_count',
        help='Maximum number of records per CSV output file',
        type=int
    )
    parser.add_argument(
        dest='infiles',
        help='SAP txt dump files to read',
        type=argparse.FileType('rb'),
        nargs='+',
    )
    args = parser.parse_args()
    splitcsv(args)

if __name__ == '__main__':
    main()
