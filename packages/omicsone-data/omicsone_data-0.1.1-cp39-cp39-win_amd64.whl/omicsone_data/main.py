import argparse
import sys, os, re

import numpy as np
import pandas as pd
from tqdm import tqdm

from plugins.data import ProteomeData, GlycoproteomeData

from plugins.param import Parameter


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def standardrize_file(input_path, param_path, outdir_path):
    param = Parameter(param_path)
    folder, bn = os.path.split(input_path)
    bn, ext = os.path.splitext(bn)

    output_path = outdir_path + os.sep + bn + "-OmicsOneData.txt"
    if param['type'] == 'proteome':
        p = ProteomeData(input_path)
        p.data.to_csv(output_path, sep="\t")
    elif param['type'] == 'glycoproteome':
        p = GlycoproteomeData(input_path)
        p.data.to_csv(output_path, sep="\t")


def main():
    parser = MyParser(description='OmicsOne-data: data reader and converter for omics data analysis')
    parser.add_argument('-i', dest="input_file",
                        help="input file")
    parser.add_argument('-o', dest='output_dir', help='output directory')
    parser.add_argument('-p', dest='param_file', help='parameter file (.param)')

    args = parser.parse_args()

    # check inputs
    if args.input_file is None or (not os.path.exists(args.input_file)):
        print('invalid input file')
        parser.print_help()
        sys.exit(1)
    if args.output_dir is None or (not os.path.exists(args.output_dir)):
        print('invalid output directory')
        parser.print_help()
        sys.exit(1)
    if args.param_file is None or (not os.path.exists(args.param_file)):
        print('invalid parameter file')
        parser.print_help()
        sys.exit(1)

    standardrize_file(input_path=args.input_file, param_path=args.param_file, outdir_path=args.output_dir)


if __name__ == "__main__":
    main()
