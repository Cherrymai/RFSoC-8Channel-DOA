#ifndef PLATFORM_IF_H
#define PLATFORM_IF_H

#include <stddef.h>
#include <stdint.h>

#define ARRAY_CHANNELS 8u
#define FRAME_SAMPLES  256u

typedef struct {
    int16_t i;
    int16_t q;
} iq16_t;

int platform_init(void);
size_t platform_read_frame(iq16_t frame[ARRAY_CHANNELS][FRAME_SAMPLES]);
void platform_shutdown(void);

#endif

