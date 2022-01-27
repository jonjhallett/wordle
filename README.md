# wordle

A quick and dirty program to generate Wordle guesses using
words from /usr/share/dict/words. `wordle.py` uses character frequency
analysis with penalties aimed at generating the most information from each
guess.
```
$ python3 wordle.py stern XYYXX clamp XXXXX bidet XYXGG
quiet
```

where X is grey, Y is yellow and G is green.

To test starter words, run `play_wordle`, which will give you the spread of
rounds played and an average.

```
$ ./play_wordle stern clamp
 3 **********
 4 *************************
 5 ****************
 6 ****
 7 *
 8
 9
4.395
```
