#!/bin/bash
# author: Cristian Spoiala scristian@gmail.com

S3_BUCKET="bucket"
CFG_LOCATIONS="/etc/sysconfig/backup/locations"
MAIL="scristian@gmail.com"

# Read backup locations
# For each location upload file
cat $CFG_LOCATIONS | while read LINE ; do
    BACKUP_LOCATION=$LINE
    cd $BACKUP_LOCATION
    BACKUP_FILE=`ls -lt | grep ^- | awk '{print $9}' | head -1`

    # Add to amazon s3 ea_files
    echo "Add to amazon s3 file: $BACKUP_FILE"

    /root/s3cmd/s3cmd/s3cmd --multipart-chunk-size-mb=1000 put $BACKUP_FILE "s3://$S3_BUCKET/$BACKUP_FILE"

    if [ $? -eq 0 ]
    then
	echo "UPLOAD with SUCCESS file: $BACKUP_FILE to bucket $S3_BUCKET"
      else
        echo "UPLOAD FAILED for file $BACKUP_FILE to bucket: $S3_BUCKET." | mail -s "[BACKUP] FAILED files backup [EA]" $MAIL
    fi

done
