`timescale 1ns/1ps

module tb_beamformer8_q15;
    logic clk = 1'b0;
    logic rst_n = 1'b0;
    logic valid_in = 1'b0;
    logic signed [15:0] ch_re [0:7];
    logic signed [15:0] ch_im [0:7];
    logic signed [15:0] weight_re [0:7];
    logic signed [15:0] weight_im [0:7];
    logic valid_out;
    logic signed [15:0] beam_re, beam_im;
    integer k;

    always #5 clk = ~clk;

    beamformer8_q15 dut (
        .clk(clk), .rst_n(rst_n), .valid_in(valid_in),
        .ch_re(ch_re), .ch_im(ch_im),
        .weight_re(weight_re), .weight_im(weight_im),
        .valid_out(valid_out), .beam_re(beam_re), .beam_im(beam_im)
    );

    initial begin
        for (k = 0; k < 8; k = k + 1) begin
            ch_re[k] = 16'sd1000;
            ch_im[k] = 16'sd0;
            weight_re[k] = 16'sd4096; // 1/8 in Q1.15
            weight_im[k] = 16'sd0;
        end

        repeat (4) @(posedge clk);
        @(negedge clk);
        rst_n = 1'b1;
        @(negedge clk);
        valid_in = 1'b1;
        @(posedge clk);
        #1;

        if (!valid_out || beam_re < 16'sd996 || beam_re > 16'sd1004 || beam_im != 0) begin
            $error("Unexpected beamformer output: valid=%0d re=%0d im=%0d", valid_out, beam_re, beam_im);
            $finish(1);
        end
        $display("PASS beam_re=%0d beam_im=%0d", beam_re, beam_im);
        @(negedge clk);
        valid_in = 1'b0;
        $finish(0);
    end
endmodule

