import sys
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from optimizer import Optimizer
from code_generator import CodeGenerator
from sast_analyzer import SASTAnalyzer

class IRGenerator:
    def __init__(self):
        self.ir_code = []
        self.temp_counter = 0
        self.label_counter = 0
        self.symbol_table_stack = [] # To manage scopes for variable lookup

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def emit(self, instruction):
        self.ir_code.append(instruction)

    def generate(self, ast):
        self.visit(ast)
        return self.ir_code

    def visit(self, node):
        if node is None:
            return
        method_name = f"visit_{node.type}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Program(self, node):
        for child in node.children:
            self.visit(child)

    def visit_FunctionDeclaration(self, node):
        func_name = node.value
        self.emit(f"FUNC {func_name}:")
        self.symbol_table_stack.append({}) # New scope for function
        # Add parameters to current symbol table (simplified for IR generation)
        for param in node.children[0].children:
            self.symbol_table_stack[-1][param.value] = param.metadata["type"]

        self.visit(node.children[1]) # Visit function body (Block)
        self.emit(f"END_FUNC {func_name}")
        self.symbol_table_stack.pop()

    def visit_Block(self, node):
        for statement in node.children:
            self.visit(statement)

    def visit_VariableDeclaration(self, node):
        var_name = node.value
        # Store variable in current scope for lookup
        self.symbol_table_stack[-1][var_name] = node.metadata.get("type", "unknown")
        if node.children:
            expr_result = self.visit(node.children[0])
            self.emit(f"ASSIGN {var_name}, {expr_result}")

    def visit_AssignmentStatement(self, node):
        var_name = node.value
        expr_result = self.visit(node.children[0])
        self.emit(f"ASSIGN {var_name}, {expr_result}")

    def visit_IfStatement(self, node):
        condition_result = self.visit(node.children[0])
        else_label = self.new_label()
        end_if_label = self.new_label()
        self.emit(f"IF_FALSE {condition_result} GOTO {else_label}")
        self.visit(node.children[1]) # True block
        self.emit(f"GOTO {end_if_label}")
        self.emit(f"{else_label}:")
        if node.children[2]:
            self.visit(node.children[2])
        self.emit(f"{end_if_label}:")

    def visit_ForStatement(self, node):
        self.symbol_table_stack.append({}) # New scope for for loop
        # Init
        if node.children[0]:
            self.visit(node.children[0])
        loop_start_label = self.new_label()
        loop_end_label = self.new_label()
        self.emit(f"{loop_start_label}:")
        # Condition
        condition_result = self.visit(node.children[1])
        self.emit(f"IF_FALSE {condition_result} GOTO {loop_end_label}")
        # Body
        self.visit(node.children[3])
        # Update
        if node.children[2]:
            self.visit(node.children[2])
        self.emit(f"GOTO {loop_start_label}")
        self.emit(f"{loop_end_label}:")
        self.symbol_table_stack.pop()

    def visit_WhileStatement(self, node):
        loop_start_label = self.new_label()
        loop_end_label = self.new_label()
        self.emit(f"{loop_start_label}:")
        condition_result = self.visit(node.children[0])
        self.emit(f"IF_FALSE {condition_result} GOTO {loop_end_label}")
        self.visit(node.children[1]) # Body
        self.emit(f"GOTO {loop_start_label}")
        self.emit(f"{loop_end_label}:")

    def visit_ReturnStatement(self, node):
        expr_result = self.visit(node.children[0])
        self.emit(f"RETURN {expr_result}")

    def visit_PrintStatement(self, node):
        expr_result = self.visit(node.children[0])
        self.emit(f"PRINT {expr_result}")

    def visit_BinaryExpression(self, node):
        left_result = self.visit(node.children[0])
        right_result = self.visit(node.children[1])
        op = node.value
        temp = self.new_temp()
        self.emit(f"BIN_OP {temp}, {left_result}, {op}, {right_result}")
        return temp

    def visit_NumberLiteral(self, node):
        return node.value

    def visit_StringLiteral(self, node):
        return node.value

    def visit_Identifier(self, node):
        for scope in reversed(self.symbol_table_stack):
            if node.value in scope:
                return node.value
        return node.value


