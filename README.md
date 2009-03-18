tsvutils -- utilities for processing tab-separated files
=====================================================================

*tsvutils* are scripts that can convert and manipulate the TSV file format: tab-separated values, sometimes with a header.  They are intended to allow ad-hoc but reliable processing and summarization of tabular data, with interfaces to Excel and MySQL.

github.com/brendano/tsvutils - by Brendan O'Connor - anyall.org


Convert to tsv:

* csv2tsv  - convert Excel-compatible csv to tsv.
* json2tsv - convert JSON array of records to tsv.
* ssv2tsv  - convert space-separated values to tsv.
* xlsx2tsv - convert Excel's .xlsx format to tsv.

Manipulate tsv:

* namecut - like 'cut' but with header names.
* tsvcat  - concatenate tsv's, aligning common columns.
* hwrap   - wraps pipeline process but preserves stdin's header.
* tabsort - 'sort' wrapper with tab delimiter.
* tabawk  - 'awk' wrapper with tab delimiter.

Convert out of tsv:

* tsv2csv - convert tsv to Excel-compatible csv.
* tsv2my  - load tsv into a new MySQL table.
* tsv2fmt - format as ASCII-art table.

Here, the "tsv" file format is honest-to-goodness tab-separated values, usually with a header.  No quoting, escaping, or comments.  All rows should have the same number of fields.  Rows end with a unix \n newline.  Cell values cannot have tabs or newlines.

These conditions are all enforced in scripts that convert to tsv.  For programs that convert *out* of tsv, if these assumptions do not hold, the script's behavior is undefined.

TSV is an easy format for other programs to handle: after removing the newline, split("\t") correctly parses a row.  

Note that "tail +2" or "tail -n+2" strips out a tsv file's header.

Weak naming convention: programs that don't work well with headers call that format "tab"; ones that either need a header or are agnostic call that "tsv".  E.g., for tabsort you don't want to sort the header, but tsv2my is impossible without the header.  csv2tsv and tsv2csv are agnostic, since a csv file may or may not have a header.


Examples
--------

The TSV format is intended to work with many other pipeline-friendly programs.  Examples include:

* cat, head, tail, tail -n+X, cut, merge, diff, comm, sort, uniq, uniq -c, wc -l
* perl -pe, ruby -ne, awk, sed, tr
* echo 'select a,b from bla' | mysql
* echo -e "a\tb"; echo "select a,b from bla" | sqlite3 -separator $(echo -e '\t')
* echo -e "a\tb"; echo "select a,b from bla" | psql -tqAF $(echo -e '\t')
* [shuffle][]
* [md5sort][]   
* [setdiff][]
* [mapagg][]
* [pv][]
* (GUI) Excel: copy-and-paste cells <-> text as tsv (though kills double quotes)
* (GUI) Web browsers: copy rendered HTML table -> text as tsv

[shuffle]: http://www.w3.org/People/Bos/Shuffle
[md5sort]: http://gist.github.com/22959
[setdiff]: http://gist.github.com/22958
[mapagg]: http://gist.github.com/67656
[pv]: http://www.ivarch.com/programs/pv.shtml


A common pattern is to preserve preserve the header while manipulating the rows.  For example, the following sorts a file.

    $ (head -1 file; tail +2 file | tabsort -k2) > outfile

Or equivalently:

    $ hwrap tabsort -k2 <file >outfile

Parsing TSV-with-headers in Ruby:

    cols = STDIN.readline.chomp.split("\t")
    STDIN.each do |line|
      vals = line.chomp.split("\t")
      record = (0...cols.size).map {|j| [cols[j], vals[j]]}.to_h
      pp record  # => hash of key/values
    end

Parsing TSV-with-headers in Python:

    cols = sys.stdin.readline()[:-1]
    for line in sys.stdin:
      vals = line[:-1].split("\t")
      record = dict((cols[j],vals[j]) for j in range(len(cols)))
      print record  # => hash of key/values

Or equivalently,

    tsv_reader = lambda f: csv.DictReader(f, dialect=None, delimiter='\\t', quoting=csv.QUOTE_NONE)
    for record in tsv_reader(sys.stdin):
      print record  # => hash of key/values


Installation
------------

Lots of these scripts aren't very polished -- needing fixes for python utf-8 stdin/stdout and the like -- so you're best off just putting the entire directory on your PATH in case you need to hack up the scripts.


The philosophy of tsvutil
-------------------------

Short version:

These utilities are good at data munging back and forth between MySQL and Excel.

Long version:

There are many data processing and analysis situations where data consists of tables.  A "table" is a list of flat records each with the same set of named attributes, where it's easy to manipulate a particular attribute across all records -- a "column".  The main data structures in SQL, R, and Excel are tables.  A more complex alternative is to encode in arbitrarily nested structures (XML, JSON).  Due to their potential complexity, it's always error-prone to use them.  Ad-hoc querying is generally difficult.  A simpler alternative is a table with positional, un-named columns, but it's difficult to remember which column is which.  Tables with named columns hit a sweet spot of both maintainability and simplicity.

But SQL databases and Excel spreadsheets are often inconvenient data management environments compared to the filesystem on the unix commandline.  Unfortunately, the most common file format for tables is CSV, which is complex and has several incompatible versions.  It plays only moderately nicely with the unix commandline, which is the best ad-hoc processing tool for filesystem data.  Often the only correct way to handle CSV is to use a parsing library, but it's inconvenient to fire up a python/perl/ruby session just to do simple sanity checks and casually inspect data.

To balance these needs, so far I've found that TSV-with-headers is the most convenient canonical format for table data in the filesystem/commandline environment. It's also good as a lingua franca intermediate format in shell pipelines.  These utilities are just a little bit of glue to make TSV play nicely with Excel, MySQL, and Unix tools.  Interfaces in and out of other table-centric environments could easily be added.


