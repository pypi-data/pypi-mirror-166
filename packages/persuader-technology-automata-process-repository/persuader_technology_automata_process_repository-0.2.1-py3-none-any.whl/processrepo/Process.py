from dataclasses import dataclass, field
from enum import Enum

from processrepo.ProcessRunProfile import RunProfile


class ProcessStatus(str, Enum):
    INITIALIZED = 'initialized'
    RUNNING = 'running'
    IDLE = 'idle'
    ERROR = 'error'
    STOPPED = 'stopped'
    DISABLED = 'disabled'
    UNKNOWN = 'unknown'

    @staticmethod
    def parse(value):
        result = [member for name, member in ProcessStatus.__members__.items() if member.value.lower() == value.lower()]
        return result[0]


@dataclass
class Process:
    market: str
    name: str
    version: str
    instant: int
    run_profile: RunProfile = field(default=RunProfile.ASAP)
    status: ProcessStatus = field(default=ProcessStatus.UNKNOWN)
