#!/bin/bash

APACHE_LOGS_LOCATION="/var/log/apache2/"

zipped_count=`zcat $APACHE_LOGS_LOCATION/access.log.*.gz | grep '/mobile' | cut -d' ' -f1 | sort -u | wc -l`
unzipped_count=`cat $APACHE_LOGS_LOCATION/access.log $APACHE_LOGS_LOCATION/access.log.1 | grep '/mobile' | cut -d' ' -f1 | sort -u | wc -l`
total=`expr $zipped_count + $unzipped_count`
echo $total




