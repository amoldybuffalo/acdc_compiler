from acdcast import *

class SemanticError(Exception):
    pass


def semanticanalysis(program: list[ASTNode]) -> None:

    declared_floats = []
    initialized_floats = []
    declared_ints = []
    initialized_ints = []

    for linenumber, statement in enumerate(program, start=1):
        _semantic_check_stmt(statement, declared_ints, initialized_ints, declared_floats, initialized_floats, linenumber)
    return 


def _semantic_check_stmt(statement: ASTNode, declared_ints, initialized_ints, declared_floats, initialized_floats, linenumber: int) -> None:
    if isinstance(statement, IntDclNode):
        varname = statement.varname
        if varname in declared_ints:
            raise SemanticError(f"Variable {varname!r} redeclared at line {linenumber}")
        else:
            declared_ints.append(varname)
            return 

    elif isinstance(statement, FloatDclNode):
        varname = statement.varname
        if varname in declared_floats:
            raise SemanticError(f"Variable {varname!r} redeclared at line {linenumber}")
        else:
            declared_floats.append(varname)
            return 

        
    if isinstance(statement, PrintNode):
        varname = statement.varname
        if not (varname in declared_ints or varname in declared_floats):
            raise SemanticError(f"Trying to print undeclared variable {varname!r} at line {linenumber}")
        elif not (varname in initialized_ints or varname in initialized_floats):
            raise SemanticError(f"Trying to print uninitialized variable {varname!r} at line {linenumber}")
        return
    
    if isinstance(statement, AssignNode):
        varname = statement.varname
        if not (varname in declared_floats or varname in declared_ints):
            raise SemanticError(f"Assignment to undeclared variable {varname!r} at line {linenumber}")
        elif (varname in declared_ints) and (isinstance(statement.expr, FloatLitNode) or (isinstance(statement.expr, BinOpNode) and statement.expr.result_type == float)):
            raise SemanticError(f"Attempting to assign a floating point value to an integer variable")
        declared = declared_ints + declared_floats
        initialized = initialized_ints + initialized_floats
        _semantic_check_expr(statement.expr, declared, initialized, linenumber)
        if varname in declared_ints:
            initialized_ints.append(varname)
        else:
            initialized_floats.append(varname)
        return


    raise SemanticError("Unknown statement type at line {linenumber}")
    # Catches any weird statement types; this should never happen for a validly parsed program
    # Keeping it here though will help if your parser has an undiscovered or unfixed bug


def _semantic_check_expr(expr: ASTNode, declared: list[str], initialized: list[str], linenumber: int):
    if isinstance(expr, IntLitNode) or isinstance(expr, FloatLitNode):
        return
    
    if isinstance(expr, VarRefNode):
        varname = expr.varname
        if not varname in declared:
            raise SemanticError(f"Use of undeclared variable {varname!r} at line {linenumber}")
        if not varname in initialized:
            raise SemanticError(f"Use of unitialized variable {varname!r} at line {linenumber}")
        return
        
    if isinstance(expr, BinOpNode):
        _semantic_check_expr(expr.left, declared, initialized, linenumber)
        _semantic_check_expr(expr.right, declared, initialized, linenumber)
        return
    
    raise SemanticError(f"Unknown expression type at line {linenumber}")
    # Catches any weird statement types; this should never happen for a validly parsed program
    # Keeping it here though will help if your parser has an undiscovered or unfixed bug