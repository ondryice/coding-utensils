class LoggingError (RuntimeError):
  def __init__ (self, cls, *args):
    self.cls = cls
    super().__init__(*args)
class NegativeLogIndentError (LoggingError):
  def __init__ (self, cls: type):
    super().__init__(cls, f"cannot decrease {cls.__name__} indent - log cannot have negative indentation")
