CC = cc
CFLAGS = -march=native -fopenmp -O3 -lm

heat: src/GUI/heatAux.c
	$(CC) -o src/GUI/temp/heat $^ -lm

well: src/GUI/wellAux.c
	$(CC) -o src/GUI/temp/well $^ -lm

runtest: main.c
	$(CC) -o $@ $^ $(CFLAGS)

all: heat well runtest

clean:
	rm -f src/GUI/temp/heat src/GUI/temp/well runtest
