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

            if dot_pos + 1 < len(rhs):
                symbol = rhs[dot_pos + 1]
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
            new_rhs = rhs[:dot_pos] + symbol + "." + rhs[dot_pos + 2:]
            moved.add(f"{lhs}→{new_rhs}")

    return closure(moved)


# =========================================================
# BUILD LR(0) STATES
# =========================================================

def build_lr0_states():
    # Start with initial item
    start_item = "E'→.E"
    I0 = closure({start_item})
    
    states = [I0]
    transitions = {}
    
    # Get all symbols
    symbols = ["E", "T", "F", "+", "*", "(", ")", "id", "num"]
    
    changed = True
    while changed:
        changed = False
        
        for i, state in enumerate(states):
            for symbol in symbols:
                goto_state = goto(state, symbol)
                
                if goto_state and goto_state not in states:
                    states.append(goto_state)
                    transitions[(i, symbol)] = len(states) - 1
                    changed = True
                elif goto_state:
                    # Find existing state index
                    for idx, s in enumerate(states):
                        if s == goto_state:
                            transitions[(i, symbol)] = idx
                            break
    
    return states, transitions


# =========================================================
# PRINT STATES WITH GOTO
# =========================================================

def print_states(states, transitions):
    for i, state in enumerate(states):
        print(f"\nI{i}:")
        # Sort items for consistent output
        for item in sorted(state):
            print(f"    {item}")
        
        # Print goto transitions
        gotos = []
        for (from_state, symbol), to_state in transitions.items():
            if from_state == i:
                gotos.append(f"{symbol}->I{to_state}")
        
        if gotos:
            print(f"\n    GOTO: {', '.join(gotos)}")


# =========================================================
# MAIN
# =========================================================

states, transitions = build_lr0_states()
print_states(states, transitions)

print(f"\n\nTotal states: {len(states)}")
