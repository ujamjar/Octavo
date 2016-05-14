
import string
import random

from Misc import misc, octavo_files

install_base = misc.base_install_path()

def create_project_file(all_parameters, path):
    """Create a minimal .qpf file."""
    qpf_template = string.Template(
"""
PROJECT_REVISION = "${PROJECT_NAME}"
""")
    qpf = qpf_template.substitute(all_parameters)
    project_name = all_parameters["PROJECT_NAME"]
    misc.write_file(path, project_name + ".qpf", qpf)

def random_20bit_hex():
    rnd = random.getrandbits(20)
    return hex(rnd)[2:-1] # chop '0x' and 'L', leaving bare number

def random_color():
    return abs(int(random.getrandbits(24)))

def create_Scalar_partition(all_parameters):
    color = random_color()
    partition_id = random_20bit_hex()
    dp_template = string.Template(
"""        # start DESIGN_PARTITION(Scalar:Scalar)
    # -------------------------------------
        set_global_assignment -name PARTITION_NETLIST_TYPE SOURCE -section_id "Scalar:Scalar"
        set_global_assignment -name PARTITION_FITTER_PRESERVATION_LEVEL PLACEMENT_AND_ROUTING -section_id "Scalar:Scalar"
        set_global_assignment -name PARTITION_COLOR ${COLOR} -section_id "Scalar:Scalar"
        set_instance_assignment -name PARTITION_HIERARCHY scala_${ID} -to "${CPU_NAME}:DUT|Scalar:Scalar" -section_id "Scalar:Scalar"
    # end DESIGN_PARTITION(Scalar:Scalar)
    # -----------------------------------
""")
    all_parameters.update({"COLOR"  : color,
                           "ID"     : partition_id})
    dp = dp_template.substitute(all_parameters)
    return dp

def create_settings_file(all_parameters, path, install_base = install_base):
    """Create a .qsf file with all the necessary initial settings."""
    qsf_template = string.Template(
"""
# Project-Wide Assignments
# ========================
set_global_assignment -name LAST_QUARTUS_VERSION 15.1.0
set_global_assignment -name FLOW_DISABLE_ASSEMBLER ON
set_global_assignment -name SMART_RECOMPILE ON
set_global_assignment -name NUM_PARALLEL_PROCESSORS ${QUARTUS_NUM_PARALLEL_PROCESSORS}
set_global_assignment -name SDC_FILE ${install_base}/Octavo/Misc/timing.sdc
${octavo_files}
set_global_assignment -name VERILOG_FILE ${install_base}/Octavo/Octavo/Scalar.v
set_global_assignment -name VERILOG_FILE ${install_base}/Harness/output_register.v
set_global_assignment -name VERILOG_FILE ${install_base}/Harness/shift_register.v
set_global_assignment -name VERILOG_FILE ${install_base}/Harness/registered_reducer.v
set_global_assignment -name VERILOG_FILE ../${CPU_NAME}.v
set_global_assignment -name VERILOG_FILE ${PROJECT_NAME}.v
set_global_assignment -name FLOW_ENABLE_RTL_VIEWER OFF

# Classic Timing Assignments
# ==========================
set_global_assignment -name MIN_CORE_JUNCTION_TEMP 0
set_global_assignment -name MAX_CORE_JUNCTION_TEMP 85
set_global_assignment -name TIMEQUEST_MULTICORNER_ANALYSIS OFF
set_global_assignment -name TIMEQUEST_DO_REPORT_TIMING ON

# Compiler Assignments
# ====================
set_global_assignment -name OPTIMIZATION_MODE "AGGRESSIVE PERFORMANCE"

# Analysis & Synthesis Assignments
# ================================
set_global_assignment -name FAMILY "${FAMILY}"
set_global_assignment -name TOP_LEVEL_ENTITY ${PROJECT_NAME}
set_global_assignment -name DEVICE_FILTER_SPEED_GRADE FASTEST
set_global_assignment -name OPTIMIZATION_TECHNIQUE SPEED
set_global_assignment -name ADV_NETLIST_OPT_SYNTH_WYSIWYG_REMAP ON
set_global_assignment -name AUTO_SHIFT_REGISTER_RECOGNITION OFF
set_global_assignment -name REMOVE_REDUNDANT_LOGIC_CELLS ON
set_global_assignment -name MUX_RESTRUCTURE OFF
set_global_assignment -name ALLOW_ANY_ROM_SIZE_FOR_RECOGNITION ON
set_global_assignment -name ALLOW_ANY_RAM_SIZE_FOR_RECOGNITION ON
set_global_assignment -name ALLOW_ANY_SHIFT_REGISTER_SIZE_FOR_RECOGNITION OFF
set_global_assignment -name AUTO_RAM_RECOGNITION ON
set_global_assignment -name AUTO_RAM_TO_LCELL_CONVERSION OFF
set_global_assignment -name SYNTH_TIMING_DRIVEN_SYNTHESIS ON
set_global_assignment -name USE_LOGICLOCK_CONSTRAINTS_IN_BALANCING ON
set_global_assignment -name SAVE_DISK_SPACE OFF
set_global_assignment -name REMOVE_DUPLICATE_REGISTERS ON
set_global_assignment -name AUTO_RESOURCE_SHARING OFF
set_global_assignment -name SYNCHRONIZATION_REGISTER_CHAIN_LENGTH 3
set_global_assignment -name SYNTH_PROTECT_SDC_CONSTRAINT OFF
set_global_assignment -name SYNTHESIS_EFFORT AUTO
set_global_assignment -name PRE_MAPPING_RESYNTHESIS ON
set_global_assignment -name AUTO_PARALLEL_SYNTHESIS ON

# Fitter Assignments
# ==================
set_global_assignment -name DEVICE ${DEVICE}
set_global_assignment -name FITTER_EFFORT "STANDARD FIT"
set_global_assignment -name OPTIMIZE_IOC_REGISTER_PLACEMENT_FOR_TIMING OFF
set_global_assignment -name PHYSICAL_SYNTHESIS_COMBO_LOGIC ON
set_global_assignment -name PHYSICAL_SYNTHESIS_REGISTER_RETIMING ON
set_global_assignment -name PHYSICAL_SYNTHESIS_REGISTER_DUPLICATION ON
set_global_assignment -name PHYSICAL_SYNTHESIS_EFFORT EXTRA
set_global_assignment -name ROUTER_LCELL_INSERTION_AND_LOGIC_DUPLICATION ON
set_global_assignment -name ROUTER_TIMING_OPTIMIZATION_LEVEL MAXIMUM
set_global_assignment -name PHYSICAL_SYNTHESIS_COMBO_LOGIC_FOR_AREA OFF
set_global_assignment -name QII_AUTO_PACKED_REGISTERS NORMAL
set_global_assignment -name ROUTER_CLOCKING_TOPOLOGY_ANALYSIS ON
set_global_assignment -name PHYSICAL_SYNTHESIS_MAP_LOGIC_TO_MEMORY_FOR_AREA OFF
set_global_assignment -name BLOCK_RAM_TO_MLAB_CELL_CONVERSION OFF
set_global_assignment -name SEED 145014776
set_global_assignment -name PLACEMENT_EFFORT_MULTIPLIER 4
set_global_assignment -name ROUTER_EFFORT_MULTIPLIER 4
set_global_assignment -name AUTO_DELAY_CHAINS OFF
set_global_assignment -name OPTIMIZE_HOLD_TIMING "ALL PATHS"
set_global_assignment -name OPTIMIZE_MULTI_CORNER_TIMING ON
set_global_assignment -name BLOCK_RAM_AND_MLAB_EQUIVALENT_POWER_UP_CONDITIONS AUTO
set_global_assignment -name BLOCK_RAM_AND_MLAB_EQUIVALENT_PAUSED_READ_CAPABILITIES CARE
set_global_assignment -name OPTIMIZE_TIMING "NORMAL COMPILATION"
set_global_assignment -name FINAL_PLACEMENT_OPTIMIZATION ALWAYS
set_global_assignment -name FITTER_AGGRESSIVE_ROUTABILITY_OPTIMIZATION ALWAYS
set_global_assignment -name PERIPHERY_TO_CORE_PLACEMENT_AND_ROUTING_OPTIMIZATION OFF
set_global_assignment -name IO_PLACEMENT_OPTIMIZATION ON
set_global_assignment -name ROUTER_REGISTER_DUPLICATION AUTO
set_global_assignment -name OPTIMIZE_FOR_METASTABILITY ON
set_global_assignment -name FORCE_FITTER_TO_AVOID_PERIPHERY_PLACEMENT_WARNINGS OFF
set_global_assignment -name CLAMPING_DIODE OFF
set_global_assignment -name ADVANCED_PHYSICAL_OPTIMIZATION ON

# Design Assistant Assignments
# ============================
set_global_assignment -name ENABLE_DA_RULE "C101, C102, C103, C104, C105, C106, R101, R102, R103, R104, R105, T101, T102, A101, A102, A103, A104, A105, A106, A107, A108, A109, A110, S101, S102, S103, S104, D101, D102, D103, M101, M102, M103, M104, M105"
set_global_assignment -name ENABLE_DRC_SETTINGS ON

# Power Estimation Assignments
# ============================
set_global_assignment -name POWER_PRESET_COOLING_SOLUTION "NO HEAT SINK WITH STILL AIR"
set_global_assignment -name POWER_BOARD_THERMAL_MODEL "NONE (CONSERVATIVE)"
set_global_assignment -name POWER_USE_DEVICE_CHARACTERISTICS MAXIMUM

# Incremental Compilation Assignments
# ===================================
set_global_assignment -name RAPID_RECOMPILE_MODE OFF

# Netlist Viewer Assignments
# ==========================
set_global_assignment -name RTLV_GROUP_COMB_LOGIC_IN_CLOUD_TMV OFF

# -----------------------------------
# start ENTITY(${PROJECT_NAME})

    # start LOGICLOCK_REGION(${CPU_NAME}:DUT)
    # ------------------------------------

        # LogicLock Region Assignments
        # ============================
        set_global_assignment -name LL_ENABLED ${LL_ENABLED} -section_id "${CPU_NAME}:DUT"
        set_global_assignment -name LL_RESERVED ${LL_RESERVED} -section_id "${CPU_NAME}:DUT"
        set_global_assignment -name LL_SECURITY_ROUTING_INTERFACE OFF -section_id "${CPU_NAME}:DUT"
        set_global_assignment -name LL_IGNORE_IO_BANK_SECURITY_CONSTRAINT OFF -section_id "${CPU_NAME}:DUT"
        set_global_assignment -name LL_PR_REGION OFF -section_id "${CPU_NAME}:DUT"
        set_global_assignment -name LL_HEIGHT ${LL_HEIGHT} -section_id "${CPU_NAME}:DUT"
        set_global_assignment -name LL_WIDTH ${LL_WIDTH} -section_id "${CPU_NAME}:DUT"
        set_global_assignment -name LL_ORIGIN ${LL_ORIGIN} -section_id "${CPU_NAME}:DUT"
        set_global_assignment -name LL_STATE FLOATING -section_id "${CPU_NAME}:DUT"
        set_global_assignment -name LL_AUTO_SIZE ${LL_AUTO_SIZE} -section_id "${CPU_NAME}:DUT"
        set_global_assignment -name LL_ROUGH OFF -section_id "${CPU_NAME}:DUT"
        set_instance_assignment -name LL_MEMBER_OF "${CPU_NAME}:DUT" -to "${CPU_NAME}:DUT" -section_id "${CPU_NAME}:DUT"
        set_instance_assignment -name LL_MEMBER_EXCEPTIONS "MEMORY:DSP" -to "${CPU_NAME}:DUT" -section_id "${CPU_NAME}:DUT"
		set_instance_assignment -name LL_MEMBER_OF "${CPU_NAME}:DUT" -to "${CPU_NAME}:DUT|Scalar:Scalar|ControlPath:ControlPath|Controller:Controller|Controller_threads:threads_pc" -section_id "${CPU_NAME}:DUT"

    # end LOGICLOCK_REGION(${CPU_NAME}:DUT)
    # ----------------------------------

    # start LOGICLOCK_REGION(Root Region)
    # -----------------------------------

        # LogicLock Region Assignments
        # ============================
        set_global_assignment -name LL_ROOT_REGION ON -section_id "Root Region"
        set_global_assignment -name LL_MEMBER_STATE LOCKED -section_id "Root Region"

    # end LOGICLOCK_REGION(Root Region)
    # ---------------------------------

    # start DESIGN_PARTITION(Top)
    # ---------------------------

        # Incremental Compilation Assignments
        # ===================================
        set_global_assignment -name PARTITION_NETLIST_TYPE SOURCE -section_id Top
        set_global_assignment -name PARTITION_FITTER_PRESERVATION_LEVEL PLACEMENT_AND_ROUTING -section_id Top
        set_global_assignment -name PARTITION_COLOR 16764057 -section_id Top
        set_instance_assignment -name PARTITION_HIERARCHY root_partition -to | -section_id Top

    # end DESIGN_PARTITION(Top)
    # -------------------------

    # start DESIGN_PARTITION(${CPU_NAME}:DUT)
    # ------------------------------------

        # Incremental Compilation Assignments
        # ===================================
        set_global_assignment -name PARTITION_NETLIST_TYPE SOURCE -section_id "${CPU_NAME}:DUT"
        set_global_assignment -name PARTITION_FITTER_PRESERVATION_LEVEL PLACEMENT_AND_ROUTING -section_id "${CPU_NAME}:DUT"
        set_global_assignment -name PARTITION_COLOR 39423 -section_id "${CPU_NAME}:DUT"
        set_instance_assignment -name PARTITION_HIERARCHY dut_2ae21 -to "${CPU_NAME}:DUT" -section_id "${CPU_NAME}:DUT"

    # end DESIGN_PARTITION(${CPU_NAME}:DUT)
    # ----------------------------------

${SCALAR_PARTITION}

# end ENTITY(${PROJECT_NAME})
# ---------------------------------
""")
    all_parameters["install_base"] = install_base
    all_parameters["octavo_files"] = string.join( 
        map(lambda f: \
                ("set_global_assignment -name VERILOG_FILE " + 
                install_base + "/Octavo/" + f), \
            # keep the file order similar to previous version.
            # octavo_files.all_files would probably work fine here as well.
            #
            # Thread_Number + PortActive are in a different order anyway
            # EmptyFullBit was excluded before.
            (octavo_files.misc + 
            octavo_files.data_path + 
            octavo_files.control_path + 
            octavo_files.io + 
            octavo_files.branching + 
            octavo_files.addressing + 
            octavo_files.memory)),
        "\n")

    if all_parameters["PARTITION_SCALAR"] == True:
        scalar_module_partition = create_Scalar_partition(all_parameters)
    else:
        scalar_module_partition = ""

    all_parameters.update({"SCALAR_PARTITION":scalar_module_partition})
    qsf = qsf_template.substitute(all_parameters)
    project_name = all_parameters["PROJECT_NAME"]
    misc.write_file(path, project_name + ".qsf", qsf)

#def create_stub_mem_init_files(all_parameters, path):
#    misc.write_file(path, all_parameters["A_INIT_FILE"].strip('"'),  "")
#    misc.write_file(path, all_parameters["B_INIT_FILE"].strip('"'),  "")
#    misc.write_file(path, all_parameters["I_INIT_FILE"].strip('"'),  "")
#    misc.write_file(path, all_parameters["PC_INIT_FILE"].strip('"'), "")

def create_warning_suppress_file(all_parameters, path):
    """Create a .srf file which suppresses the common useless warnings and infos."""
    project_name = all_parameters["PROJECT_NAME"]
    srf_file_contents = """
{ "" "" "" "*" {  } {  } 0 10230 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 276020 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 20028 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 170136 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 292013 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 16303 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 12021 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 12127 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 12128 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 12130 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 12133 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 12131 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 276014 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 19000 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 17026 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 332115 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 332114 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 332140 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 332146 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 332102 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 332097 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 332123 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 332151 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 334003 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 334004 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 332104 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 21077 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 293026 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 286030 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 17049 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 16010 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 21057 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 119006 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 171004 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 176045 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 184020 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 11191 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 184021 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 176233 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 176222 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 332129 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 332111 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 176235 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 128000 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 128002 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 128003 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 128001 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 11798 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 170189 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 14951 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 170190 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 170191 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 170137 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 170192 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 170193 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 170195 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 170194 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 11888 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 11801 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 308046 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 308044 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 308012 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 23030 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 308007 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 308002 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*" {  } {  } 0 11105 "" 0 0 "Design Software" 0 -1 0 ""}
{ "" "" "" "*translation_table*" {  } {  } 0 9999 "" 0 0 "Design Software" 0 -1 0 ""}
"""
    misc.write_file(path, project_name + ".srf", srf_file_contents)

def project(all_parameters, path):
    create_project_file(all_parameters, path)
    create_settings_file(all_parameters, path)
    create_warning_suppress_file(all_parameters, path)
#    create_stub_mem_init_files(all_parameters, path)

