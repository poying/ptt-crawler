test:
	@nosetests --with-mocha-reporter

format:
	@autopep8 -r --in-place --aggressive --aggressive ptt_crawler
