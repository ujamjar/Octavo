
// Generates a new PC and Jump signal if the current PC matches a branch origin
// and the result flags of the previous thread instruction match the condition
// code, otherwise all outputs got to zero. Later OR-reduction computes the
// final new PC and Jump signal for the Controller.

module Branch_Check
#(
    parameter   PC_WIDTH                            = 0,
    parameter   D_OPERAND_WIDTH                     = 0,
    parameter   WORD_WIDTH                          = 0,

    parameter   INITIAL_THREAD                      = 0,
    parameter   THREAD_COUNT                        = 0,
    parameter   THREAD_ADDR_WIDTH                   = 0,

    parameter   ORIGIN_WORD_WIDTH                   = 0,
    parameter   ORIGIN_ADDR_WIDTH                   = 0,
    parameter   ORIGIN_DEPTH                        = 0,
    parameter   ORIGIN_RAMSTYLE                     = 0,
    parameter   ORIGIN_INIT_FILE                    = 0,

    parameter   DESTINATION_WORD_WIDTH              = 0,
    parameter   DESTINATION_ADDR_WIDTH              = 0,
    parameter   DESTINATION_DEPTH                   = 0,
    parameter   DESTINATION_RAMSTYLE                = 0,
    parameter   DESTINATION_INIT_FILE               = 0,

    parameter   CONDITION_WORD_WIDTH                = 0,
    parameter   CONDITION_ADDR_WIDTH                = 0,
    parameter   CONDITION_DEPTH                     = 0,
    parameter   CONDITION_RAMSTYLE                  = 0,
    parameter   CONDITION_INIT_FILE                 = 0,

    parameter   PREDICTION_WORD_WIDTH               = 0,
    parameter   PREDICTION_ADDR_WIDTH               = 0,
    parameter   PREDICTION_DEPTH                    = 0,
    parameter   PREDICTION_RAMSTYLE                 = 0,
    parameter   PREDICTION_INIT_FILE                = 0,

    parameter   PREDICTION_ENABLE_WORD_WIDTH        = 0,
    parameter   PREDICTION_ENABLE_ADDR_WIDTH        = 0,
    parameter   PREDICTION_ENABLE_DEPTH             = 0,
    parameter   PREDICTION_ENABLE_RAMSTYLE          = 0,
    parameter   PREDICTION_ENABLE_INIT_FILE         = 0,

    parameter   FLAGS_WORD_WIDTH                    = 0,
    parameter   FLAGS_ADDR_WIDTH                    = 0
)
(
    input   wire                                    clock,
    input   wire    [PC_WIDTH-1:0]                  PC,
    input   wire    [FLAGS_WORD_WIDTH-1:0]          flags,
    input   wire                                    IO_ready_previous,

    input   wire                                    ALU_wren_BO,    // Branch Origin Memory
    input   wire                                    ALU_wren_BD,    // Branch Destination Memory
    input   wire                                    ALU_wren_BC,    // Branch Condition Memory
    input   wire                                    ALU_wren_BP,    // Branch Prediction Memory
    input   wire                                    ALU_wren_BPE,   // Branch Prediction Enable Memory

    // Subsets of full data word, so we can align multiple memories along a single word.
    // We want to keep all memory map knowledge in the encapsulating module.
    input   wire    [ORIGIN_WORD_WIDTH-1:0]         ALU_write_data_BO,
    input   wire    [DESTINATION_WORD_WIDTH-1:0]    ALU_write_data_BD,
    input   wire    [CONDITION_WORD_WIDTH-1:0]      ALU_write_data_BC,
    input   wire    [PREDICTION_WORD_WIDTH-1:0]     ALU_write_data_BP,
    input   wire    [PREDICTION_ENABLE_WORD_WIDTH-1:0]  ALU_write_data_BPE,

    output  wire    [PC_WIDTH-1:0]                  branch_destination,
    output  wire                                    jump,
    output  wire                                    cancel
);

// -----------------------------------------------------------

    wire    [THREAD_ADDR_WIDTH-1:0]     read_thread;
    wire    [THREAD_ADDR_WIDTH-1:0]     write_thread;

    Branching_Thread_Number
    #(
        .INITIAL_THREAD     (INITIAL_THREAD),
        .THREAD_COUNT       (THREAD_COUNT),
        .THREAD_ADDR_WIDTH  (THREAD_ADDR_WIDTH)   
    )
    BTC
    (
        .clock              (clock),
        .read_thread        (read_thread),
        .write_thread       (write_thread)
    );

// -----------------------------------------------------------

    wire    [ORIGIN_WORD_WIDTH-1:0]     branch_origin;

    Branch_Origin
    #(
        .WORD_WIDTH     (ORIGIN_WORD_WIDTH),
        .ADDR_WIDTH     (ORIGIN_ADDR_WIDTH),
        .DEPTH          (ORIGIN_DEPTH),
        .RAMSTYLE       (ORIGIN_RAMSTYLE),
        .INIT_FILE      (ORIGIN_INIT_FILE)
    )
    BO
    (
        .clock          (clock),
        .wren           (ALU_wren_BO),
        .write_addr     (write_thread),
        .write_data     (ALU_write_data_BO),
        .read_addr      (read_thread),
        .branch_origin  (branch_origin)
    );

// -----------------------------------------------------------

    wire    [DESTINATION_WORD_WIDTH-1:0]    branch_destination_raw;

    Branch_Destination
    #(
        .WORD_WIDTH         (DESTINATION_WORD_WIDTH),
        .ADDR_WIDTH         (DESTINATION_ADDR_WIDTH),
        .DEPTH              (DESTINATION_DEPTH),
        .RAMSTYLE           (DESTINATION_RAMSTYLE),
        .INIT_FILE          (DESTINATION_INIT_FILE)
    )
    BD
    (
        .clock              (clock),
        .wren               (ALU_wren_BD),
        .write_addr         (write_thread),
        .write_data         (ALU_write_data_BD),
        .read_addr          (read_thread),
        .branch_destination (branch_destination_raw)
    );

// -----------------------------------------------------------

    wire    [CONDITION_WORD_WIDTH-1:0]      branch_condition;

    Branch_Condition
    #(
        .WORD_WIDTH         (CONDITION_WORD_WIDTH),
        .ADDR_WIDTH         (CONDITION_ADDR_WIDTH),
        .DEPTH              (CONDITION_DEPTH),
        .RAMSTYLE           (CONDITION_RAMSTYLE),
        .INIT_FILE          (CONDITION_INIT_FILE)
    )
    BC
    (
        .clock              (clock),
        .wren               (ALU_wren_BC),
        .write_addr         (write_thread),
        .write_data         (ALU_write_data_BC),
        .read_addr          (read_thread),
        .branch_condition   (branch_condition)
    );

// -----------------------------------------------------------

    wire    [PREDICTION_WORD_WIDTH-1:0]      branch_prediction;

    Branch_Prediction
    #(
        .WORD_WIDTH         (PREDICTION_WORD_WIDTH),
        .ADDR_WIDTH         (PREDICTION_ADDR_WIDTH),
        .DEPTH              (PREDICTION_DEPTH),
        .RAMSTYLE           (PREDICTION_RAMSTYLE),
        .INIT_FILE          (PREDICTION_INIT_FILE)
    )
    BP
    (
        .clock              (clock),
        .wren               (ALU_wren_BP),
        .write_addr         (write_thread),
        .write_data         (ALU_write_data_BP),
        .read_addr          (read_thread),
        .branch_prediction  (branch_prediction)
    );

// -----------------------------------------------------------

    wire    [PREDICTION_ENABLE_WORD_WIDTH-1:0]  branch_prediction_enable;

    Branch_Prediction_Enable
    #(
        .WORD_WIDTH         (PREDICTION_ENABLE_WORD_WIDTH),
        .ADDR_WIDTH         (PREDICTION_ENABLE_ADDR_WIDTH),
        .DEPTH              (PREDICTION_ENABLE_DEPTH),
        .RAMSTYLE           (PREDICTION_ENABLE_RAMSTYLE),
        .INIT_FILE          (PREDICTION_ENABLE_INIT_FILE)
    )
    BPE
    (
        .clock              (clock),
        .wren               (ALU_wren_BPE),
        .write_addr         (write_thread),
        .write_data         (ALU_write_data_BPE),
        .read_addr          (read_thread),
        .branch_prediction_enable   (branch_prediction_enable)
    );

// -----------------------------------------------------------

    wire    [PC_WIDTH-1:0]  PC_synced;

    delay_line
    #(
        .DEPTH  (2),
        .WIDTH  (PC_WIDTH)
    )
    PC_synchronizer
    (
        .clock  (clock),
        .in     (PC),
        .out    (PC_synced)
    );

// -----------------------------------------------------------

    wire    branch_origin_hit_stage2;
    wire    branch_origin_hit_stage3;

    Branch_Origin_Check
    #(
        .PC_WIDTH       (PC_WIDTH)
    )
    BOC
    (
        .clock          (clock),
        .PC             (PC_synced),
        .branch_origin  (branch_origin),
        .hit_stage2     (branch_origin_hit_stage2),
        .hit_stage3     (branch_origin_hit_stage3)
    );

// -----------------------------------------------------------

    wire    [PC_WIDTH-1:0]  branch_destination_origin_masked_raw;

    // If the branch origin doesn't match, zero-out the branch destination

    Instruction_Annuller
    #(
        .INSTR_WIDTH    (PC_WIDTH)
    )
    BD_origin_mask
    (
        .instr_in       (branch_destination_raw),
        .annul          (~branch_origin_hit_stage2),
        .instr_out      (branch_destination_origin_masked_raw)
    );
// -----------------------------------------------------------

    wire    [PC_WIDTH-1:0]  branch_destination_origin_masked;

    delay_line
    #(
        .DEPTH  (1),
        .WIDTH  (PC_WIDTH)
    )
    BD_origin_mask_pipeline
    (
        .clock  (clock),
        .in     (branch_destination_origin_masked_raw),
        .out    (branch_destination_origin_masked)
    );

// -----------------------------------------------------------

    wire    flag_raw;

    Addressed_Mux
    #(
        .WORD_WIDTH     (1),
        .ADDR_WIDTH     (FLAGS_ADDR_WIDTH),
        .INPUT_COUNT    (FLAGS_WORD_WIDTH),
        .REGISTERED     (`FALSE)
    )
    flag_selector
    (
        .clock          (clock),
        .addr           (branch_condition),
        .data_in        (flags),
        .data_out       (flag_raw)
    );

// -----------------------------------------------------------

    wire    jump_previous;
    wire    adjusted_flag;

    // ECL XXX If we return here because the instruction in parallel with the
    // branch was re-issued while waiting for I/O, then use the original jump
    // decision, not the current one. Otherwise, the decision would be made on
    // the previous result of *this* instruction, previously annulled and
    // necessarily zero, rather than the result of the actual previous
    // instruction.

    // ECL XXX This feels like a can of worms, potentially introducing bad
    // interactions between branches and I/O predication if branch conditions
    // depend on I/O.

    // always @(*) begin
    //     if (IO_ready_previous == `HIGH) begin
    //         flag <= flag_raw;
    //     end
    //     else begin
    //         flag <= jump_previous;
    //     end
    // end

    Addressed_Mux
    #(
        .WORD_WIDTH     (1),
        .ADDR_WIDTH     (1),
        .INPUT_COUNT    (2),
        .REGISTERED     (`FALSE)
    )
    adjusted_flag_selector
    (
        .clock          (clock),
        .addr           (IO_ready_previous),
        .data_in        ({flag_raw, jump_previous}),
        .data_out       (adjusted_flag)
    );

// -----------------------------------------------------------

    wire    flag;

    delay_line
    #(
        .DEPTH  (1),
        .WIDTH  (1)
    )
    flag_pipeline
    (
        .clock  (clock),
        .in     (adjusted_flag),
        .out    (flag)
    );


// -----------------------------------------------------------

    // Note we use the IO_ready adjusted flag, as we would not want to cancel a
    // pending annulled instruction because the flags changed.

    Branch_Cancel
    // No parameters
    Cancel_instruction
    (
        .clock                      (clock),
        .branch_prediction          (branch_prediction),
        .branch_prediction_enable   (branch_prediction_enable),
        .branch_origin_hit          (branch_origin_hit_stage2),
        .flag                       (adjusted_flag),
        .cancel                     (cancel)
    );

// -----------------------------------------------------------

    wire    [PC_WIDTH-1:0]  branch_destination_flag_masked_raw;

    // If the branch condition doesn't match, zero-out the branch destination
    
    Instruction_Annuller
    #(
        .INSTR_WIDTH    (PC_WIDTH)
    )
    BD_flag_mask
    (
        .instr_in       (branch_destination_origin_masked),
        .annul          (~flag),
        .instr_out      (branch_destination_flag_masked_raw)
    );

// -----------------------------------------------------------

    delay_line
    #(
        .DEPTH  (1),
        .WIDTH  (PC_WIDTH)
    )
    BD_flag_mask_pipeline
    (
        .clock  (clock),
        .in     (branch_destination_flag_masked_raw),
        .out    (branch_destination)
    );

// -----------------------------------------------------------

    reg     jump_raw;

    // If the branch origin doesn't match, zero-out the jump decision We only
    // branch if the branch origin *and* the branch condition match.
    // Otherwise, we zero out both the branch destination and jump signal.  A
    // higher module OR-reduces all the instances to generate the final branch
    // destination and jump signal.

    always @(*) begin
        jump_raw <= flag & branch_origin_hit_stage3;
    end

    delay_line
    #(
        .DEPTH  (1),
        .WIDTH  (1)
    )
    jump_pipeline
    (
        .clock  (clock),
        .in     (jump_raw),
        .out    (jump)
    );

// -----------------------------------------------------------

    // Recicrculate the local jump decision for re-issue of annulled instr.
    // ECL XXX hardcoded...
    // -2 from 8 since jump registered out of stage 4, after IO_ready, and we use in stage 3
    delay_line
    #(
        .DEPTH  (6),
        .WIDTH  (1)
    )
    jump_previous_pipeline
    (
        .clock  (clock),
        .in     (jump),
        .out    (jump_previous)
    );


endmodule


