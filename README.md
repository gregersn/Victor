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

