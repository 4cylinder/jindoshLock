import pandas as pd
from collections import defaultdict

NAMES = ['Marcolla', 'Contee', 'Winslow', 'Finch', 'Natsiou']
DRINKS = ['Whiskey', 'Absinthe', 'Wine', 'Beer', 'Rum']
HEIRLOOMS = ['War Medal', 'Ring', 'Diamond', 'Snuff Tin', 'Bird Pendant']
CITIES = ['Dabokva', 'Fraeport', 'Karnaca', 'Baleton', 'Dunwall']
COLOURS = ['Purple', 'Red', 'White', 'Green', 'Blue']
POSITIONS = ['0', '1', '2', '3', '4']

# First we use cross-joins to get all possible combinations
namedf = pd.DataFrame({'key':[1]*5, 'Name': NAMES})
drinkdf = pd.DataFrame({'key':[1]*5, 'Drink': DRINKS})
citydf = pd.DataFrame({'key':[1]*5, 'City': CITIES})
Heirloomdf = pd.DataFrame({'key':[1]*5, 'Heirloom': HEIRLOOMS})
colourdf = pd.DataFrame({'key':[1]*5, 'Colour': COLOURS})
positiondf = pd.DataFrame({'key':[1]*5, 'Position': POSITIONS})

# This dataframe will be repeatedly filtered as we figure out the relationships
bigdf = pd.merge(namedf, drinkdf, on='key')
bigdf = pd.merge(bigdf, citydf, on='key')
bigdf = pd.merge(bigdf, Heirloomdf, on='key')
bigdf = pd.merge(bigdf, colourdf, on='key')
bigdf = pd.merge(bigdf, positiondf, on='key')
bigdf = bigdf.drop(columns=['key'])
bigdf = bigdf.reset_index(drop=True)

print("Welcome to the Jindosh Lock Solver. Please fill in the blanks below (mind your spelling!).")
print("You do NOT need to include the ladies' titles (e.g. Doctor, Countess, etc).")

f = open('riddle.txt', 'r')
riddle = f.read()
print(riddle)
f.close()

variables = []
titles = ["Doctor", "Lady", "Countess", "Madam", "Baroness"]
def validate(category, value, raw, valid):
    if value not in valid:
        print("The %s %s is not valid. Please enter one of: [%s]" % (category, raw, ','.join(valid)))
        return False
    return True

for i in range(25):
    prompt = "[ %d ]: " % (i + 1)
    accept = False
    while not accept:
        raw = input(prompt)
        value = raw.title().strip()
        if i in [1, 3, 4, 5, 8]:
            accept = validate("colour", value, raw, COLOURS)
        elif i in [6, 17, 19, 21, 22]:
            accept = validate("drink", value, raw, DRINKS)
        elif i in [0, 2, 11, 18, 23]:
            for title in titles: # remove titles from names for simplication
                value = value.replace(title, "").strip()
            accept = validate("name", value, raw, NAMES)
        elif i in [7, 10, 13, 16, 20, 24]:
            accept = validate("city", value, raw, CITIES)
        else:
            accept = validate("Heirloom", value, raw, HEIRLOOMS)
        if accept:
            riddle = riddle.replace("[ %d ]" % (i+1), raw)
            variables.append(value)

print("\nThis is the riddle you entered:")
print(riddle)
isValid = ''
while isValid.lower() != 'y' and isValid.lower() != 'n':
    isValid = input("Please make sure it is valid (y/n):")
if isValid.lower() == 'n':
    print("Exiting...")
    exit()
else:
    print("\nProcessing...")
# Save the known relationships into this dataframe
kdf = pd.read_csv('known.csv')
# kdf = pd.read_excel('knownvalues.xlsx', sheet_name='Known')
# Save any "next to" position hints here
ndf = pd.read_csv('neighbours.csv')
# ndf = pd.read_excel('knownvalues.xlsx', sheet_name='Next')
for i in range(25):
    kdf = kdf.replace( "[%d]" % (i+1), variables[i])
    ndf = ndf.replace( "[%d]" % (i+1), variables[i])

# Now we start narrowing down possibilities based on what we know
# Start eliminating rows that violate known relationships.
# For example, if the riddle says that Winslow wears a green hat, then
# we remove any rows where Winslow wears any colour that isn't green, 
# as well as any rows where green is worn by anyone not named Winslow
print("Eliminating possibilities...")
for row in kdf.itertuples(index=False):
    key1, value1, key2, value2 = row
    bigdf = bigdf[~( (bigdf[key1] == value1) & (bigdf[key2] != value2) )]
    bigdf = bigdf[~( (bigdf[key1] != value1) & (bigdf[key2] == value2) )]

bigdf = bigdf.reset_index(drop=True)
# Now start using recursion to guess the answer, 
# validating each guess against the known "Next" relationships
# Validation helper function
def checkAnswer(guessdf):
    if len(guessdf)!=5: return False
    for row in ndf.itertuples(index=False):
        key1, value1, place, key2, value2 = row
        r1 = guessdf[guessdf[key1] == value1]
        r2 = guessdf[guessdf[key2] == value2]
        if (r1.empty) or (r2.empty):
            return False
        p1 = int(r1.iloc[0].Position)
        p2 = int(r2.iloc[0].Position)
        if place =='Left' and p1 != p2-1:
            return False
        if place=='Next' and ((p1 != p2-1) and (p1 != p2+1)):
            return False
    return True

# Recursive function to guess the arrangement of the ladies
def backtrack(i, tdf):
    if i==5 and checkAnswer(tdf):
        return tdf
    else:
        subsetdf = bigdf[bigdf.Position == str(i)]
        subsetdf = subsetdf[~subsetdf.Name.isin(list(tdf.Name))]
        subsetdf = subsetdf[~subsetdf.Heirloom.isin(list(tdf.Heirloom))]
        subsetdf = subsetdf[~subsetdf.City.isin(list(tdf.City))]
        subsetdf = subsetdf[~subsetdf.Drink.isin(list(tdf.Drink))]
        subsetdf = subsetdf[~subsetdf.Colour.isin(list(tdf.Colour))]
        for index, row in subsetdf.iterrows():
            tmpdf = backtrack(i+1, tdf.append(row))
            if len(tmpdf) > 0: return tmpdf
        return pd.DataFrame()

print("Verifying possible solutions...")
answer = backtrack(0, pd.DataFrame(columns=bigdf.columns))
answer = answer.reset_index(drop=True)
if not answer.empty:
    print("Your solution is:")
    print(answer[['Name', 'Heirloom']])
else:
    print("The riddle is unsolvable. Please check your input and try again.")