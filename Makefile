tests:
	nosetests3 test

clean:
	find -name "*~" | xargs rm -v
	find -name "*.pyc" | xargs rm -v
