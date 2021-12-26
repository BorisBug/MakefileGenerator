#include <stdio.h>
#include "buffer.h"

#define SIZE 5

int main(void)
{
    uint8_t array[SIZE];
    printf("this is a test using 'buffer.h'\n");
    buffer_set(array, SIZE, 0);
    return 0;
}
