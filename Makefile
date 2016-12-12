clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf beam.egg-info
	rm -rf dist build
	rm -rf .eggs
	rm -rf cover .coverage
