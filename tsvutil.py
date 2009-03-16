import sys,csv,codecs

warning_count = 0
warning_max = 20
def warning(s):
  global warning_count
  warning_count += 1
  if warning_count > warning_max: return
  print>>sys.stderr, "WARNING: %s" % s

def cell_text_clean(text):
  s = text
  if isinstance(s,str):
    s = unicode(s, 'utf8', 'replace')
  #print repr(text)
  #s = unicode(text,'utf8','replace')
  #s = unicode(text,'utf8')
  if "\t" in s: warning("Clobbering embedded tab")
  if "\n" in s: warning("Clobbering embedded newline")
  if "\r" in s: warning("Clobbering embedded carriage return")
  s = s.replace("\t"," ").replace("\n"," ").replace("\r"," ")
  return s

def fix_stdio():
  sys.stdout = codecs.open('/dev/stdout','w',encoding='utf8',buffering=0)
  sys.stdout = IOWrapper(sys.stdout)

class IOWrapper:
  def __init__(self, fp):
    self.fp = fp
  def write(self,*a,**k):
    try:
      self.fp.write(*a,**k)
    except IOError as e:
      if e.errno == 32:  # broken pipe
        sys.exit(0)
      raise e

################### 
# http://docs.python.org/library/csv.html


import csv, codecs, cStringIO

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
      #s = self.reader.next()
      #return s.encode('utf-8','replace')
      return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

