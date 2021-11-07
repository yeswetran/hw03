# hw03

I created this repo for [a homework assignment](https://github.com/mikeizbicki/cmc-csci040/tree/2021fall/hw_03) in [Mike Izbicki's CSCI040 course.](https://github.com/mikeizbicki/cmc-csci040)

Using the `requests` and `bs4` libraries, `ebay-dl.py` downloads and extracts the first 10 webpage results for a given eBay search term. As examples, I have conducted eBay searches for "claremont mckenna," "pomona college," and "donald trump autograph."

To generate the results as json files, type each of the following into the command line:
```
$ python ebay-dl.py 'claremont mckenna'
$ python ebay-dl.py 'pomona college'
$ python ebay-dl.py 'donald trump autograph'
```

To generate the results as csv files, type the commands with a `--csv` flag, as so:
```
$ python ebay-dl.py 'claremont mckenna' --csv
$ python ebay-dl.py 'pomona college' --csv
$ python ebay-dl.py 'donald trump autograph' --csv
```
