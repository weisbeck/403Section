Exercise 4 for CSE 403 quiz section.
- Peter Weisbeck
- USAGE: url_validator.py -f [FILE]
- OPTIONAL TESTING: url_validator.py -f [FILE] -t [canonicalizer, comparator, or validator]
- Regex for url validation (credit): http://mathiasbynens.be/demo/url-regex (the one by @diegoperini)
- Module containing the url canonicalizer I used (credit): https://github.com/scrapy/scrapy
	- Specific file containing canonicalizer function (canonicalize_url): https://github.com/scrapy/scrapy/blob/master/scrapy/utils/url.py

The following URL validation design is a modified form of my team (https://github.com/caylan/403Section/wiki/URL-Validation) design. My implementation differences are noted. The code implementation itself if a modified version of the team's url sorting code to handle the specifications of this exercise.

The three functions that are the URL validator, canonicalizer, and comparators are within the program, however no unit tests were made because the validator has already been tested (on the website linked), the canonicalizer is used for a webcrawler, so it must have already been tested rigorously, and the comparator I am used is merely the built-in string comparator, which is trivial to test.

URL Validation
- The URL will be checked by a regex to see if it is valid or not.

Specifying a definition for a valid URL
- We will be following the definition provided by http://www.ietf.org/rfc/rfc3986.txt to validate off of the RFC 3986 Reg-ex, where a URL is defined as having the general form: scheme://netloc/path;parameters?query#fragment.
- Personally, I ended up using the regex defined by Diego Perini, found: http://mathiasbynens.be/demo/url-regex

Defining a canonical form
- URL Normalization function: I ended up using a built in function (scrapy.utils.url import canonicalize_url) in the github project "scrapy", which is a web-crawling framework: https://github.com/scrapy/scrapy
So my definition of a canonical form aligns with theirs as defined in their function:

"""
	Canonicalize the given url by applying the following procedures:

    - sort query arguments, first by key, then by value
    - percent encode paths and query arguments. non-ASCII characters are
      percent-encoded using UTF-8 (RFC-3986)
    - normalize all spaces (in query arguments) '+' (plus symbol)
    - normalize percent encodings case (%2f -> %2F)
    - remove query arguments with blank values (unless keep_blank_values is True)
    - remove fragments (unless keep_fragments is True)

    The url passed can be a str or unicode, while the url returned is always a
    str.

    For examples see the tests in scrapy.tests.test_utils_url
"""

Defining a canonicalizer
- The canonicalizer function I used can be found here: https://github.com/scrapy/scrapy/blob/master/scrapy/utils/url.py

Defining a comparator operator for URLs (<, >, ==)
- Comparisons performed on URLs will match the results of string comparisons.