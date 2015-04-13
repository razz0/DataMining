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
    return len([row for row in transactions if set(itemset) <= set(row)])


def _apriori_gen(frequent_sets):
    """
    Generate candidate itemsets

    :param frequent_sets: list of tuples, containing frequent itemsets [ORDERED]

    >>> _apriori_gen([('A',), ('B',), ('C',)])
    [('A', 'B'), ('A', 'C'), ('B', 'C')]
    >>> _apriori_gen([('A', 'B'), ('A', 'C'), ('B', 'C')])
    [('A', 'B', 'C')]
    >>> _apriori_gen([tuple(item) for item in ['ABC', 'ABD', 'ABE', 'ACD', 'BCD', 'BCE', 'CDE']])
    [('A', 'B', 'C', 'D'), ('A', 'B', 'C', 'E'), ('A', 'B', 'D', 'E'), ('B', 'C', 'D', 'E')]
    >>> cc = [('55015', '55314'), ('55015', '55315'), ('55314', '55315'), ('57016', '57017'), ('57043', '57047'), ('581325', '582103')]
    >>> _apriori_gen(cc)
    [('55015', '55314', '55315')]
    """

    new_candidates = []
    for index, frequent_item in enumerate(frequent_sets):
        for next_item in frequent_sets[index + 1:]:
            if len(frequent_item) == 1:
                new_candidates.append(tuple(frequent_item) + tuple(next_item))
            elif frequent_item[:-1] == next_item[:-1]:
                new_candidates.append(tuple(frequent_item) + (next_item[-1],))
            else:
                break

    return new_candidates


def generate_transaction_subsets(transaction, k):
    """
    Get subsets of transactions of length k

    >>> generate_transaction_subsets(['A', 'B', 'C', 'D', 'E'], 4)
    [('A', 'B', 'C', 'D'), ('A', 'B', 'C', 'E'), ('A', 'B', 'D', 'E'), ('A', 'C', 'D', 'E'), ('B', 'C', 'D', 'E')]

    :param transaction: list
    :param k: int
    :return:
    """
    subsets = []

    if k == 1:
        return [(t,) for t in transaction]

    elif k > len(transaction):
        return []

    elif k == len(transaction):
        return [tuple(transaction)]

    elif k == len(transaction) - 1:
        for i in reversed(range(0, len(transaction))):
            subset = tuple(transaction[:i] + transaction[i + 1:])
            subsets.append(subset)

    else:
        for i in range(0, len(transaction) - (k - 1)):
            for t in generate_transaction_subsets(transaction[i + 1:], k - 1):
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
    [('007',), ('666',), ('777',), ('007', '666')]
    >>> apriori(simple_transactions, alphabet, 0.6)
    [('007',)]
    >>> apriori(simple_transactions, alphabet, 0.5, fixed_k=2)
    [('007', '666')]
    >>> apriori(simple_transactions, alphabet, 0.75)
    [('007',)]
    >>> apriori(simple_transactions, alphabet, 0.9)
    []
    """

    all_items = sorted(list(all_items))

    k = 1
    N = len(transactions)

    frequent_itemsets = [[], []]  # k index, zero always empty
    support = defaultdict(int)
    transaction_subsets = dict()

    for item in all_items:
        new_item = (item,)
        support[new_item] = support_count(new_item, transactions)

        if support[new_item] >= N * minsup:
            frequent_itemsets[1].append(new_item)

    pruned_candidates = [True, 'dummy']

    while pruned_candidates and len(pruned_candidates) > 1 and (not fixed_k or k < fixed_k):
        candidate_sets = _apriori_gen(frequent_itemsets[k])
        k += 1
        if verbose:
            print 'k=%s - set count %s - support list length %s' % (k, len(candidate_sets), len(support))
        if not candidate_sets:
            break

        #candidate_sets_as_set = set(candidate_sets)

        # TODO: Optimize by looping through candidates instead of all transactions.
        # TODO: Check if any of the immediate subsets is infrequent and prune if so.

        for tindex, t in enumerate(transactions):
            if verbose and k > 3 and tindex % (len(transactions) / (100 * (k - 3))) == 0:
                print 'Transaction %s / %s' % (tindex, len(transactions))
            subsets = generate_transaction_subsets(t, k)

            for subset in subsets:
                if subset not in frequent_itemsets[len(subset)]:
                    break
                if subset in candidate_sets:
                #if set([subset]) <= candidate_sets_as_set:
                    support[subset] += 1

        # Free up some memory
        for key in [removable for removable in support.iterkeys() if len(removable) < k]:
            del support[key]

        pruned_candidates = [item for item in candidate_sets if support[item] >= N * minsup]

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
