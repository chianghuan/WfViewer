tags:
	ctags -R .

.PHONY : clean
clean:
	find . -type f | sed -n '/\~$$/p; /\.pyc$$/p; /\.swp$$/p' | xargs rm -f 
	rm -f tags
