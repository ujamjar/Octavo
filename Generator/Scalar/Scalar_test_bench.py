#! /usr/bin/python

import string
import os
import sys

from Misc import misc, parameters_misc, octavo_files

default_bench = "Hailstone/hailstone"
install_base = misc.base_install_path()
quartus_base_path = misc.quartus_base_path

def test_bench(parameters, default_bench = default_bench, install_base = install_base):
    assembler_base = os.path.join(install_base, "Assembler")
    test_bench_template = string.Template(
"""module ${CPU_NAME}_test_bench
#(
    parameter       A_WORD_WIDTH                = ${A_WORD_WIDTH},
    parameter       B_WORD_WIDTH                = ${B_WORD_WIDTH},

    parameter       INSTR_WIDTH                 = ${INSTR_WIDTH},

    parameter       A_IO_READ_PORT_COUNT        = ${A_IO_READ_PORT_COUNT},
    parameter       A_IO_WRITE_PORT_COUNT       = ${A_IO_WRITE_PORT_COUNT},
    parameter       B_IO_READ_PORT_COUNT        = ${B_IO_READ_PORT_COUNT},
    parameter       B_IO_WRITE_PORT_COUNT       = ${B_IO_WRITE_PORT_COUNT},

    parameter       A_INIT_FILE                 = "${assembler_base}/${default_bench}.A",
    parameter       B_INIT_FILE                 = "${assembler_base}/${default_bench}.B",
    parameter       I_INIT_FILE                 = "${assembler_base}/${default_bench}.I",
    parameter       PC_INIT_FILE                = "${assembler_base}/${default_bench}.PC",

    parameter       A_DEFAULT_OFFSET_INIT_FILE  = "${assembler_base}/${default_bench}.ADO",
    parameter       B_DEFAULT_OFFSET_INIT_FILE  = "${assembler_base}/${default_bench}.BDO",
    parameter       D_DEFAULT_OFFSET_INIT_FILE  = "${assembler_base}/${default_bench}.DDO",

    parameter       A_PROGRAMMED_OFFSETS_INIT_FILE  = "${assembler_base}/${default_bench}.APO",
    parameter       B_PROGRAMMED_OFFSETS_INIT_FILE  = "${assembler_base}/${default_bench}.BPO",
    parameter       D_PROGRAMMED_OFFSETS_INIT_FILE  = "${assembler_base}/${default_bench}.DPO",

    parameter       A_INCREMENTS_INIT_FILE  = "${assembler_base}/${default_bench}.AIN",
    parameter       B_INCREMENTS_INIT_FILE  = "${assembler_base}/${default_bench}.BIN",
    parameter       D_INCREMENTS_INIT_FILE  = "${assembler_base}/${default_bench}.DIN",

    parameter       ORIGIN_INIT_FILE       = "${assembler_base}/${default_bench}.BO",
    parameter       DESTINATION_INIT_FILE  = "${assembler_base}/${default_bench}.BD",
    parameter       CONDITION_INIT_FILE    = "${assembler_base}/${default_bench}.BC",
    parameter       PREDICTION_INIT_FILE    = "${assembler_base}/${default_bench}.BP",
    parameter       PREDICTION_ENABLE_INIT_FILE    = "${assembler_base}/${default_bench}.BPE"
)
(
    output  wire    [INSTR_WIDTH-1:0]                           I_read_data,

    output  reg     [(A_WORD_WIDTH * A_IO_READ_PORT_COUNT)-1:0] A_in,
    output  wire    [(               A_IO_READ_PORT_COUNT)-1:0] A_rden,
    output  reg     [(               A_IO_READ_PORT_COUNT)-1:0] A_in_EF,
    output  wire    [(A_WORD_WIDTH * A_IO_WRITE_PORT_COUNT)-1:0] A_out, 
    output  wire    [(               A_IO_WRITE_PORT_COUNT)-1:0] A_wren,
    output  reg     [(               A_IO_WRITE_PORT_COUNT)-1:0] A_out_EF,
    
    output  reg     [(B_WORD_WIDTH * B_IO_READ_PORT_COUNT)-1:0] B_in,
    output  wire    [(               B_IO_READ_PORT_COUNT)-1:0] B_rden,
    output  reg     [(               B_IO_READ_PORT_COUNT)-1:0] B_in_EF,
    output  wire    [(B_WORD_WIDTH * B_IO_WRITE_PORT_COUNT)-1:0] B_out, 
    output  wire    [(               B_IO_WRITE_PORT_COUNT)-1:0] B_wren,    
    output  reg     [(               B_IO_WRITE_PORT_COUNT)-1:0] B_out_EF
);
    integer     cycle;
    reg         clock;
    reg         half_clock;

    initial begin
        cycle       = 0;
        clock       = 0;
        half_clock  = 0;
        A_in        = -1;
        B_in        = -1;
        A_in_EF     = -1;
        A_out_EF    = 0;
        B_in_EF     = -1;
        B_out_EF    = 0;
        `DELAY_CLOCK_CYCLES(200000) $$stop;
    end

    always begin
        `DELAY_CLOCK_HALF_PERIOD clock <= ~clock;
    end

    always @(posedge clock) begin
        half_clock <= ~half_clock;
    end

    always @(posedge clock) begin
        cycle <= cycle + 1;
    end

    // End Hailstone at end of sequence.
    always @(posedge clock) begin
        if (A_wren == 1'b1) begin
            $$display("AOUT: %d", A_out);
            if (A_out == 'd1) begin
                $$stop;
            end
        end
    end

//    always begin
//        // Read Empty, Write Full
//        `DELAY_CLOCK_CYCLES(100)
//        A_in_EF  = 0;
//        A_out_EF = -1;
//        B_in_EF  = 0;
//        B_out_EF = -1;
        
//        // Read Full, Write Empty
//        `DELAY_CLOCK_CYCLES(100)
//        A_in_EF  = -1;
//        A_out_EF = 0;
//        B_in_EF  = -1;
//        B_out_EF = 0;

//        // Read Empty, Write Empty
//        `DELAY_CLOCK_CYCLES(100)
//        A_in_EF  = 0;
//        A_out_EF = 0;
//        B_in_EF  = 0;
//        B_out_EF = 0;

//        // Read Full, Write Full
//        `DELAY_CLOCK_CYCLES(100)
//        A_in_EF  = -1;
//        A_out_EF = -1;
//        B_in_EF  = -1;
//        B_out_EF = -1;

//    end

    localparam WREN_OTHER_DEFAULT = `HIGH;
    localparam ALU_C_IN_DEFAULT   = `LOW;

    ${CPU_NAME} 
    #(
        .A_INIT_FILE                    (A_INIT_FILE),
        .B_INIT_FILE                    (B_INIT_FILE),
        .I_INIT_FILE                    (I_INIT_FILE),
        .PC_INIT_FILE                   (PC_INIT_FILE),

        .A_DEFAULT_OFFSET_INIT_FILE     (A_DEFAULT_OFFSET_INIT_FILE),
        .B_DEFAULT_OFFSET_INIT_FILE     (B_DEFAULT_OFFSET_INIT_FILE),
        .D_DEFAULT_OFFSET_INIT_FILE     (D_DEFAULT_OFFSET_INIT_FILE),

        .A_PROGRAMMED_OFFSETS_INIT_FILE     (A_PROGRAMMED_OFFSETS_INIT_FILE),
        .B_PROGRAMMED_OFFSETS_INIT_FILE     (B_PROGRAMMED_OFFSETS_INIT_FILE),
        .D_PROGRAMMED_OFFSETS_INIT_FILE     (D_PROGRAMMED_OFFSETS_INIT_FILE),

        .A_INCREMENTS_INIT_FILE     (A_INCREMENTS_INIT_FILE),
        .B_INCREMENTS_INIT_FILE     (B_INCREMENTS_INIT_FILE),
        .D_INCREMENTS_INIT_FILE     (D_INCREMENTS_INIT_FILE),

        .ORIGIN_INIT_FILE           (ORIGIN_INIT_FILE),
        .DESTINATION_INIT_FILE      (DESTINATION_INIT_FILE),
        .CONDITION_INIT_FILE        (CONDITION_INIT_FILE),
        .PREDICTION_INIT_FILE        (PREDICTION_INIT_FILE),
        .PREDICTION_ENABLE_INIT_FILE        (PREDICTION_ENABLE_INIT_FILE)
    )
    DUT 
    (
        .clock              (clock),
        .half_clock         (half_clock),

        .I_wren_other       (`HIGH),
        .A_wren_other       (WREN_OTHER_DEFAULT),
        .B_wren_other       (WREN_OTHER_DEFAULT),

        .ALU_c_in           (ALU_C_IN_DEFAULT),
        .ALU_c_out          (),

        .I_read_data        (I_read_data),

        .A_in               (A_in),
        .A_rden             (A_rden),
        .A_in_EF            (A_in_EF),
        .A_out              (A_out),
        .A_wren             (A_wren),
        .A_out_EF           (A_out_EF),
        
        .B_in               (B_in),
        .B_rden             (B_rden),
        .B_in_EF            (B_in_EF),
        .B_out              (B_out),
        .B_wren             (B_wren),
        .B_out_EF           (B_out_EF)
    );
endmodule
""")
    parameters["default_bench"] = default_bench
    parameters["assembler_base"] = assembler_base
    return test_bench_template.substitute(parameters)

def test_bench_script(parameters, default_bench = default_bench, install_base = install_base, quartus_base_path = quartus_base_path):
    test_bench_script_template = string.Template(
"""#! /bin/bash

INSTALL_BASE="${install_base}"

TOP_LEVEL_MODULE="${CPU_NAME}_test_bench"
TESTBENCH="./$${TOP_LEVEL_MODULE}.v"

LPM_LIBRARY="${quartus_base_path}/quartus/eda/sim_lib/220model.v"
ALT_LIBRARY="${quartus_base_path}/quartus/eda/sim_lib/altera_mf.v"

OCTAVO="$$INSTALL_BASE/Octavo/${octavo_files} \\
        $$INSTALL_BASE/Octavo/Octavo/Scalar.v \\
        ../${CPU_NAME}.v \\
"

VLIB="work"

VSIM_ACTIONS="vcd file $$TOP_LEVEL_MODULE.vcd ; vcd add -r /* ; run -all ; quit"

rm $$TOP_LEVEL_MODULE.wlf $$TOP_LEVEL_MODULE.vcd
vlib $$VLIB 2>&1 > LOG
vlog -mfcu -incr -lint $$LPM_LIBRARY $$ALT_LIBRARY $$OCTAVO $$TESTBENCH 2>&1 >> LOG
vsim -voptargs="+acc" -c -do "$$VSIM_ACTIONS" $$TOP_LEVEL_MODULE 2>&1 >> LOG
vcd2wlf $$TOP_LEVEL_MODULE.vcd $$TOP_LEVEL_MODULE.wlf 2>&1 >> LOG
rm vsim.wlf
grep AOUT LOG | sed -e's/# AOUT:\s*//' > output
""")
    parameters["default_bench"]     = default_bench
    parameters["install_base"]      = install_base
    parameters["quartus_base_path"] = quartus_base_path
    parameters["octavo_files"]      = string.join(octavo_files.all_files, 
                                                  " \\\n        $INSTALL_BASE/Octavo/")
    return test_bench_script_template.substitute(parameters)

def file_list(parameters, install_base):
  files = octavo_files.all_files + ["Octavo/Scalar.v" ]
  files = map(lambda f: install_base + "/Octavo/" + f + "\n", files)
  files = files + ["../" + parameters["CPU_NAME"] + ".v\n"]
  return string.join(files, "")

def test_bench_script_icarus(parameters):
  test_bench_template = string.Template(
"""
rm a.out
TOP_LEVEL_MODULE="${CPU_NAME}_test_bench"
TESTBENCH="./$${TOP_LEVEL_MODULE}.v"
LPM_LIBRARY="${quartus_base_path}/quartus/eda/sim_lib/220model.v"
ALT_LIBRARY="${quartus_base_path}/quartus/eda/sim_lib/altera_mf.v"
iverilog $$LPM_LIBRARY $$ALT_LIBRARY -ffile_list.txt $$TESTBENCH -s $$TOP_LEVEL_MODULE
./a.out
""")
  return test_bench_template.substitute(parameters)

def main(parameters = {}):
    name                 = parameters["CPU_NAME"]
    test_bench_name      = name + "_" + misc.bench_name
    test_bench_file      = test_bench(parameters)
    test_bench_run       = test_bench_script(parameters)
    test_bench_run_icarus= test_bench_script_icarus(parameters)
    test_bench_dir       = os.path.join(os.getcwd(), misc.bench_name)
    test_bench_file_list = file_list(parameters, install_base)
    misc.write_file(test_bench_dir, test_bench_name + ".v", test_bench_file)
    misc.write_file(test_bench_dir, "run_" + misc.bench_name, test_bench_run)
    misc.make_file_executable(test_bench_dir, "run_" + misc.bench_name)
    misc.write_file(test_bench_dir, "file_list.txt", str(test_bench_file_list))
    misc.write_file(test_bench_dir, "run_" + misc.bench_name + "_icarus", test_bench_run_icarus)
    misc.make_file_executable(test_bench_dir, "run_" + misc.bench_name + "_icarus")
    
if __name__ == "__main__":
    parameters          = parameters_misc.parse_cmdline(sys.argv[1:])
    main(parameters)
