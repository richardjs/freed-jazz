render:
	scripts/render_scores.py

clean:
	rm -f content/songs/*/*.pdf
	rm -f content/songs/*/*.mscz
	rm -f content/songs/*/*.svg
	rm -f content/songs/*/*.png

# vim: set noexpandtab sts=0:
