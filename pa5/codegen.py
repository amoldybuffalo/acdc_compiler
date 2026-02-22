from acdcast import *

class InstructionList:

    def __init__(self):

        self.instructions = []

    def append(self, instruction: str):

        self.instructions.append(instruction)

    def extend(self, newinstructions: "InstructionList"):
        
        self.instructions.extend(newinstructions.instructions)

    def __iter__(self):
        return iter(self.instructions)




def codegenerator(program: list[ASTNode]) -> InstructionList:

    code = InstructionList()

    for statement in program:

        newcode = stmtcodegen(statement)
        code.extend(newcode)

    return code
    

def stmtcodegen(statement: ASTNode) -> InstructionList:

    code = InstructionList()

    if isinstance(statement, IntDclNode):
        return code

    if isinstance(statement, IntLitNode):
        code.append(str(statement.value))
        return code

    if isinstance(statement, VarRefNode):
        code.append(f"l{statement.varname}")
        return code

    if isinstance(statement, PrintNode):
        code.append(f"l{statement.varname} p")
        return code

    if isinstance(statement, AssignNode):
        code.extend(stmtcodegen(statement.expr))
        code.append(f"s{statement.varname}")
        return code

    if isinstance(statement, BinOpNode):
        if statement.optype.value == "^" and isinstance(statement.right, IntLitNode):
            code.extend(stmtcodegen(statement.left))
            for i in range(statement.right.value-1):
                code.append("d")
            for i in range(statement.right.value-1):
                code.append("*")
               
        else:
            code.extend(stmtcodegen(statement.left))
            code.extend(stmtcodegen(statement.right))
            code.append(statement.optype.value)
        return code
    

    # Should never get here
    return code
