# Affirms

A good way to slip affirmations into your white/background noise.

### Notes

Currently set up using Flask, but only takes a text input for the affirmations. Hopefully can have more options in the future.

Settings are customizable in the  `create_audio()` function.

### Requirements

`python3`: on mac this can be installed using:
```
brew install python
```

`ffmpeg`: on mac this can be installed using:
```
 brew install ffmpeg
```

### Running

Using python3:

```
cd <repo>
python3 main.py
```

This will host it on port 5000 (unless told otherwise) > http://127.0.0.1:5000