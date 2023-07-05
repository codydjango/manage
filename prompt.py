from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

# Define your list of sentences
sentences = ['The quick brown fox jumps over the lazy dog',
             'Pack my box with five dozen liquor jugs',
             'How vexingly quick daft zebras jump',
             'Bright vixens jump; dozy fowl quack']

# Create a word completer
word_completer = WordCompleter(sentences, ignore_case=True)

# Use the word completer in a prompt
user_input = prompt("Start typing a sentence: ", completer=word_completer)

print('You said: ', user_input)