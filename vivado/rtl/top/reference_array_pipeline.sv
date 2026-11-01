// Board-independent top level for the eight-channel beamforming stage.
module reference_array_pipeline (
    input  logic                     clk,
    input  logic                     rst_n,
    input  logic                     sample_valid,
    input  logic signed [15:0]        adc_re [0:7],
    input  logic signed [15:0]        adc_im [0:7],
    input  logic signed [15:0]        weight_re [0:7],
    input  logic signed [15:0]        weight_im [0:7],
    output logic                     beam_valid,
    output logic signed [15:0]        beam_re,
    output logic signed [15:0]        beam_im
);
    beamformer8_q15 u_beamformer (
        .clk        (clk),
        .rst_n      (rst_n),
        .valid_in   (sample_valid),
        .ch_re      (adc_re),
        .ch_im      (adc_im),
        .weight_re  (weight_re),
        .weight_im  (weight_im),
        .valid_out  (beam_valid),
        .beam_re    (beam_re),
        .beam_im    (beam_im)
    );
endmodule

