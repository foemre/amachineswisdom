from textgenrnn import textgenrnn
from datetime import datetime
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--modelname",
                    help="Specify model name", 
                    default="amachineswisdom", 
                    type=str, 
                    action="store")

parser.add_argument("-t","--temperature",
                    help="Temperature", 
                    default=0.5, 
                    type=int, 
                    action="store")

args = parser.parse_args()

model_name=args.modelname

textgen = textgenrnn(weights_path='model/{}_weights.hdf5'.format(model_name),
                       vocab_path='model/{}_vocab.json'.format(model_name),
                       config_path='model/{}_config.json'.format(model_name))

model_cfg = {
    'word_level': True,   # set to True if want to train a word-level model (requires more data and smaller max_length)
    'rnn_size': 128,   # number of LSTM cells of each layer (128/256 recommended)
    'rnn_layers': 6,   # number of LSTM layers (>=2 recommended)
    'rnn_bidirectional': False,   # consider text both forwards and backward, can give a training boost
    'max_length': 3,   # number of tokens to consider before predicting the next (20-40 for characters, 5-10 for words recommended)
    'max_words': 10000,   # maximum number of words to model; the rest will be ignored (word-level model only)
}

train_cfg = {
    'line_delimited': True,   # set to True if each text has its own line in the source file
    'num_epochs': 10,   # set higher to train the model for longer
    'gen_epochs': 10,   # generates sample text from model after given number of epochs
    'train_size': 1,   # proportion of input data to train on: setting < 1.0 limits model from learning perfectly
    'dropout': 0.3,   # ignore a random proportion of source tokens each epoch, allowing model to generalize better
    'validation': False,   # If train__size < 1.0, test on holdout dataset; will make overall training slower
    'is_csv': False   # set to True if file is a CSV exported from Excel/BigQuery/pandas
}

# You can modify the temperature list to your preference
# changing the temperature schedule can result in wildly different output!
temperature = args.temperature
prefix = None   # if you want each generated text to start with a given seed text

if train_cfg['line_delimited']:
  n=50
  max_gen_length = 50 if model_cfg['word_level'] else 300
else:
  n = 1
  max_gen_length = 2000 if model_cfg['word_level'] else 10000
  
timestring = datetime.now().strftime('%Y%m%d_%H%M%S')
gen_file = '{}_gentext_{}.txt'.format(model_name, timestring)

textgen.generate_to_file(gen_file,
                         temperature=temperature,
                         prefix=prefix,
                         n=n,
                         max_gen_length=max_gen_length)