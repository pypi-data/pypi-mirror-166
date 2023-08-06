
.PHONY: help all clean develop lib install bin uninstall test deploy deploy_test

all: install

help:
	@echo "make install"
	@echo "         install event-api"
	@echo "make clean"
	@echo "         clean previous build"
	@echo "make test"
	@echo "         test event-api"
	@echo "make uninstall"
	@echo "         uninstall event-api"

clean:
	cargo clean

develop:
	export VIRTUAL_ENV=/data/zhangjy/git/event-api/venv
	pip install maturin
	unset CONDA_PREFIX && maturin develop

lib:
	pip install maturin
	maturin build --interpreter python --release

install:
	pip install .

bin:
	maturin build --interpreter python --release -b bin

uninstall:
	pip uninstall event-api

test:
	cargo test
	pip install pytest
	RUST_BACKTRACE=1 pytest -s

deploy:
	maturin publish --interpreter python -r pypi

deploy_test:
	maturin publish --interpreter python -r testpypi