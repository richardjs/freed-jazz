render:
	scripts/render_scores.py

clean:
	rm -f content/songs/*/*.pdf
	rm -f content/songs/*/*.mscz
	rm -f content/songs/*/*.svg
	rm -f content/songs/*/*.png

fmt:
	find layouts/ -name *.html | xargs prettier -w
	find content/ -name *.md | xargs prettier -w

# vim: set noexpandtab sts=0:
