import enum


class Status(enum.Enum):
    STATUS_OK = 0
    STATUS_NOT_FOUND = -1


class GrabResult:
    def __init__(self, status: Status, data: str):
        self.status = status
        self.data = data
