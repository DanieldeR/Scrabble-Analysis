# %%
import os
import re
import numpy as np
from tqdm import tqdm
from scrabble_database import add_word_to_database, create_connection
from letter_values import letter_values
# %%
data_path = os.path.abspath('raw_data/scrabble_words.txt')

# %%


def get_points(word):

    total = np.sum([letter_values[i.upper()] for i in list(word)])

    return total


# %%
data = []

with open(data_path) as f:
    for line in tqdm(f.readlines()):
        split = line.replace('\n', '').split('\t')

        if len(split) == 2:
            word = split[0]
            definition = split[1]

            # deal with the fact that there might be a root
            m = re.match('[A-Z]*, ', definition)
            if m:
                root = m[0]
                temp = definition.split(root)
                definition = temp[1]
            else:
                root = ''

            # deal with the word type
            m = re.findall('\[.*?\]', definition)
            if len(m) > 0:
                word_type = m[0].replace(
                    '[', '').replace(']', '').split(' ')[0]

                # remove the previous values
                definition = definition.replace(m[0], '').strip()
            else:
                word_type = ''

            data.append({
                'word': word,
                'root': root.split(',')[0],
                'definition': definition,
                'word_type': word_type,
                'points': str(get_points(word))
            })
# %%
conn = create_connection('dictionary.sqlite')

for word in tqdm(data):
    with conn:
        word_to_insert = (
            word['word'],
            word['root'],
            word['definition'],
            word['word_type'],
            word['points'],
        )

        add_word_to_database(conn, word_to_insert)
