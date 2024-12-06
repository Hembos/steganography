from enum import Enum


class WorkType(Enum):
    ENCODE = 0
    DECODE = 1

class FileWorkType(Enum):
    IMAGE = 0
    AUDIO = 1
    VIDEO = 2

class Work:
    type: WorkType
    fileType: FileWorkType
    inFile: str
    toFile: str
    outFile: str

def check_work(work: Work) -> bool:
    return True