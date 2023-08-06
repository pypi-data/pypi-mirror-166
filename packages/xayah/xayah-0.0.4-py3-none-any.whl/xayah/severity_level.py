import enum


class SeverityLevel(enum.Enum):
    BLOCKER = 'blocker'
    CRITICAL = 'critical'
    NORMAL = 'normal'
    MINOR = 'minor'
    TRIVIAL = 'trivial'
