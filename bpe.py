"""
BPE from lazy heap. (merging tokens by highest bigram frequency.
ties broken by lexicographic order of resulting token.

Naming convention:
    - token_id or id (int) refer to the integer id of a token.
    - token or tok (bytes) refer to the content of a token
"""
from collections import Counter, defaultdict
from dataclasses import dataclass
import heapq
import itertools
from typing import Iterable, Self

import regex


class Node:
    content: int
    prev: Self | None
    next: Self | None

    def __init__(self, content):
        self.content = content


class LinkedList:
    sentinel: Node

    def __init__(self):
        self.sentinel = Node(-1)
        self.sentinel.prev = self.sentinel.next = self.sentinel

    def append(self, content) -> Node:
        last = self.sentinel.prev
        node = last.next = self.sentinel.prev = Node(content)
        node.prev, node.next = last, self.sentinel
        return node

    def iter_nodes(self):
        node = self.sentinel.next
        while node.next is not self.sentinel:
            yield node


def tokenize(corpus: str, max_vocab_size: int, special_token_strs: list[str]) -> tuple[bytes]:
    vocab, token_id_ll = pre_tokenize(corpus)
    bigram_to_count: dict[tuple[int, int], int] = Counter()
    bigram_heap_lazy: list[tuple[int, bytes, tuple[int, int]]] = []  # (-count, token, bigram)
    bigram_to_nodes_lazy: dict[tuple[int, int], list[Node[int]]]  = defaultdict(list)
    def new_heap_tup(bigram: tuple[int, int]):
        count = bigram_to_count[bigram]
        return (-count, bytes(vocab[bigram[0]] + vocab[bigram[1]]), bigram)
    """
    invariants:
        bigram_heap_lazy: Only push to heap when a new bigram is added to bigram_to_count.
            (exception: lazy update involves a pop of bigram with stale count
                immediately followed by push of same bigram with true count.)
        bigram_to_nodes_lazy: Guaranteed that value is a superset of all valid bigrams.
            Will need to prune invalid nodes.
    """

    for node in token_id_ll.iter_nodes():
        if node.next is token_id_ll.sentinel:
            break
        bigram = node.content, node.next.content
        bigram_to_count[bigram] += 1
        bigram_to_nodes_lazy[bigram].append(node)
    for bigram, count in bigram_to_count.items():
        heapq.heappush(bigram_heap_lazy, new_heap_tup(bigram))

    while len(vocab) < max_vocab_size:
        neg_count, _, bigram = heapq.heappop(bigram_heap_lazy)
        count = -neg_count
        assert count >= 0
        if count == 0:
            continue
        if count != bigram_to_count[bigram]:  # stale
            heapq.heappush(bigram_heap_lazy, new_heap_tup(bigram)))
            continue

        # Add token to vocabulary
        new_id = len(vocab)
        vocab.append(vocab[bigram[0]] + vocab[bigram[1]])

        # Update token_id_linked_list
        new_bigrams = set()
        for node_a in bigram_to_nodes_lazy[bigram]:
            node_b = noda_a.next
            if node_b is None:
                continue
            if bigram != (node_a.content, node_b.content):
                continue
            # splice in merged node
            merged_node = Node(new_id)
            merged_node.prev = node_a.prev
            merged_node.next = node_b.next
            # invalidate old nodes
            node_a.prev = node_a.next = None
            node_b.prev = node_b.next = None

            # Update counts
            old_seq = (merged_node.prev.content, node_a.content, node_b.content,
                       merged_node.next.content)
            new_seq = (merged_node.prev.content, merged_node.content,
                       merged_node.next.content)
            for bigram in itertools.pairwise(old_seq):
                bigram_to_count[bigram] -= 1
            for bigram in itertools.pairwise(new_seq):
                if bigram[0] in special_token_ids or bigram[1] in special_token_ids:
                    continue  # Do not add bigrams containing special tokens
                bigram_to_count[bigram] += 1
                new_bigrams.add(bigram)
        # Update heap
        for bigram in new_bigrams:
            heapq.heappush(bigram_heap_lazy, new_heap_tup(bigram))
    return vocab


def pre_tokenize_embarassingly_parallel(chunks: Iterable[str], end_token_str: str):
    # SOMEDAY
    pass


def pre_tokenize(corpus: str, end_token_str: str, special_token_strs: list[str]
                 ) -> tuple[tuple[bytes], LinkedList]:
    GPT2_PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
    chunks: list[str] = corpus.split(end_token_str)
    vocab_set: set(bytes) = set()
    ll = LinkedList()

    # Add special tokens
    # # NOTE: No parsing for general special tokens yet.
    #   SOMEDAY: Call corpus.split() avoid with special_token_strs instead.
    assert end_token_str in special_token_strs:
    for s in special_tokens_strs:
        vocab_set.add(s.encode())

    # Add tokens corresponding to each byte 0-255
    for i in range(256):
        token = bytes([i])
        vocab_set.add(bytes([i]))

    # Add all other tokens
    for chunk in chunks:
        for match in regex.finditer(GPT2_PAT, document):
            next_tok = match.group().encode()
            vocab_set.add(next_tok)
            ll.append(next_tok)
        ll.append(end_token_str.encode())
    return tuple(vocab_set), ll
