import pandas as pd
from functions import clean

MAX_PROMPT_LENGTH = 9000
PREFIX = 'Here is a list of abilities and their correlation with personality traits. ' \
         'Conduct research. Do not list correlation pairs and their values. ' \
         'I need only synthesis. So make a generalization for correlations. Provide only causal relationships, not correlations. ' \
         'Focus only on non-obvious, strange and unexpected patterns from the point of view of neuroscience and psychology. ' \
         'Do not list obvious correlations, because i know them myself.\n\n'

SUFFIX = "Let's work this out in a step by step way to be sure we have the right answer."

df = pd.read_csv('data/data.csv', index_col=0)
df = df.rename(columns={i: clean(i) for i in df.columns})

dct = dict()

# iterate over index and columns
for ability in df.index:
    if ability == 'Mean across all abilities':
        continue

    ability_parsed = ability.replace('ability', '').replace('abilities', '')
    ability_parsed = ability_parsed.rstrip()

    for personality in df.columns:
        value = df.loc[ability, personality]
        if value != value:  # NaN
            continue

        if isinstance(value, str):
            negative = True if '−' in value else False
            value = value.replace('−', '')
            value = float(value)
            if negative:
                value *= -1

        dct[f'{personality} vs {ability_parsed}'] = value

# sort dct by absolute value
dct = {k: v for k, v in sorted(dct.items(), key=lambda item: abs(item[1]), reverse=True)}

prompt = PREFIX
for text, value in dct.items():
    prompt += f'{text}: {value}\n'
    if len(prompt) > MAX_PROMPT_LENGTH:
        break

prompt += f'\n{SUFFIX}'
print(prompt)


