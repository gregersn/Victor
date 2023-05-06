# Victor

A character/monster generator for TTPRGs.

## Introduction

Victor makes monsters as instructed.  
By giving Victor a markdown file that contains instructions for how stats should be calculated, creations will come alive.

As an example of how these are defined, you can look in the examples folder, for how Guff is defined.

To have Victor make a Guff, you simply run the command

`$ victor ./examples/guff.md`

Which will print out information about the generated Guff in Markdown.

## Usage and options

Victor is a command line tool.
The required parameter is the markdown file that contains the definitions to be used.
There are also some options.

`--average` will calculate the average values for dice rolls, instead of using random numbers. This is useful to see what an average monster would look like.

`--fill PATH` takes the path to a PDF with a fillable form, and will put the values of the generated creature into the fields with the same name in the PDF.

`--output PATH` takes the path to where to store the outputted PDF.

## Language

The language is Python-based, and has a lot of similarities.
But it is also made to be somewhat specific for making character sheets.

To have a variable be a part of the result, you would assign it to a subselector of the object `$`.

As an example `$.Strength = 5`

Variables made without the `$` object will be accessible only within the generator script, and not a part of the result.

You use the `random` function for random values, like so:
`$.Charm = random(1, 8)`

To roll dice, there is a `roll` function that takes strings based on the Troll language to return a result.
Example `$.Dexterity = roll("sum 3 largest 4d6")`, which will give Dexterity a value that is the sum of the 3 largest among 4 d6 rolled. For more information on Troll, see: TODO: Insert link

### Functions

- `roll(string)` - Do a dice roll based on Troll
- `min` - Return the smallest of provided values
- `max` - Return the largest of provided values
- `swap` - Swap two values
- `swap_largest(candidates, target)` - Swap the largest value among `candidates` with the one in `target`, where `candidates` is a dictonary of value, and `target` the name of one.
- `apply_modifiers` - Apply values from a table
- `print` - Print out info
- `round_up` - Round up a value
- `random` - Return a random value
- `distribute(points, bins)` - Randomly distribute `points` into `bins`
- `evaluate(string)` - Evaluate `string` as an expression
- `len(list)` - Return the number of elements in `list`
- `assign(values, variables)` - Assign `values` to `variables` specified as a list of strings.

#### Tables

- `load_tables(filename)` - Load tables from a yaml-file.
- `random_table(table, count = 1)` - Pick `count` random values from `table`. Can be both a list with equal chance, or a dictionary with ranges for each item.

- `table_lookup(table, key)` - Return the value of `key` in `table`

- `ranged_table(table, key)` - Return the value of `key` in a `table` with ranges.
