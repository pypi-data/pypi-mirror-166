import argparse
from plugins.param import Parameter
import sys, os, re
from this import d

import numpy as np
import pandas as pd
from tqdm import tqdm

from plugins.diff import compare_two_groups
from omicsone_meta.plugins.meta import Meta


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def main():
    parser = MyParser(description='hzdiff: do differential expression analysis on two groups.')
    parser.add_argument('-i', dest="input_file",
                        help="input file (.tsv)")
    parser.add_argument('-m', dest='meta_file', help='a file contains all name of group A')
    parser.add_argument('-p', dest='param_file', help='parameter file (.param)')
    parser.add_argument('-o', dest='output_dir', help='output directory')

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

    if args.meta_file is None or (not os.path.exists(args.meta_file)):
        print('invalid meta file')
        parser.print_help()
        sys.exit(1)

    data_path = args.input_file
    meta_path = args.meta_file
    param_path = args.param_file
    out_dir = args.output_dir

    folder, bn = os.path.split(data_path)
    bn, ext = os.path.splitext(bn)

    data = pd.read_csv(data_path, sep="\t")
    data = data.set_index('Index')

    meta = Meta(meta_path)

    a = [i + "-T" for i in meta.get_tumor_samples()]
    b = [i + "-N" for i in meta.get_normal_samples()]

    param = Parameter(param_path)

    method = param['method']
    diff_df = compare_two_groups(data, a, b, method)

    out_path = out_dir + os.sep + "{}-diff.tsv".format(bn)
    diff_df.to_csv(out_path, sep="\t")


if __name__ == "__main__":
    main()
