/**
 * @file buffer.c
 * @author Boris Snäll (borissnaell@gmail.com)
 * @brief Solution for CI assignment on YrkesAkademin
 * @version 0.1
 * @date 2021-12-05
 */

#include "buffer.h"

#define MAX_UINT8_BITS  (8u)
#define MAX_UINT64_BITS (64u)
#define MAX_BUFFER_BITS (256u+64u)
#define MAX_BUFFER_SIZE (MAX_BUFFER_BITS/8u)

void buffer_insert(uint8_t *buf, uint8_t start, uint8_t length, uint64_t value)
{
    if(buf && length>0)
    {
        uint32_t end = start; // change type to uint32_t
        // no more than max capacity of uint64_t
        if(length>MAX_UINT64_BITS)
            length = MAX_UINT64_BITS;

        end += length;

        for(uint32_t bit=start; bit<end; bit++, value>>=1)
        {
            uint8_t mask = 1u << bit%MAX_UINT8_BITS; 

            if(value&1ull)
                buf[bit/MAX_UINT8_BITS] |= mask;
            else
                buf[bit/MAX_UINT8_BITS] &=~mask;
        }
    }
}

uint64_t buffer_extract(uint8_t *buf, uint8_t start, uint8_t length)
{
    uint64_t value = 0;

    if(buf && length>0)
    {
        uint32_t end = start; // change type to uint32_t
        // no more than max capacity of uint64_t
        if(length>MAX_UINT64_BITS)
            length = MAX_UINT64_BITS;

        end += length;
        for(uint32_t bit=start; bit<end; bit++)
            if(buf[bit/MAX_UINT8_BITS] & (1ull << bit%MAX_UINT8_BITS))
                value |= 1ull<<(bit-start);
    }

    return value;
}
