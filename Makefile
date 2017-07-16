test:
	@nosetests --with-mocha-reporter

lint:
	@flake8 ptt_crawler

format:
	@autopep8 -r --in-place --aggressive --aggressive ptt_crawler

release:
	python setup.py register
	python setup.py bdist_egg upload
	python setup.py bdist_wininst upload
	python setup.py sdist upload

.PHONY: build
