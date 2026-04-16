"""
BPE from lazy heap. (merging tokens by highest bigram frequency.
ties broken by lexicographic order of resulting token.

Naming convention:
    - token_id or id (int) refer to the integer id of a token.
    - token or tok (bytes) refer to the content of a token
"""
from collections import Counter
import heapq

def tokenize(corpus: str, max_vocab_size: int, special_tokens: list[str]):
    vocabulary: tuple[bytes] = ()
    vocab_set: set[bytes] = set()
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
