import gzip
import pathlib
import random
import time
from datetime import datetime


def resample():
    path = r'D:\Development\GIS\test-data\yeast'
    reads_file1 = 'FSY1742-reads.fasta'
    reads_file2 = 'S288C-reads.fasta'
    write_file = 'combined-reads.fasta'

    total_reads1 = 249476
    total_reads2 = 396326
    choose_reads = 30000

    random.seed(time.time())
    index_list1 = random.sample(range(total_reads1), choose_reads)
    index_list2 = random.sample(range(total_reads2), choose_reads)
    position_list1 = random.sample(range(choose_reads * 2), choose_reads)

    index_set1 = set(index_list1)
    index_set2 = set(index_list2)
    position_set = set(position_list1)

    print(f'Start, time: {datetime.now().strftime("%H:%M:%S")}')

    with open(pathlib.Path(path, reads_file1), 'r') as in_file1:
        with open(pathlib.Path(path, reads_file2), 'r') as in_file2:
            with open(pathlib.Path(path, write_file), 'w') as out_file:
                copy_reads(in_file1, in_file2, out_file, choose_reads, index_set1, index_set2, position_set)

    print(f'Done, time: {datetime.now().strftime("%H:%M:%S")}')


def copy_reads(in_file1, in_file2, out_file, choose_reads, index_set1, index_set2, position_set):
    in_strand1 = 0
    in_strand2 = 0
    out_strand = 0

    while out_strand < choose_reads * 2:
        if out_strand in position_set:
            in_strand1 = copy_strand(in_file1, out_file, in_strand1, index_set1)
        else:
            in_strand2 = copy_strand(in_file2, out_file, in_strand2, index_set2)
        out_strand += 1
        if out_strand % 1000 == 0:
            print(f'Written strand: {out_strand}, time: {datetime.now().strftime("%H:%M:%S")}')


def copy_strand(infile, outfile, in_strand, index_set):
    copy_started = False
    while True:
        pos = infile.tell()
        line = infile.readline()
        if not line:
            return in_strand

        if line[0] == '>' and copy_started:
            in_strand += 1
            infile.seek(pos)
            return in_strand

        if line[0] == '>' and not copy_started:
            if in_strand in index_set:
                copy_started = True
            in_strand += 1

        if copy_started:
            outfile.write(line)


# Main
if __name__ == '__main__':
    resample()
