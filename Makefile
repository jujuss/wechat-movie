help:
	@echo 'Makefile for wechat-movie				'
	@echo '											'
	@echo 'Usage:									'
	@echo '   make depend 	install dependencies	'
	@echo '   make cron 	set up cron				'
	@echo '   make decrypt	decrypt config'
	@echo '   make encrypt	encrypt config'

depend:
	pip install -q -r requirements.txt

cron:
	sh bin/schedule.sh && crontab ~/.crontab

decrypt:
	ansible-vault decrypt config.py

encrypt:
	ansible-vault encrypt config.py
	
	
Test
