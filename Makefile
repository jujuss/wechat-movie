help:
	@echo 'Makefile for wechat-movie				'
	@echo '											'
	@echo 'Usage:									'
	@echo '   make depend 	install dependencies	'
	@echo '   make cron 	set up cron				'
	@echo '   make env	set up pythonpath'

depend:
	pip install -q -r requirements.txt

