fmt:
	find layouts/ -name *.html | xargs prettier -w
	find content/ -name *.md | xargs prettier -w

# vim: set noexpandtab sts=0:
