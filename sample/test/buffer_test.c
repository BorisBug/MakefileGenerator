#include "unity.h"
#include "buffer.h"

#define MAX_BUFFER_SIZE 10u

void setUp(void) {}
void tearDown(void) {}

void test_buffer()
{
    uint8_t buf[MAX_BUFFER_SIZE] = {0};

    for(uint32_t i=0; i<MAX_BUFFER_SIZE; i++)
        TEST_ASSERT_EQUAL_UINT32(0, buf[i]);

    buffer_set(buf, MAX_BUFFER_SIZE, 'x');

    for(uint32_t i=0; i<MAX_BUFFER_SIZE; i++)
        TEST_ASSERT_EQUAL_UINT32('x', buf[i]);
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_buffer);
    return UNITY_END();
}
