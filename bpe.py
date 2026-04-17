"""
BPE from lazy heap. (merging tokens by highest bigram frequency.
ties broken by lexicographic order of resulting token.

Naming convention:
    - token_id or id (int) refer to the integer id of a token.
    - token or tok (bytes) refer to the content of a token
"""
from collections import Counter
from dataclasses import dataclass
import heapq

from typing import Iterable, Self


class LinkedList:
    class Node:
        content: int
        prev: Self | None
        next: Self | None
        def __init__(self, content):
            self.content = content

    sentinel: Node
    def __init__(self):
        self.sentinel = Node(-1)
        self.sentinel.prev = self.sentinel.next = self.sentinel

    def append(self, content) -> Node:
        last = self.sentinel.prev
        node = last.next = self.sentinel.prev = Node(content)
        node.prev, node.next = last, self.sentinel
        return node

    @property
    def first(self):
        if self.sentinel.next is self.sentinel:
            return None
        return self.sentinel.next

    @property
    def last(self):
        if self.sentinel.prev is self.sentinel:
            return None
        return self.sentinel.prev


def tokenize(corpus: str, max_vocab_size: int, special_token_strs: list[str]):
    vocab_dict, token_id_ll = pre_tokenize(corpus)
    bigram_to_count: dict[tuple[int, int], int] = Counter()
    bigram_heap_lazy: list[tuple[int, bytes, int, int]] = []  # (-count, token, id_a, id_b)
    bigram_to_nodes_lazy: dict[tuple[int, int], list[Node[int]]]  = {}

    while len(vocabulary) < max_vocab_size:
        pass


def pre_tokenize_embarassingly_parallel(chunks: Iterable[str], end_token_str: str):
    # SOMEDAY
    pass


def pre_tokenize(corpus: str, end_token_str: str) -> tuple[dict[bytes, int], LinkedList]:
    GPT2_PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
    chunks: list[str] = corpus.split(end_token_str)
    vocab_dict: dict[bytes, int] = {}
    ll = LinkedList()

    # Add special tokens
    # # NOTE: No support for general special tokens yet.
    # special_token_strs = [end_token_str]  # TODO: use parameter instead
    # for s in special_tokens_strs:
    #     token = s.encode()
    #     if token not in vocab_dict.keys():
    #         vocab_dict[token] = len(vocab_dict)

    # Add tokens corresponding to each byte 0-255
    for i in range(256):
        token = bytes([i])
        if token not in vocab_dict.keys():
            vocab_dict[token] = len(vocab_dict)

    # Add all other tokens
    vocab_dict.append()
    for chunk in chunks:
        for match in regex.finditer(GPT2_PAT, document):
            next_tok = match.group().encode()
            ll.append(next_tok)
            if next_tok not in vocab_dict.keys():
                vocab_dict[next_tok] = len(vocab_dict)
                vocab_dict.append(next_tok)
        ll.append(end_token_str.encode())
    return vocab_dict, ll
