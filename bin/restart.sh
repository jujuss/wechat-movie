# kill service

ps -ef | grep index | grep -v grep | awk '{print $2}'  | sed -e "s/^/kill -9 /g" | sh -

# start service
sh bin/start.sh
