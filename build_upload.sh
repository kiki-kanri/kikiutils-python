#!/bin/sh

python3.11 setup.py sdist bdist_wheel &&
	python3.11 -m twine upload dist/* &&
	rm -rf build dist kiki_utils.egg-info
