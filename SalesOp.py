import argparse
import xml.etree.ElementTree as ET
import os

if __name__ == "__main__":
    # parse the filenames

    parser = argparse.ArgumentParser(
        description='Parses account sales by package and parish sales by '
                    'package, compares them, and returns the top X packages '
                    'in parish not included in the account.')
    parser.add_argument('items_path', metavar='items_file', type=str,
                        help='the path to the account items xml file')
    parser.add_argument('parish_path', metavar='parish_file', type=str,
                        help='the path to the account parsh xml file')
    parser.add_argument('--log_level', metavar='level', type=str,
                        help='level of logging to display, default is WARNING '
                             '(set to INFO for very basic details)',
                        default='WARNING')
    args = parser.parse_args()


    # validate the existence of the provided files
    assert os.path.exists(args.items_path), \
        "File not found: "+args.items_path
    assert os.path.exists(args.parish_path), \
        "File not found: "+args.parish_path

    items = ET.parse(args.items_path)
    parish = ET.parse(args.parish_path)

    print 'printing items...'
    for child in items.getroot():
        for stuff in child:
            print stuff.tag, stuff.attrib, stuff.text

    print 'printing parish...'
    for child in parish.getroot():
        for stuff in child:
            print stuff.tag, stuff.attrib, stuff.text