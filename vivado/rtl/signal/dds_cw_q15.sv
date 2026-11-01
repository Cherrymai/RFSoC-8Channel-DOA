// Small lookup-table DDS for simulation and portable synthesis experiments.
module dds_cw_q15 (
    input  logic               clk,
    input  logic               rst_n,
    input  logic               enable,
    input  logic        [31:0] phase_step,
    output logic signed [15:0] i_out,
    output logic signed [15:0] q_out,
    output logic               valid_out
);
    logic [31:0] phase_acc;

    always_ff @(posedge clk) begin
        if (!rst_n) begin
            phase_acc <= 32'd0;
            valid_out <= 1'b0;
        end else begin
            valid_out <= enable;
            if (enable)
                phase_acc <= phase_acc + phase_step;
        end
    end

    always_comb begin
        unique case (phase_acc[31:28])
            4'h0: begin i_out =  16'sd32767; q_out =      16'sd0; end
            4'h1: begin i_out =  16'sd30273; q_out =  16'sd12539; end
            4'h2: begin i_out =  16'sd23170; q_out =  16'sd23170; end
            4'h3: begin i_out =  16'sd12539; q_out =  16'sd30273; end
            4'h4: begin i_out =      16'sd0; q_out =  16'sd32767; end
            4'h5: begin i_out = -16'sd12539; q_out =  16'sd30273; end
            4'h6: begin i_out = -16'sd23170; q_out =  16'sd23170; end
            4'h7: begin i_out = -16'sd30273; q_out =  16'sd12539; end
            4'h8: begin i_out = -16'sd32767; q_out =      16'sd0; end
            4'h9: begin i_out = -16'sd30273; q_out = -16'sd12539; end
            4'ha: begin i_out = -16'sd23170; q_out = -16'sd23170; end
            4'hb: begin i_out = -16'sd12539; q_out = -16'sd30273; end
            4'hc: begin i_out =      16'sd0; q_out = -16'sd32767; end
            4'hd: begin i_out =  16'sd12539; q_out = -16'sd30273; end
            4'he: begin i_out =  16'sd23170; q_out = -16'sd23170; end
            default: begin i_out = 16'sd30273; q_out = -16'sd12539; end
        endcase
    end
endmodule

