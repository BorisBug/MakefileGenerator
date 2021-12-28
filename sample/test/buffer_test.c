/**
 * @file buffer_test.c
 * @author Boris Snäll (borissnaell@gmail.com)
 * @brief Solution for CI assignment on YrkesAkademin
 *        Test the functions buffer_insert and buffer_extract on different scenarions
 * @version 0.1
 * @date 2021-12-05
 */

#include "unity.h"
#include "buffer.h"

#define MAX_UINT8_BITS  (8u)
#define MAX_UINT64_BITS (64u)
#define MAX_BUFFER_BITS (256u+64u)
#define MAX_BUFFER_SIZE (MAX_BUFFER_BITS/8u)

void setUp(void) {}

void tearDown(void) {}

void mem_set(uint32_t size, uint8_t buf[size], uint8_t val)
{
    for(uint32_t i=0; i<size; i++)
        buf[i] = val;
}

void test_buffer_preloaded()
{
    uint8_t buf0[MAX_BUFFER_SIZE] = {0};
    uint8_t buf1[MAX_BUFFER_SIZE] = {0};
    mem_set(sizeof(buf1), buf1, 0xFF);

    // all combinations of "start & length" inside the boundaries
    for(uint32_t len=1; len<=MAX_UINT64_BITS; len++)
    {
        uint64_t test = (~0ull) >> (MAX_UINT64_BITS-len);
        for(uint32_t start=len-1; start<MAX_BUFFER_BITS; start++)
        {
            // all bits in 0
            TEST_ASSERT_EQUAL_UINT64(   0, buffer_extract(buf0, start, len));
            // all bits in 1
            TEST_ASSERT_EQUAL_UINT64(test, buffer_extract(buf1, start, len));
        }
    }
}

void test_buffer_write_read()
{
    uint8_t buf[MAX_BUFFER_SIZE] = {0};

    // all combinations of "start & length" inside the boundaries
    for(uint32_t len=1; len<=MAX_UINT64_BITS; len++)
    {
        uint64_t test = (~0ull) >> (MAX_UINT64_BITS-len);
        for(uint32_t start=len-1; start<MAX_BUFFER_BITS; start++)
        {
            // buffer with 0s
            mem_set(sizeof(buf), buf, 0);
            // insert 'len' bits, value is 64 bits with '1'
            buffer_insert(buf, start, len, ~0ull);
            // the value extracted is max 'len' bits with '1'
            TEST_ASSERT_EQUAL_UINT64(test, buffer_extract(buf, start, len));
        }
    }

    // write more than 64 bits
    buffer_insert(buf, 0, 65, 0xFEDCBA9876543210ull);
    // the resulting read is capped to 64 bits..
    TEST_ASSERT_EQUAL_UINT64(0xFEDCBA9876543210ull, buffer_extract(buf, 0, 65));

}

void test_buffer_patterns()
{
    uint8_t buf[MAX_BUFFER_SIZE] = {0};
    const size_t len = 16u;

    // write patterns repeteadly starting in "odd" positions
    // then read with different length and expect a "truncated" value
    for(size_t start=6; start<19; start++)
    {
        // buffer with 0s
        mem_set(sizeof(buf), buf, 0);

        // 1 bit ZIG ZAG
        // 0b1010101010101010 0xAAAA
        buffer_insert(buf, start, len, 0xAAAA);
        for(size_t i=0; i<len; i++)
            TEST_ASSERT_EQUAL_UINT64((0xAAAA>>i)&0xFFFF, buffer_extract(buf, start+i, len-i));

        // 2 bits ZIG ZAG
        // 0b1100110011001100 0xCCCC  
        buffer_insert(buf, start, len, 0xCCCC);
        for(size_t i=0; i<len; i++)
            TEST_ASSERT_EQUAL_UINT64((0xCCCC>>i)&0xFFFF, buffer_extract(buf, start+i, len-i));

        // 3 bits ZIG ZAG
        // 0b1000111000111000 0x8E38  
        buffer_insert(buf, start, len, 0x8E38);
        for(size_t i=0; i<len; i++)
            TEST_ASSERT_EQUAL_UINT64((0x8E38>>i)&0xFFFF, buffer_extract(buf, start+i, len-i));
    }
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_buffer_preloaded);
    RUN_TEST(test_buffer_write_read);
    RUN_TEST(test_buffer_patterns);
    return UNITY_END();
}
