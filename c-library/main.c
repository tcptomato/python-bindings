#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

#include "library.h"

void
print_line(const event_t* const state)
{
    if (state == NULL)
        return;

    printf("Callback value %d\n", state->interface_id);
}

int
main()
{
    pthread_t thread_id;

    library_init();

    printf("Time is %d\n", library_get_counter_ms());

    register_callback(print_line);

    library_deinit();

    return 0;
}
