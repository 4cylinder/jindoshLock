# jindoshLock

## About JindoshLock

One of my all-time favourite video games is Dishonored 2, made by Arkane Studios.

In the sixth mission, known as "Dust District", the player's path is blocked by an elaborate lock designed by Kirin Jindosh, who is one of the game's antagonists. The lock contains a riddle that must be solved in order to proceed with the game. Optionally, the player can venture out into the district and obtain the answer from an NPC, but solving the riddle can be more fun, and also allows the player to skip a large portion of the level.

I started this side project to practice my Pandas skills and also to provide myself with a quick and easy way to solve the riddle every time I replay Dishonored 2 and get to that section. This solver program runs on Python 3 and uses Pandas dataframes to make the guesswork as fast as possible. It starts by using cross products to get every possible combination of variables. It then eliminates combinations which violate the hints that were given in the riddle text.

## How to Run

Ensure you have Python 3 and Pandas installed.

From your console, type: `python3 lockSolver.py` and fill in all the blanks when prompted.

Optionally, you can pre-fill the blanks as separate lines in a text file and use I/O redirection:
`python3 lockSolver.py < sample_inputs.txt` (the sample file is provided inside this package).

Make sure you spell all names correctly with spaces where appropriate (e.g. do not enter "Warmedal" in place of "War Medal"). The script is not case-sensitive.

If you filled in the blanks correctly, the answer should be outputted within seconds. There is only one possible answer for every valid combination of variables.

## Example Riddle and Solution
![image](https://github.com/4cylinder/jindoshLock/blob/master/example.jpg?raw=true)

![image](https://github.com/4cylinder/jindoshLock/blob/master/examplesolution.png?raw=true)
