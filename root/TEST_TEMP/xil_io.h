#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>

#include <unistd.h>
#include <fcntl.h>

#define PAGE_SIZE  ((size_t)getpagesize())
#define PAGE_MASK ((uint64_t) (long)~(PAGE_SIZE - 1))

void Xil_Out32(uint64_t phyaddr, uint32_t val);

int Xil_In32(uint64_t phyaddr);

