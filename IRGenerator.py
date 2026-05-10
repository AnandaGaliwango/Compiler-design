class IRGenerator:
    def __init__(self):
        self.temp_count = 0
        self.label_count = 0
        self.tac_instructions = []  # Three-Address Code (Medium Level)
        self.low_level_code = []    # Assembly-like (Low Level)

    def new_temp(self):
        """Creates a new temporary variable (t0, t1, ...)."""
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def generate_ir(self, node):
        """
        Main entry point for generating Medium-Level IR (3AC).
        Returns the result variable/value of the node.
        """
        if node is None:
            return None

        # Leaf Node: Identifier or Number
        if node.left is None and node.right is None:
            return str(node.value)

        # Recursive step: Generate IR for children
        left_val = self.generate_ir(node.left)
        right_val = self.generate_ir(node.right)

        # Create a 3-Address Code instruction: result = arg1 op arg2
        temp_res = self.new_temp()
        instruction = f"{temp_res} = {left_val} {node.value} {right_val}"
        self.tac_instructions.append(instruction)

        # Generate Low-Level IR (Assembly-like) simultaneously
        self.generate_low_level(node.value, left_val, right_val, temp_res)

        return temp_res

    def generate_low_level(self, op, arg1, arg2, result):
        """Translates 3AC to a hypothetical Assembly IR."""
        op_map = {'+': 'ADD', '*': 'MUL', '-': 'SUB', '/': 'DIV'}
        asm_op = op_map.get(op, 'MOVE')
        
        self.low_level_code.append(f"LOAD R1, {arg1}")
        self.low_level_code.append(f"LOAD R2, {arg2}")
        self.low_level_code.append(f"{asm_op} R3, R1, R2")
        self.low_level_code.append(f"STORE {result}, R3")

    def display(self):
        print("\n" + "="*30)
        print("MEDIUM-LEVEL IR (Three-Address Code)")
        print("="*30)
        for instr in self.tac_instructions:
            print(f"  {instr}")

        print("\n" + "="*30)
        print("LOW-LEVEL IR (Pseudo-Assembly)")
        print("="*30)
        for instr in self.low_level_code:
            print(f"  {instr}")

# =========================================================
# INTEGRATION WITH YOUR EXISTING CODE
# =========================================================
if __name__ == "__main__":
    # Import or copy the Node and Parser from your colleague's code here
    from ast_landr import Parser, tokens # Assuming your colleague's file is ast_landr.py

    # 1. Parse tokens into AST
    parser = Parser(tokens)
    ast_root = parser.parse_E()

    # 2. Generate IR
    ir_gen = IRGenerator()
    ir_gen.generate_ir(ast_root)
    
    # 3. Output results
    ir_gen.display()