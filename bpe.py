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

def tokenize(corpus: str, max_vocab_size: int, special_tokens: list[str]):
    vocabulary: tuple[bytes] = ()
    token_to_token_id: dict[bytes, int]
    bigram_to_count: dict[tuple[int, int], int] = Counter()
    bigram_heap_lazy: list[tuple[int, bytes, int, int]] = []  # (-count, token, id_a, id_b)
    token_id_lists: list[LinkedList] = LinkedList()
    bigram_to_nodes_lazy: dict[tuple[int, int], list[Node[int]]]  = {}

    # Edge Case: suppose we have two different bigram merges resulting the the same token.
    #   This should result in the same token_id.

    while len(vocabulary) < max_vocab_size:
        pass
        

def pre_tokenize():
    # TODO: Use GPT-2 regex
    # LATER: parallelization
    pass


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
