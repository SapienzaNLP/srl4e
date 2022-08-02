import warnings

import regex
from typing import List, Union, Tuple
from collections import Counter
from itertools import groupby
from utils import deep_flatten
from nltk.tokenize import RegexpTokenizer
import edlib
# from fuzzywuzzy import fuzz


def fuzzy_search(sub, text, max_typos=3, word_borders=False, best_match=True, ignore_case=True):
    """
    Fuzzy search, i.e. search a fuzzy/approximated substring with typos and returns its span char indices in the text.
    The best match is always returned.

    :param sub: the sub to search.
    :param text: the text to search in.
    :param max_typos: maximum amount of typos (substitutions, insertions, deletions). If set to None, an unlimited
    amount of typos is considered. Note: the best match is always returned
    :param word_borders: if True, tries to match word borders
    :param best_match: if True returns the best match, otherwise returns the first enhanced match (i.e. with minimized
    typos). See regex BEST_MATCH and ENHANCED_MATCH flags for details.
    :param ignore_case: if True, ignores the text casing.
    :return: None if no match is found, otherwise a tuple (start, end) containing span start and span end.
    """
    sub = regex.escape(sub)
    r_typos = r"" if max_typos is None else fr"<={max_typos}"
    r_best_match = r"b" if best_match else r"e"
    r_borders = r"\b" if word_borders else ""
    r = r_borders + r'(?' + r_best_match + ')(' + sub + r'){e' + r_typos + r'}' + r_borders
    result = regex.search(r, text, flags=regex.IGNORECASE if ignore_case else 0)
    if result is None:
        return None
    else:
        return result.span()


def find_span_annotation_intersections(
        text: str,
        spans_annotations: List[List[str]],
        fuzzy: bool = False,
        occurrences_adjudication: Union[bool, int] = False,
        return_occurrences: bool = False,
        merge_contiguous_spans: bool = True,
        *args,
        **kwargs
):
    """
    Returns a list of intersections/adjudications between span annotations in the original text
    :param text: the original text
    :param spans_annotations: a list of annotations, where each annotation is a list of spans, i.e. a list of lists of
    spans
    :param fuzzy: whether to use builtin Python str.find(...) or a fuzzy search (also includes results with typos)
    :param occurrences_adjudication: if False, returns the intersection between all the annotations, otherwise checks
    occurrences of span annotations and returns the adjudicated (i.e. most frequent) ones. If True, by default returns
    the occurrences of all spans appearing at least one time. If an int value *x* is provided, spans occurring at least
    *x* times will be returned.
    :param return_occurrences: if True, returns a list of spans with occurrences count: [[begin, end], count].
    Otherwise only returns a list of spans: [begin, end]
    Has effects only if *occurrences_adjudication* is not False.
    :param merge_contiguous_spans: if True, merges contiguous spans. E.g. [5, 8], [8, 10] are merged into [5, 10]. This
    has effect only if *return_occurrences* is not True.
    :param args: arguments for fuzzy search
    :param kwargs: keyword arguments for fuzzy search
    :return: list of intersections (in char ranges)
    """

    def _range_intersections(a, b):
        return [(max(first[0], second[0]), min(first[1], second[1]))
                for first in a for second in b
                if max(first[0], second[0]) <= min(first[1], second[1])]

    def _get_ranges_count(a):
        """
        Given a list of indices and occurrences, groups the ranges based on occurrences
        :param a: list of (index, occurrences)
        :return: list of ((begin, end), occurrences)
        """
        a = sorted(a)
        r = []
        for k, group in groupby(a, lambda x: x[1]):
            g = list(group)
            r.append(((g[0][0], g[-1][0] + 1), k))
        return r

    assert type(spans_annotations) is list and len(spans_annotations) > 0, "spans_annotations format wrong"

    annot_span_positions = []

    # find spans in the text (converting to ranges of indices)
    for annot in spans_annotations:
        assert type(annot) is list, "spans_annotations type must be List[List[str]]"
        span_positions = []
        for span in annot:
            assert type(span) is str, "spans_annotations type must be List[List[str]]"
            if fuzzy:
                s = fuzzy_search(span, text, *args, **kwargs)
                if s is None:
                    raise ValueError(f"Could not find span '{span}' in text '{text}'. "
                                     f"Try using increasing the amount of possible typos with max_typos=N!")
                span_positions.append(s)
            else:
                pos = text.find(span)
                if pos == -1:
                    raise ValueError(f"Could not find span '{span}' in text '{text}'. "
                                     f"Try using fuzzy=True if there can be typos in the spans!")
                s = (pos, pos + len(span))
                span_positions.append(s)
        annot_span_positions.append(span_positions)

    # check spans occurrences
    if type(occurrences_adjudication) is int or (type(occurrences_adjudication) is bool and occurrences_adjudication is True):
        if type(occurrences_adjudication) is bool and occurrences_adjudication is True:
            occurrences_adjudication = 1
        occ = list(range(len(text)))
        for annot in annot_span_positions:
            for span in annot:
                occ += list(range(span[0], span[1]))
        c = Counter(occ)
        c.subtract(Counter(list(range(len(text)))))
        occ = sorted(c.most_common())
        result = _get_ranges_count(occ)
        result = list(filter(lambda x: x[1] >= occurrences_adjudication, result))
        if not return_occurrences:
            result = [r[0] for r in result]
        if not return_occurrences and merge_contiguous_spans:
            new_result = []
            for r in result:
                if len(new_result) == 0:
                    new_result.append(r)
                elif new_result[-1][1] == r[0]:
                    new_result[-1] = (new_result[-1][0], r[1])
                else:
                    new_result.append(r)
            result = new_result

    else:  # return spans intersections
        result = annot_span_positions[0]
        for i in range(1, len(annot_span_positions)):
            result = _range_intersections(result, annot_span_positions[i])

    return result

def longest_common_substring(s1, s2, return_indices=True):
    '''
    Solution to longest common substring problem. Can also be used with lists (longest common subsequence)
    :param s1: first string
    :param s2: second string
    :param return_indices: whether to return indices (in s1) or substring
    :return: longest common substring. (indices refer to s1)
    '''
    m = [[0] * (1 + len(s2)) for _ in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
       for y in range(1, 1 + len(s2)):
           if s1[x - 1] == s2[y - 1]:
               m[x][y] = m[x - 1][y - 1] + 1
               if m[x][y] > longest:
                   longest = m[x][y]
                   x_longest = x
           else:
               m[x][y] = 0
    return x_longest - longest, x_longest if return_indices else s1[x_longest - longest: x_longest]

def split_longest_common_substrings(sub, text, tokenizer, max_typos=1):
    '''

    :param sub: the substring to search
    :param text: text to search in
    :param max_typos: Uses fuzzy_search to search a span with typos in *text*. If None, an unlimited number of typos
    will be considered.
    :return: The string splitted in an optimal manner.
    '''
    def _split_list(_sub: list, _text: list):
        if len(_sub) <= 1:
            return _sub
        else:
            # lcs = longest_common_substring(_sub, _text, return_indices=True)
            # todo:there's a bug returning wrong capitalization.
            #      e.g. test sub="come stai bene grazie tu bene", text="Ciao cOMe stai io beNe graZie e tu bEne ancHio"
            #      returns ['cOMe stai', 'beNe graZie', 'tu beNe'], where the second 'beNe' is wrong (should be 'bEne').
            #      in fact, _sub must be taken from _sub indices while _text must be taken from _text indices! It is
            #      fine in our case, since the correct indices will be associated correctly in a later stage, because
            #      capitalization will not be considered. However, keep in mind that if the application is case
            #      sensitive, there could be issues. To solve
            #      this we would just need to replace [" ".join(_sub[lcs[0]:lcs[1]])] with [" ".join(_text[X:Y])],
            #      but giving correct X and Y indices to search in _text for the same span found for _sub. This could be
            #      done by forcing longest_common_substring to return the found indices also for s2, and using the
            #      returned s2 indices as X and Y (i.e. in this case, the indices finding the span in _text).
            # _.lower() is necessary to avoid a bug associating wrong word if capitalized in a different way
            lcs = longest_common_substring([x.lower() for x in _sub], [x.lower() for x in _text], return_indices=True)
            return _split_list(_sub[: lcs[0]], _text) + [" ".join(_sub[lcs[0]:lcs[1]])] + _split_list(_sub[lcs[1]:], _text)

    def _split_str(_sub: str, _text: str):
        if len(_sub) == 0:
            return []
        else:
            # lcs = longest_common_substring(_sub, _text, return_indices=True)
            # todo:there's a bug returning wrong capitalization.
            #      e.g. test sub="come stai bene grazie tu bene", text="Ciao cOMe stai io beNe graZie e tu bEne ancHio"
            #      returns ['cOMe stai', 'beNe graZie', 'tu beNe'], where the second 'beNe' is wrong (should be 'bEne').
            #      in fact, _sub must be taken from _sub indices while _text must be taken from _text indices! It is
            #      fine in our case, since the correct indices will be associated correctly in a later stage, because
            #      capitalization will not be considered. However, keep in mind that if the application is case
            #      sensitive, there could be issues. To solve
            #      this we would just need to replace [" ".join(_sub[lcs[0]:lcs[1]])] with [" ".join(_text[X:Y])],
            #      but giving correct X and Y indices to search in _text for the same span found for _sub. This could be
            #      done by forcing longest_common_substring to return the found indices also for s2, and using the
            #      returned s2 indices as X and Y (i.e. in this case, the indices finding the span in _text).
            # _.lower() is necessary to avoid a bug associating wrong word if capitalized in a different way
            lcs = longest_common_substring(_sub.lower(), _text.lower(), return_indices=True)
            return _split_str(_sub[: lcs[0]].strip(), _text) + [_sub[lcs[0]:lcs[1]]] + _split_str(_sub[lcs[1]:].strip(), _text)


    tokenizer = RegexpTokenizer(r'\w+')
    sub_split = tokenizer.tokenize(sub) # word_tokenize(sub.replace(".", " . "))
    text_split = tokenizer.tokenize(text) # word_tokenize(text.replace(".", " . "))
    if len(text_split) == 0:
        return None
    for w in range(len(sub_split)):
        # a list composed of tuples [edit_distance, word]
        ordered_matches = sorted([(edlib.align(x.lower(), sub_split[w].lower())["editDistance"], x) for x in text_split])
        edit_dist, best_match = ordered_matches[0]
        if edit_dist > max_typos:
            return None
        else:
            sub_split[w] = best_match
    first_split = _split_list(sub_split, text_split)  # spell correction, typos and copypaste correction
    second_split = deep_flatten([_split_str(s, text) for s in first_split])  # real splitting on original text
    return second_split

def merge_contiguous_spans(original_text: str, spans: List[Tuple], max_distance=2, allowed_chars=(" ", "-", "'", '"', "`", "‘", "’", "“", "”")):
    allowed_chars = set(allowed_chars)
    if len(spans) == 0:
        warnings.warn("spans is an empty list!")
        return []

    spans = sorted(spans)
    new_spans = [spans[0]]
    for i in range(1, len(spans)):
        before_begin, before_end = new_spans[-1]
        next_begin, next_end = spans[i]
        l = len(original_text)
        assert before_begin <= l and before_end <= l and next_begin <= l and next_end <= l, "Span indices must be <= len(original_text)"
        assert before_begin >= 0 and before_end >= 0 and next_begin >= 0 and next_end >= 0, "Span indices must be >= 0."
        assert before_begin <= before_end and next_begin <= next_end and before_end <= next_begin, "Spans are overlapping or have inconsistencies."
        if before_end - next_begin <= max_distance and all(c in allowed_chars for c in original_text[before_end:next_begin]):

            new_spans[-1] = (before_begin, next_end)  # merge
        else:
            new_spans.append((next_begin, next_end))  # do not merge
    return new_spans

def end_overlap(a, b):
    '''
    Returns the amount of characters of overlapping between the end of string a and the beginning of string b
    :param a: first string
    :param b: last string
    :return: amount of characters of overlapping between the end of string a and the beginning of string b
    '''
    for i in range(0, len(a)):
        if b.startswith(a[-i:]):
            return i
    return 0