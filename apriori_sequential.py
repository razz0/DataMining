"""Implementation of the Apriori algorithm for sequential patterns, F(k-1) x F(k-1) variant.

Model sequences like ((1, 2, 3), (4, 5), (4, 6)).
"""

from collections import defaultdict
import copy
import itertools


def flatten(sequence):
    """Flatten events in sequence elements to list of events"""
    return [event for element in sequence for event in element]


def subsequence(seq1, seq2):
    """Check if seq1 is a subsequence of seq2

    >>> subsequence(((2,), (3, 5)), ((2, 4), (3, 5, 6), (8,)))
    True
    >>> subsequence(((1,), (2,)), ((1, 2), (3, 4)))
    False
    >>> subsequence(((2,), (4,)), ((2, 4), (2, 4), (2, 5)))
    True
    """
    seq = copy.deepcopy(seq1)
    for element in seq2:
        if seq and set(seq[0]) <= set(element):
            seq = seq[1:]

    return True if not seq else False


def support_count(sequence, seq_list):
    """
    Count support count for sequence

    :param itemset: items to measure support count for
    :param transactions: list of sets (all transactions)

    >>> simple_seqs = [((1,), (2, 3)), ((2,), (3,)), ((2, 4,),), ((4,),)]
    >>> [support_count(((item,),), simple_seqs) for item in range(1, 5)]
    [1, 3, 2, 2]
    """
    return len([seq for seq in seq_list if subsequence(sequence, seq)])


def _sequential_candidate_generation(sequences, k):
    """
    Generate candidate sequences

    :param sequences: list of sequences containing elements containing events
    :param k: > 1

    >>> _sequential_candidate_generation([(('A',),), (('B',),), (('C',),)], 2)
    [(('A',), ('B',)), (('A', 'B'),), (('A',), ('C',)), (('A', 'C'),), (('B',), ('A',)), (('B',), ('C',)), (('B', 'C'),), (('C',), ('A',)), (('C',), ('B',))]
    >>> _sequential_candidate_generation([(('A', 'B'),), (('A', 'C'),), (('B',), ('C',))], 3)
    [('A', 'B', 'C')]
    >>> _sequential_candidate_generation([(('A',), ('B',)), (('A', 'C'),), (('B', 'C'),), (('C', 'C'),)], 3)
    [(('A',), ('B', 'C')), (('A', 'C', 'C'),), (('B', 'C', 'C'),)]
    """

    new_candidates = []
    for index1, seq1 in enumerate(sequences):
        for index2, seq2 in enumerate(sequences):
            if index1 == index2:
                continue
            seq1_flattened = flatten(seq1)
            seq2_flattened = flatten(seq2)
            if k == 2:
                # Assume we get 1-sequences like we should
                new_candidates.append((seq1[0], seq2[0],))
                if seq1[0] < seq2[0]:
                    new_candidates.append(((seq1[0] + seq2[0]),))
            elif k > 2:
                if seq1_flattened[1:] == seq2_flattened[:-1]:
                    new_sequence = copy.deepcopy(seq1)
                    if len(seq2[-1]) > 1:
                        new_sequence = new_sequence[:-1] + (new_sequence[-1] + (seq2_flattened[-1],),)
                    else:
                        new_sequence += (seq2_flattened[-1][-1],)
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


def apriori_sequential(sequences, sequence_list, minsup, fixed_k=None, verbose=False):
    """
    Apriori method for sequential patterns

    :param transactions: list of iterables (list of transactions containing items)
    :param all_items: list distinct items
    :param minsup: minimum support

    >>> simple_sequences = [(('007', '666', '777'), ('007', 'BC',), ('007', '666'), ('777',)), \
                            ((), ('007',), ('666',), ('BC',))]
    >>> alphabet = ['007', '666', '777', 'BC']
    >>> apriori_sequential(simple_sequences, alphabet, 0.3)
    [('007',), ('666',), ('777',), ('007', '666')]
    >>> apriori_sequential(simple_sequences, alphabet, 0.6)
    [('007',)]
    >>> apriori_sequential(simple_sequences, alphabet, 0.5, fixed_k=2)
    [('007', '666')]
    >>> apriori_sequential(simple_sequences, alphabet, 0.75)
    [('007',)]
    >>> apriori_sequential(simple_sequences, alphabet, 0.9)
    []
    """

    sequence_list = sorted(list(sequence_list))

    k = 1
    N = len(sequences)

    frequent_sequences = [[], []]  # k index, zero always empty
    support = defaultdict(int)

    for seq in sequence_list:
        new_seq = (seq,)
        support[new_seq] = support_count(new_seq, sequences)

        if support[new_seq] >= N * minsup:
            frequent_sequences[1].append(new_seq)

    pruned_candidates = [True, 'dummy']

    while pruned_candidates and len(pruned_candidates) > 1 and (not fixed_k or k < fixed_k):
        candidate_sets = _sequential_candidate_generation(frequent_sequences[k], k)
        k += 1
        if verbose:
            print 'k=%s - set count %s - support list length %s' % (k, len(candidate_sets), len(support))
        if not candidate_sets:
            break

        candidate_sets_as_set = set(candidate_sets)

        for tindex, t in enumerate(sequences):
            if verbose and k > 3 and tindex % (len(sequences) / (100 * (k - 3))) == 0:
                print 'Transaction %s / %s' % (tindex, len(sequences))
            subsets = transaction_subsets(t, k)

            for subset in subsets:
                if set([subset]) <= candidate_sets_as_set:
                    support[subset] += 1

        # Free up some memory
        for key in [removable for removable in support.iterkeys() if len(removable) < k]:
            del support[key]

        pruned_candidates = [seq for seq in candidate_sets if support[seq] >= N * minsup]

        frequent_sequences.append(pruned_candidates)

    if fixed_k:
        try:
            return frequent_sequences[fixed_k]
        except IndexError:
            return []

    return list(itertools.chain(*frequent_sequences))


if __name__ == "__main__":
    print 'Running doctests'
    import doctest
    res = doctest.testmod()
    if not res[0]:
        print 'OK!'
