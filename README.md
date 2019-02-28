![alt text](https://raw.githubusercontent.com/foemre/amachineswisdom/master/common/imwithtext1.jpg "A Machine's Wisdom")
### The source code for A Machine's Wisdom.

# How to use
Scrape quotes from [Wisdom Quotes](http://wisdomquotes.com "Wisdom Quotes"), specifying various options like string length:
```sh
$ python scrape.py --help
usage: scrape.py [-h] [-i INPUTFILE] [-o OUTPUTFILE] [--maxlen MAXLEN]
                 [--minlen MINLEN]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputfile INPUTFILE
                        Name of the input file that stores links, one link per
                        line
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        Name of the file to store quotes
  --maxlen MAXLEN       Maximum length of the quotes stored
  --minlen MINLEN       Minimum length of the quotes stored
```
Train with scraped text:
```sh
$ python train.py
```
In `train.py`, config entries are hardcoded. You will need to change them manually.
```python
model_cfg = {
    'word_level': True,
    'rnn_size': 128,
    'rnn_layers': 6,
    'rnn_bidirectional': False,
    'max_length': 3,
    'max_words': 10000
}

train_cfg = {
    'line_delimited': True,
    'num_epochs': 10,
    'gen_epochs': 10,
    'train_size': 1,
    'dropout': 0.3,
    'validation': False,
    'is_csv': False
}
```

Generate random quotes (make sure the configs are the same as those in `train.py`:
```sh
$ python generatetext.py
```
Overlay "exactly" 3 lines of text over a generated image (use generated text or supply your own text file):
```sh
$ python imagegen.py
usage: imagegen.py [-h] [-x X] [-y Y] [-n NUM_NEURONS] [-l NUM_LAYERS]
                   [-c COUNT] [-f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -x X                  Width
  -y Y                  Height
  -n NUM_NEURONS, --num_neurons NUM_NEURONS
                        Number of neurons
  -l NUM_LAYERS, --num_layers NUM_LAYERS
                        Number of layers
  -c COUNT, --count COUNT
                        Number of images to be generated
  -f FILE, --file FILE  Name of the quotes file
```

### TODO:
- Implement with Instagram Graph API (Facebook needs to open the API to everyone)
- JSON config file
- Maybe a GUI
