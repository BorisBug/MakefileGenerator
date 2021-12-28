#include "buffer.h"
#include "canbus.h"

typedef struct MESSAGE {
	uint32_t id;
	uint8_t len;
	uint8_t buf[8];
} message_t;

static message_t messages[] = {
	{.id=0x100, .len=8, .buf={0}},
	{.id=0x101, .len=6, .buf={0}}};

void setUp() {}
void tearDown() {}


static uint64_t make_unsigned(int64_t val, uint8_t bits)
{
    uint64_t mask = ~0ull>>(64-bits);
    return val & mask; // mask out extra bits
}

static int64_t make_signed(uint64_t val, uint8_t bits)
{
    uint64_t mask = ~0ull>>(64-bits);
    int64_t res = val & mask; // mask out extra bits
    if(val & (1ull<<(bits-1))) // if negative bit is set..
        res = -((~val+1)&mask); // ..use the complement+1
    return res;
}

bool canbus_set_temperature(float value)
{
	bool result = false;
	value *= 10;
	// validate range [10.0, 50.0]
	if(value>=100 && value<=500)
	{
		result = true;
		uint64_t ui = make_unsigned(value, 10);
		buffer_insert(messages[0].buf, 0, 10, ui);
	}

	return result;
}

float canbus_get_temperature(void)
{
	// return range [10.0, 50.0]
	uint64_t ui = buffer_extract(messages[0].buf, 0, 10);
	return (float)make_signed(ui, 10)/10.0;
}

bool canbus_set_humidity(uint8_t value)
{
	bool result = false;
	// validate range [0, 100]
	if(value<=100)
	{
		result = true;
		buffer_insert(messages[0].buf, 10, 7, value);
	}

	return result;
}

uint8_t canbus_get_humidity(void)
{
	// return range [0, 100]
	return (uint8_t)buffer_extract(messages[0].buf, 10, 7);
}

bool canbus_set_dht_sensor_status(uint8_t value)
{
	bool result = false;
	// validate status: 0=ERROR, 1=WARNING, 2=OKAY
	if(value<=OKAY)
	{
		result = true;
		buffer_insert(messages[0].buf, 17, 2, value);
	}

	return result;
}

uint8_t canbus_get_dht_sensor_status(void)
{
	// return status: 0=ERROR, 1=WARNING, 2=OKAY
	return (uint8_t)buffer_extract(messages[0].buf, 17, 2);
}

bool canbus_set_flow_rate(uint16_t value)
{
	bool result = false;
	// validate range [17, 500]
	if(value>=17 && value<=500)
	{
		result = true;
		buffer_insert(messages[0].buf, 19, 9, value);
	}

	return result;
}

uint16_t canbus_get_flow_rate(void)
{
	// return range [17, 500]
	return (uint16_t)buffer_extract(messages[0].buf, 19, 9);
}

bool canbus_set_flow_meter_sensor_status(uint8_t value)
{
	bool result = false;
	// validate status: 0=ERROR, 1=WARNING, 2=OKAY
	if(value<=OKAY)
	{
		result = true;
		buffer_insert(messages[0].buf, 28, 2, value);
	}

	return result;
}

uint8_t canbus_get_flow_meter_sensor_status(void)
{
	// return status: 0=ERROR, 1=WARNING, 2=OKAY
	return (uint8_t)buffer_extract(messages[0].buf, 28, 2);
}

bool canbus_set_light_intensity(uint8_t value)
{
	bool result = false;
	// validate range [0, 100]
	if(value<=100)
	{
		result = true;
		buffer_insert(messages[0].buf, 30, 7, value);
	}

	return result;
}

uint8_t canbus_get_light_intensity(void)
{
	// return range [0, 100]
	return (uint8_t)buffer_extract(messages[0].buf, 30, 7);
}

bool canbus_set_light_intensity_sensor_status(uint8_t value)
{
	bool result = false;
	// validate status: 0=ERROR, 1=WARNING, 2=OKAY
	if(value<=OKAY)
	{
		result = true;
		buffer_insert(messages[0].buf, 37, 2, value);
	}

	return result;
}

uint8_t canbus_get_light_intensity_sensor_status(void)
{
	// return status: 0=ERROR, 1=WARNING, 2=OKAY
	return (uint8_t)buffer_extract(messages[0].buf, 37, 2);
}

bool canbus_set_water_level(uint8_t value)
{
	bool result = false;
	// validate range [0, 100]
	if(value<=100)
	{
		result = true;
		buffer_insert(messages[0].buf, 39, 7, value);
	}

	return result;
}

uint8_t canbus_get_water_level(void)
{
	// return range [0, 100]
	return (uint8_t)buffer_extract(messages[0].buf, 39, 7);
}

bool canbus_set_water_level_sensor_status(uint8_t value)
{
	bool result = false;
	// validate status: 0=ERROR, 1=WARNING, 2=OKAY
	if(value<=OKAY)
	{
		result = true;
		buffer_insert(messages[0].buf, 46, 2, value);
	}

	return result;
}

uint8_t canbus_get_water_level_sensor_status(void)
{
	// return status: 0=ERROR, 1=WARNING, 2=OKAY
	return (uint8_t)buffer_extract(messages[0].buf, 46, 2);
}

bool canbus_set_soil_moisture(uint8_t value)
{
	bool result = false;
	// validate range [0, 100]
	if(value<=100)
	{
		result = true;
		buffer_insert(messages[0].buf, 48, 7, value);
	}

	return result;
}

uint8_t canbus_get_soil_moisture(void)
{
	// return range [0, 100]
	return (uint8_t)buffer_extract(messages[0].buf, 48, 7);
}

bool canbus_set_soil_moisture_sensor_status(uint8_t value)
{
	bool result = false;
	// validate status: 0=ERROR, 1=WARNING, 2=OKAY
	if(value<=OKAY)
	{
		result = true;
		buffer_insert(messages[0].buf, 55, 2, value);
	}

	return result;
}

uint8_t canbus_get_soil_moisture_sensor_status(void)
{
	// return status: 0=ERROR, 1=WARNING, 2=OKAY
	return (uint8_t)buffer_extract(messages[0].buf, 55, 2);
}

bool canbus_set_rtc_year(uint16_t value)
{
	bool result = false;
	// validate range [2021, 2040]
	if(value>=2021 && value<=2040)
	{
		result = true;
		buffer_insert(messages[1].buf, 0, 11, value);
	}

	return result;
}

uint16_t canbus_get_rtc_year(void)
{
	// return range [2021, 2040]
	return (uint16_t)buffer_extract(messages[1].buf, 0, 11);
}

bool canbus_set_rtc_month(uint8_t value)
{
	bool result = false;
	// validate range [1, 12]
	if(value>=1 && value<=12)
	{
		result = true;
		buffer_insert(messages[1].buf, 11, 4, value);
	}

	return result;
}

uint8_t canbus_get_rtc_month(void)
{
	// return range [1, 12]
	return (uint8_t)buffer_extract(messages[1].buf, 11, 4);
}

bool canbus_set_rtc_day(uint8_t value)
{
	bool result = false;
	// validate range [1, 31]
	if(value>=1 && value<=31)
	{
		result = true;
		buffer_insert(messages[1].buf, 15, 5, value);
	}

	return result;
}

uint8_t canbus_get_rtc_day(void)
{
	// return range [1, 31]
	return (uint8_t)buffer_extract(messages[1].buf, 15, 5);
}

bool canbus_set_rtc_hour(uint8_t value)
{
	bool result = false;
	// validate range [0, 23]
	if(value<=23)
	{
		result = true;
		buffer_insert(messages[1].buf, 20, 5, value);
	}

	return result;
}

uint8_t canbus_get_rtc_hour(void)
{
	// return range [0, 23]
	return (uint8_t)buffer_extract(messages[1].buf, 20, 5);
}

bool canbus_set_rtc_minute(uint8_t value)
{
	bool result = false;
	// validate range [0, 59]
	if(value<=59)
	{
		result = true;
		buffer_insert(messages[1].buf, 25, 6, value);
	}

	return result;
}

uint8_t canbus_get_rtc_minute(void)
{
	// return range [0, 59]
	return (uint8_t)buffer_extract(messages[1].buf, 25, 6);
}

bool canbus_set_rtc_second(uint8_t value)
{
	bool result = false;
	// validate range [0, 59]
	if(value<=59)
	{
		result = true;
		buffer_insert(messages[1].buf, 31, 6, value);
	}

	return result;
}

uint8_t canbus_get_rtc_second(void)
{
	// return range [0, 59]
	return (uint8_t)buffer_extract(messages[1].buf, 31, 6);
}

bool canbus_set_rtc_status(uint8_t value)
{
	bool result = false;
	// validate status: 0=ERROR, 1=WARNING, 2=OKAY
	if(value<=OKAY)
	{
		result = true;
		buffer_insert(messages[1].buf, 37, 2, value);
	}

	return result;
}

uint8_t canbus_get_rtc_status(void)
{
	// return status: 0=ERROR, 1=WARNING, 2=OKAY
	return (uint8_t)buffer_extract(messages[1].buf, 37, 2);
}

bool canbus_set_water_pump_state(uint8_t value)
{
	bool result = false;
	// validate states: 0=OFF, 1=ON
	if(value<=ON)
	{
		result = true;
		buffer_insert(messages[1].buf, 39, 1, value);
	}

	return result;
}

uint8_t canbus_get_water_pump_state(void)
{
	// return states: 0=OFF, 1=ON
	return (uint8_t)buffer_extract(messages[1].buf, 39, 1);
}

bool canbus_set_water_pump_status(uint8_t value)
{
	bool result = false;
	// validate status: 0=ERROR, 1=WARNING, 2=OKAY
	if(value<=OKAY)
	{
		result = true;
		buffer_insert(messages[1].buf, 40, 2, value);
	}

	return result;
}

uint8_t canbus_get_water_pump_status(void)
{
	// return status: 0=ERROR, 1=WARNING, 2=OKAY
	return (uint8_t)buffer_extract(messages[1].buf, 40, 2);
}

bool canbus_set_water_valve_state(uint8_t value)
{
	bool result = false;
	// validate states: 0=OFF, 1=ON
	if(value<=ON)
	{
		result = true;
		buffer_insert(messages[1].buf, 42, 1, value);
	}

	return result;
}

uint8_t canbus_get_water_valve_state(void)
{
	// return states: 0=OFF, 1=ON
	return (uint8_t)buffer_extract(messages[1].buf, 42, 1);
}

bool canbus_set_water_valve_status(uint8_t value)
{
	bool result = false;
	// validate status: 0=ERROR, 1=WARNING, 2=OKAY
	if(value<=OKAY)
	{
		result = true;
		buffer_insert(messages[1].buf, 43, 2, value);
	}

	return result;
}

uint8_t canbus_get_water_valve_status(void)
{
	// return status: 0=ERROR, 1=WARNING, 2=OKAY
	return (uint8_t)buffer_extract(messages[1].buf, 43, 2);
}

bool canbus_set_fans_state(uint8_t value)
{
	bool result = false;
	// validate states: 0=OFF, 1=ON
	if(value<=ON)
	{
		result = true;
		buffer_insert(messages[1].buf, 45, 1, value);
	}

	return result;
}

uint8_t canbus_get_fans_state(void)
{
	// return states: 0=OFF, 1=ON
	return (uint8_t)buffer_extract(messages[1].buf, 45, 1);
}

bool canbus_set_fans_status(uint8_t value)
{
	bool result = false;
	// validate status: 0=ERROR, 1=WARNING, 2=OKAY
	if(value<=OKAY)
	{
		result = true;
		buffer_insert(messages[1].buf, 46, 2, value);
	}

	return result;
}

uint8_t canbus_get_fans_status(void)
{
	// return status: 0=ERROR, 1=WARNING, 2=OKAY
	return (uint8_t)buffer_extract(messages[1].buf, 46, 2);
}

