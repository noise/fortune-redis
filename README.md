# Overview

This is a simple project to aid myself in learning some more python. It consists of a basic REST API for accessing fortunes (http://en.wikipedia.org/wiki/Fortune_(Unix)) that have been parsed from the original files and stored in Redis sets.

# Dependencies

This project uses Python 2.7.x, Flask, and Redis.

Linux:

```sh
sudo apt-get install redis-server
sudo pip install flask 
```

OS X:

```sh
sudo pip install flask 
brew install redis
```


# Storage Design

The following redis key patterns are used:

- fid : fortune id counter
- f/{id} : a single fortune keyed by ID
- fmod/{module} : Set of fortune ids for the named fortune-mod data set, e.g. f/bofh-excuses
- fmods : set of fortune-mod names
- u/{id}/{module}/seen : Set of seen fortune ids for a given user ID and module

# Selection algorithm

For per-user non-repeating random selection we do the following:

```sh
# choose a random fortune-mod set
mod = srandmember fmods 
# eliminate seen ids
sdiffstore u/{id}/tmp fmod/{mod} u/{id}/{mod}/seen
# random from remaining
if (scard u{id}/tmp == 0):
    # seen them all, reset
    del u/{id}/{module}/seen
    fid = srandmember fmod/{mod}
else"
    fid = srandmember u/{id}/tmp
sadd u/{id}/{mod}/seen fid
f = get f/{id}
# cleanup
del u{id}/tmp
```

# TODO

- per-user logic
- add users to a list
- keep per-user stats - counts per set, etc.
- short fortune option
- content-types - json, html, raw
- Jquery frontend
- deploy to abitrandom.net/fortune/
- user-generated content? ratings thereof?