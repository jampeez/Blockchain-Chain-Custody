#!/usr/bin/env python3
all:
	cp cq4.py bchoc
	chmod +x bchoc
	dos2unix cq4.py
clean:
	rm bchoc