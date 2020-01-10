.PHONY: gui clean tox test

gui:
	pyside2-uic ./part_map/gui.ui -o ./part_map/gui.py

tox:
	tox -p all

test:
	tox -e py37

clean:
	rm -rf .tox .pytest_cache htmlcov *.egg-info .coverage
