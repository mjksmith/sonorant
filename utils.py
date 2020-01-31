"""meow"""
from string import ascii_lowercase

import nltk
import pandas as pd
from sklearn.model_selection import train_test_split


ALLOWABLE_LETTERS = set(ascii_lowercase)
CMU = nltk.corpus.cmudict.dict()


def load_data(include_stress=False):
    """Return a DataFrame with columns for `word` and `pronunciation`."""
    records = []
    for word, pronunciations in CMU.items():
        if not all(letter in ALLOWABLE_LETTERS for letter in word):
            continue

        for pronunciation in pronunciations:
            if not include_stress:
                pronunciation = _strip_stress(pronunciation)
            records.append({'word': word, 'pronunciation': pronunciation})

    return pd.DataFrame(records)


def split_data(df, dev_proportion, test_proportion, random_state=47):
    """Return three DataFrames (train, dev, test)."""
    train_proportion = 1 - (dev_proportion + test_proportion)

    train_df, dev_df = train_test_split(
        df,
        test_size=dev_proportion + test_proportion,
        random_state=random_state)

    dev_df, test_df = train_test_split(
        dev_df,
        test_size=test_proportion / (dev_proportion + test_proportion),
        random_state=random_state)

    return train_df, dev_df, test_df


def _strip_stress(pronunciation):
    new_pronunciation = []
    for phoneme in pronunciation:
        for stress in '012':
            phoneme = phoneme.replace(stress, '')
        new_pronunciation.append(phoneme)

    return new_pronunciation

def decreased(scores, in_last):
    """Return True iff the score in the last `in_last` descended."""
    if in_last >= len(scores):
        return True
    
    last = scores[-(in_last+1)]
    for score in scores[-in_last:]:
        if score < last:
            return True
        last = score
        
    return False
    
# TODO: put this in tests 
# def check(scores, in_last, expected):
#     assert decreased(scores, in_last) == expected

# check([2, 1], 1, True)
# check([2, 1], 2, True)
# check([1, 2], 2, True)
# check([1, 2], 1, False)
# check([], 1, True)
# check([1, 2, 1, 4], 3, True)