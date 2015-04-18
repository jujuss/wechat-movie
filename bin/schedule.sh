BASEDIR=`dirname $0`
BASEDIR=`(cd "$BASEDIR"; pwd)`
CRONTAB_CMD="* */12 * * * python $BASEDIR/bin/spider.py > $BASEDIR/spider.log 2>&1 &"
(crontab -l 2>/dev/null | echo "$CRONTAB_CMD") | crontab -
COUNT=`crontab -l |  grep -v "grep"|wc -l `
if [ $COUNT -lt 1 ]; then
        echo "fail to add crontab $PROGRAM"
        exit 1
fi
