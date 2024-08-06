#include <stdint.h>
#include <time.h>
#include <stdio.h>
#include <unistd.h>
#include "pthread.h"

#include "library.h"

static pthread_t thread_id;
static void (*local_callback)(const event_t* const state) = NULL;

uint32_t
register_callback(void (*callback)(const event_t* const state))
{
    if (callback == NULL)
        return 0;

    local_callback = callback;

    return 0;
}

void*
print_every_second(void* arg)
{
    int count = 0;
    while (1)
    {
        if (local_callback != NULL)
        {
            event_t event;
            event.interface_id = count++;
            local_callback(&event);
        }
        else
            printf("Callback is not registered\n");

        sleep(1);
    }
    return NULL;
}

uint32_t
library_init(void)
{
    pthread_create(&thread_id, NULL, print_every_second, NULL);

    return 0;
}

uint32_t
library_deinit(void)
{
    pthread_join(thread_id, NULL);

    return 0;
}

uint32_t
library_get_counter_ms(void)
{
    struct timespec time;
    clock_gettime(CLOCK_MONOTONIC, &time);
    return time.tv_sec * 1000 + time.tv_nsec / 1000000;
}
