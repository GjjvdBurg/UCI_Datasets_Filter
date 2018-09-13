

all: scrape html push

scrape:
	git checkout master
	cd ./uci && scrapy crawl uci && cd -
	mv uci/items.json ./items.json

html:
	git checkout gh-pages
	python make_html.py ./items.json

push:
	git push --all

clean:
	rm -f ./items.json
