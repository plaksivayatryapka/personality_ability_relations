import pandas as pd
from functions import clean

MAX_PROMPT_LENGTH = 8000
PREFIX = 'Here are meta-analytic relations of extraversion-related and openness-related traits with cognitive abilities. ' \
         'Conduct research. Do not take into account single pairs of relation, because i can see it by myself. ' \
         'What i need is a synthesis. So you have to combine traits and abilities into groups that form generalizations. ' \
         'Focus only on non-obvious, strange and unexpected generalizations from the point of view of neuroscience and psychology. ' \
         'Provide ideas about the reasons and possible causal relationships. ' \
         'Do not list obvious generalizations and ideas, because i know them myself. \n\n'

PREFIX = 'Here are meta-analytic relations of extraversion-related and openness-related traits with cognitive abilities. ' \
         "Let's create a new psychology theory based in this relations\n\n" \

SUFFIX = "Let's work this out in a step by step way to be sure we have the right answer."

df = pd.read_csv('data/extraversion.csv')
df['abs'] = df['value'].abs()
df = df.sort_values(by=['abs'], ascending=False)
df = df[df['trait'] != 'Factor Beta']

prompt = PREFIX
for ability, trait, value in zip(df['ability'], df['trait'], df['value']):
    prompt += f'{ability} vs {trait}: {value}\n'
    if len(prompt) > MAX_PROMPT_LENGTH:
        break

prompt += f'\n{SUFFIX}'
print(prompt)
exit()



print(f'{ability}: {train}')

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


