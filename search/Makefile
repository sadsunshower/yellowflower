CC=gcc
CFLAGS=-O2 -std=c99 -lm -Wall -Werror

combine:
	$(CC) combine.c fastdict.c fastdict.h footrule.c footrule.h $(CFLAGS) -o combine

search_ldd:
	$(CC) search_ldd.c $(CFLAGS) -o search_ldd

all: combine search_ldd

clean:
	rm combine search_ldd