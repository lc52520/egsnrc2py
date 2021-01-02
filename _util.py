"""Various routines for analyzing what are calls, what are constants, etc."""
import re
from typing import Tuple
from pprint import pprint
from textwrap import dedent

# def evaluate_using(P1, P2, P3):
#     if P2 == SNAME1:
#         P1=P2}1(L{P3})*{P3}+{P2}0(L{P3})
#     else:
#         {P1}={P2}1(L{P3},MEDIUM)*{P3}+{P2}0(L{P3},MEDIUM)

def test_eval_subst(code):
    pattern = r"\$EVALUATE (\w*) USING (\w*)\((\w*)\);?"
    subst = """
    [IF] '\g<2>'=SNAME1
    [\g<1>=\g<2>1(L\g<3>)*\g<3>+\g<2>0(L\g<3>);] [ELSE]
    [\g<1>=\g<2>1(L\g<3>,MEDIUM)*\g<3>+\g<2>0(L\g<3>,MEDIUM);]}
    """
    # subst = r"\1"
    # m = re.search(pattern, code)
    # print(m.groups())

    code = re.sub(pattern, subst, code, re.MULTILINE)
    return code


# REPLACE {$EVALUATE#USING#(#);} WITH {
#   [IF] '{P2}'=SNAME1
#   [{P1}={P2}1(L{P3})*{P3}+{P2}0(L{P3});] [ELSE]
#   [{P1}={P2}1(L{P3},MEDIUM)*{P3}+{P2}0(L{P3},MEDIUM);]}
# "{P1} IS VARIABLE TO BE ASSIGNED VALUE."
# "{P2} IS THE FUNCTION BEING APPROXIMATED."
# "{P3} IS THE ARGUMENT OF THE FUNCTION. IN THE CURRENT"
# "PWLF METHOD, THE ARGUMENT DETERMINES AN INTERVAL USING THE"
# "$SET INTERVAL MACROS.   WITH IN THIS INTERVAL THE"
# "FUNCTION IS APPROXIMATED AS A LINEAR FUNCTION OF"
# "THE ARGUMENT. BUT"
# "IF {P2}=SIN IT DOES NOT DEPEND ON MEDIUM"

# REPLACE {$EVALUATE#USING#(#,#);} WITH {
#   {P1}={P2}0(L{P3},L{P4})+{P2}1(L{P3},L{P4})*{P3}+
#   {P2}2(L{P3},L{P4})*
#   {P4};}"2-D APPROXIMATION INDEPENDENT OF MEDIUM"
# SPECIFY SNAME AS ['sinc'|'blc'|'rthr'|'rthri'|'SINC'|'BLC'|'RTHR'|'RTHRI'];
# SPECIFY SNAME1 AS ['sin'|'SIN'];


def find_all_macros_used(code):
    """Return all identifiers starting with $ in the code"""
    pattern = r" *?(\$[\w-]+)" #r"^ *?(\$[-\w]*)"
    matches = re.findall(pattern, code)
    return set(matches)


def find_macros_including_macros(code):
    """Matches where the WITH replace also has $ in it"""
    # pattern = r"REPLACE\s*?\{\s*?(\$[\w-]*);?\}\s*?WITH\s*?\{(.*\$.*);?\}"
    # matches = [m for m in re.finditer(pattern, code, flags=re.MULTILINE)]
    # return [m.groups() for m in matches]

    return {
        k:v for k,v in find_all_replaces(code).items()
        if '$' in v
    }


def find_all_replaces(code):
    pattern = r"REPLACE\s*?\{(.*)\}\s*?WITH\s*?\{(.*)\}"
    return dict(m.groups() for m in re.finditer(pattern, code))


def macro_types(code) -> Tuple[list, list, list]:
    """Scan through code to check if macros are ever assigned, or called

    Returns
    -------
        (constant, callable, defined_block)

    Note: search with r"\$\w*?\s*?=" in full egsnrc.mortran
       found no assigned <$var =>'s, except in string printouts,
       so if not called, then are constant
    """
    macros = find_all_macros_used(code)
    called = []
    constant = []
    defined_block = []

    for macro in set(macros):
        # See if called - if alone on a line (except comments):
        if macro.startswith(("$COMIN", "$DEFINE", "$DECLARE")):
            defined_block.append(macro)
            continue
        macro_str = macro.replace("$", r"\$")
        alone_pattern = rf'^ *{macro_str}\s*?(["#].*?$)?;?'
        if re.search(alone_pattern, code, flags=re.MULTILINE):
            called.append(macro)
        # See if has a open bracket right after it
        # pattern = rf"\W{macro}\s*?\("
        # if re.search(pattern, code, flags=re.MULTILINE):
        #     called.append(macro)
        else:
            constant.append(macro)

    return constant, called, defined_block


def generate_macros_py(filename:str, code: str) -> None:
    """Generate py code with info used by the transpile code

    e.g. lists of macros that are const vs callables
    code should be full egsnrc.mortran to capture full information
    """
    constant_macros, called_macros, defined_block_macros = macro_types(code)

    with open(filename, 'w') as f:
        f.write("# autogenerated by _util.generate_macros_py")
        for name, _list in [
            ("constant_macros", constant_macros),
            ("called_macros", called_macros),
            ("defined_blocks_macros", defined_block_macros)
        ]:
            f.write("\n\n")
            f.write(f"{name} = [\n")
            f.write(
                "".join(f"    '{name}',\n" for name in sorted(_list))
            )
            f.write("]")

def nested_brace_value(s: str, start: int, open="{", close="}") -> str:
    depth = 1
    orig_start = start
    while depth > 0:
        i_close = s.find("}", start)
        i_open = s.find("{", start)
        if i_open >= 0 and i_open < i_close:
            depth += 1
            start = i_open + 1
        elif i_close < 0:
            raise ValueError(f"Closing brace after position {start} not found")
        else:
            depth -= 1
            start = i_close + 1
    return s[orig_start:i_close]

def map_replace_from_to(code: str) -> str:
    all_from_to = {}
    pattern = r"^ *REPLACE\s*\{(.*)\}\s*WITH\s*\{"
    i = 0
    subcode = code  # need to update search string to exclude REPLACE in val
    while True:
        match = re.search(pattern, subcode, flags=re.MULTILINE)
        if not match:
            break
        replace_from = match.group(1)
        replace_to = nested_brace_value(subcode, match.end())
        all_from_to[replace_from] = replace_to
        # print(replace_from, " -> ", replace_to)
        i += len(match.group(0)) + len(replace_to) + 1  # one extra for }
        subcode = code[i:]

    return all_from_to


def generate_replaces_py(filename:str, code: str) -> None:
    from_to = replace_from_to(code)
    with open(filename, 'w') as f:
        f.write("# autogenerated by _util.generate_macros_py")


if __name__ == "__main__":
    # test_code = "$EVALUATE dedx0 USING ededx(elke);"
    # print("Subst for ", test_code)
    # print(test_eval_subst(test_code))

    in_filename = "mortran/electr.mortran"
    with open(in_filename, 'r') as f:
        code = f.read()

    with open("mortran/egsnrc.macros", 'r') as f:
        macros_code = f.read()

    with open("mortran/egsnrc.mortran", 'r') as f:
        full_egs_code = f.read()


    s = dedent(r"""
        REPLACE {$SHORT_INT} WITH {;integer*2} "change this to integer*4 for compilers"

        REPLACE {$TRACE#,#;} WITH {$TRACE{P1};$TRACE{P2};}
        REPLACE {$S1TRACE#,#;} WITH {$S1TRACE{P1};$S1TRACE{P2};}

        REPLACE {$DUMP#,#;} WITH
        {;{SETR A=NEWLABEL}
            V{COPY A}={P1};OUTPUT V{COPY A};(' {P1}=',1PG15.7);
            [IF] {EXIST 2} [$DUMP{P2};] ;}
    "NOTICE: THE LIST OF VARIABLES MUST BE FOLLOWED BY A COMMA"
    "FOR EXAMPLE $DUMP S,T(U,V),W,; OR $DUMP A,;"
    ;  "---------- BUFFER FLUSH SEMICOLON ----------"
    """
    )

    # generate_macros_py("build/macros.py", full_egs_code)
    map_replaces = map_replace_from_to(macros_code)
    print(map_replaces)
    print("Nulls:")
    for k,v in map_replaces.items():
        if v.strip() == ";":
            print(f"{k} -> {v}")

    print("\nConstants:")
    for k,v in map_replaces.items():
        try:
            x = float(v.replace(";", " ").strip())  # shouldn't have ; though
        except:
            continue
        print(f"{k} -> {v}")
