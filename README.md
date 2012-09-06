

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

- fidgen : fortune id counter
- f/{id} : a single fortune keyed by ID
- fmod/{module} : Set of fortune ids for the named fortune-mod, e.g. f/bofh-excuses
- fmods : set of fortune-mod names
- u/{id}/{module}/seen : Set of seen fortune ids for a given user ID and module

for non-repeating random selection we do the following:
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
f = f/{id}
# cleanup
del u{id}/tmp


