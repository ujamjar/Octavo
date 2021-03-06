module Bitwise 
#(
    parameter               OPCODE_WIDTH        = 0,
    parameter               WORD_WIDTH          = 0 
)
(
    input                                       clock,
    input   wire            [OPCODE_WIDTH-1:0]  op,
    input   wire            [WORD_WIDTH-1:0]    add_sub_result,
    input   wire    signed  [WORD_WIDTH-1:0]    A,
    input   wire            [WORD_WIDTH-1:0]    B,
    output  reg             [WORD_WIDTH-1:0]    R
);
    reg     [WORD_WIDTH-1:0]   result;

    // These must match opcode LSBs in params.v
    always @(*) begin
        case (op)
            'b000: result <= A ^ B;
            'b001: result <= A & B;
            'b010: result <= A | B;
            'b011: result <= add_sub_result;    // SUB
            'b100: result <= add_sub_result;    // ADD
            'b101: result <= ~(A ^ B);          // Placeholders
            'b110: result <= ~(A & B);          //
            'b111: result <= ~(A | B);          //
            default: result <= A;  
        endcase 
    end

    always @(posedge clock) begin
        R <= result;
    end

    initial begin
        R = 0;
    end
endmodule


