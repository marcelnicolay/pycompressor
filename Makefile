# Turn echoing commands off
.SILENT:

clean:
	echo "Cleaning up build and *.pyc files..."
	find . -name '*.pyc' -exec rm -rf {} \;
	rm -rf build

unit: clean
	echo "Running pycompressor unit tests..."
	export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/pycompressor  &&  \
		nosetests -s --verbose --with-coverage --cover-package=pycompressor tests/unit/*

functional: clean
	echo "Running pycompressor functional tests..."
	export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/pycompressor  &&  \
		nosetests -s --verbose --with-coverage --cover-package=pycompressor tests/functional/*