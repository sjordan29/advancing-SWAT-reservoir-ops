CC = gcc
MPICC = mpicxx
CFLAGS = -O3
LDFLAGS = -Wl,-R,\.
LIBS = -lm
UNAME_S = $(shell uname -s)

ifneq (, $(findstring SunOS, $(UNAME_S)))
	LIBS += -lnsl -lsocket -lresolv
endif

compile:
	$(CC) $(CFLAGS) $(LDFLAGS) -o dtlz2_serial.exe dtlz2_serial.c -L. -lborg $(LIBS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o dtlz2_advanced.exe dtlz2_advanced.c -L. -lborg $(LIBS)
	$(MPICC) $(CFLAGS) $(LDFLAGS) -o dtlz2_ms.exe dtlz2_ms.c -L. -lborgms $(LIBS)
	$(MPICC) $(CFLAGS) $(LDFLAGS) -o mainParallel_omo_irrKoysha_SWAT.exe mainParallel_omo_irrKoysha_SWAT.cpp -L. -lborgmm $(LIBS)
	$(MPICC) $(CFLAGS) $(LDFLAGS) -o dtlz2_mm.exe dtlz2_mm.c -L. -lborgmm $(LIBS)
.PHONY: compile
