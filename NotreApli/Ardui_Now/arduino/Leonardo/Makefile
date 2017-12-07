CC=gcc
SRCS=$(wildcard src/*)
OBJS=$(SRCS:src/%.c=obj/%.o)
OBJSPIC=$(SRCS:src/%.c=obj/%.fpic.o)
AR=ar
CFLAGS=-I include
LDLIBS=-lIL


bin/main: $(OBJS)
	mkdir -p bin
	$(CC) $(LDLIBS) -o $@ $^

obj/main.o: $(OBJS)
	mkdir -p obj
	$(CC)  $(CFLAGS)-c -o $@ $<

obj/%.o: src/%.c include/%.h
	mkdir -p obj
	$(CC) $(CFLAGS) -c -o $@ $<

run:bin/main
	./bin/main
	
clean:
	rm -f obj/* bin/*

archive.tar.bz2: $(wildcard include/*) $(wildcard src/*) Makefile
	tar jcvf  $@ $^
