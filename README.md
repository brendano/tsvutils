tsvutils -- utilities for processing tab-separated files
========================================================

*tsvutils* are scripts that can convert and manipulate tabular data in the TSV file format: tab-separated values, sometimes with a header.  They build on top of standard Unix utilities to allow ad-hoc, efficient, and reliable processing and summarization of tabular data from the shell.

Overview of scripts
-------------------

Convert into tsv:

* csv2tsv  - convert from Excel-compatible csv.
* json2tsv - convert from concatenated JSON records.
* xlsx2tsv - convert from Excel's .xlsx format.
* others: eq2tsv ssv2tsv uniq2tsv yaml2tsv ...

Manipulate tsv:

* tsvawk  - gives you column names in your awk.
* hwrap   - wraps pipeline process but preserves stdin's header.
* tsvcat  - concatenate tsv's, aligning common columns.
* namecut - like 'cut' but with header names.
* tabsort, tabawk - wrappers for tab delimitation.

Convert out of tsv:

* tsv2csv - convert tsv to Excel-compatible csv.
* tsv2my  - load tsv into a new MySQL table.
* tsv2fmt - format as ASCII-art table.
* tsv2html - format as HTML table.
* others: tsv2yaml tsv2tex ...

By "tsv" we mean honest-to-goodness tab-separated values, often with a header.  No quoting, escaping, or comments.  All rows should have the same number of fields.  Rows end with a unix \n newline.  Cell values cannot have tabs or newlines.

These conditions are all enforced in scripts that output tsv.  For programs that take tsv input, if these assumptions do not hold, the script's behavior is undefined.

TSV is an easy format for other programs to handle:

* After stripping the newline, split("\t") correctly parses a row.  
* To strip out the header beforehand: "tail -n+2" or "tail +2".

Weak naming convention: programs that don't work well with headers call that format "tab"; ones that either need a header or are agnostic call that "tsv".  E.g., for tabsort you don't want to sort the header, but tsv2my is impossible without the header.  csv2tsv and tsv2csv are agnostic, since a csv file may or may not have a header.


Examples: pipelines
-------------------

The TSV format is intended to work with many other pipeline-friendly programs.  Examples include:

* General
 * cat, head, tail, tail -n+X, cut, merge, diff, comm, sort, uniq, uniq -c, wc -l
* Multipurpose
 - perl -pe, ruby -ne, awk, sed, tr
* SQL to TSV
 - echo 'select a,b from bla' | mysql
 - echo a b | ssv2tsv; echo "select a,b from bla" | sqlite3 -separator $(echo -e '\t')
 - echo a b | ssv2tsv; echo "select a,b from bla" | psql -tqAF $(echo -e '\t')
* GUI to TSV
 - Excel: copy-and-paste cells <-> text as tsv (though kills double quotes)
 - Web browsers: copy rendered HTML table -> text as tsv
* Misc
 - [pv][] (Highly recommended!)
 - [shuffle][]
 - [md5sort][]
 - [setdiff][]

The tsvutils scripts' comments include further examples.


[shuffle]: http://www.w3.org/People/Bos/Shuffle
[md5sort]: http://gist.github.com/22959
[setdiff]: http://gist.github.com/22958
[pv]: http://www.ivarch.com/programs/pv.shtml


Examples: Named columns in programs
-----------------------------------

Here are examples of parsing TSV-with headers in several script-y languages, such that you get to refer to columns by their names, instead of positions.  This makes the scripts much more maintainable.

_Python_ has a built-in facility for TSV-with-headers:

    tsv_reader = lambda f: csv.DictReader(f, dialect=None, delimiter='\t', quoting=csv.QUOTE_NONE)
    for record in tsv_reader(sys.stdin):
      print record  # => hash of key/values

Or equivalently:

    cols = sys.stdin.readline()[:-1]
    for line in sys.stdin:
      vals = line[:-1].split("\t")
      record = dict((cols[j],vals[j]) for j in range(len(cols)))
      print record  # => hash of key/values

_Ruby_:

    cols = STDIN.readline.chomp.split("\t")
    STDIN.each do |line|
      vals = line.chomp.split("\t")
      record = (0...cols.size).map {|j| [cols[j], vals[j]]}.to_h
      p record  # => hash of key/values
    end


_R_ has a built-in facility:

    data = read.delim("data.tsv", sep="\t")


Installation
------------

It's probably useful to look at or tweak these scripts, so you're best off just putting the entire directory on your PATH.


The philosophy of tsvutils
--------------------------

There are many data processing and analysis situations where data consists of tables.  A "table" is a list of flat records each with the same set of named attributes, where it's easy to manipulate a particular attribute across all records -- a "column".  The main data structures in SQL, R, and Excel are tables.

TSV-with-headers sits in a sweet spot on the spectrum of data format complexity.

- A more complex alternative is to encode in arbitrarily nested structures (XML, JSON).  These have greater representational capacity, but are less convenient for data analysis.  Since they can have high structural complexity, it's often error-prone to use them -- ad-hoc querying is generally difficult.  Furthermore, it's wasteful of space to repeat key names over and over if all records are known to have the same set of keys.  Finally, when doing data analysis, especially statistical analysis, you want to turn columns into vectors, which presupposes a flatter, more table-like structure.
- A simpler alternative is a table with positional, un-named columns.  The main weakness is that for more than several columns, it's hard to remember which column is which.  Named columns improve maintainability.

But: SQL databases and Excel spreadsheets are often inconvenient data management environments compared to the filesystem on the unix commandline.  Unfortunately, the most common file format for tables is CSV, which is complex and has several incompatible versions.  It plays only moderately nicely with the unix commandline, which is the best ad-hoc processing tool for filesystem data.  Often the only correct way to handle CSV is to use a parsing library, but it's inconvenient to fire up a python/perl/ruby session just to do simple sanity checks and casually inspect data.

To balance these needs, so far I've found that TSV-with-headers is the most convenient canonical format for table data in the filesystem/commandline environment, or at least the lingua franca in shell pipelines.  These utilities are just a little bit of glue to make TSV play nicely with CSV, Excel, MySQL, and Unix tools.  Interfaces in and out of other table-centric environments could easily be added.

On the philosophy of having NO escaping or special data value conventions: If you want those things in your data, make up your own convention (like backslash escaping, URL escaping, or whatever) and have your application be aware of it.  Our philosophy is, a data processing utility should ignore that stuff in order to have safe and predictable behavior.  I've seen too many bugs because some intermediate program imposed a special meaning on "NA" or "\N" or "NULL", etc., when really a program further downstream should have had sole responsibility for this interpretation.


In Conclusion
-------------

Hope you enjoy tsvutils!

- tsvutils: http://github.com/brendano/tsvutils
- By Brendan O'Connor: http://anyall.org
