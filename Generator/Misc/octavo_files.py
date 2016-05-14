#! /usr/bin/python

misc = [
  "Misc/params.v",
  "Misc/delay_line.v",
  "Misc/Address_Decoder.v",
  "Misc/Address_Translator.v",
  "Misc/Addressed_Mux.v",
  "Misc/Translated_Addressed_Mux.v",
  "Misc/Instruction_Annuller.v",
  "Misc/Thread_Number.v",
  "Misc/Instr_Decoder.v",
]

data_path = [ 
  "DataPath/ALU/AddSub_Carry_Select.v",
  "DataPath/ALU/AddSub_Ripple_Carry.v",
  "DataPath/ALU/Mult.v",
  "DataPath/ALU/Bitwise.v",
  "DataPath/ALU/ALU.v",
  "DataPath/DataPath.v",
]

control_path = [
  "ControlPath/Controller.v",
  "ControlPath/ControlPath.v",
]

memory = [
  "Memory/RAM_SDP.v",
  "Memory/RAM_SDP_no_fw.v",
  "Memory/Write_Enable.v",
  "Memory/Memory.v",
]

addressing = [
  "Addressing/Address_Adder.v",
  "Addressing/Addressing_Mapped_AB.v",
  "Addressing/Addressing_Mapped_D.v",
  "Addressing/Addressing_Thread_Number.v",
  "Addressing/Addressing.v",
  "Addressing/Address_Translation.v",
  "Addressing/Default_Offset.v",
  "Addressing/Increment_Adder.v",
  "Addressing/Increments.v",
  "Addressing/Programmed_Offsets.v",
  "Addressing/Write_Priority.v",
  "Addressing/Write_Synchronize.v",
]

branching = [
  "Branching/Branch_Check_Mapped.v",
  "Branching/Branch_Check.v",
  "Branching/Branch_Condition.v",
  "Branching/Branch_Destination.v",
  "Branching/Branch_Folding.v",
  "Branching/Branching_Flags.v",
  "Branching/Branching_Thread_Number.v",
  "Branching/Branch_Origin.v",
  "Branching/Branch_Origin_Check.v",
  "Branching/Branch_Cancel.v",
  "Branching/Branch_Prediction.v",
  "Branching/Branch_Prediction_Enable.v",
  "Branching/OR_Reducer.v",
]

io = [
  "IO/EmptyFullBit.v",
  "IO/IO_Active.v",
  "IO/IO_All_Ready.v",
  "IO/IO_Check.v",
  "IO/IO_Read.v",
  "IO/IO_Write.v",
  "IO/Port_Active.v",
]

all_files = misc + data_path + control_path + memory + addressing + branching + io
