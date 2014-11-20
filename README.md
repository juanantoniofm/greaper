# Apache log grepper

a small script to get some specifiq data from apache logfiles


## How it works

Its based on the producer/consumer model, having several consumer fo one producer (the method that reads the log).

It was tested in a 300MB file, using 99% of 1 CPU thread, and 6MB of RAM to run during 49-53 seconds (approx).

It is highly portable, and easily extendable, what means that can be used for many other purposes, like application logs, etc.
In fact, as-is is ready to handle any other log from apache (with our current configuration).

It's focused on the log format present in the central log servers, so it also parses the timestamp in the beggining of the line.

## Dependencies

so far, everything is built in.

# Bugs, Improvements, etc

- the code in the stats builder method should be cleaner and splitted
- It would be better to use command line args to specify
	- the logfile
	- the level of detail reporting
	- the addresses to send the email to
- use proper regex in the grepit prefilter, instead of plain string matching
- being able to cat/tail logs into the script.

## Proposed use cases:

### specify fields in the command line

greap.py --query host,request


### specify custom-built filter for more advanced output

We can create filters in python, with more advanced features, like sum, average, etc.

	greap -i file.log --filter sum(r["bytes"]) 

### specify input file

	grep --input filename.log

	grep -i filename.log

### pre  grep-ping

being able to filter the lines we want to process, before actually parse the line.

	greap --grep <expresion>  -i file.log

	greap -g <expresion>  -i file.log


### negative grep-ping

being able to filter the things we DON'T want to process, before actually parse the line.

	greap --ngrep <expresion>  -i file.log

	greap --ng <expresion>  -i file.log


### 
