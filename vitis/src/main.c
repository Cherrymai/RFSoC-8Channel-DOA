#include "platform_if.h"

#include <inttypes.h>
#include <stdio.h>

static iq16_t frame[ARRAY_CHANNELS][FRAME_SAMPLES];

int main(void) {
    if (platform_init() != 0) {
        fputs("platform_init failed\n", stderr);
        return 1;
    }

    const size_t count = platform_read_frame(frame);
    if (count == 0u) {
        fputs("no samples received\n", stderr);
        platform_shutdown();
        return 2;
    }

    /* Equal-weight beamforming example. Real weights are written by the control layer. */
    for (size_t n = 0; n < 8u && n < count; ++n) {
        int32_t sum_i = 0;
        int32_t sum_q = 0;
        for (size_t ch = 0; ch < ARRAY_CHANNELS; ++ch) {
            sum_i += frame[ch][n].i;
            sum_q += frame[ch][n].q;
        }
        printf("sample=%zu beam_i=%" PRId32 " beam_q=%" PRId32 "\n",
               n, sum_i / (int32_t)ARRAY_CHANNELS, sum_q / (int32_t)ARRAY_CHANNELS);
    }

    platform_shutdown();
    return 0;
}

