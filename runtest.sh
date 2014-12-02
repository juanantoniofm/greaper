#!/bin/bash

echo "----------- apache no kind"
./greap -i sample.apache.log  -q host,referrer,user,datetime,method,request,proto,status,bytes,from,useragent  | tail -n 5

echo "----------- apache w query"
./greap -i sample.apache.log  -k apache -q host,referrer,user,datetime,method,request,proto,status,bytes,from,useragent  | tail -n 5

echo "----------- apache no query"
./greap -i sample.apache.log  -k apache | tail -n 5

echo "----------- channel manager no kind"
./greap -i sample.app.log | tail -n 5

echo "----------- channel manager w kind  no query"
./greap -i sample.app.log -k channel_manager | tail -n 5

echo "----------- channel manager w kind w query"
./greap -i sample.app.log -k channel_manager -q loglevel,action,jobtype | tail -n 5

echo "----------- channel breaker w kind  no query"
./greap -i sample.ap2.log -k channel_manager | tail -n 5

echo "----------- channel breaket w kind w query"
./greap -i sample.ap2.log -k channel_manager -q loglevel,action,jobtype | tail -n 5

echo "----------- channel breaker 3 w kind  no query"
./greap -i sample.ap3.log -k channel_manager | tail -n 5

echo "----------- channel breaker 3 w kind w query"
./greap -i sample.ap3.log -k channel_manager -q loglevel,action,jobtype | tail -n 5

echo "----------- channel breaker 3 w kind w query w pregrep"
./greap -i sample.ap3.log -k channel_manager -g completed -q loglevel,action,jobtype | tail -n 5
