all: clean git dist
	echo "Ready to deploy"

.PHONY: sphinx docs

sphinx docs: /dev/null
	echo "Making docs"
	sphinx-build sphinx/ doc
	git add doc
	if [ `git diff --cached --numstat | wc -l` != 0  ]; then \
		git commit -m 'updating docs (via sphinx autodoc)'; \
	fi

git:
	echo "Remember that make doesn't commit any uncommited changes, for your safety"
	git push

dist:
	echo "Release version to pypi: " `cat VERSION.txt`
	python setup.py sdist bdist_wheel

deploy: 
	twine upload dist/*
	python util/update_version.py -n
	echo "Next version: " `cat VERSION.txt`
	git add VERSION.txt
	git commit -m 'new version'
	git push

clean:
	rm -rf dist
