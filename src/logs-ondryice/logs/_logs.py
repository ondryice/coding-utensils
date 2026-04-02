from logs._files import STDOUT

class LOGBASE:
  output = STDOUT

  @classmethod
  def push (cls, *values, sep=' ', end='\n', flush=False):
    cls.output.write(*values, sep=sep, end=end, flush=flush)
    return cls
