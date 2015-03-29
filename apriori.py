"""Implementation of The Apriori algorithm, F(k-1) x F(k-1) variant."""

import itertools


def support_count(itemset, transactions):
    """
    Count support count for itemset

    :param itemset: set of items to measure support count for
    :param transactions: list of sets (all transactions)

    >>> some_transactions = [set(['beer', 'bread', 'milk']), set(['beer']), set(['milk'])]
    >>> support_count(set(['beer', 'bread', 'milk']), some_transactions)
    1
    >>> support_count(set(['beer']), some_transactions)
    2
    >>> support_count(set(['bread']), some_transactions)
    1
    >>> support_count(set(['milk']), some_transactions)
    2
    """
    return len([row for row in transactions if set(itemset) <= set(row)])


def apriori(transactions, itemset, minsup):
    """
    Apriori method

    :param transactions: list of all transactions
    :param itemset: set of all items
    :param minsup: minimum support

    >>> some_transactions = [set(['beer', 'bread', 'milk']), set(['beer', 'bread', 'apple juice']), set(['milk'])]
    >>> apriori(some_transactions, set(['beer', 'bread', 'milk', 'apple juice']), 0.5)
    [set(['beer']), set(['bread']), set(['milk']), set(['beer', 'bread']), set(['beer', 'bread', 'milk'])]
    >>> apriori(some_transactions, set(['beer', 'bread', 'milk', 'apple juice']), 0.9)
    []
    """

    def _apriori_gen(frequent_sets):
        """

        :param frequent_sets: ORDERED list of frequent itemsets
        """
        new_candidates = []
        for index, frequent_item in enumerate(frequent_sets):
            #addition = 1
            #if index + addition == len(frequent_sets) and frequent_item[:-1] == frequent_sets[index + addition][:-1]:
            #    new_candidates.append(frequent_item + frequent_sets[index + addition][-1])
            #    addition += 1
            for next_item in frequent_sets[index + 1:]:
                if frequent_item[:-1] == next_item[:-1]:
                    new_candidates.append(frequent_item + next_item[-1])
                else:
                    break

        return new_candidates

    def _prune(candidate_itemsets):
        new_itemset = []
        for item in candidate_itemsets:
            if support_count(item, transactions) >= N * minsup:
                new_itemset.add(set(item))
        return new_itemset

    itemset = sorted(list(itemset))

    k = 1
    N = len(transactions)

    frequent_itemsets = [set()]

    frequent_itemsets.append(sorted(
        [item for item in itemset if support_count(set([item]), transactions) >= N * minsup]))

    while frequent_itemsets[k]:
        k += 1
        # candidate_sets = [i.union(j) for i in itemset for j in itemset if len(i.union(j)) == k]
        candidate_sets = _apriori_gen(frequent_itemsets[k-1])
        frequent_itemsets.append(_prune(candidate_sets))

    #print list(itertools.chain(*frequent_itemsets))
    return list(itertools.chain(*frequent_itemsets))


if __name__ == "__main__":
    print 'Running doctests'
    import doctest
    res = doctest.testmod()
    if not res[0]:
        print 'OK!'
