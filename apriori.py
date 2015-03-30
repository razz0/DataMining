"""Implementation of The Apriori algorithm, F(k-1) x F(k-1) variant."""

import itertools


def support_count(itemset, transactions):
    """
    Count support count for itemset

    :param itemset: items to measure support count for
    :param transactions: list of sets (all transactions)

    >>> simple_transactions = ['ABC', 'BC', 'BD', 'D']
    >>> [support_count(item, simple_transactions) for item in 'ABCDE']
    [1, 3, 2, 2, 0]
    >>> some_transactions = [set(['beer', 'bread', 'milk']), set(['beer']), set(['milk'])]
    >>> support_count(set(['beer']), some_transactions)
    2
    """
    # print set([itemset])
    # print set(transactions[0])
    return len([row for row in transactions if set([itemset]) <= set(row)])


def _apriori_gen(frequent_sets):
    """
    Generate candidate itemsets

    :param frequent_sets: ORDERED list of k-1 frequent itemsets as tuples

    >>> _apriori_gen([('A',), ('B',), ('C',)])
    [('A', 'B'), ('A', 'C'), ('B', 'C')]
    >>> ''.join(_apriori_gen([('AB',), ('AC',), ('BC',)]))
    ['ABC']
    >>> [''.join(items for items in _apriori_gen(['ABC', 'ABD', 'ABE', 'ACD', 'BCD', 'BCE', 'CDE']))]
    ['ABCD', 'ABCE', 'ABDE', 'BCDE']
    """
    new_candidates = []
    for index, frequent_item in enumerate(frequent_sets):
        for next_item in frequent_sets[index + 1:]:
            if len(frequent_item) == 1:
                new_candidates.append(frequent_item + next_item)
            elif frequent_item[:-1] == next_item[:-1]:
                new_candidates.append(tuple(list(frequent_item) + [next_item[-1]]))
            else:
                break

    return new_candidates


def apriori(transactions, all_items, minsup, fixed_k=None):
    """
    Apriori method

    :param transactions: list of lists of tuples (list of transactions containing list of items as tuples)
    :param all_items: list of tuples with all distinct items
    :param minsup: minimum support

    >>> simple_transactions = [[tuple(piece) for piece in item] for item in ['ABC', 'BC', 'BD', 'D']]
    >>> alphabet = [tuple(letter) for letter in 'ABCDE']
    >>> res = apriori(simple_transactions, alphabet, 0.25)
    >>> print [''.join(item) for item in res]
    ['A', 'B', 'C', 'D', 'AB', 'AC', 'AD', 'BC', 'BD', 'CD', 'ABC', 'ABD', 'ACD', 'BCD', 'ABCD']
    >>> res = apriori(simple_transactions, alphabet, 0.5)
    >>> print [''.join(item) for item in res]
    ['B', 'C', 'D', 'BC', 'BD', 'CD', 'BCD']
    >>> res = apriori(simple_transactions, alphabet, 0.5, fixed_k=2)
    >>> print [''.join(item) for item in res]
    ['BC', 'BD', 'CD']
    >>> res = apriori(simple_transactions, alphabet, 0.75)
    >>> print [''.join(item) for item in res]
    ['B']
    >>> apriori(simple_transactions, alphabet, 0.9)
    []
    """

    def _prune(candidate_itemsets, previous_frequent):
        pruned_itemset = []
        for candidate in candidate_itemsets:
            for i in range(0, len(candidate)):
                if all([(candidate[:i] + candidate[i+1:]) in previous_frequent]):
                    pruned_itemset.append(candidate)
        return sorted(list(set(tuple(pruned_itemset))))

    all_items = sorted(list(all_items))

    # print all_items
    # print transactions

    k = 1
    N = len(transactions)

    frequent_itemsets = [[], sorted(
        [item for item in all_items if support_count(item, transactions) >= N * minsup])]

    if len(frequent_itemsets[1]):
        # print 'K %s sets - %s' % (k, frequent_itemsets)
        assert len(frequent_itemsets[1][0]) == 1

    pruned_candidates = [set([True])]

    while pruned_candidates and pruned_candidates[0] and (not fixed_k or k < fixed_k):
        k += 1
        candidate_sets = _apriori_gen(frequent_itemsets[k-1])
        # print 'K %s sets - %s' % (k, candidate_sets)
        pruned_candidates = _prune(candidate_sets, frequent_itemsets[k-1])
        # print 'Pruned K %s sets - %s' % (k, pruned_candidates)
        frequent_itemsets.append(pruned_candidates)

    if fixed_k:
        return frequent_itemsets[fixed_k]

    return list(itertools.chain(*frequent_itemsets))


if __name__ == "__main__":
    print 'Running doctests'
    import doctest
    res = doctest.testmod()
    if not res[0]:
        print 'OK!'
