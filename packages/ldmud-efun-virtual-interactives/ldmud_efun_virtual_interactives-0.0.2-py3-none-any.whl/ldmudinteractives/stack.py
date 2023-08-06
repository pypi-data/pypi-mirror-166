import ldmud
import traceback

current_interactive = None
current_stack_depth = 0
current_command_stack_depth = 0

def call_interactive(inter_ob, fun):
    # Call fun for inter_ob. We'll hide the current stack
    last_interactive = current_interactive
    last_stack_depth = current_stack_depth
    last_command_stack_depth = current_command_stack_depth
    last_command_giver = ldmud.efuns.this_player()

    try:
        current_interactive = inter_ob
        current_stack_depth = ldmud.efuns.caller_stack_depth()
        current_command_stack_depth = ldmud.efuns.command_stack_depth()
        ldmud.efuns.set_this_player(inter_ob)

        fun()
    except:
        traceback.print_exc()
    finally:
        current_interactive = last_interactive
        current_stack_depth = last_stack_depth
        current_command_stack_depth = last_command_stack_depth
        ldmud.efuns.set_this_player(last_command_giver)

def efun_caller_stack(add_inter: int = None) -> ldmud.Array:
    if current_interactive is None:
        return ldmud.efuns.caller_stack(add_inter or 0)[:-1]

    stack = ldmud.efuns.caller_stack()[:-1]

    if current_stack_depth:
        stack = stack[current_stack_depth:-1]
    if add_inter:
        stack += ldmud.Array((current_interactive,))

    return stack

def efun_caller_stack_depth() -> int:
    depth = ldmud.efuns.caller_stack_depth()
    if current_interactive is None:
        return depth - 1
    return depth - current_stack_depth - 1


def efun_previous_object(i: int = None) -> ldmud.Object:
    if current_interactive is None:
        if i is None:
            print("PO:", ldmud.efuns.previous_object(1), "Stack:", *ldmud.efuns.caller_stack())
            return ldmud.efuns.previous_object(1) or ldmud.efuns.previous_object()
        else:
            return ldmud.efuns.previous_object(i+1)

    depth = ldmud.efuns.caller_stack_depth() - 1
    if depth == current_stack_depth:
        if i is None:
            return ldmud.efuns.this_object()
        else:
            return None
    elif current_stack_depth + i > depth:
        return None
    elif i is None:
        return ldmud.efuns.previous_object(1) or ldmud.efuns.this_object()
    else:
        return ldmud.efuns.previous_object(i+1)

def efun_this_interactive() -> ldmud.Object:
    if current_interactive is None:
        return ldmud.efuns.this_interactive()
    else:
        return current_interactive

def efun_command_stack() -> ldmud.Array:
    stack = ldmud.efuns.command_stack()
    if current_interactive is None:
        return stack
    return stack[current_command_stack_depth:]

def efun_command_stack_depth() -> int:
    depth = ldmud.efuns.command_stack_depth()
    if current_interactive is None:
        return depth
    return depth - current_command_stack_depth
