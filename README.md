# b

## description

Inspired by [한컴타자연습 산성비](https://namu.wiki/w/%ED%95%9C%EC%BB%B4%ED%83%80%EC%9E%90%EC%97%B0%EC%8A%B5%202007#s-6.1)

## English-Japanese Katakana Word Game

A Pygame-based word matching game where English words fall from the top of the screen, and the player needs to type their Japanese katakana equivalents before they reach the bottom.

### Game Features:
- Words fall from the top of the screen like rain
- Type the Japanese katakana equivalent to make the word disappear
- 5 lives - lose a life when a word reaches the bottom
- Game over screen shows matched word pairs, score, and play time
- Restart option to play again

### How to Run:
```
python rain_words_game.py
```

### Requirements:
- Python 3.x
- Pygame

### Word Pairs:
Word pairs are stored in `word_pairs.txt` in the format: `english_word, japanese_katakana`
