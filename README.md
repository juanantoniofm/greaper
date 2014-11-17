# Apache IOPS report

a small script to get some specifiq reports for the opera-myfidelio.

More information on this confluence page:
https://siteminder.atlassian.net/wiki/display/APPSUP/APACHE+IOPS+REPORT


It has to send an email reporting:
- number of error codes generated in the last 24 hours
- mention in the template what exactly is checking
	- in which machine is running
	- the purpose of the check
- is has to be easy to maintain
- report also so me of the relevant errors like:

	- most common 500 errors
	- most common 400 errors


## Dependencies

- jinja2
- 


# Defects

- the code in the stats builder method should be cleaner and splitted
- we are not really using gens to open the file

