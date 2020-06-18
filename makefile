clean:
	rm -f cedar/*/*.so
	rm -f cedar/*/*.c
	rm -f cedar/*/*.html
	rm -rf cedar/*/build
	rm -rf cedar/*/__pycache__
	rm -rf cedar/__pycache__

build:
	cd cedar/cedar_single; python3 setup.py build_ext --inplace; cd ..
	cd cedar/cedar_layer; python3 setup.py build_ext --inplace; cd ..
	cd cedar/cedar_pyramid; python3 setup.py build_ext --inplace; cd ..
	cd cedar/exact; python3 setup.py build_ext --inplace; cd ..

get_deps:
	pip3 install -r requirements.txt

all: clean get_deps build