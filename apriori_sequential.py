"""Implementation of the Apriori algorithm for sequential patterns, F(k-1) x F(k-1) variant."""

from collections import defaultdict
import copy
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


def _sequential_candidate_generation(sequences, k):
    """
    Generate candidate sequences

    :param sequences: list of sequences containing elements containing events
    :param k: > 1

    >>> _sequential_candidate_generation([('A',), ('B',), ('C',)], 2)
    [('A', 'B'), ('A', 'C'), ('B', 'C')]
    >>> _sequential_candidate_generation([('A', 'B'), ('A', 'C'), ('B', 'C')], 3)
    [('A', 'B', 'C')]
    >>> _sequential_candidate_generation([('A', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'C')], 3)
    [('A', 'B', 'C'), ('A', 'C', 'C'), ('B', 'C', 'C')]
    """

    def _flatten(sequence):
        """Flatten events in sequence elements to list of events"""
        return [event for element in sequence for event in element]

    new_candidates = []
    for index, sequence in enumerate(sequences):
        for next_sequence in sequences[index + 1:]:
            if k == 2:
                # Assume we get 1-sequences like we should
                new_candidates.append((sequence[0], next_sequence[0]))
            elif k > 2:
                next_flattened = _flatten(next_sequence)
                if _flatten(sequence)[1:] == next_flattened[:-1]:
                    new_sequence = copy.deepcopy(sequence)
                    if len(next_sequence[:-1]) > 1:
                        new_sequence[-1] += (next_flattened[-1],)
                    else:
                        new_sequence += (next_flattened[-1],)
                    new_candidates.append(new_sequence)

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

    if k == 1:
        return [(t,) for t in transaction]

    elif k > len(transaction):
        return []

    for i in range(0, len(transaction) - (k - 1)):
        for t in transaction_subsets(transaction[i + 1:], k - 1):
            subset = (transaction[i],) + t
            subsets.append(subset)

    return subsets


def apriori_sequential(transactions, all_items, minsup, fixed_k=None, verbose=False):
    """
    Apriori method for sequential patterns

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

    for item in all_items:
        new_item = (item,)
        support[new_item] = support_count(new_item, transactions)

        if support[new_item] >= N * minsup:
            frequent_itemsets[1].append(new_item)

    pruned_candidates = [True, 'dummy']

    while pruned_candidates and len(pruned_candidates) > 1 and (not fixed_k or k < fixed_k):
        candidate_sets = _sequential_candidate_generation(frequent_itemsets[k], k)
        k += 1
        if verbose:
            print 'k=%s - set count %s - support list length %s' % (k, len(candidate_sets), len(support))
        if not candidate_sets:
            break

        candidate_sets_as_set = set(candidate_sets)

        for tindex, t in enumerate(transactions):
            if verbose and k > 3 and tindex % (len(transactions) / (100 * (k - 3))) == 0:
                print 'Transaction %s / %s' % (tindex, len(transactions))
            subsets = transaction_subsets(t, k)

            for subset in subsets:
                if set([subset]) <= candidate_sets_as_set:
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
