def deep_flatten(element_or_list):
    '''
    Deeply flattens input list composed of nested lists.
    E.g. if element=[1,[[[2],[2.5,[2.6]]]],[[3],[4,5,[6,[[[[7]]]]]]]], output=[1, 2, 2.5, 2.6, 3, 4, 5, 6, 7]
    :param element: list to flatten
    :return: flattened list
    '''
    def _iter_all_generator(elem):
        if isinstance(elem, list):
            for el in elem:
                yield from _iter_all_generator(el)
        else:
            yield elem
    g = _iter_all_generator(element_or_list)
    return [e for e in g]