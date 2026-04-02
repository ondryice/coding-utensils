from datetime import datetime
from io import TextIOWrapper

class LOGFILE:
  file: None|TextIOWrapper
  times: list[datetime]
  indent: int
  blocked: int
