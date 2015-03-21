books = set(['T', 'W', 'H', 'I', 'P', 'E', 'O'])

book_orders = [
    'TOI',
    'TIETO',
    'HETI',
    'WETO',
    'PIHWI',
    'TIIPII',
    'POET',
    'EHTO',
    'TEHO',
    'HIIHTO',
    'PIHWIT',
    'PETI',
    'HEP',
    'PETO',
    'PITO',
    'HEPO',
    'OTE',
    'PEIPPO',
    'TIE',
    ]

itemsets = ['E', 'O', 'P', 'W', 'EO', 'EP', 'EW', 'OP', 'OW', 'PW', 'EOP', 'EOW', 'EPW', 'OPW', 'EOPW']

for itemset in itemsets:
    support_count = len([order for order in book_orders if set(itemset) <= set(order)])
    support = support_count / float(len(book_orders))
    print 'Itemset %s Support: %.3f' % (itemset, support)