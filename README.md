# Apache log grepper

a small script to get some specifiq data from apache logfiles


## How it works

Its based on the producer/consumer model, having several consumer fo one producer (the method that reads the log).

It was tested in a 300MB file, using 99% of 1 CPU thread, and 6MB of RAM to run during 49-53 seconds (approx).

It is highly portable, and easily extendable, what means that can be used for many other purposes, like application logs, etc.
In fact, as-is is ready to handle any other log from apache (with our current configuration).

## Dependencies

so far, everything is built in.

# Bugs, Improvements, etc

- use proper regex in the grepit prefilter, instead of plain string matching
- being able to cat/tail logs into the script.
- be able to specify a `-f,--follow` param to behave like `tail -f`
- multiple input files specified in the command line (that will trigger multiple producers, and follow some order)
- if no query values are specified, but there is a -q flag, show the available fields
- for cm sync logs, take the "Enqueue sync request <tokens>" and use a consumer to detect it, and print aditional tracking info for it.
- be able to specify a format string instead of a simple list of fields
- include more than one -g or -ng in the same command line
	- right now, we can already do it, but is in "OR" mode, not in "AND"


## Proposed use cases:

### specify fields in the command line

With this tool, we can specify the fields that we want in the output of the execution. The order of the fields will be the same specified in this parameter. 

	greap.py --query host,request


### specify custom-built filter for more advanced output

We can create filters in python, with more advanced features, like sum, average, etc.

	greap -i file.log --filter sum(r["bytes"]) 

### specify input file

	greap --input filename.log

	greap -i filename.log

### pre  grep-ping

being able to filter the lines we want to process, before actually parse the line.

	greap --grep <expresion>  -i file.log

	greap -g <expresion>  -i file.log


### negative grep-ping

being able to filter the things we DON'T want to process, before actually processing the line, saving effort.

	greap --ngrep <expresion>  -i file.log

	greap -ng <expresion>  -i file.log


### Verbose

so far there are only 2 modes, normal, and verbose. 
Verbose shows debug output about greap itself. Use it when extending greap.

The output of the app is preceded always by a special prefix:
	
	GREAP <LOGLEVEL> Error message

### file format chooser

the first version supports apache logs, but as functionality expands, we need a way to clearly tell the tool which kind of log are we talking about. 

the current logic is pretty simple, based on the name of the input file, or falling back to apache if undetermined.

	greap -i file.log -k apache

	greap -i file.log -k channel


