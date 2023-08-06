import argparse
import sys, os, re

import numpy as np
import pandas as pd
from tqdm import tqdm

try:
    from plugins.volcano import volcano, volcano2
    from plugins.param import Parameter
except:
    from .plugins.volcano import volcano, volcano2
    from .plugins.param import Parameter


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

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

    input_path = args.input_file
    param_path = args.param_file
    output_dir = args.output_dir

    stat_df = pd.read_csv(input_path,sep="\t")
    param = Parameter(param_path)

    volcano(stat_df=stat_df, out_dir=output_dir, param=param)
    volcano2(stat_df=stat_df, out_dir=output_dir, param=param)


if __name__ == "__main__":
    main()
