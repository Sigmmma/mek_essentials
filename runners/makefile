LINK_ARGS=-static-libgcc -lkernel32
GCC=i686-w64-mingw32-gcc

build:
	mkdir -p bin
	rm -f bin/*.exe

	$(GCC) mozzarilla.c $(LINK_ARGS) -o "bin/Mozzarilla.exe"
	$(GCC) hek_pool.c   $(LINK_ARGS) -o "bin/Pool.exe"
	$(GCC) refinery.c   $(LINK_ARGS) -o "bin/Refinery.exe"
	$(GCC) updater.c    $(LINK_ARGS) -o "bin/Updater.exe"
