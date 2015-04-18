BASEDIR=`dirname $0`
BASEDIR=`(cd "$BASEDIR/.."; pwd)`

# spider
CRONTAB_CMD="30 0 * * * python $BASEDIR/bin/spider.py > $BASEDIR/spider.log 2>&1 &"
echo "$CRONTAB_CMD" | crontab -
CRONTAB_CMD="0 8 * * * python $BASEDIR/bin/spider.py > $BASEDIR/spider.log 2>&1 &"
echo "$CRONTAB_CMD" | crontab -

#upload media
CRONTAB_CMD="0 16 * * * python $BASEDIR/bin/media.py > $BASEDIR/upload_media.log 2>&1 &"
echo "$CRONTAB_CMD" | crontab -


#send msg
CRONTAB_CMD="30 17 * * * python $BASEDIR/bin/msg.py > $BASEDIR/push_msg.log 2>&1 &"
echo "$CRONTAB_CMD" | crontab -
