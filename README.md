# twivility-superbowl-51

Processing work on advertiser tweets from Super Bowl 51 gathered by
[twivility](https://github.com/CraigKelly/twivility)

## Prep

You need the tweets gathered and placed in the `./data` directory. The three
files you should have are:

1. hashtags.txt - the list of accounts and tweets watched (mainly for
   documentation)
1. stream.json - the bulk of the data
1. direct_tweets.json - the tweets from the "home timeline" of the account.
   You must export these using the twivility command line. If you copied the
   entire folder from the server you can run:

```
./tool dump > direct_tweets.json
```

Also note that twivility-stderr.log contains data on stream sampling, but
isn't used.

## Running

You need [dmk](https://github.com/CraigKelly/dmk) and Python 3. If those are
both installed, you should be able to run `dmk` in this directory to get the
final zip file `data/superbowl-twitter.zip`

## License

All the code here is MIT unless otherwise specified. Please see `LICENSE`
