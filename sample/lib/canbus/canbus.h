#ifndef CANBUS_H
#define CANBUS_H

#include <stdint.h>
#include <stdbool.h>

#define OFF 0
#define ON 1
#define ERROR 0
#define WARNING 1
#define OKAY 2

/**
* @brief the ambient temperature
* return bool: true on success, false when value is out of range
**/
bool canbus_set_temperature(float value);

/**
* @brief the ambient temperature
**/
float canbus_get_temperature(void);

/**
* @brief the ambient humidity percentage
* return bool: true on success, false when value is out of range
**/
bool canbus_set_humidity(uint8_t value);

/**
* @brief the ambient humidity percentage
**/
uint8_t canbus_get_humidity(void);

/**
* @brief the dht sensor status
* return bool: true on success, false when value is out of range
**/
bool canbus_set_dht_sensor_status(uint8_t value);

/**
* @brief the dht sensor status
**/
uint8_t canbus_get_dht_sensor_status(void);

/**
* @brief the flow rate in milliliter per second
* return bool: true on success, false when value is out of range
**/
bool canbus_set_flow_rate(uint16_t value);

/**
* @brief the flow rate in milliliter per second
**/
uint16_t canbus_get_flow_rate(void);

/**
* @brief the flow meter sensor status
* return bool: true on success, false when value is out of range
**/
bool canbus_set_flow_meter_sensor_status(uint8_t value);

/**
* @brief the flow meter sensor status
**/
uint8_t canbus_get_flow_meter_sensor_status(void);

/**
* @brief the light intensity percentage
* return bool: true on success, false when value is out of range
**/
bool canbus_set_light_intensity(uint8_t value);

/**
* @brief the light intensity percentage
**/
uint8_t canbus_get_light_intensity(void);

/**
* @brief the light intensity sensor status
* return bool: true on success, false when value is out of range
**/
bool canbus_set_light_intensity_sensor_status(uint8_t value);

/**
* @brief the light intensity sensor status
**/
uint8_t canbus_get_light_intensity_sensor_status(void);

/**
* @brief the water level percentage
* return bool: true on success, false when value is out of range
**/
bool canbus_set_water_level(uint8_t value);

/**
* @brief the water level percentage
**/
uint8_t canbus_get_water_level(void);

/**
* @brief the water level sensor status
* return bool: true on success, false when value is out of range
**/
bool canbus_set_water_level_sensor_status(uint8_t value);

/**
* @brief the water level sensor status
**/
uint8_t canbus_get_water_level_sensor_status(void);

/**
* @brief the soil moisture percentage
* return bool: true on success, false when value is out of range
**/
bool canbus_set_soil_moisture(uint8_t value);

/**
* @brief the soil moisture percentage
**/
uint8_t canbus_get_soil_moisture(void);

/**
* @brief the soil moisture sensor status
* return bool: true on success, false when value is out of range
**/
bool canbus_set_soil_moisture_sensor_status(uint8_t value);

/**
* @brief the soil moisture sensor status
**/
uint8_t canbus_get_soil_moisture_sensor_status(void);

/**
* @brief the current RTC year
* return bool: true on success, false when value is out of range
**/
bool canbus_set_rtc_year(uint16_t value);

/**
* @brief the current RTC year
**/
uint16_t canbus_get_rtc_year(void);

/**
* @brief the current RTC month
* return bool: true on success, false when value is out of range
**/
bool canbus_set_rtc_month(uint8_t value);

/**
* @brief the current RTC month
**/
uint8_t canbus_get_rtc_month(void);

/**
* @brief the current RTC day
* return bool: true on success, false when value is out of range
**/
bool canbus_set_rtc_day(uint8_t value);

/**
* @brief the current RTC day
**/
uint8_t canbus_get_rtc_day(void);

/**
* @brief the current RTC hour
* return bool: true on success, false when value is out of range
**/
bool canbus_set_rtc_hour(uint8_t value);

/**
* @brief the current RTC hour
**/
uint8_t canbus_get_rtc_hour(void);

/**
* @brief the current RTC minute
* return bool: true on success, false when value is out of range
**/
bool canbus_set_rtc_minute(uint8_t value);

/**
* @brief the current RTC minute
**/
uint8_t canbus_get_rtc_minute(void);

/**
* @brief the current RTC second
* return bool: true on success, false when value is out of range
**/
bool canbus_set_rtc_second(uint8_t value);

/**
* @brief the current RTC second
**/
uint8_t canbus_get_rtc_second(void);

/**
* @brief the RTC status
* return bool: true on success, false when value is out of range
**/
bool canbus_set_rtc_status(uint8_t value);

/**
* @brief the RTC status
**/
uint8_t canbus_get_rtc_status(void);

/**
* @brief the water pump state
* return bool: true on success, false when value is out of range
**/
bool canbus_set_water_pump_state(uint8_t value);

/**
* @brief the water pump state
**/
uint8_t canbus_get_water_pump_state(void);

/**
* @brief the water_pump status
* return bool: true on success, false when value is out of range
**/
bool canbus_set_water_pump_status(uint8_t value);

/**
* @brief the water_pump status
**/
uint8_t canbus_get_water_pump_status(void);

/**
* @brief the water valve state
* return bool: true on success, false when value is out of range
**/
bool canbus_set_water_valve_state(uint8_t value);

/**
* @brief the water valve state
**/
uint8_t canbus_get_water_valve_state(void);

/**
* @brief the water_valve status
* return bool: true on success, false when value is out of range
**/
bool canbus_set_water_valve_status(uint8_t value);

/**
* @brief the water_valve status
**/
uint8_t canbus_get_water_valve_status(void);

/**
* @brief the fan state
* return bool: true on success, false when value is out of range
**/
bool canbus_set_fans_state(uint8_t value);

/**
* @brief the fan state
**/
uint8_t canbus_get_fans_state(void);

/**
* @brief the fan status
* return bool: true on success, false when value is out of range
**/
bool canbus_set_fans_status(uint8_t value);

/**
* @brief the fan status
**/
uint8_t canbus_get_fans_status(void);

#endif
