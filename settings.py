

#logfile = "access-www.siteminder.co.uk.log"  # really big file
logfile = "/var/log/apache2/access-www.siteminder.co.uk.log"
#logfile = "access-www.channelrooms.com.log" # file to check other logs
template_file = "email_tmplt.html"
subject = """APACHE OPERA MYFIDELIO REPORT ON {{ date }}""".format("SAMPLEDATE")
