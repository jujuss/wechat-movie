help:
	@echo 'Makefile for wechat-movie				'
	@echo '											'
	@echo 'Usage:									'
	@echo '   make depend 	install dependencies	'
	@echo '   make decrypt	decrypt config'
	@echo '   make encrypt	encrypt config'

depend:
	pip install -r requirements.txt

decrypt:
	ansible-vault decrypt movie/settings.py

encrypt:
	ansible-vault encrypt movie/settings.py
