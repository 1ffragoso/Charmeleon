import re
class Optimizer:
    def __init__(self, ir_code):
        self.ir_code = ir_code
    def _parse(self, instr):
        # Returns (def_var, use_vars, kind)
        instr = instr.strip()
        if not instr:
            return (None, [], "empty")
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:\s*$", instr):
            return (None, [], "label")
        m = re.match(r"^FUNC\s+([^:]+):$", instr)
        if m:
            return (None, [], "func")
        m = re.match(r"^END_FUNC\s+(.+)$", instr)
        if m:
            return (None, [], "end")
        m = re.match(r"^IF_FALSE\s+([^\s]+)\s+GOTO\s+(.+)$", instr)
        if m:
            cond = m.group(1)
            return (None, [cond], "if")
        m = re.match(r"^GOTO\s+(.+)$", instr)
        if m:
            return (None, [], "goto")
        m = re.match(r"^PRINT\s+(.+)$", instr)
        if m:
            return (None, [m.group(1)], "print")
        m = re.match(r"^RETURN\s+(.+)$", instr)
        if m:
            return (None, [m.group(1)], "return")
        m = re.match(r"^ASSIGN\s+([^,]+),\s+(.+)$", instr)
        if m:
            target = m.group(1).strip()
            value = m.group(2).strip()
            uses = []
            # consider temps and identifiers as uses (simple heuristic)
            tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|t\d+", value)
            for tok in tokens:
                if re.match(r"^t\d+$", tok) or re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", tok):
                    uses.append(tok)
            return (target, uses, "assign")
        m = re.match(r"^BIN_OP\s+([^,]+),\s+([^,]+),\s+([^,]+),\s+(.+)$", instr)
        if m:
            target = m.group(1).strip()
            left = m.group(2).strip()
            op = m.group(3).strip()
            right = m.group(4).strip()
            uses = [left, right]
            return (target, uses, "binop")
        return (None, [], "other")
    def eliminate_dead_code(self):
        used = set()
        out = []
        for instr in reversed(self.ir_code):
            d, uses, kind = self._parse(instr)
            keep = False
            if kind in {"label", "func", "end", "if", "goto", "print", "return", "other"}:
                # keep labels, control flow, side-effects and unknowns
                keep = True
            else:
                # assign or binop
                # be conservative: keep if defines a non-temp (program variable)
                if d is not None and not re.match(r"^t\d+$", d):
                    keep = True
                # keep if its result is used later
                elif d is not None and d in used:
                    keep = True
            if keep:
                # update liveness
                if d in used:
                    used.remove(d)
                for u in uses:
                    # consider only names that look like temps or identifiers
                    if re.match(r"^t\d+$", u) or re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", u):
                        used.add(u)
                out.insert(0, instr)
        return out


