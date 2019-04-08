import re

dataSegmentOutputFile = open("DataSegment.txt", "w+")
codeSegmentOutputFile = open("CodeSegment.txt", "w+")
inputFile = open("example.txt", "r+")
allLines = inputFile.readlines()

variablesCounter = 0
instcount = 0
dataCounter = 0
textCounter = 0
dataSection = 0
textSection = 0
linecounter = 0

labelsDic = dict()
labelsDic2 = dict()
instructionList = []

registersDic = {
    "$zero": "00000",
    "$at": "00001",
    "$v0": "00010",
    "$v1": "00011",
    "$a0": "00100",
    "$a1": "00101",
    "$a2": "00110",
    "$a3": "00111",
    "$t0": "01000",
    "$t1": "01001",
    "$t2": "01010",
    "$t3": "01011",
    "$t4": "01100",
    "$t5": "01101",
    "$t6": "01110",
    "$t7": "01111",
    "$s0": "10000",
    "$s1": "10001",
    "$s2": "10010",
    "$s3": "10011",
    "$s4": "10100",
    "$s5": "10101",
    "$s6": "10110",
    "$s7": "10111",
    "$t8": "11000",
    "$t9": "11001",
    "$sp": "11101",
    "$ra": "11111"
}
RFormatDic_op_fn = {
    "add": ("000000", "100000"),
    "and": ("000000", "100100"),
    "sub": ("000000", "100010"),
    "nor": ("000000", "100111"),
    "or": ("000000", "100101"),
    "slt": ("000000", "101010")
}
opCode_IFormatDic = {
    "beq": "000100",
    "bne": "000101",
    "addi": "001000",
    "lw": "100011",
    "sw": "101011"
}
opCode_JFormatDic = {
    "j": "000010"
}


####################################################################################################
def IFunction(index, instruction, instructionPointer):
    machineCode = ""
    machineCode += opCode_IFormatDic[instruction[index]]  # instruction

    if instruction[index] == "lw" or instruction[index] == "sw":
        machineCode += registersDic[instruction[index + 3]]  # rs
        machineCode += registersDic[instruction[index + 1]]  # rt
        # offset
        # law el offset label h7ot el address bta3o
        if labelsDic.get(instruction[index + 2]):
            machineCode += '{0:016b}'.format(labelsDic[instruction[index + 2]])
        else:
            machineCode += '{0:016b}'.format(int(instruction[index + 2]))

    elif instruction[index] == "beq" or instruction[index] == "bne":
        machineCode += registersDic[instruction[index + 1]]  # rs
        machineCode += registersDic[instruction[index + 2]]  # rt
        binSubAddress = ""
        # law el add ely 3aiza aro7o 2bly
        # add el label ely 3aiza aro7o    # add el instruction ely wa2fa 3lih dlwa2ty
        if labelsDic[instruction[index + 3]] < instructionPointer:

            subAddresses = (instructionPointer + 1) - labelsDic[instruction[index + 3]]
            binSubAddress = '{0:016b}'.format(subAddresses)
            boolcomplement = 0

            binSubAddressList = list(binSubAddress)

            for j in range(binSubAddressList.__len__() - 1, -1, -1):
                if boolcomplement == 1 and binSubAddressList[j] == "1":
                    binSubAddressList[j] = "0"
                elif boolcomplement == 1 and binSubAddressList[j] == "0":
                    binSubAddressList[j] = "1"
                elif boolcomplement == 0 and binSubAddressList[j] == "1":
                    boolcomplement = 1

            binSubAddress = "".join(binSubAddressList)
        # law el add ely 3aiza aro7o b3dy
        else:
            subAddresses = labelsDic[instruction[index + 3]] - (instructionPointer + 1)
            binSubAddress = '{0:016b}'.format(subAddresses)

        machineCode += str(binSubAddress)

    elif instruction[index] == "addi":
        machineCode += registersDic[instruction[index + 2]]  # rs
        machineCode += registersDic[instruction[index + 1]]  # rt
        machineCode += '{0:016b}'.format(int(instruction[index + 3]))

    codeSegmentOutputFile.write("MEMORY(" + str(instcount - variablesCounter) + ") := " + '"' + machineCode + '" ;' + '\n')


def concat_RInstruct(index, line):
    RInstructionBin = ""
    if line[index] in RFormatDic_op_fn.keys():
        op = RFormatDic_op_fn[line[index]][0]
        rd = registersDic[line[index + 1]]
        rs = registersDic[line[index + 2]]
        rt = registersDic[line[index + 3]]
        fn = RFormatDic_op_fn[line[index]][1]
        RInstructionBin += op + rs + rt + rd + "00000" + fn
        codeSegmentOutputFile.write('MEMORY(' + str(instcount - variablesCounter) + ') := ' + '"' + RInstructionBin + '" ;' + '\n')


def concat_JInstruction(index, line):
    JInstructionbin = ""
    x = labelsDic2[line[index + 1]]
    x = '{0:026b}'.format(int(x))
    JInstructionbin += opCode_JFormatDic[line[index]] + x
    codeSegmentOutputFile.write('MEMORY(' + str(instcount - variablesCounter) + ') := ' + '"' + JInstructionbin + '" ;' + '\n')


def dataTranslation(instructionList):
    dataIndex = 0
    unintializedString = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    for instruction in instructionList:
        if instruction[0] == ".text":
            break
        if instruction[0] != ".data":
            if instruction[1] == ".space":
                for i in range(int(instruction[2])):
                    dataSegmentOutputFile.write('MEMORY(' + str(dataIndex) + ') <= ' + '"' + unintializedString + '" ;' + '\n')
                    dataIndex += 1

            else:
                for i in range(instruction.__len__() - 2):
                    dataSegmentOutputFile.write('MEMORY(' + str(dataIndex) + ') <= ' + '"' + '{0:032b}'.format(
                        int(instruction[i + 2])) + '" ;' + '\n')
                    dataIndex += 1


####################################################################################################
for line in allLines:
    head, sep, tail = line.partition("#")
    splitedInstruction = re.split('[ ,#*()\\t\\n]+', head)
    # to remove NULLS
    splitedInstruction = [element for element in splitedInstruction if element]
    if splitedInstruction != []:
        instructionList.append(splitedInstruction)
        if splitedInstruction[0] == ".data":
            dataSection = 1
        elif splitedInstruction[0] == ".text":
            textSection = 1
            dataSection = 0

        if dataSection == 1 and textSection == 0 and splitedInstruction[0] != ".data":
            variablesCounter += 1
            splitedInstruction[0] = splitedInstruction[0].replace(":", "")
            labelsDic[splitedInstruction[0]] = dataCounter

            # if array
            if splitedInstruction[1] == ".space":
                dataCounter += (int(splitedInstruction[2]) * 4)

            # if word array and initialized
            elif splitedInstruction[1] == ".word":
                dataCounter += (4 * (int(splitedInstruction.__len__() - 2)))

        elif textSection == 1 and dataSection == 0 and splitedInstruction[0] != ".text":
            if re.search(":$", splitedInstruction[0]):
                splitedInstruction[0] = splitedInstruction[0].replace(":", "")
                labelsDic[splitedInstruction[0]] = textCounter
                labelsDic2[splitedInstruction[0]] = linecounter
            textCounter += 1

            linecounter += 1

# variable instructionPointer for no of variables + .data + .text
# then we subtract the variable instructionPointer from the instuction instructionPointer
variablesCounter += 2

dataSegmentOutputFile.write("#Translation of Data Segment \n")
dataTranslation(instructionList)
dataSegmentOutputFile.close()

codeSegmentOutputFile.write("#Translation of Code Segment \n")

instructionPointer = 0
for instruction in instructionList:

    if labelsDic.get(instruction[0]) == None and opCode_IFormatDic.get(instruction[0]) != None:
        IFunction(0, instruction, instructionPointer - variablesCounter)

    elif labelsDic.get(instruction[0]) != None and opCode_IFormatDic.get(instruction[1]) != None:
        IFunction(1, instruction, instructionPointer - variablesCounter)

    elif labelsDic.get(instruction[0]) == None and RFormatDic_op_fn.get(instruction[0]):
        concat_RInstruct(0, instruction)

    elif labelsDic.get(instruction[0]) != None and RFormatDic_op_fn.get(instruction[1]):
        concat_RInstruct(1, instruction)

    elif labelsDic.get(instruction[0]) == None and opCode_JFormatDic.get(instruction[0]):
        concat_JInstruction(0, instruction)

    elif labelsDic.get(instruction[0]) != None and opCode_JFormatDic.get(instruction[1]):
        concat_JInstruction(1, instruction)
    instcount += 1
    instructionPointer += 1

codeSegmentOutputFile.close()