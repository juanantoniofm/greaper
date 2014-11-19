# Apache IOPS report

a small script to get some specifiq reports for the opera-myfidelio.

More information on this confluence page:
https://siteminder.atlassian.net/wiki/display/APPSUP/APACHE+IOPS+REPORT


It has to send an email reporting:
- number of error codes generated in the last 24 hours
- mention in the template what exactly is checking
	- in which machine is running
	- the purpose of the check
- report also so me of the relevant errors like:

	- most common 500 errors
	- most common 400 errors

## How it works

Its based on the producer/consumer model, having several consumer fo one producer (the method that reads the log).

It was tested in a 300MB file, using 99% of 1 CPU thread, and 6MB of RAM to run during 49-53 seconds (approx).

It is highly portable, and easily extendable, what means that can be used for many other purposes, like application logs, etc.
In fact, as-is is ready to handle any other log from apache (with our current configuration)



## Dependencies

- jinja2
	- markupsafe
- smtplib (builtin)


# Bugs, Improvements, etc

- the code in the stats builder method should be cleaner and splitted
- It would be better to use command line args to specify
	- the logfile
	- the level of detail reporting
	- the addresses to send the email to


