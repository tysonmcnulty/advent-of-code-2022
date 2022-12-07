from re import match


class DatastreamBuffer:
    def __init__(self, data_stream: str):
        self.data_stream = data_stream

    def __eq__(self, other):
        if isinstance(other, DatastreamBuffer):
            return self.data_stream == other.data_stream
        else:
            return NotImplemented

    def _find_marker(self, marker_length: int):
        for i in range(marker_length, len(self.data_stream)):
            unique_chars = set()
            for char in self.data_stream[i - marker_length : i]:
                if char in unique_chars:
                    break
                unique_chars.add(char)

            if len(unique_chars) == marker_length:
                return i

    @property
    def first_start_of_packet_marker(self):
        return self._find_marker(4)

    @property
    def first_start_of_message_marker(self):
        return self._find_marker(14)


def parse(data: str) -> DatastreamBuffer:
    return DatastreamBuffer(data.strip())
