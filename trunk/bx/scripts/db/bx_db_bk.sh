#!/bin/bash
#by coco wu
#2017-04-05

DATE=`date "+%Y%m%d"`
BIN_DIR="/usr/local/mysql/bin"
BAK_DIR="/data/dbbk/local"
BAK_PATH=$BAK_DIR/$DATE

#echo "come here"
if [ ! -d $BAK_PATH ] ; then
  mkdir -p $BAK_PATH
fi

DB_NAME="bx_abc crondeamon"
for db_name in $DB_NAME
  do
        DATE1=`date "+%Y%m%d %T"`
       echo -e "\033[32m $DATE1 $db_name backup begin...\033[0m" >>$BAK_DIR/backup-log.txt
    if $BIN_DIR/mysqldump --opt --single-transaction --default-character-set="utf8" -h118.89.220.36 -umha_user -pgc895316 -R --hex-blob --databases $db_name | gzip > $BAK_PATH/$db_name-$DATE.sql.gz ; then
        DATE1=`date "+%Y%m%d %T"`
	echo -e "\033[32m $DATE1 $db_name backup OK! \033[0m" >>$BAK_DIR/backup-log.txt
    else
        DATE1=`date "+%Y%m%d %T"`
        echo -e "\033[31;5m $DATE1 $db_name backup false...\033[0m" >>$BAK_DIR/backup-log.txt
    fi
  done
echo -e "\033[32m ------------------------------$DATE1  backup END...\033[0m" >>$BAK_DIR/backup-log.txt
find $BAK_DIR -name "*" -mtime +10 |xargs rm -rf
find $BAK_DIR -type d -empty |xargs rm -rf
exit 0
