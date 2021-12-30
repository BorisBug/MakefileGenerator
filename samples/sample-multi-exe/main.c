#include <stdio.h>
#include "memset.h"
#include "canbus.h"

#define SIZE 5

int main(void)
{
    uint8_t array[SIZE];
    printf("This is a test using 'memset.h' and 'canbus.h'\n");
    mem_set(array, SIZE, 0);
    canbus_set_humidity(50);
    return 0;
}
