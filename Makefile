default: build

clean:
	rm -f -r build/
	rm -f -r bin/
build:
	mkdir build/
	mkdir bin/
	cp -r ipranger build/
	pip3 install -r requirements.txt -t build
	rm -rf build/__pycache__ build/*.dist-info
	shiv --site-packages build -E --compressed -e ipranger.ipranger:main -o bin/ipranger -p "/usr/bin/env -S python3 -sE"

rebuild: clean build
