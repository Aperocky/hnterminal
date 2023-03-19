build:
	@pip3 install .

pack:
	@python3 -m build

upload:
	@twine upload dist/* --skip-existing

.PHONY: build pack upload
