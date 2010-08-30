tsvutils -- utilities for processing tab-separated files
=====================================================================

*tsvutils* are scripts that can convert and manipulate the TSV file format: tab-separated values, sometimes with a header.  They build on top of standard Unix utilities to allow ad-hoc, efficient, and reliable processing and summarization of tabular data.

github.com/brendano/tsvutils - by Brendan O'Connor - anyall.org


Convert to tsv; often from a sequence of records:

* csv2tsv  - convert from Excel-compatible csv.
* json2tsv - convert from concatenated JSON records.
* xlsx2tsv - convert from Excel's .xlsx format.
* others: eq2tsv ssv2tsv uniq2tsv yaml2tsv

Manipulate tsv; header smartness:

* tsvawk  - gives you column names in your awk.
* hwrap   - wraps pipeline process but preserves stdin's header.
* tsvcat  - concatenate tsv's, aligning common columns.
* namecut - like 'cut' but with header names.

Manipulate tsv; wrappers for Unix utilities:

* tabsort - 'sort' wrapper with tab delimiter.
* tabawk  - 'awk' wrapper with tab delimiter.

Convert out of tsv:

* tsv2csv - convert tsv to Excel-compatible csv.
* tsv2my  - load tsv into a new MySQL table.
* tsv2fmt - format as ASCII-art table.
* tsv2html - format as HTML table.
* others: tsv2yaml tsv2tex

By "tsv" we mean honest-to-goodness tab-separated values, often with a header.  No quoting, escaping, or comments.  All rows should have the same number of fields.  Rows end with a unix \n newline.  Cell values cannot have tabs or newlines.

These conditions are all enforced in scripts that convert to tsv.  For programs that convert *out* of tsv, if these assumptions do not hold, the script's behavior is undefined.

TSV is an easy format for other programs to handle:

* After stripping the newline, split("\t") correctly parses a row.  
* To strip out the header beforehand: "tail -n+2" or "tail +2".

Weak naming convention: programs that don't work well with headers call that format "tab"; ones that either need a header or are agnostic call that "tsv".  E.g., for tabsort you don't want to sort the header, but tsv2my is impossible without the header.  csv2tsv and tsv2csv are agnostic, since a csv file may or may not have a header.


Examples
--------

The TSV format is intended to work with many other pipeline-friendly programs.  Examples include:

* cat, head, tail, tail -n+X, cut, merge, diff, comm, sort, uniq, uniq -c, wc -l
* perl -pe, ruby -ne, awk, sed, tr
* echo 'select a,b from bla' | mysql
* (echo a b | ssv2tsv; echo "select a,b from bla") | sqlite3 -separator $(echo -e '\t')
* (echo a b | ssv2tsv; echo "select a,b from bla") | psql -tqAF $(echo -e '\t')
* [shuffle][]
* [md5sort][]   
* [setdiff][]
* [pv][]
* (GUI) Excel: copy-and-paste cells <-> text as tsv (though kills double quotes)
* (GUI) Web browsers: copy rendered HTML table -> text as tsv

[shuffle]: http://www.w3.org/People/Bos/Shuffle
[md5sort]: http://gist.github.com/22959
[setdiff]: http://gist.github.com/22958
[pv]: http://www.ivarch.com/programs/pv.shtml


Here are examples of parsing TSV-with headers in various languages, such that you get to refer to columns by their names, instead of positions.  This makes the scripts much more maintainable.

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

    tsv_reader = lambda f: csv.DictReader(f, dialect=None, delimiter='\t', quoting=csv.QUOTE_NONE)
    for record in tsv_reader(sys.stdin):
      print record  # => hash of key/values

Loading in R:

    data = read.delim("data.tsv", sep="\t")


Installation
------------

It's probably useful to look at or tweak these scripts, so you're best off just putting the entire directory on your PATH.


The philosophy of tsvutils
--------------------------

Short version:

These utilities are good at data munging back and forth between MySQL and Excel.

Long version:

There are many data processing and analysis situations where data consists of tables.  A "table" is a list of flat records each with the same set of named attributes, where it's easy to manipulate a particular attribute across all records -- a "column".  The main data structures in SQL, R, and Excel are tables.  A more complex alternative is to encode in arbitrarily nested structures (XML, JSON).  These have greater representational capacity, but are less convenient for data analysis.  Since they can have high structural complexity, it's often error-prone to use them -- ad-hoc querying is generally difficult.  A simpler alternative is a table with positional, un-named columns, but for more than several columns, it's hard to remember which column is which.  Tables with named columns hit a sweet spot of both maintainability and simplicity.

But SQL databases and Excel spreadsheets are often inconvenient data management environments compared to the filesystem on the unix commandline.  Unfortunately, the most common file format for tables is CSV, which is complex and has several incompatible versions.  It plays only moderately nicely with the unix commandline, which is the best ad-hoc processing tool for filesystem data.  Often the only correct way to handle CSV is to use a parsing library, but it's inconvenient to fire up a python/perl/ruby session just to do simple sanity checks and casually inspect data.

To balance these needs, so far I've found that TSV-with-headers is the most convenient canonical format for table data in the filesystem/commandline environment, or at least the lingua franca in shell pipelines.  These utilities are just a little bit of glue to make TSV play nicely with CSV, Excel, MySQL, and Unix tools.  Interfaces in and out of other table-centric environments could easily be added.

On the philosophy of having NO escaping or special data value conventions: If you want those things in your data, make up your own convention (like backslash escaping) and have your application be aware of it.  Our philosophy is, a data processing utility should ignore that stuff in order to have safe and predictable behavior.  I've seen too many bugs because some intermediate program imposed a special meaning on "NA" or "\N" etc. when really a program further downstream should have had sole responsibility for this interpretation.
