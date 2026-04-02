from logs._files import STDOUT

class LOGBASE:
  output = STDOUT

  @classmethod
  def push (cls, *values, sep=' ', end='\n', flush=False):
    if not cls.output.blocked:
      cls.output.write(*values, sep=sep, end=end, flush=flush).block()
    return cls
