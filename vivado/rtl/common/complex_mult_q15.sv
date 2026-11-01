// Q1.15 complex multiplier. Portable reference RTL; no board-specific logic.
module complex_mult_q15 (
    input  logic signed [15:0] a_re,
    input  logic signed [15:0] a_im,
    input  logic signed [15:0] b_re,
    input  logic signed [15:0] b_im,
    output logic signed [15:0] y_re,
    output logic signed [15:0] y_im
);
    logic signed [31:0] p_rr, p_ii, p_ri, p_ir;
    logic signed [32:0] full_re, full_im;
    logic signed [32:0] scaled_re, scaled_im;

    function automatic logic signed [15:0] sat16(input logic signed [32:0] value);
        if (value > 33'sd32767)
            sat16 = 16'sh7fff;
        else if (value < -33'sd32768)
            sat16 = 16'sh8000;
        else
            sat16 = value[15:0];
    endfunction

    always_comb begin
        p_rr = a_re * b_re;
        p_ii = a_im * b_im;
        p_ri = a_re * b_im;
        p_ir = a_im * b_re;
        full_re = $signed({p_rr[31], p_rr}) - $signed({p_ii[31], p_ii});
        full_im = $signed({p_ri[31], p_ri}) + $signed({p_ir[31], p_ir});
        scaled_re = full_re >>> 15;
        scaled_im = full_im >>> 15;
        y_re = sat16(scaled_re);
        y_im = sat16(scaled_im);
    end
endmodule

