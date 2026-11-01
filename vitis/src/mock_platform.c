/* Software data source for interface testing. Replace with real RFDC/DMA code on hardware. */
#include "platform_if.h"

#include <math.h>

int platform_init(void) {
    return 0;
}

size_t platform_read_frame(iq16_t frame[ARRAY_CHANNELS][FRAME_SAMPLES]) {
    const double pi = 3.14159265358979323846;
    for (size_t n = 0; n < FRAME_SAMPLES; ++n) {
        const double sample_phase = 2.0 * pi * 0.07 * (double)n;
        for (size_t ch = 0; ch < ARRAY_CHANNELS; ++ch) {
            const double array_phase = 0.20 * (double)ch;
            frame[ch][n].i = (int16_t)(12000.0 * cos(sample_phase + array_phase));
            frame[ch][n].q = (int16_t)(12000.0 * sin(sample_phase + array_phase));
        }
    }
    return FRAME_SAMPLES;
}

void platform_shutdown(void) {
}

