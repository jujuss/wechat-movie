pip install -r requirements.txt
python index.py >> wechat-movie.log 2>&1 &
python tools/crawler.py >> crawler.log 2>&1 &

BASEDIR=`dirname $0`
BASEDIR=`(cd "$BASEDIR"; pwd)`
CRONTAB_CMD="* */12 * * * python $BASEDIR/tools/crawler.py > $BASEDIR/crawler.log 2>&1 &"
(crontab -l 2>/dev/null | echo "$CRONTAB_CMD") | crontab -
COUNT=`crontab -l |  grep -v "grep"|wc -l `
if [ $COUNT -lt 1 ]; then
        echo "fail to add crontab $PROGRAM"
        exit 1
fi
