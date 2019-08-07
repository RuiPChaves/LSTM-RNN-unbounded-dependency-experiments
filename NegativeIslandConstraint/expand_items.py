import os
import sys

import pandas as pd

conditions = {
    'that_no-gap_pos': ['prefix', 'that', 'subject', 'paux', 'verb', 'object', 'continuation'],
    'that_gap_pos' : ['prefix', 'that', 'subject', 'paux', 'verb', 'continuation'],
    'what_no-gap_pos': ['prefix', 'what', 'subject', 'paux','verb', 'object', 'continuation'],
    'what_gap_pos' : ['prefix', 'what', 'subject', 'paux', 'verb', 'continuation'],

    'that_no-gap_neg': ['prefix', 'that', 'subject', 'naux', 'verb', 'object', 'continuation'],
    'that_gap_neg' : ['prefix', 'that', 'subject', 'naux', 'verb', 'continuation'],
    'what_no-gap_neg': ['prefix', 'what', 'subject', 'naux','verb', 'object', 'continuation'],
    'what_gap_neg' : ['prefix', 'what', 'subject', 'naux', 'verb', 'continuation']
}

end_condition_included = False
autocaps = True

def expand_items(df):
    output_df = pd.DataFrame(rows(df))
    output_df.columns = ['sent_index', 'word_index', 'word', 'region', 'condition']
    return output_df

def rows(df):
    for condition in conditions:
        for sent_index, row in df.iterrows():
            word_index = 0
            for region in conditions[condition]:
                for word in row[region].split():
                    if autocaps and word_index == 0:
                        word = word.title()
                    yield sent_index, word_index, word, region, condition
                    word_index += 1
            if not end_condition_included:
                yield sent_index, word_index + 1, ".", "End", condition
                yield sent_index, word_index + 2, "<eos>", "End", condition
            
def main(filename):
    input_df = pd.read_excel(filename)
    output_df = expand_items(input_df)
    try:
        os.mkdir("tests")
    except FileExistsError:
        pass
    output_df.to_csv("tests/items.tsv", sep="\t")

if __name__ == "__main__":
    main(*sys.argv[1:])
