// Parameterized complex FIR. Coefficients are real-valued Q1.15 values.
module complex_fir_q15 #(
    parameter integer TAPS = 16
) (
    input  logic                     clk,
    input  logic                     rst_n,
    input  logic                     valid_in,
    input  logic signed [15:0]        x_re,
    input  logic signed [15:0]        x_im,
    input  logic signed [15:0]        coeff [0:TAPS-1],
    output logic                     valid_out,
    output logic signed [15:0]        y_re,
    output logic signed [15:0]        y_im
);
    logic signed [15:0] delay_re [0:TAPS-1];
    logic signed [15:0] delay_im [0:TAPS-1];
    logic signed [47:0] acc_re, acc_im;
    logic signed [47:0] scaled_re, scaled_im;
    integer k;

    function automatic logic signed [15:0] sat16(input logic signed [47:0] value);
        if (value > 48'sd32767)
            sat16 = 16'sh7fff;
        else if (value < -48'sd32768)
            sat16 = 16'sh8000;
        else
            sat16 = value[15:0];
    endfunction

    always_comb begin
        acc_re = $signed(x_re) * $signed(coeff[0]);
        acc_im = $signed(x_im) * $signed(coeff[0]);
        for (k = 1; k < TAPS; k = k + 1) begin
            acc_re = acc_re + $signed(delay_re[k-1]) * $signed(coeff[k]);
            acc_im = acc_im + $signed(delay_im[k-1]) * $signed(coeff[k]);
        end
        scaled_re = acc_re >>> 15;
        scaled_im = acc_im >>> 15;
    end

    always_ff @(posedge clk) begin
        if (!rst_n) begin
            valid_out <= 1'b0;
            y_re <= 16'sd0;
            y_im <= 16'sd0;
            for (k = 0; k < TAPS; k = k + 1) begin
                delay_re[k] <= 16'sd0;
                delay_im[k] <= 16'sd0;
            end
        end else begin
            valid_out <= valid_in;
            if (valid_in) begin
                for (k = TAPS-1; k > 0; k = k - 1) begin
                    delay_re[k] <= delay_re[k-1];
                    delay_im[k] <= delay_im[k-1];
                end
                delay_re[0] <= x_re;
                delay_im[0] <= x_im;
                y_re <= sat16(scaled_re);
                y_im <= sat16(scaled_im);
            end
        end
    end
endmodule

