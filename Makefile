serve:
	hugo serve

render:
	scripts/render_scores.py

clean:
	rm -f content/songs/*/*.pdf
	rm -f content/songs/*/*.mscz
	rm -f content/songs/*/*.svg
	rm -f content/songs/*/*.png
	rm -f scores/*/*_tmp.mscx

fresh: clean render

# vim: set noexpandtab sts=0:
