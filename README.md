# wordle

A quick and dirty program to generate Wordle guesses using
/usr/share/dict/words.

```
$ python3 wordle.py arose YXXXX until XXXXX psych XXXGX
whack
```

where X is grey, Y is yellow and G is green.

To test starter words, run `play_wordle`, which will give you the spread of
rounds played and an average.

```
$ ./play_wordle stern clamp
[3, 4, 5, 6, 7, 8, 9]
4.333
```
