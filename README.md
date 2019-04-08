# Assembler
this program takes a MIPS assembly program from the user and shows 
its corresponding machine code.The required instructions are 
1. R-type instructions: add, and, sub, or, nor and slt, 
2. I-type instructions: addi, lw, sw, beq, bne and 
3. J-type instruction: j. 

3.1 User Input 
• The user code consists of data declarations followed by a program code
• The data declaration starts with an assembler directive .data
• The code starts with assembler directive .text
3.2 Project output 
• Your assembler should output the binary translation of each segment in two 
separate textboxes or text file. Each segment contains n lines consisting of 32 
binary digits 
3.3 High-level Tasks
The project should do the following high-level tasks:
1. Scan for all labels either in the code or data segments to calculate and store their 
addresses 
2. Allocate space for memory variables, keep their addresses and fill the 
initialization data
3. Translate the instructions 
4. Ignore comments (anything after # symbol)
Remember that an assembler considers only the translation of the assembly code into 
the binary code not to run the instructions themselves.
3.3.1 Scan for labels
In the beginning, you need to extract all labels from input assembly code. Then, you 
can start translating the instructions.
1. You need to have a counter that counts the memory locations allocated for each 
instruction or variable. Remember that memory in MIPS is byte-addressable 
(each byte has an address) and all instructions are 4 bytes each. Thus, for each 
assembly instruction, you need to increment this counter by 4. 
2. Since we have a separate memory for data and another for code, each segment 
starts at address 0. Thus, you should have 2 address counters (one for data 
segment and another for code segment)
3. Search for labels in both the data and code segments store them with their 
corresponding address into a generic data structure e.g. dictionary<string, 
string>.
4. A label is a string followed by a colon : (like, L1:, loop:) 
5. In data segment, you need to allocate variables and fill their initial value based 
on the given storage type. Storage types are either .word or .space as explained 
later.
3.3.2 Data Declarations
Format for declarations: name: data_type value(s)
• create storage for variable of the specified type with given name and specified 
value
• Storage types are:
o .word value which allocates 4 bytes of memory and fill them by the 
given initial value
o .space n which allocates n uninitialized words (n*4 bytes). 
• value(s) usually gives initial value(s); for storage type .space, gives number of 
spaces to be allocated
Examples:
var1: .word 3 # create a single integer variable (4 bytes) with initial value 3
arr1: .word 3, 2, 4 # create an integer array (12 bytes) with initial values 3, 2, 4
array2: .space 10 # allocate 10 consecutive words (40 bytes) (uninitialized) 
3.3.3 Code translation 
Once labels are recognized and their addresses are recorded, you can translate the 
assembly instructions into their binary code. You should have a hash table of 
instruction names and its corresponding opcode and funct and another hash table for 
registers and their regcodes. 
• R-type: map instructions and registers to their corresponding binary codes. 
I-Type: translate the immediate value (in addi), the offset (in lw/sw) or the 
relative address of the label (in beq/bne) into their binary value. 
• J-type: translate the direct the address of the label into binary