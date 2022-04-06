# wordle

A quick and dirty program to generate Wordle guesses using
words from /usr/share/dict/words. `wordle.py` uses character frequency
analysis with penalties aimed at generating the most information from each
guess.
```
$ python3 wordle.py stern XYYXX clamp XXXXX debit XYXYG | head
eight
quiet
```

where X is grey, Y is yellow and G is green.

To test starter words, run `play_wordle`, which will give you the spread of
rounds played and an average, based on a sample of random target words. You'll to extract the answer word list from the Wordle web page and save to a file called `answer_words.txt`.

```
$ ./play_wordle.py stern clamp
[...]
thing
 rents XXYYX clamp XXXXX ingot YYYXY
Got it!

grill
 rents YXXXX clamp XYXXX drily XGGGX brill XGGGG frill XGGGG
Got it!

lipid
 rents XXXXX clamp XYXXY poilu YXYYX
Got it!
 1  0.0%
 2 * 1.8%
 3 ************ 20.8%
 4 ***************************** 49.8%
 5 ************* 21.8%
 6 ** 4.6%
 7  0.9%
 8  0.2%
 9  0.0%
4.100647948164147
```
