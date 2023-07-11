import pandas as pd
from functions import clean

PREFIX = ('Here are meta-analytic relations of traits and abilities. ' +
          # 'Here is a lot of data, try to take into account all of it, not only pairs with high level of relation. ' +
          # 'Conduct research. Do not take into account single pairs of relation, because i can see it by myself. ' \
          # 'Conduct research. What i need is a synthesis. So you have to combine traits and abilities into groups that form generalizations. ' \
          # 'Conduct research. What i need is a synthesis. ' \
          'Conduct research. ' \
          # 'Focus only on non-obvious, strange and unexpected generalizations from the point of view of neuroscience and psychology. ' +
          # 'Create a psychological theory and provide ideas about the reasons and possible causal relationships. ' \
          'Focus ONLY on non-obvious and unexpected conclusions. ' +
          # 'Do not list obvious generalizations and ideas, because i know them myself. ' \
          # "Let's create a new psychology theory based in this relations. The level of generalisation must be very high. \n\n"
          # "Let's create a new psychology theory based in this relations." \
          # "Let's try to contrast the traits of extraversion, agreeableness and neurotism to themselves. " +
          # "and create a monolith theory of psychology which consistently unite all the relations written below. " +
          "Take into account ALL of pairs written below. \n\n" +
          "Create your own terms that would generalize the relations below. Skip knowledge-bases abilities, let's focus on something more interesting. \n\n")
          # "Don't focus on single pairs of relations, try to generalize.")
          # "The level of generalisation must be very high. Take into account ALL of pairs below. \n\n")
MAX_PROMPT_LENGTH = 110000

# PREFIX = 'Here are meta-analytic relations of extraversion-related and openness-related traits with cognitive abilities. ' \
#          "Let's create a new psychology theory based in this relations\n\n" \

SUFFIX = "Let's work this out in a step by step way to be sure we have the right answer."

df = pd.read_csv('data/data.csv')
df['abs'] = df['value'].abs()
df = df.sort_values(by=['abs'], ascending=False)
# df['value'] = df['value'] / 2
df['value'] = df['value'].apply(lambda x: round(x, 2))
df = df[df['trait'] != 'Factor Beta']
df = df[df['trait'] != 'Factor Alpha']
df = df[df['trait'] != 'Type A']
df = df[df['ability'] != 'Military & Police']

df = df[df['trait'] != 'General Factor of Personality']

prompt = PREFIX
for ability, trait, value in zip(df['ability'], df['trait'], df['value']):
    ability_parsed = ability.replace('ability', '').replace('abilities', '').replace('Ability', '')
    ability_parsed = ability_parsed.rstrip()

    prompt += f'{ability_parsed} vs {trait}: {value}\n'
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

