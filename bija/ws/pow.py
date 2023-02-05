import time
from bija.ws.event import Event

def zero_bits(b: int) -> int:
    n = 0

    if b == 0:
        return 8

    while b >> 1:
        b = b >> 1
        n += 1

    return 7 - n

def count_leading_zero_bits(event_id: str) -> int:
    total = 0
    for i in range(0, len(event_id) - 2, 2):
        bits = zero_bits(int(event_id[i:i+2], 16))
        total += bits

        if bits != 8:
            break

    return total

def mine_event(content: str, difficulty: int, public_key: str, kind: int, tags: list=[]) -> Event:
    all_tags = [["nonce", "1", str(difficulty)]]
    all_tags.extend(tags)

    created_at = int(time.time())
    event_id = Event.compute_id(public_key, created_at, kind, all_tags, content)
    num_leading_zero_bits = count_leading_zero_bits(event_id)

    attempts = 1
    while num_leading_zero_bits < difficulty:
        attempts += 1
        all_tags[0][1] = str(attempts)
        created_at = int(time.time())
        event_id = Event.compute_id(public_key, created_at, kind, all_tags, content)
        num_leading_zero_bits = count_leading_zero_bits(event_id)

    return Event(public_key, content, created_at, kind, all_tags, event_id)
