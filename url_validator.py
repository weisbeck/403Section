#!/usr/bin/env python
"""
Usage: url_validator.py -f [FILE]

https://github.com/scrapy/scrapy
"""

import optparse
import sys
import string
import re

from scrapy.utils.url import canonicalize_url
"""https://github.com/scrapy/scrapy"""

def read_file(f):
  '''
  Reads in a file line by line, creating an array of strings.
  '''
  urls = []
  url = ''
  for line in f:
    url = line.strip()
    if url != '':
      urls.append(url)
  return urls

def controller():
  '''
  Parses the command line arguments and returns the newly created parser,
  the arguments that have been parsed, and the options that have been parsed.
  '''
  p = optparse.OptionParser(description="URL Sorter. Takes in a file, "
                                        "sorts the URLs and then writes them "
                                        "to a file",
                          prog='url_validator.py',
                          version='0.1',
                          usage='%prog -f [FILE]')
  p.add_option('--file', '-f', dest="filename",
               help="The FILE from which we will read", metavar="FILE")
  p.add_option('--test', '-t', dest="test",
               help="The type of test we will perform")
  (opts, args) = p.parse_args()
  return (p, opts, args)

def handle_io_exception(f, ex):
    print("I/O error({1}) -- \"{0}\" : {2}".format(f, ex.errno, ex.strerror))
    sys.exit(1)
    
def validator(url):
    """
    Credit: Diego Perini
    Source: http://mathiasbynens.be/demo/url-regex
    
    Returns whether the passed URL is valid.
    """
    return bool(re.match(re.compile(ur"^(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$", re.UNICODE), url))

def canonicalizer(url):
    """
    Source: https://github.com/scrapy/scrapy
    
    Normalizes the URL.
    """
    return canonicalize_url(url)

def comparator(url1, url2):
    """
    Since each URL is a string, will just use the built in comparator for strings.
    Returns -1 if 1 < 2, 1 if 1 > 2, and 0 if they are equal
    """
    if url1 < url2:
      return -1
    elif url1 > url2:
      return 1
    else:
      return 0

def main():
  '''
  Takes in the command line arguments, selects a sorter,
  and then sorts the URLs.  After they've been sorted, the 
  URLs are written out to a file the user has selected (else
  the default file).
  '''
  (parser, opts, args) = controller()
  if not opts.filename:
    parser.print_help()
    sys.exit(1)
  filename = opts.filename
  try:
    f = open(filename, 'r')
    unsorted = read_file(f)
  except IOError as e:
    handle_io_exception(filename, e) 

  try:
    '''
    Builds the list of source and normalized urls, and then runs a checklist against each url.
    '''
    if not opts.test:
      canonized_urls = {}
      source_urls = {}
      for url in unsorted:
        if url in source_urls:
          source_urls[url] += 1
        else:
          source_urls[url] = 1
        can_url = canonicalizer(url)
        if can_url in canonized_urls:
          canonized_urls[can_url] += 1
        else:
          canonized_urls[can_url] = 1
      
      for url in unsorted:
        print("Source: " + url)
        print("Valid: " + str(validator(url)))
        can_url = canonicalizer(url)
        print("Canonical: " + can_url)
        print("Source Unique: " + str(source_urls[url] == 1))
        print("Canonicalized URL unique: " + str(canonized_urls[can_url] == 1))
    else:
      if opts.test == "canonicalizer":
        for url in unsorted:
          print("Source: " + url)
          can_url = canonicalizer(url)
          print("Canonical: " + can_url)
      elif opts.test == "comparator":
        for url1 in unsorted:
          for url2 in unsorted:
            print("Source1: " + url1)
            print("Source2: " + url2)
            print("Comparator: " + str(comparator(url1, url2)))
      elif  opts.test == "validator":
        for url in unsorted:
          print("Source: " + url)
          print("Valid: " + str(validator(url)))
          
  except IOError as e:
    handle_io_exception(output, e)

if __name__ == "__main__":
  main()
