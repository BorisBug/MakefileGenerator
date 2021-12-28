#include "unity.h"
#include "canbus.h"

void test_canbus_temperature(void)
{
	// test range [10.0, 50.0] <signed>
	// boundaries of float = [-2147483648, 2147483647]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_temperature(10.0));
	TEST_ASSERT_EQUAL_FLOAT(10.0, canbus_get_temperature());
	// more than min value
	TEST_ASSERT_TRUE(canbus_set_temperature(10.1));
	TEST_ASSERT_EQUAL_FLOAT(10.1, canbus_get_temperature());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_temperature(30.0));
	TEST_ASSERT_EQUAL_FLOAT(30.0, canbus_get_temperature());
	// less than max value
	TEST_ASSERT_TRUE(canbus_set_temperature(49.9));
	TEST_ASSERT_EQUAL_FLOAT(49.9, canbus_get_temperature());
	// max value
	TEST_ASSERT_TRUE(canbus_set_temperature(50.0));
	TEST_ASSERT_EQUAL_FLOAT(50.0, canbus_get_temperature());
	// outside of the boundaries, expecting FALSE
	// less than min value
	TEST_ASSERT_FALSE(canbus_set_temperature(9.9));
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_temperature(50.1));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_FLOAT(50.0, canbus_get_temperature());
}

void test_canbus_humidity(void)
{
	// test range [0, 100] <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_humidity(0));
	TEST_ASSERT_EQUAL_UINT8(0, canbus_get_humidity());
	// more than min value
	TEST_ASSERT_TRUE(canbus_set_humidity(1));
	TEST_ASSERT_EQUAL_UINT8(1, canbus_get_humidity());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_humidity(50));
	TEST_ASSERT_EQUAL_UINT8(50, canbus_get_humidity());
	// less than max value
	TEST_ASSERT_TRUE(canbus_set_humidity(99));
	TEST_ASSERT_EQUAL_UINT8(99, canbus_get_humidity());
	// max value
	TEST_ASSERT_TRUE(canbus_set_humidity(100));
	TEST_ASSERT_EQUAL_UINT8(100, canbus_get_humidity());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_humidity(101));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(100, canbus_get_humidity());
}

void test_canbus_dht_sensor_status(void)
{
	// test status: 0=ERROR, 1=WARNING, 2=OKAY <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_dht_sensor_status(ERROR));
	TEST_ASSERT_EQUAL_UINT8(ERROR, canbus_get_dht_sensor_status());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_dht_sensor_status(WARNING));
	TEST_ASSERT_EQUAL_UINT8(WARNING, canbus_get_dht_sensor_status());
	// max value
	TEST_ASSERT_TRUE(canbus_set_dht_sensor_status(OKAY));
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_dht_sensor_status());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_dht_sensor_status(OKAY+1));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_dht_sensor_status());
}

void test_canbus_flow_rate(void)
{
	// test range [17, 500] <unsigned>
	// boundaries of uint16_t = [0, 65535]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_flow_rate(17));
	TEST_ASSERT_EQUAL_UINT16(17, canbus_get_flow_rate());
	// more than min value
	TEST_ASSERT_TRUE(canbus_set_flow_rate(18));
	TEST_ASSERT_EQUAL_UINT16(18, canbus_get_flow_rate());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_flow_rate(258));
	TEST_ASSERT_EQUAL_UINT16(258, canbus_get_flow_rate());
	// less than max value
	TEST_ASSERT_TRUE(canbus_set_flow_rate(499));
	TEST_ASSERT_EQUAL_UINT16(499, canbus_get_flow_rate());
	// max value
	TEST_ASSERT_TRUE(canbus_set_flow_rate(500));
	TEST_ASSERT_EQUAL_UINT16(500, canbus_get_flow_rate());
	// outside of the boundaries, expecting FALSE
	// less than min value
	TEST_ASSERT_FALSE(canbus_set_flow_rate(16));
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_flow_rate(501));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT16(500, canbus_get_flow_rate());
}

void test_canbus_flow_meter_sensor_status(void)
{
	// test status: 0=ERROR, 1=WARNING, 2=OKAY <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_flow_meter_sensor_status(ERROR));
	TEST_ASSERT_EQUAL_UINT8(ERROR, canbus_get_flow_meter_sensor_status());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_flow_meter_sensor_status(WARNING));
	TEST_ASSERT_EQUAL_UINT8(WARNING, canbus_get_flow_meter_sensor_status());
	// max value
	TEST_ASSERT_TRUE(canbus_set_flow_meter_sensor_status(OKAY));
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_flow_meter_sensor_status());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_flow_meter_sensor_status(OKAY+1));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_flow_meter_sensor_status());
}

void test_canbus_light_intensity(void)
{
	// test range [0, 100] <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_light_intensity(0));
	TEST_ASSERT_EQUAL_UINT8(0, canbus_get_light_intensity());
	// more than min value
	TEST_ASSERT_TRUE(canbus_set_light_intensity(1));
	TEST_ASSERT_EQUAL_UINT8(1, canbus_get_light_intensity());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_light_intensity(50));
	TEST_ASSERT_EQUAL_UINT8(50, canbus_get_light_intensity());
	// less than max value
	TEST_ASSERT_TRUE(canbus_set_light_intensity(99));
	TEST_ASSERT_EQUAL_UINT8(99, canbus_get_light_intensity());
	// max value
	TEST_ASSERT_TRUE(canbus_set_light_intensity(100));
	TEST_ASSERT_EQUAL_UINT8(100, canbus_get_light_intensity());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_light_intensity(101));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(100, canbus_get_light_intensity());
}

void test_canbus_light_intensity_sensor_status(void)
{
	// test status: 0=ERROR, 1=WARNING, 2=OKAY <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_light_intensity_sensor_status(ERROR));
	TEST_ASSERT_EQUAL_UINT8(ERROR, canbus_get_light_intensity_sensor_status());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_light_intensity_sensor_status(WARNING));
	TEST_ASSERT_EQUAL_UINT8(WARNING, canbus_get_light_intensity_sensor_status());
	// max value
	TEST_ASSERT_TRUE(canbus_set_light_intensity_sensor_status(OKAY));
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_light_intensity_sensor_status());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_light_intensity_sensor_status(OKAY+1));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_light_intensity_sensor_status());
}

void test_canbus_water_level(void)
{
	// test range [0, 100] <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_water_level(0));
	TEST_ASSERT_EQUAL_UINT8(0, canbus_get_water_level());
	// more than min value
	TEST_ASSERT_TRUE(canbus_set_water_level(1));
	TEST_ASSERT_EQUAL_UINT8(1, canbus_get_water_level());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_water_level(50));
	TEST_ASSERT_EQUAL_UINT8(50, canbus_get_water_level());
	// less than max value
	TEST_ASSERT_TRUE(canbus_set_water_level(99));
	TEST_ASSERT_EQUAL_UINT8(99, canbus_get_water_level());
	// max value
	TEST_ASSERT_TRUE(canbus_set_water_level(100));
	TEST_ASSERT_EQUAL_UINT8(100, canbus_get_water_level());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_water_level(101));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(100, canbus_get_water_level());
}

void test_canbus_water_level_sensor_status(void)
{
	// test status: 0=ERROR, 1=WARNING, 2=OKAY <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_water_level_sensor_status(ERROR));
	TEST_ASSERT_EQUAL_UINT8(ERROR, canbus_get_water_level_sensor_status());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_water_level_sensor_status(WARNING));
	TEST_ASSERT_EQUAL_UINT8(WARNING, canbus_get_water_level_sensor_status());
	// max value
	TEST_ASSERT_TRUE(canbus_set_water_level_sensor_status(OKAY));
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_water_level_sensor_status());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_water_level_sensor_status(OKAY+1));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_water_level_sensor_status());
}

void test_canbus_soil_moisture(void)
{
	// test range [0, 100] <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_soil_moisture(0));
	TEST_ASSERT_EQUAL_UINT8(0, canbus_get_soil_moisture());
	// more than min value
	TEST_ASSERT_TRUE(canbus_set_soil_moisture(1));
	TEST_ASSERT_EQUAL_UINT8(1, canbus_get_soil_moisture());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_soil_moisture(50));
	TEST_ASSERT_EQUAL_UINT8(50, canbus_get_soil_moisture());
	// less than max value
	TEST_ASSERT_TRUE(canbus_set_soil_moisture(99));
	TEST_ASSERT_EQUAL_UINT8(99, canbus_get_soil_moisture());
	// max value
	TEST_ASSERT_TRUE(canbus_set_soil_moisture(100));
	TEST_ASSERT_EQUAL_UINT8(100, canbus_get_soil_moisture());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_soil_moisture(101));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(100, canbus_get_soil_moisture());
}

void test_canbus_soil_moisture_sensor_status(void)
{
	// test status: 0=ERROR, 1=WARNING, 2=OKAY <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_soil_moisture_sensor_status(ERROR));
	TEST_ASSERT_EQUAL_UINT8(ERROR, canbus_get_soil_moisture_sensor_status());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_soil_moisture_sensor_status(WARNING));
	TEST_ASSERT_EQUAL_UINT8(WARNING, canbus_get_soil_moisture_sensor_status());
	// max value
	TEST_ASSERT_TRUE(canbus_set_soil_moisture_sensor_status(OKAY));
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_soil_moisture_sensor_status());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_soil_moisture_sensor_status(OKAY+1));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_soil_moisture_sensor_status());
}

void test_canbus_rtc_year(void)
{
	// test range [2021, 2040] <unsigned>
	// boundaries of uint16_t = [0, 65535]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_rtc_year(2021));
	TEST_ASSERT_EQUAL_UINT16(2021, canbus_get_rtc_year());
	// more than min value
	TEST_ASSERT_TRUE(canbus_set_rtc_year(2022));
	TEST_ASSERT_EQUAL_UINT16(2022, canbus_get_rtc_year());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_rtc_year(2030));
	TEST_ASSERT_EQUAL_UINT16(2030, canbus_get_rtc_year());
	// less than max value
	TEST_ASSERT_TRUE(canbus_set_rtc_year(2039));
	TEST_ASSERT_EQUAL_UINT16(2039, canbus_get_rtc_year());
	// max value
	TEST_ASSERT_TRUE(canbus_set_rtc_year(2040));
	TEST_ASSERT_EQUAL_UINT16(2040, canbus_get_rtc_year());
	// outside of the boundaries, expecting FALSE
	// less than min value
	TEST_ASSERT_FALSE(canbus_set_rtc_year(2020));
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_rtc_year(2041));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT16(2040, canbus_get_rtc_year());
}

void test_canbus_rtc_month(void)
{
	// test range [1, 12] <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_rtc_month(1));
	TEST_ASSERT_EQUAL_UINT8(1, canbus_get_rtc_month());
	// more than min value
	TEST_ASSERT_TRUE(canbus_set_rtc_month(2));
	TEST_ASSERT_EQUAL_UINT8(2, canbus_get_rtc_month());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_rtc_month(6));
	TEST_ASSERT_EQUAL_UINT8(6, canbus_get_rtc_month());
	// less than max value
	TEST_ASSERT_TRUE(canbus_set_rtc_month(11));
	TEST_ASSERT_EQUAL_UINT8(11, canbus_get_rtc_month());
	// max value
	TEST_ASSERT_TRUE(canbus_set_rtc_month(12));
	TEST_ASSERT_EQUAL_UINT8(12, canbus_get_rtc_month());
	// outside of the boundaries, expecting FALSE
	// less than min value
	TEST_ASSERT_FALSE(canbus_set_rtc_month(0));
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_rtc_month(13));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(12, canbus_get_rtc_month());
}

void test_canbus_rtc_day(void)
{
	// test range [1, 31] <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_rtc_day(1));
	TEST_ASSERT_EQUAL_UINT8(1, canbus_get_rtc_day());
	// more than min value
	TEST_ASSERT_TRUE(canbus_set_rtc_day(2));
	TEST_ASSERT_EQUAL_UINT8(2, canbus_get_rtc_day());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_rtc_day(16));
	TEST_ASSERT_EQUAL_UINT8(16, canbus_get_rtc_day());
	// less than max value
	TEST_ASSERT_TRUE(canbus_set_rtc_day(30));
	TEST_ASSERT_EQUAL_UINT8(30, canbus_get_rtc_day());
	// max value
	TEST_ASSERT_TRUE(canbus_set_rtc_day(31));
	TEST_ASSERT_EQUAL_UINT8(31, canbus_get_rtc_day());
	// outside of the boundaries, expecting FALSE
	// less than min value
	TEST_ASSERT_FALSE(canbus_set_rtc_day(0));
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_rtc_day(32));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(31, canbus_get_rtc_day());
}

void test_canbus_rtc_hour(void)
{
	// test range [0, 23] <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_rtc_hour(0));
	TEST_ASSERT_EQUAL_UINT8(0, canbus_get_rtc_hour());
	// more than min value
	TEST_ASSERT_TRUE(canbus_set_rtc_hour(1));
	TEST_ASSERT_EQUAL_UINT8(1, canbus_get_rtc_hour());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_rtc_hour(11));
	TEST_ASSERT_EQUAL_UINT8(11, canbus_get_rtc_hour());
	// less than max value
	TEST_ASSERT_TRUE(canbus_set_rtc_hour(22));
	TEST_ASSERT_EQUAL_UINT8(22, canbus_get_rtc_hour());
	// max value
	TEST_ASSERT_TRUE(canbus_set_rtc_hour(23));
	TEST_ASSERT_EQUAL_UINT8(23, canbus_get_rtc_hour());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_rtc_hour(24));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(23, canbus_get_rtc_hour());
}

void test_canbus_rtc_minute(void)
{
	// test range [0, 59] <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_rtc_minute(0));
	TEST_ASSERT_EQUAL_UINT8(0, canbus_get_rtc_minute());
	// more than min value
	TEST_ASSERT_TRUE(canbus_set_rtc_minute(1));
	TEST_ASSERT_EQUAL_UINT8(1, canbus_get_rtc_minute());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_rtc_minute(29));
	TEST_ASSERT_EQUAL_UINT8(29, canbus_get_rtc_minute());
	// less than max value
	TEST_ASSERT_TRUE(canbus_set_rtc_minute(58));
	TEST_ASSERT_EQUAL_UINT8(58, canbus_get_rtc_minute());
	// max value
	TEST_ASSERT_TRUE(canbus_set_rtc_minute(59));
	TEST_ASSERT_EQUAL_UINT8(59, canbus_get_rtc_minute());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_rtc_minute(60));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(59, canbus_get_rtc_minute());
}

void test_canbus_rtc_second(void)
{
	// test range [0, 59] <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_rtc_second(0));
	TEST_ASSERT_EQUAL_UINT8(0, canbus_get_rtc_second());
	// more than min value
	TEST_ASSERT_TRUE(canbus_set_rtc_second(1));
	TEST_ASSERT_EQUAL_UINT8(1, canbus_get_rtc_second());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_rtc_second(29));
	TEST_ASSERT_EQUAL_UINT8(29, canbus_get_rtc_second());
	// less than max value
	TEST_ASSERT_TRUE(canbus_set_rtc_second(58));
	TEST_ASSERT_EQUAL_UINT8(58, canbus_get_rtc_second());
	// max value
	TEST_ASSERT_TRUE(canbus_set_rtc_second(59));
	TEST_ASSERT_EQUAL_UINT8(59, canbus_get_rtc_second());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_rtc_second(60));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(59, canbus_get_rtc_second());
}

void test_canbus_rtc_status(void)
{
	// test status: 0=ERROR, 1=WARNING, 2=OKAY <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_rtc_status(ERROR));
	TEST_ASSERT_EQUAL_UINT8(ERROR, canbus_get_rtc_status());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_rtc_status(WARNING));
	TEST_ASSERT_EQUAL_UINT8(WARNING, canbus_get_rtc_status());
	// max value
	TEST_ASSERT_TRUE(canbus_set_rtc_status(OKAY));
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_rtc_status());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_rtc_status(OKAY+1));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_rtc_status());
}

void test_canbus_water_pump_state(void)
{
	// test states: 0=OFF, 1=ON <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_water_pump_state(OFF));
	TEST_ASSERT_EQUAL_UINT8(OFF, canbus_get_water_pump_state());
	// max value
	TEST_ASSERT_TRUE(canbus_set_water_pump_state(ON));
	TEST_ASSERT_EQUAL_UINT8(ON, canbus_get_water_pump_state());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_water_pump_state(ON+1));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(ON, canbus_get_water_pump_state());
}

void test_canbus_water_pump_status(void)
{
	// test status: 0=ERROR, 1=WARNING, 2=OKAY <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_water_pump_status(ERROR));
	TEST_ASSERT_EQUAL_UINT8(ERROR, canbus_get_water_pump_status());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_water_pump_status(WARNING));
	TEST_ASSERT_EQUAL_UINT8(WARNING, canbus_get_water_pump_status());
	// max value
	TEST_ASSERT_TRUE(canbus_set_water_pump_status(OKAY));
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_water_pump_status());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_water_pump_status(OKAY+1));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_water_pump_status());
}

void test_canbus_water_valve_state(void)
{
	// test states: 0=OFF, 1=ON <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_water_valve_state(OFF));
	TEST_ASSERT_EQUAL_UINT8(OFF, canbus_get_water_valve_state());
	// max value
	TEST_ASSERT_TRUE(canbus_set_water_valve_state(ON));
	TEST_ASSERT_EQUAL_UINT8(ON, canbus_get_water_valve_state());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_water_valve_state(ON+1));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(ON, canbus_get_water_valve_state());
}

void test_canbus_water_valve_status(void)
{
	// test status: 0=ERROR, 1=WARNING, 2=OKAY <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_water_valve_status(ERROR));
	TEST_ASSERT_EQUAL_UINT8(ERROR, canbus_get_water_valve_status());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_water_valve_status(WARNING));
	TEST_ASSERT_EQUAL_UINT8(WARNING, canbus_get_water_valve_status());
	// max value
	TEST_ASSERT_TRUE(canbus_set_water_valve_status(OKAY));
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_water_valve_status());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_water_valve_status(OKAY+1));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_water_valve_status());
}

void test_canbus_fans_state(void)
{
	// test states: 0=OFF, 1=ON <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_fans_state(OFF));
	TEST_ASSERT_EQUAL_UINT8(OFF, canbus_get_fans_state());
	// max value
	TEST_ASSERT_TRUE(canbus_set_fans_state(ON));
	TEST_ASSERT_EQUAL_UINT8(ON, canbus_get_fans_state());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_fans_state(ON+1));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(ON, canbus_get_fans_state());
}

void test_canbus_fans_status(void)
{
	// test status: 0=ERROR, 1=WARNING, 2=OKAY <unsigned>
	// boundaries of uint8_t = [0, 255]

	// inside of the boundaries, expecting TRUE
	// min value
	TEST_ASSERT_TRUE(canbus_set_fans_status(ERROR));
	TEST_ASSERT_EQUAL_UINT8(ERROR, canbus_get_fans_status());
	// mid value
	TEST_ASSERT_TRUE(canbus_set_fans_status(WARNING));
	TEST_ASSERT_EQUAL_UINT8(WARNING, canbus_get_fans_status());
	// max value
	TEST_ASSERT_TRUE(canbus_set_fans_status(OKAY));
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_fans_status());
	// outside of the boundaries, expecting FALSE
	// more than max value
	TEST_ASSERT_FALSE(canbus_set_fans_status(OKAY+1));
	// invalid data should not be inserted..
	// expecting last valid value
	TEST_ASSERT_EQUAL_UINT8(OKAY, canbus_get_fans_status());
}

int main(void)
{
	UNITY_BEGIN();
	RUN_TEST(test_canbus_temperature);
	RUN_TEST(test_canbus_humidity);
	RUN_TEST(test_canbus_dht_sensor_status);
	RUN_TEST(test_canbus_flow_rate);
	RUN_TEST(test_canbus_flow_meter_sensor_status);
	RUN_TEST(test_canbus_light_intensity);
	RUN_TEST(test_canbus_light_intensity_sensor_status);
	RUN_TEST(test_canbus_water_level);
	RUN_TEST(test_canbus_water_level_sensor_status);
	RUN_TEST(test_canbus_soil_moisture);
	RUN_TEST(test_canbus_soil_moisture_sensor_status);
	RUN_TEST(test_canbus_rtc_year);
	RUN_TEST(test_canbus_rtc_month);
	RUN_TEST(test_canbus_rtc_day);
	RUN_TEST(test_canbus_rtc_hour);
	RUN_TEST(test_canbus_rtc_minute);
	RUN_TEST(test_canbus_rtc_second);
	RUN_TEST(test_canbus_rtc_status);
	RUN_TEST(test_canbus_water_pump_state);
	RUN_TEST(test_canbus_water_pump_status);
	RUN_TEST(test_canbus_water_valve_state);
	RUN_TEST(test_canbus_water_valve_status);
	RUN_TEST(test_canbus_fans_state);
	RUN_TEST(test_canbus_fans_status);
	return UNITY_END();
}

