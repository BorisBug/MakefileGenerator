#include "buffer.h"

void buffer_set(uint8_t *buf, uint32_t size, uint8_t byte)
{
    for(uint32_t i=0; i<size; i++)
        buf[i] = byte;
}
