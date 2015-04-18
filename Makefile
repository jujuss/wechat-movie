help:
	@echo 'Makefile for wechat-movie				'
	@echo '											'
	@echo 'Usage:									'
	@echo '   make depend 	install dependencies	'
	@echo '   make cron 	set up cron				'

depend:
	pip install -q -r requirements.txt

cron:
	sh bin/schedule.sh
