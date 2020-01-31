"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.flags = [0] * 8
    
    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, filename):
        """Load a program into memory."""
        #re-factor
        # file = open(filename, "r")
        # address = 0
        # for line in file:
        #     comments = line.split("#")
        #     numbers = comments[0].strip()
        #     if numbers == "":
        #         continue
        #     instruction = int(numbers, 2)
        #     self.ram[address] = instruction
        #     address += 1

        try:
            address = 0
            with open(filename) as cur_file:
                # print(cur_file.read())
                for line in cur_file:
                    # print(line)
                    comments = line.split("#")
                    numbers = comments[0].strip()
                    if numbers == "":
                        continue
                    instruction = int(numbers, 2)
                    self.ram[address] = instruction
                    address += 1
                    # print(numbers)
        except:
            print("nahh")

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CMP = 0b10100111
        JEQ = 0b01010101
        JNE = 0b01010110
        JMP = 0b01010100
        while running:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR == HLT:
                running = False
            elif IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == MUL:
                print(self.reg[0] * self.reg[1])
                self.pc += 3
            elif IR == PUSH:
                reg_index = self.ram_read(self.pc + 1)
                self.reg[self.sp] -= 1
                self.ram_write( self.reg[self.sp] , self.reg[reg_index] )
                self.pc += 2
            elif IR == POP:
                reg_index = self.ram_read(self.pc + 1)
                self.reg[reg_index] = self.ram_read(self.reg[self.sp])
                self.reg[self.sp] += 1
                self.pc += 2
            elif IR == CMP:
                if (self.reg[operand_a] == self.reg[operand_b]):
                    self.flags[7] = 1
                elif (self.reg[operand_a] < self.reg[operand_b]):
                    self.flags[5] = 1
                elif (self.reg[operand_a] > self.reg[operand_b]):
                    self.flags[6] = 1
                self.pc += 3
            elif IR == JEQ:
                if self.flags[7] != 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif IR == JNE:
                if self.flags[7] == 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif IR == JMP:
                self.pc = self.reg[operand_a]

            
            




# CMP
# This is an instruction handled by the ALU.

# CMP registerA registerB

# Compare the values in two registers.

# If they are equal, set the Equal E flag to 1, otherwise set it to 0.

# If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.

# If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.



 # jmp
# Jump to the address stored in the given register.

# Set the PC to the address stored in the given register.

# JEQ register

# If equal flag is set (true), jump to the address stored in the given register.

# JNE register

# If E flag is clear (false, 0), jump to the address stored in the given register.