import argparse
import xml.etree.ElementTree as ET
import os
import time

import logging

log = logging.getLogger()


def account_difference(parish_name, account_id, items, sales):
    """
    Determine the difference between a parish's item list and the list of
    items sold by an account ID, and return the top 10 unsold item IDs in order
    of rank.
    :param parish_name: name of the parish, exactly as it appears in sales
    :param account_id: account's ID, exactly as it appears in items
    :param items: parsed XML from accountItems.xml
    :param sales: parsed XML from parishSales.xml
    :return: a list of the top 10 unsold item IDs in order of rank in the sales
    data.
    """
    started = time.time()
    # gather all the unique items under this parish name from the sales data
    sales_items_and_rank = {}
    for ranked_item in sales.findall(".//*[countySimple='%s']" % parish_name):
        itemID = ranked_item.find('itemID').text
        rank = ranked_item.find('Rank').text

        sales_items_and_rank[itemID] = rank

    # gather all the unique items under this account ID from the items data
    account_items_and_sold = {}
    for ranked_item in items.findall(".//*[CMACCT='%s']" % account_id):
        itemID = ranked_item.find('ITEM_x0023_').text
        sold = ranked_item.find('acctUnitSold').text

        account_items_and_sold[itemID] = sold

    # find out what unique items exist under the parish that the
    # account ID did not sell
    difference = list(set(sales_items_and_rank.keys()) -
                      set(account_items_and_sold.keys()))

    top_unsold = sorted(difference,
                        key=lambda i: int(sales_items_and_rank[i]),
                        reverse=False)

    # MESS
    log.info('displaying the top 10 unsold for parish_name %s, '
             'account_id %s...' % (parish_name, account_id))
    for i in range(10):
        thing = top_unsold[i]
        log.info('itemID: %s, rank in parish: %s'
                 % (thing, sales_items_and_rank[thing]))
    log.debug('account_difference finished in %.4f seconds' %
             (time.time() - started))
    return top_unsold


if __name__ == "__main__":
    # parse the files from command line
    parser = argparse.ArgumentParser(
        description='Parses account sales by package and parish sales by '
                    'package, compares them, and returns the top X packages '
                    'in parish not included in the account.')
    parser.add_argument('items_path', metavar='items_file', type=str,
                        help='the path to the account items xml file')
    parser.add_argument('parish_path', metavar='parish_file', type=str,
                        help='the path to the account parish xml file')
    parser.add_argument('--log_level', metavar='level', type=str,
                        help='level of logging to display, default is INFO '
                             '(set to INFO for very basic details)',
                        default='INFO')
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)

    # validate the existence of the provided files
    assert os.path.exists(args.items_path), \
        "File not found: "+args.items_path
    assert os.path.exists(args.parish_path), \
        "File not found: "+args.parish_path

    parse_start = time.time()
    accountItems = ET.parse(args.items_path)
    parse1_done = time.time()
    log.debug('accountItems parsed in %.4f seconds' %
             (parse1_done - parse_start))
    parishSales = ET.parse(args.parish_path)
    log.debug('parishSales parsed in %.4f seconds' %
             (time.time() - parse1_done))

    # build the parish ranking dictionary


    account_difference('ACADIA', '00622',
                       accountItems.getroot(), parishSales.getroot())