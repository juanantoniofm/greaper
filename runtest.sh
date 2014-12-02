#!/bin/bash

echo "----------- apache no kind"
./greap -i ../crap/apache-onweb/access-vpn.fidelio.log  -q host,referrer,user,datetime,method,request,proto,status,bytes,from,useragent  | tail -n 5

echo "----------- apache no query"
./greap -i ../crap/apache-onweb/access-vpn.fidelio.log  | tail -n 5

echo "----------- channel manager no kind"
./greap -i sample.app.log | tail -n 5

echo "----------- channel manager w kind  no query"
./greap -i sample.app.log -k channel_manager | tail -n 5

echo "----------- channel manager w kind w query"
./greap -i sample.app.log -k channel_manager -q loglevel,action,jobtype | tail -n 5

echo "----------- channel manager w kind w whole-query"
./greap -i sample.app.log -k channel_manager -q logdate,machine,logfile,datetime,loglevel,tracing,jobtype,action | tail -n 5
