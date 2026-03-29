from datetime import datetime, UTC

PROGRAM_START = datetime.now(UTC).astimezone()
LOCAL_TIME = PROGRAM_START.tzinfo

