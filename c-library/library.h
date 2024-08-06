#ifndef LIBRARY_H
#define LIBRARY_H

#include <stdint.h>

typedef struct event_t
{
    uint16_t interface_id;
    char msg[5];
} event_t;

uint32_t
library_init(void);

uint32_t
library_deinit(void);

uint32_t
library_get_counter_ms(void);

uint32_t
register_callback(void (*callback)(const event_t* const state));

#endif
