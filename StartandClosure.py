# =========================================================
# LR(0) GRAMMAR
# =========================================================

grammar = {
    "E'": ["E"],
    "E": ["E+T", "T"],
    "T": ["T*F", "F"],
    "F": ["(E)", "id", "num"]
}


# =========================================================
# LR(0) ITEM REPRESENTATION
# =========================================================

def add_dot(production):
    return production[:1] + "." + production[1:]


# =========================================================
# CLOSURE FUNCTION
# =========================================================

def closure(items):
    closure_set = set(items)
    changed = True

    while changed:
        changed = False

        new_items = set()

        for item in closure_set:
            lhs, rhs = item.split("→")
            rhs = rhs.strip()

            dot_pos = rhs.index(".")

            # symbol after dot
            if dot_pos + 1 < len(rhs):
                symbol = rhs[dot_pos + 1]

                # if non-terminal
                if symbol in grammar:
                    for prod in grammar[symbol]:
                        new_item = f"{symbol}→.{prod}"
                        if new_item not in closure_set:
                            new_items.add(new_item)

        if new_items:
            closure_set |= new_items
            changed = True

    return closure_set


# =========================================================
# GOTO FUNCTION
# =========================================================

def goto(items, symbol):
    moved = set()

    for item in items:
        lhs, rhs = item.split("→")
        rhs = rhs.strip()

        dot_pos = rhs.index(".")

        if dot_pos + 1 < len(rhs) and rhs[dot_pos + 1] == symbol:
            new_rhs = (
                rhs[:dot_pos] +
                symbol +
                "." +
                rhs[dot_pos + 2:]
            )
            moved.add(f"{lhs}→{new_rhs}")

    return closure(moved)


# =========================================================
# BUILD LR(0) STATES
# =========================================================

def build_lr0_states():
    start_item = "E'→.E"
    I0 = closure({start_item})

    states = [I0]
    transitions = {}

    symbols = list(grammar.keys()) + ["E", "T", "F", "+", "*", "(", ")", "id", "num"]

    changed = True

    while changed:
        changed = False

        for state in list(states):
            for symbol in symbols:
                goto_state = goto(state, symbol)

                if goto_state and goto_state not in states:
                    states.append(goto_state)
                    transitions[(tuple(state), symbol)] = goto_state
                    changed = True

    return states, transitions


# =========================================================
# PRINT STATES
# =========================================================

def print_states(states):
    for i, state in enumerate(states):
        print(f"\nI{i}:")
        for item in state:
            print("   ", item)


# =========================================================
# RUN LR(0)
# =========================================================

states, transitions = build_lr0_states()

print("=== LR(0) STATES (CLOSURE + GOTO) ===")
print_states(states)