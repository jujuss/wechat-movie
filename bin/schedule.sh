BASEDIR=`dirname $0`
BASEDIR=`(cd "$BASEDIR/.."; pwd)`

crontab -l > ~/.crontab

PYTHON="/data/virtualenv/wechat-movie/bin/python"

# spider
CRONTAB_CMD="30 0 * * * $PYTHON $BASEDIR/bin/spider.py >> $BASEDIR/spider.log 2>&1 &"
echo "$CRONTAB_CMD" >> ~/.crontab
CRONTAB_CMD="0 8 * * * $PYTHON $BASEDIR/bin/spider.py >> $BASEDIR/spider.log 2>&1 &"
echo "$CRONTAB_CMD" >> ~/.crontab

#upload media
CRONTAB_CMD="0 16 * * * $PYTHON $BASEDIR/bin/media.py >> $BASEDIR/upload_media.log 2>&1 &"
echo "$CRONTAB_CMD" >> ~/.crontab


#send msg
CRONTAB_CMD="30 17 * * * $PYTHON $BASEDIR/bin/msg.py >> $BASEDIR/push_msg.log 2>&1 &"
echo "$CRONTAB_CMD" >> ~/.crontab

