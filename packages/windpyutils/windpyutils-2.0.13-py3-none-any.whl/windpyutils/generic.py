# -*- coding: UTF-8 -*-
""""
Created on 31.01.20
This module contains generic utils

:author:     Martin Dočekal
"""
import heapq
import math
from typing import Sequence, List, Tuple, Iterable, Union, Any, Generator, Callable, TypeVar

from windpyutils.typing import Comparable


def get_all_subclasses(cls):
    """
    Searches all subclasses of given class.

    :param cls: The base class.
    :type cls: class
    """

    stack = [cls]
    sub = []
    while len(stack):
        base = stack.pop()
        for child in base.__subclasses__():
            if child not in sub:
                sub.append(child)
                stack.append(child)

    return sub


def sub_seq(s1: Sequence, s2: Sequence) -> bool:
    """
    Checks if sequence s1 is subsequence of s2,

    :param s1: First sequence.
    :type s1: Sequence
    :param s2: Second sequence.
    :type s2: Sequence
    :return: True if s1 is subsequence of s2.
    :rtype: bool
    """

    if len(s1) <= len(s2) and \
            any(s1 == s2[offset:offset + len(s1)] for offset in range(0, len(s2) - len(s1) + 1)):
        return True

    return False


def search_sub_seq(s1: Sequence, s2: Sequence) -> List[Tuple[int, int]]:
    """
    Searches all occurrences of sequence s1 in s2,

    :param s1: First sequence.
    :type s1: Sequence
    :param s2: Second sequence.
    :type s2: Sequence
    :return: List of searched spans. Span is a tuple [start, end).
        Empty list maybe return in case when there are no spans found.
    :rtype: List[Tuple[int, int]]
    :raise ValueError: When one of input sequences haves zero len.
    """

    if len(s1) == 0 or len(s2) == 0:
        raise ValueError("Both sequences must have non zero length.")

    if len(s1) <= len(s2):
        res = []
        for offset in range(0, len(s2) - len(s1) + 1):
            end_offset = offset + len(s1)
            if s1 == s2[offset:end_offset]:
                res.append((offset, end_offset))

        return res

    return []


class RoundSequence(object):
    """
    Wrapper for an Sequence that should iterate infinitely in cyclic fashion.
    """

    def __init__(self, i: Sequence):
        """
        Initialization of wrapper.

        :param i: Sequence you want to wrap.
        :type i: Sequence
        """

        self.s = i
        self.i = iter(self.s)

    def __iter__(self):
        return self.i

    def __next__(self, *args, **kwargs):
        try:
            x = next(self.i)
        except StopIteration:
            self.i = iter(self.s)
            x = next(self.i)

        return x


def compare_pos_in_iterables(a: Iterable, b: Iterable) -> bool:
    """
    Positionally invariant compare of two iterables.

    Example of two same iterables:
        [1,2,3]
        [3,2,1]

    Example of two different iterables:
        [1,2,3]
        [1,4,3]

    :param a: First iterable for comparison.
    :type a: Iterable
    :param b: Second iterable for comparison.
    :type b: Iterable
    :return: True considered the same. False otherwise.
    :rtype: bool
    """

    b = list(b)
    try:
        for x in a:
            b.remove(x)
    except ValueError:
        return False
    return len(b) == 0


class Batcher:
    """
    Allows accessing data in batches
    """

    def __init__(self, batchify_data: Union[Sequence[Any], Tuple[Sequence[Any], ...]], batch_size: int):
        """
        Initialization of batcher.

        :param batchify_data: data that should be batchified
            it could be a single sequence or tuple of sequences
            in case it is a tuple of sequences batcher will return a batch for every sequene in tuple
        :param batch_size:
        :raise ValueError: when the batch size is invalid or the sequences are of different length
        """
        if isinstance(batchify_data, tuple) \
                and any(len(x) != len(y) for x, y in zip(batchify_data[:-1], batchify_data[1:])):
            raise ValueError("Sequences are of different length")

        if batch_size <= 0:
            raise ValueError("Batch size must be positive integer.")

        self.data = batchify_data
        self.batch_size = batch_size

    def __len__(self):
        """
        Number of batches.
        """

        samples = len(self.data[0]) if isinstance(self.data, tuple) else len(self.data)
        return math.ceil(samples / self.batch_size)

    def __getitem__(self, item) -> Union[Sequence[Any], Tuple[Sequence[Any], ...]]:
        """
        Get batch on given index.

        :param item: index of a batch
        :return: Batch on given index or, in case the tuple was provided in constructor, tuple with batches.
            One for each data sequence.
        :raise IndexError: on invalid index
        """
        if item >= len(self):
            raise IndexError()

        offset = item * self.batch_size

        if isinstance(self.data, tuple):
            return tuple(x[offset:offset + self.batch_size] for x in self.data)
        else:
            return self.data[offset:offset + self.batch_size]


class BatcherIter:
    """
    Allows batching of iterables
    """

    def __init__(self, batchify_data: Union[Iterable[Any], Tuple[Iterable[Any], ...]], batch_size: int):
        """
        Initialization of batcher.

        :param batchify_data: data that should be batchified
            it could be a single iterable or tuple of iterables
            in case it is a tuple of iterables batcher will return a batch for every iterable in tuple
                the iteration is stopped when the shortest iterator is finished
        :param batch_size:
        :raise ValueError: when the batch size is invalid
        """

        if batch_size <= 0:
            raise ValueError("Batch size must be positive integer.")

        self.data = batchify_data
        self.batch_size = batch_size

    def __iter__(self) -> Generator[Union[List[Any], Tuple[List[Any], ...]], None, None]:
        """
        generates batches

        :return: generator of batches
        """

        if isinstance(self.data, tuple):
            batch = tuple([] for _ in range(len(self.data)))
            for x in zip(*self.data):
                for i, s in enumerate(x):
                    batch[i].append(s)
                if len(batch[0]) == self.batch_size:
                    yield batch
                    batch = tuple([] for _ in range(len(self.data)))

            if len(batch[0]) > 0:
                yield batch

        else:
            batch = []
            for x in self.data:
                batch.append(x)
                if len(batch) == self.batch_size:
                    yield batch
                    batch = []

            if len(batch) > 0:
                yield batch


def roman_2_int(n: str) -> int:
    """
    Converts roman number to integer.

    :param n: roman number
    :return: integer representation
    """

    conv_table = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    c = [conv_table[x] for x in n]
    return sum(-x if i < len(n) - 1 and x < c[i + 1] else x for i, x in enumerate(c))


def int_2_roman(n: int) -> str:
    """
    Converts integer to roman number.

    :param n: integer
    :return: roman number representation
    """

    def gen(remainder):
        for v, r in [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
                     (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]:
            times, remainder = divmod(remainder, v)
            yield r * times
            if remainder == 0:
                break

    return "".join(gen(n))


T = TypeVar("T")


def sorted_combinations(elements: Iterable[T], key: Callable[[Tuple[T, ...]], Comparable]) -> \
        Generator[Tuple[T, ...], None, None]:
    """
    Generator of all combinations in sorted order.
    It assumes that for a combination c and an element e, holds the following property:
        a + (e, ) >= a
    Thus adding an element to a combination could only make the new combination greater or equal to the original one.

    The time complexity is:
        O(2^n log n)
    as it uses heapq which has O(log n) for push and pop instead of constant.

    :param elements: iterable of elements that you want to combine
    :param key: Function that is used to extract a comparison key from each combination.
    :return: generator of combinations in sorted order
    """
    priority_queue = [(key((e,)), 1, (e,), i) for i, e in enumerate(elements)]  # 2. pos. assures sorting by comb len

    heapq.heapify(priority_queue)   # O(n)
    while priority_queue:   # O(2^n)
        score, _, comb, index = heapq.heappop(priority_queue)  # O(log n)
        comb: Tuple[T, ...]
        yield comb
        offset = index + 1
        for i, e in enumerate(elements[offset:]):
            new_comb = comb + (e,)
            heapq.heappush(priority_queue, (key(new_comb), len(new_comb), new_comb, i+offset))  # O(log n)
