# Expert_System
Backward chaining (optimised) rule-based system

![my-image](https://user-images.githubusercontent.com/58159635/124013045-1e5a4200-d9e2-11eb-9ac8-79820ed865eb.png)

## Starring

- rmarracc : https://github.com/0auBSQ

- ythomas : https://github.com/N0panda

## Dependencies

```
Lark : pip install git+https://github.com/lark-parser/lark.git@priority_decay
Ete3 : pip install ete3
Pandas : pip install pandas
```

## Usage

```
python3 expsys.py [flags] [file]

flags (optional) :

-h : Displays the program usage helper
-m, --modify : Prompts the user after the execution to modify the state of a fact or to add rules
-v, --visual : Shell visualisation of the different rule's parsing tree
-d, --display_trees : Display graphically each rule's parsing tree
-V, --verbose : Additional informations showing the execution steps during the resolution

file (optional):
File with sets of rules, facts and queries, if not set the program will promps the user and read on STDIN.
```

## File format

```
## Rules

# Imply
A | (D ^ !E) => B + C

# If and only if (Double Imply)
A <=> !F

## Queries

# Display the following facts' states after the execution
?ABC

# Remove queries (useful while using the modify flag)
?!A!B

## Facts

# Set TRUE
=AB

# Set FALSE (all facts are originally "FALSE_UNSET", "FALSE_UNSET" facts are defined using the rules during the execution, "FALSE" facts are fixed)
=!C!D

# Set UNDEFINED (State for ambiguous facts)
=~E~F

# Unset facts (useful while using the modify flag)
=$B$C$D$E$F
```
