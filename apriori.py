"""Implementation of The Apriori algorithm, F(k-1) x F(k-1) variant."""

import itertools


def support_count(itemset, transactions):
    """
    Count support count for itemset

    :param itemset: set of items to measure support count for
    :param transactions: list of sets (all transactions)

    >>> simple_transactions = ['ABC', 'BC', 'BD', 'D']
    >>> [support_count(item, simple_transactions) for item in 'ABCDE']
    [1, 3, 2, 2, 0]
    >>> some_transactions = [set(['beer', 'bread', 'milk']), set(['beer']), set(['milk'])]
    >>> support_count(set(['beer']), some_transactions)
    2
    """
    return len([row for row in transactions if set(itemset) <= set(row)])


def _apriori_gen(frequent_sets):
    """
    Generate candidate itemsets

    :param frequent_sets: ORDERED list of k-1 frequent itemsets

    >>> _apriori_gen(['A', 'B', 'C'])
    ['AB', 'AC', 'BC']
    >>> _apriori_gen(['AB', 'AC', 'BC'])
    ['ABC']
    >>> _apriori_gen(['ABC', 'ABD', 'ABE', 'ACD', 'BCD', 'BCE', 'CDE'])
    ['ABCD', 'ABCE', 'ABDE', 'BCDE']
    """
    new_candidates = []
    for index, frequent_item in enumerate(frequent_sets):
        #addition = 1
        #if index + addition == len(frequent_sets) and frequent_item[:-1] == frequent_sets[index + addition][:-1]:
        #    new_candidates.append(frequent_item + frequent_sets[index + addition][-1])
        #    addition += 1
        for next_item in frequent_sets[index + 1:]:
            if len(frequent_item) == 1:
                new_candidates.append(frequent_item + next_item)
            elif frequent_item[:-1] == next_item[:-1]:
                new_candidates.append(frequent_item + next_item[-1])
            else:
                break

    return new_candidates


def apriori(transactions, itemset, minsup):
    """
    Apriori method

    :param transactions: list of all transactions
    :param itemset: set of all items
    :param minsup: minimum support

    >>> simple_transactions = ['ABC', 'BC', 'BD', 'D']
    >>> apriori(simple_transactions, 'ABCDE', 0.25)
    ['A', 'B', 'C', 'D', 'AB', 'AC', 'AD', 'BC', 'BD', 'CD', 'ABC', 'ABD', 'ACD', 'BCD', 'ABCD']
    >>> apriori(simple_transactions, 'ABCDE', 0.5)
    ['B', 'C', 'D', 'BC', 'BD', 'CD', 'BCD']
    >>> apriori(simple_transactions, 'ABCDE', 0.75)
    ['B']
    >>> apriori(simple_transactions, 'ABCDE', 0.9)
    []
    """

    def _prune(candidate_itemsets, previous_frequent):
        pruned_itemset = []
        for candidate in candidate_itemsets:
            for i in range(0, len(candidate)):
                if all([(candidate[:i] + candidate[i+1:]) in previous_frequent]):
                    pruned_itemset.append(candidate)
        return sorted(list(set(pruned_itemset)))

    itemset = sorted(list(itemset))

    k = 1
    N = len(transactions)

    frequent_itemsets = [[], sorted(
        [item for item in itemset if support_count(set([item]), transactions) >= N * minsup])]

    pruned_candidates = True

    while pruned_candidates:
        k += 1
        candidate_sets = _apriori_gen(frequent_itemsets[k-1])
        pruned_candidates = _prune(candidate_sets, frequent_itemsets[k-1])
        frequent_itemsets.append(pruned_candidates)

    return list(itertools.chain(*frequent_itemsets))


if __name__ == "__main__":
    print 'Running doctests'
    import doctest
    res = doctest.testmod()
    if not res[0]:
        print 'OK!'
