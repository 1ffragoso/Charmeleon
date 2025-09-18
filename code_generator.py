import re
from typing import List, Dict, Tuple, Optional


class IRInstr:
    def __init__(self, kind: str, raw: str, **fields):
        self.kind = kind
        self.raw = raw
        self.__dict__.update(fields)

    def __repr__(self):
        return f"IRInstr({self.kind}, {self.__dict__})"


class CodeGenerator:
    def __init__(self, ir_code: List[str]):
        self.ir_code = [line.strip() for line in ir_code if line.strip()]
        self.python_lines: List[str] = []
        self.indent_level = 0
        self.labels: Dict[str, int] = {}
        self.consumed: set[int] = set()
        self.instrs: List[IRInstr] = []

    def indent(self) -> str:
        return "    " * self.indent_level

    def emit(self, line: str):
        self.python_lines.append(self.indent() + line)

    def parse(self):
        self.instrs = []
        for i, line in enumerate(self.ir_code):
            m = re.match(r"^FUNC\s+([^:]+):$", line)
            if m:
                self.instrs.append(IRInstr("FUNC", line, name=m.group(1)))
                continue
            m = re.match(r"^END_FUNC\s+(.+)$", line)
            if m:
                self.instrs.append(IRInstr("END_FUNC", line, name=m.group(1)))
                continue
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\:$", line)
            if m:
                label = m.group(1)
                self.labels[label] = i
                self.instrs.append(IRInstr("LABEL", line, label=label))
                continue
            m = re.match(r"^ASSIGN\s+([^,]+),\s+(.+)$", line)
            if m:
                self.instrs.append(IRInstr("ASSIGN", line, target=m.group(1).strip(), value=m.group(2).strip()))
                continue
            m = re.match(r"^BIN_OP\s+([^,]+),\s+([^,]+),\s+([^,]+),\s+(.+)$", line)
            if m:
                self.instrs.append(IRInstr("BIN_OP", line, target=m.group(1).strip(), left=m.group(2).strip(), op=m.group(3).strip(), right=m.group(4).strip()))
                continue
            m = re.match(r"^IF_FALSE\s+([^\s]+)\s+GOTO\s+(.+)$", line)
            if m:
                self.instrs.append(IRInstr("IF_FALSE", line, cond=m.group(1).strip(), label=m.group(2).strip()))
                continue
            m = re.match(r"^GOTO\s+(.+)$", line)
            if m:
                self.instrs.append(IRInstr("GOTO", line, label=m.group(1).strip()))
                continue
            m = re.match(r"^PRINT\s+(.+)$", line)
            if m:
                self.instrs.append(IRInstr("PRINT", line, expr=m.group(1).strip()))
                continue
            m = re.match(r"^RETURN\s+(.+)$", line)
            if m:
                self.instrs.append(IRInstr("RETURN", line, expr=m.group(1).strip()))
                continue
            # Fallback
            self.instrs.append(IRInstr("OTHER", line))

    def gen(self) -> str:
        self.parse()
        i = 0
        while i < len(self.instrs):
            instr = self.instrs[i]
            if instr.kind == "FUNC":
                self.emit(f"def {instr.name}():")
                self.indent_level += 1
                i = self._gen_function_body(i + 1)
                self.indent_level -= 1
                self.emit("")
            else:
                i += 1
        return "\n".join(self.python_lines)

    def _gen_function_body(self, start_idx: int) -> int:
        i = start_idx
        while i < len(self.instrs):
            instr = self.instrs[i]
            if instr.kind == "END_FUNC":
                return i + 1
            if i in self.consumed:
                i += 1
                continue

            # Evitar emitir a BIN_OP de condição imediatamente antes do IF_FALSE
            if instr.kind == "BIN_OP" and i + 1 < len(self.instrs):
                nxt = self.instrs[i + 1]
                if nxt.kind == "IF_FALSE" and nxt.cond == instr.target:
                    # Deixe o IF_FALSE lidar com a emissão de controle
                    i = self._gen_if_or_loop(i + 1)
                    continue

            if instr.kind == "LABEL":
                self.emit(f"# label: {instr.label}")
                i += 1
                continue
            if instr.kind == "IF_FALSE":
                i = self._gen_if_or_loop(i)
                continue
            if instr.kind == "ASSIGN":
                # Handle string literals with escaped quotes correctly
                value = instr.value
                if value.startswith('"') and value.endswith('"'):
                    value = value.replace('\"', '"') # Replace escaped double quotes with actual double quotes
                self.emit(f"{instr.target} = {value}")
                i += 1
                continue
            if instr.kind == "BIN_OP":
                # Dobra BIN_OP + ASSIGN imediato em uma única atribuição
                folded = False
                if i + 1 < len(self.instrs):
                    nxt = self.instrs[i + 1]
                    if nxt.kind == "ASSIGN" and nxt.value == instr.target:
                        self.emit(f"{nxt.target} = {instr.left} {instr.op} {instr.right}")
                        self.consumed.add(i + 1)
                        folded = True
                if not folded:
                    self.emit(f"{instr.target} = {instr.left} {instr.op} {instr.right}")
                i += 1
                continue
            if instr.kind == "PRINT":
                self.emit(f"print({instr.expr})")
                i += 1
                continue
            if instr.kind == "GOTO":
                tgt = instr.label
                tgt_idx = self.labels.get(tgt)
                if tgt_idx is not None and tgt_idx < i:
                    # backward goto: já deve ter sido transformado em while; ignore
                    pass
                else:
                    self.emit(f"# goto {tgt}")
                i += 1
                continue
            if instr.kind == "RETURN":
                self.emit(f"return {instr.expr}")
                i += 1
                continue
            self.emit(f"# {instr.raw}")
            i += 1
        return i

    def _gen_if_or_loop(self, if_idx: int) -> int:
        if_instr = self.instrs[if_idx]
        else_label = if_instr.label
        else_label_idx = self.labels.get(else_label, None)

        # Extrai expressão condicional
        cond_expr = if_instr.cond
        prev_instr = self.instrs[if_idx - 1] if if_idx - 1 >= 0 else None
        if prev_instr and prev_instr.kind == "BIN_OP" and prev_instr.target == if_instr.cond:
            cond_expr = f"{prev_instr.left} {prev_instr.op} {prev_instr.right}"
            self.consumed.add(if_idx - 1)

        # Encontra fim do bloco verdadeiro
        true_block_end_idx = if_idx + 1
        while true_block_end_idx < len(self.instrs):
            current_instr = self.instrs[true_block_end_idx]
            if current_instr.kind == "LABEL" and else_label_idx is not None and current_instr.label == else_label:
                break
            if current_instr.kind == "GOTO":
                break
            true_block_end_idx += 1

        # Loop: GOTO para label anterior
        if true_block_end_idx < len(self.instrs) and self.instrs[true_block_end_idx].kind == "GOTO":
            goto_instr = self.instrs[true_block_end_idx]
            target_label = goto_instr.label
            target_idx = self.labels.get(target_label)
            if target_idx is not None and target_idx < if_idx:
                self.emit(f"while {cond_expr}:")
                self.indent_level += 1
                k = if_idx + 1
                while k < true_block_end_idx:
                    if k not in self.consumed:
                        self._emit_single(k)
                        self.consumed.add(k)
                    k += 1
                self.indent_level -= 1
                # pular para depois do else_label
                if else_label_idx is not None:
                    return else_label_idx + 1
                else:
                    return true_block_end_idx + 1

        # If/Else estruturado
        self.emit(f"if {cond_expr}:")
        self.indent_level += 1
        k = if_idx + 1
        while k < true_block_end_idx:
            if k not in self.consumed:
                self._emit_single(k)
                self.consumed.add(k)
            k += 1
        self.indent_level -= 1

        if true_block_end_idx < len(self.instrs) and self.instrs[true_block_end_idx].kind == "GOTO":
            skip_label = self.instrs[true_block_end_idx].label
            skip_label_idx = self.labels.get(skip_label)
            if else_label_idx is not None and skip_label_idx is not None and skip_label_idx > else_label_idx:
                self.emit("else:")
                self.indent_level += 1
                l = else_label_idx + 1
                while l < skip_label_idx:
                    if l not in self.consumed:
                        self._emit_single(l)
                        self.consumed.add(l)
                    l += 1
                self.indent_level -= 1
                return skip_label_idx + 1
        # If simples
        if else_label_idx is not None:
            return else_label_idx + 1
        return true_block_end_idx + 1

    def _emit_single(self, idx: int):
        ins = self.instrs[idx]
        if ins.kind == "ASSIGN":
            value = ins.value
            if value.startswith('"') and value.endswith('"'):
                value = value.replace('\"', '"')
            self.emit(f"{ins.target} = {value}")
        elif ins.kind == "BIN_OP":
            # Dobra se próximo for ASSIGN consumindo o temporário
            if idx + 1 < len(self.instrs):
                nxt = self.instrs[idx + 1]
                if nxt.kind == "ASSIGN" and nxt.value == ins.target:
                    self.emit(f"{nxt.target} = {ins.left} {ins.op} {ins.right}")
                    self.consumed.add(idx + 1)
                    return
            self.emit(f"{ins.target} = {ins.left} {ins.op} {ins.right}")
        elif ins.kind == "PRINT":
            self.emit(f"print({ins.expr})")
        elif ins.kind == "RETURN":
            self.emit(f"return {ins.expr}")
        elif ins.kind == "LABEL":
            self.emit(f"# label: {ins.label}")
        elif ins.kind == "GOTO":
            self.emit(f"# goto {ins.label}")
        else:
            self.emit(f"# {ins.raw}")


if __name__ == "__main__":
    ir_code_example = [
        "FUNC main:",
        "ASSIGN x, 3",
        "L1:",
        "BIN_OP t1, x, >, 0",
        "IF_FALSE t1 GOTO L2",
        "PRINT x",
        "BIN_OP t2, x, -, 1",
        "ASSIGN x, t2",
        "GOTO L1",
        "L2:",
        "END_FUNC main",
    ]
    gen = CodeGenerator(ir_code_example)
    print(gen.gen())


