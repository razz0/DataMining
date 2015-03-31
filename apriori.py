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
    #print set(itemset)
    #print set(transactions[0])
    return len([row for row in transactions if set(itemset) <= set(row)])


def _apriori_gen(frequent_sets):
    """
    Generate candidate itemsets

    :param frequent_sets: list of tuples, containing frequent itemsets [ORDERED]

    >>> _apriori_gen([('A',), ('B',) ('C',)])
    [('A', 'B'), ('A', 'C'), ('B', 'C')]

    >>> _apriori_gen([('A', 'B'), ('A', 'C'), ('B', 'C')])
    [('A', 'B', 'C')]

    >>> _apriori_gen([tuple(item) for item in ['ABC', 'ABD', 'ABE', 'ACD', 'BCD', 'BCE', 'CDE']])
    [('A', 'B', 'C', 'D'), ('A', 'B', 'C', 'E'), ('A', 'B', 'D', 'E'), ('B', 'C', 'D', 'E')]

    >>> _apriori_gen([['57033', '58972'], ['57033', '57342']])
    [('57033', '58972', '57342')]

    >>> cc = [('55015', '55314'), ('55015', '55315'), ('55314', '55315'), ('57016', '57017'), ('57043', '57047'), ('581325', '582103')]
    >>> _apriori_gen(cc)
    [('55015', '55314', '55315')]
    """
    #print '----------------'
    #print '_apriori_gen got %s' % frequent_sets
    #print '----------------'
    new_candidates = []
    for index, frequent_item in enumerate(frequent_sets):
        for next_item in frequent_sets[index + 1:]:
            #print '%s - %s' % (type(frequent_item), frequent_item)
            #print '%s - %s' % (type(next_item), next_item)
            if len(frequent_item) == 1:
                new_candidates.append(tuple(frequent_item) + tuple(next_item))
            elif frequent_item[:-1] == next_item[:-1]:
                new_candidates.append(tuple(frequent_item) + (next_item[-1],))
            else:
                break

    #print '----------------'
    #print '_apriori_gen returning %s' % new_candidates
    #print '----------------'

    return new_candidates


def transaction_subsets(transaction, k):
    """
    Get subsets of transactions of length k

    >>> transaction_subsets(['A', 'B', 'C', 'D', 'E'], 4)
    [('A', 'B', 'C', 'D'), ('A', 'B', 'C', 'E'), ('A', 'B', 'D', 'E'), ('A', 'C', 'D', 'E'), ('B', 'C', 'D', 'E')]

    :param transaction: list
    :param k: int
    :return:
    """
    subsets = []

    #print 'TRANSACTION: %s - K: %s' % (transaction, k)

    if k == 1:
        return [(t,) for t in transaction]

    elif k > len(transaction):
        return []

    for i in range(0, len(transaction) - (k - 1)):
        for t in transaction_subsets(transaction[i + 1:], k - 1):
            subset = (transaction[i],) + t
            subsets.append(subset)

    return subsets


def apriori(transactions, all_items, minsup, fixed_k=None, verbose=False):
    """
    Apriori method

    :param transactions: list of iterables (list of transactions containing items)
    :param all_items: list distinct items
    :param minsup: minimum support

    >>> simple_transactions = [('007', '666', '777'), ('007', 'BC',), ('007', '666'), ('777',)]
    >>> alphabet = ['007', '666', '777', 'BC']
    >>> apriori(simple_transactions, alphabet, 0.3)
    [('B',), ('C',), ('D',)]
    >>> apriori(simple_transactions, alphabet, 0.6)
    [('B',)]
    >>> apriori(simple_transactions, alphabet, 0.5, fixed_k=2)
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
        support[new_item] = support_count(new_item, transactions)
    #    if support[item]:
        #print new_item
        #print transactions[0]
        #print support[item]

        if support[new_item] >= N * minsup:
            frequent_itemsets[1].append(new_item)

    pruned_candidates = [True]

    while pruned_candidates and pruned_candidates[0] and (not fixed_k or k < fixed_k):
        candidate_sets = _apriori_gen(frequent_itemsets[k])
        k += 1
        if verbose:
            print 'k=%s - set count %s' % (k, len(candidate_sets))
        #pruned_candidates = _prune(candidate_sets, frequent_itemsets[k-1])
        if not candidate_sets:
            break

        for tindex, t in enumerate(transactions):
            if verbose and k > 3 and tindex % (len(transactions) / 50) == 0:
                print 'Transaction %s / %s' % (tindex, len(transactions))
            candidates_subsets = transaction_subsets(t, k)
            #candidates_in_t = [candi for candi in candidates_subsets if set(candi) <= set(t)]
            #print [set(candi) for candi in candidates_subsets]
            #print '%s : %s vs %s' % (len(t), len(candidates_in_t), len(candidates_subsets))
            #print candidates_subsets
            #print t
            #if len(candidates_in_t) != len(candidates_subsets):
            #    print '######################'
            #    print candidates_in_t
            #    print candidates_subsets
            #    print '######################'

            # candidate_subsets _ARE_ always in t (why?!)
            for subset in candidates_subsets:
                support[subset] += 1

        pruned_candidates = [item for item in candidate_sets if support[item] >= N * minsup]

        #print 'Pruned K %s-itemsets - length %s' % (k, len(pruned_candidates))
        frequent_itemsets.append(pruned_candidates)

    if fixed_k:
        try:
            return frequent_itemsets[fixed_k]
        except IndexError:
            return []

    return list(itertools.chain(*frequent_itemsets))


if __name__ == "__main__":
    print 'Running doctests'
    import doctest
    res = doctest.testmod()
    if not res[0]:
        print 'OK!'
