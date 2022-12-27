import json
from dataclasses import dataclass
from functools import total_ordering
from operator import index
from typing import Iterator, Union

PacketData = list[Union[int, "PacketData"]]


@total_ordering
@dataclass(frozen=True)
class Packet:
    data: PacketData

    def __gt__(self, other):
        if not isinstance(other, Packet):
            return NotImplemented

        for items in zip(self.data, other.data):
            if isinstance(items[0], int) and isinstance(items[1], int):
                if items[0] > items[1]:
                    return True
                if items[0] < items[1]:
                    return False
                continue

            self_item = items[0] if isinstance(items[0], list) else [items[0]]
            other_item = items[1] if isinstance(items[1], list) else [items[1]]

            if Packet(self_item) > Packet(other_item):
                return True
            if Packet(self_item) < Packet(other_item):
                return False

        return len(self.data) > len(other.data)


def parse_pairs(lines: list[str]) -> Iterator[tuple[Packet, Packet]]:
    return zip(*([parse(lines)] * 2))


def parse(lines: list[str]) -> Iterator[Packet]:
    return (Packet(json.loads(line)) for line in lines if not line.isspace())


def get_decoder_key(
    packets: Iterator[Packet], divider_packets: tuple[Packet, Packet]
) -> int:
    sorted_packets = sorted([*packets, divider_packets[0], divider_packets[1]])
    return (sorted_packets.index(divider_packets[0]) + 1) * (
        sorted_packets.index(divider_packets[1]) + 1
    )
