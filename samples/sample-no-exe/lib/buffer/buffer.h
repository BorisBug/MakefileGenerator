#ifndef BUFFER_H
#define BUFFER_H

#include <stdint.h>

/**
 * @brief This function is used to insert the value of a data into a data buffer.
 *
 * @param value The value to insert
 * @param buf Address of the buffer
 * @param start Where value shall be inserted
 * @param length Length of value in bits
 */
void buffer_insert(uint8_t *buf, uint8_t start, uint8_t length, uint64_t value);

/**
 * @brief This function is used to extact data from a buffer.
 *
 * @param buf Address of the buffer
 * @param start Where the data starts in the buffer.
 * @param length Length of the in bits
 * @return uint64_t The extracted data.
 */
uint64_t buffer_extract(uint8_t *buf, uint8_t start, uint8_t length);

#endif /* BUFFER_H */
