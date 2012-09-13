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

# Running

## Load data

Assuming Redis is running on localhost:

```sh
./rfortune.py --load
```

for more options:
```sh
./rfortune.py -h 
```

## Start the server

```sh
./fortune_server.py
```
and go to http://http://0.0.0.0:5000

http://0.0.0.0:5000/help yields the full set of Resources.

## commandline fortunes

```sh
./rfortune.py
./rfortune.py -v
./rfortune.py -v --module bofh-excuses
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
if (scard u/{id}/tmp == 0):
    # seen them all, reset
    del u/{id}/{mod}/seen
    fid = srandmember fmod/{mod}
else"
    fid = srandmember u/{id}/tmp
sadd u/{id}/{mod}/seen fid
f = get f/{id}
# cleanup
del u{id}/tmp
```

# TODO

- add users to a list
- keep per-user stats - counts per set, etc.
- short fortune option
- content-types - json, html, raw
- Jquery frontend
- user-generated content? ratings thereof?