class LoggingError (RuntimeError):
  def __init__ (self, cls, *args):
    self.cls = cls
    super().__init__(*args)
class NegativeLogIndentError (LoggingError):
  def __init__ (self, cls: type):
    super().__init__(cls, f"cannot decrease {cls.__name__} indent - log cannot have negative indentation")

class LoggingControl (LoggingError): ...
class LogSectionExit (LoggingControl):
  def __init__ (self, cls: type, message, instant, timestamp, runtime, flush):
    super().__init__(cls, f"interrupt / exit signal for {cls.__name__} section")
    self.note = message, instant, timestamp, runtime, flush
