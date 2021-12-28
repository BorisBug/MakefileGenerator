#include <stdio.h>
#include "memset.h"

#define SIZE 5

int main(void)
{
    uint8_t array[SIZE];
    printf("this is a test using 'buffer.h'\n");
    mem_set(array, SIZE, 0);
    return 0;
}
