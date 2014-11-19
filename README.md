# Apache log grepper

a small script to get some specifiq data from apache logfiles


## How it works

Its based on the producer/consumer model, having several consumer fo one producer (the method that reads the log).

It was tested in a 300MB file, using 99% of 1 CPU thread, and 6MB of RAM to run during 49-53 seconds (approx).

It is highly portable, and easily extendable, what means that can be used for many other purposes, like application logs, etc.
In fact, as-is is ready to handle any other log from apache (with our current configuration)


## Dependencies


# Bugs, Improvements, etc

- the code in the stats builder method should be cleaner and splitted
- It would be better to use command line args to specify
	- the logfile
	- the level of detail reporting
	- the addresses to send the email to


