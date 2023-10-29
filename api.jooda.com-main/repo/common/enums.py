from enum import Enum, auto


class StringEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class IntEnum(int, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class SlackChannel(StringEnum):
    DEV = "#dev"
    ERROR_LOG = "#jooda_error_log"
    WARNING_LOG = "#jooda_warning_log"
    REQUEST_REGISTERING_CHURCH = "#request_registering_church"
    ACCOUNT_INQUIRE = "#account_inquire"
    CHURCH_INQUIRE = "#church_inquire"


class ApiUrl(StringEnum):
    V1 = "api/v1/"


class ErrorCode(IntEnum):
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    DUPLICATED_KEY = 402
    FORBIDDEN = 403
    PERMISSION_DENIED = 405
    BAD_PARAMETER_RECEIVED = 406
    INTERNER_SERVER_ERROR = 500


class PastorImageState(StringEnum):
    UPDATE = "update"
    DELETE = "delete"


class ChurchMemberState(StringEnum):
    SUCCESS = "success"
    CONFIRM = "confirm"
    REJECT = "reject"
    VISITOR = "visitor"


class AccountState(StringEnum):
    ACTIVE = auto()
    IN_ACTIVE = auto()
    WAIT_FOR = auto()


class PushNotificationType(StringEnum):
    WEEKLY = "weekly"
    NOTICE = "notice"
    CALENDAR = "calendar"


class PushNotificationDomain(StringEnum):
    CHURCH = "churchs"
