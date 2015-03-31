"""Implementation of The Apriori algorithm, F(k-1) x F(k-1) variant."""
from collections import defaultdict

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
    return len([row for row in transactions if set(itemset) <= set(row)])


def _apriori_gen(frequent_sets):
    """
    Generate candidate itemsets

    :param frequent_sets: ORDERED list of k-1 frequent itemsets as tuples

    >>> _apriori_gen(['A', 'B', 'C'])
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


def transaction_subsets(transaction, k):
    """
    Get subsets of transactions of length k

    >>> transaction_subsets(['A', 'B', 'C', 'D', 'E'], 4)
    [['A', 'B', 'C', 'D'], ['A', 'B', 'C', 'E'], ['A', 'B', 'D', 'E'], ['A', 'C', 'D', 'E'], ['B', 'C', 'D', 'E']]

    :param transaction: list
    :param k: int
    :return:
    """
    subsets = []

    if k == 1:
        return [[t] for t in transaction]

    elif k > len(transaction):
        return []

    for i in range(0, len(transaction) - (k - 1)):
        for t in transaction_subsets(transaction[i + 1:], k - 1):
            subset = [transaction[i]] + t
            subsets.append(subset)

    return subsets


def apriori(transactions, all_items, minsup, fixed_k=None):
    """
    Apriori method

    :param transactions: list of tuples (list of transactions containing items as tuples)
    :param all_items: list distinct items
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

    #print all_items
    # print transactions

    k = 1
    N = len(transactions)

    frequent_itemsets = [[], []]  # k index, zero always empty
    support = defaultdict(int)

    for item in all_items:
        new_item = (item,)
        support[new_item] = support_count([item], transactions)
    #    if support[item]:
            #print item
            #print transactions[0]
            #print support[item]

        if support[new_item] >= N * minsup:
            frequent_itemsets[1].append(new_item)

    print frequent_itemsets

    #if len(frequent_itemsets[1]):
        # print 'K %s sets - %s' % (k, frequent_itemsets)
        #assert len(frequent_itemsets[1][0]) == 1

    pruned_candidates = [True]

    while pruned_candidates and pruned_candidates[0] and (not fixed_k or k < fixed_k):
        k += 1
        candidate_sets = _apriori_gen(frequent_itemsets[k-1])
        # print 'K %s sets - %s' % (k, candidate_sets)
        # pruned_candidates = _prune(candidate_sets, frequent_itemsets[k-1])
        for t in transactions:
            candidates_t = list(set(t) & set(candidate_sets))
            candidates_subsets = transaction_subsets(candidates_t, k)
            for subset in candidates_subsets:
                support[subset] += 1

        pruned_candidates = [item for item in candidate_sets if support[item] >= N * minsup]

        print 'Pruned K %s-itemsets - length %s' % (k, len(pruned_candidates))
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
