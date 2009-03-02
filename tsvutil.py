import sys

warning_count = 0
warning_max = 20
def warning(s):
  global warning_count
  warning_count += 1
  if warning_count > warning_max: return
  print>>sys.stderr, "WARNING: %s" % s

def cell_text_clean(text):
  s = text.encode("utf8")
  if "\t" in s: warning("Clobbering embedded tab")
  if "\n" in s: warning("Clobbering embedded newline")
  if "\r" in s: warning("Clobbering embedded carriage return")
  s = s.replace("\t"," ").replace("\n"," ").replace("\r"," ")
  return s

