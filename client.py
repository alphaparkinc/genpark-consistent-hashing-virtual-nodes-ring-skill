"""
Autonomous Agent Consistent Hashing Ring Skill
Pure Python Standard Library implementation.
"""
import hashlib
from typing import List, Dict, Optional

class ConsistentHashRing:
    """
    Consistent Hashing Ring with virtual node replica weighting.
    """
    def __init__(self, replicas: int = 100):
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)

    def add_node(self, node_id: str):
        for i in range(self.replicas):
            h = self._hash(f"{node_id}:{i}")
            self.ring[h] = node_id
        self.sorted_keys = sorted(self.ring.keys())

    def remove_node(self, node_id: str):
        for i in range(self.replicas):
            h = self._hash(f"{node_id}:{i}")
            self.ring.pop(h, None)
        self.sorted_keys = sorted(self.ring.keys())

    def get_node(self, key: str) -> Optional[str]:
        if not self.ring:
            return None
        h = self._hash(key)
        low, high = 0, len(self.sorted_keys) - 1
        idx = 0
        while low <= high:
            mid = (low + high) // 2
            if self.sorted_keys[mid] >= h:
                idx = mid
                high = mid - 1
            else:
                low = mid + 1
        return self.ring[self.sorted_keys[idx % len(self.sorted_keys)]]
