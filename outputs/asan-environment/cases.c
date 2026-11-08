#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static volatile size_t invalid_offset = 16;
static volatile unsigned char global_bytes[16];

__attribute__((noinline)) static int heap_case(int mode) {
    volatile unsigned char *bytes = malloc(16);
    if (bytes == NULL) {
        return 2;
    }
    bytes[0] = 7;
    if (mode == 1) {
        bytes[invalid_offset] = 42;
    }
    if (mode == 2) {
        free((void *)bytes);
        return bytes[0];
    }
    printf("OK %u\n", (unsigned int)bytes[0]);
    free((void *)bytes);
    return 0;
}

__attribute__((noinline)) static int stack_case(void) {
    volatile unsigned char bytes[16] = {0};
    bytes[invalid_offset] = 42;
    return bytes[0];
}

int main(int argc, char **argv) {
    if (argc != 2) {
        return 2;
    }
    if (strcmp(argv[1], "normal") == 0) {
        return heap_case(0);
    }
    if (strcmp(argv[1], "heap") == 0) {
        return heap_case(1);
    }
    if (strcmp(argv[1], "uaf") == 0) {
        return heap_case(2);
    }
    if (strcmp(argv[1], "stack") == 0) {
        return stack_case();
    }
    if (strcmp(argv[1], "global") == 0) {
        global_bytes[invalid_offset] = 42;
        return 0;
    }
    return 2;
}
