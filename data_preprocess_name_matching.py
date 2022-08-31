import pycountry
import pandas as pd
import numpy as np
import difflib

# thanks to
# https://stackoverflow.com/questions/50861237/is-there-an-alternative-to-difflib-get-close-matches-that-returns-indexes-l
# mydifflib.py
from difflib import SequenceMatcher
from heapq import nlargest as _nlargest

def get_close_matches_indexes(word, possibilities, n=3, cutoff=0.6):
    """Use SequenceMatcher to return a list of the indexes of the best 
    "good enough" matches. word is a sequence for which close matches 
    are desired (typically a string).
    possibilities is a list of sequences against which to match word
    (typically a list of strings).
    Optional arg n (default 3) is the maximum number of close matches to
    return.  n must be > 0.
    Optional arg cutoff (default 0.6) is a float in [0, 1].  Possibilities
    that don't score at least that similar to word are ignored.
    """

    if not n >  0:
        raise ValueError("n must be > 0: %r" % (n,))
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))
    result = []
    s = SequenceMatcher()
    s.set_seq2(word)
    for idx, x in enumerate(possibilities):
        s.set_seq1(x)
        if s.real_quick_ratio() >= cutoff and \
           s.quick_ratio() >= cutoff and \
           s.ratio() >= cutoff:
            result.append((s.ratio(), idx))

    # Move the best scorers to head of list
    result = _nlargest(n, result)

    # Strip scores for the best n matches
    return [x for score, x in result]

def get_match(x_cleaned, regions_cleaned, regions_ISO):
    matches = get_close_matches_indexes(x_cleaned, regions_cleaned, cutoff = 0.65)

    if len(matches) == 0:
        print('WARNING: region with unknown modern name: ' + x_cleaned)

    if len(matches) > 0:
        used_name = regions_ISO[matches[0]]
        if len(matches) > 1:
            print('WARNING: ambigious iso for: ' + x_cleaned + ': [ ' + 
                  regions_cleaned[matches].to_string().replace('\n', ', ') + '] ->' + 
                  used_name)

        return used_name
    else:
        return None
