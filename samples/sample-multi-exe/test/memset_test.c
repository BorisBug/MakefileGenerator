#include "unity.h"
#include "memset.h"

#define MAX_BUFFER_SIZE 10u

void setUp(void) {}
void tearDown(void) {}

void test_memset()
{
    uint8_t buf[MAX_BUFFER_SIZE] = {0};

    for(uint32_t i=0; i<MAX_BUFFER_SIZE; i++)
        TEST_ASSERT_EQUAL_UINT8(0, buf[i]);

    mem_set(buf, MAX_BUFFER_SIZE, 'x');

    for(uint32_t i=0; i<MAX_BUFFER_SIZE; i++)
        TEST_ASSERT_EQUAL_UINT8('x', buf[i]);
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_memset);
    return UNITY_END();
}
