import os
import sys

import pandas as pd

conditions = {
    'npl_l1_vpl': ['prefix', 'npl', 'who', 'level1', 'vpl','continuation'],
    'npl_l1_vsg': ['prefix', 'npl', 'who','level1', 'vsg','continuation'],
    'nsg_l1_vpl': ['prefix', 'nsg', 'who','level1', 'vpl','continuation'],
    'nsg_l1_vsg': ['prefix', 'nsg', 'who','level1', 'vsg','continuation'],

    'npl_l2_vpl': ['prefix', 'npl', 'who','level2', 'vpl','continuation'],
    'npl_l2_vsg': ['prefix', 'npl', 'who','level2', 'vsg','continuation'],
    'nsg_l2_vpl': ['prefix', 'nsg', 'who','level2', 'vpl','continuation'],
    'nsg_l2_vsg': ['prefix', 'nsg', 'who','level2', 'vsg','continuation'],

    'npl_l3_vpl': ['prefix', 'npl', 'who','level3', 'vpl','continuation'],
    'npl_l3_vsg': ['prefix', 'npl', 'who','level3', 'vsg','continuation'],
    'nsg_l3_vpl': ['prefix', 'nsg', 'who','level3', 'vpl','continuation'],
    'nsg_l3_vsg': ['prefix', 'nsg', 'who','level3', 'vsg','continuation']

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
