# The Prevelance of the MIC in Engineering Disciplines Portrayed by Wikipedia

## Project Summary
Our project centers around the topic of how prevalent the military-industrial 
complex is within major engineering disciplines such as civil engineering, 
aerospace engineering, mechanical engineering, and electrical engineering. More
specifically, we want to know about this presence as it may shape public perception 
and opinion on these different disciplines. The primary question that we are aiming
to answer in doing this project is: How does Wikipedia present each engineering 
discipline in relation to the military-industrial complex? Because of how unfeasible 
it is to search the entire internet for topics about engineering, this question looks
specifically at Wikipedia, as it is a popular source of information people look at for
quick information and contains a lot of information about our topics.

## Requirements
In order to run the code for this project, use the following command while in our projects
directory to obtain the necessary packages from our requirements.txt file:

`pip install -r requirements.txt`

There shouldn't be any changes necessary to the code required to sucessfully run it.

## Usage
### Obtaining Data
To obtain almost identical data, execute the `process_disciplines` function with this list of 
engineering disciplines:

`["Aerospace_engineering", "Mechanical_engineering", "Electrical_engineering",
"Chemical_engineering", "Civil_engineering", "Biological_engineering"]`

This will give you the exact dictionary we used to perform our analysis and you could use this as
the argument for the rest of the code, starting with writing this data to text files.
However, there may be new edits on Wikipedia pages causing the data to be slightly different.

If you wanted to obtain similar data, but perhaps comparing different engineering disciplines
than those we chose, you could simply change the items in the list you input into the
`process_disciplines` function.

### Generating Plots
To generate plots similar to those shown in our project, you can use the provided plotting
functions:

`plot_bar_graph` for bar graphs of match counts for each discipline.

`plot_stacked_bar_graph` for stacked bar graphs showing match counts and percentages of overlap 
in total words for each discipline.

`gen_wordcloud` for generating word clouds showing keyword match frequencies.

Keep in mind that all of these require the generated dictionary containing data for match counts
and total words as their singular argument.
