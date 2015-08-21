import argparse


if __name__ == "__main__":
    # parse the filenames

    parser = argparse.ArgumentParser(
        description='Parses account sales by package and parish sales by '
                    'package, compares them, and returns the top X packages '
                    'in parish not included in the account.')
    parser.add_argument('items_path', metavar='items_file', type=str,
                        help='the path to the account items xml file')
    parser.add_argument('parsh_path', metavar='parish_file', type=str,
                        help='the path to the account parsh xml file')
    parser.add_argument('--log_level', metavar='level', type=str,
                        help='level of logging to display, default is WARNING '
                             '(set to INFO for very basic details)',
                        default='WARNING')
    args = parser.parse_args()

    print args