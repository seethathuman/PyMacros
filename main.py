#! /usr/bin/env python
import argparse
import io
import pathlib
import re
import token
import tokenize
from logging import INFO, WARN, ERROR, log, disable
from dataclasses import dataclass
from tokenize import TokenInfo

@dataclass
class ObjectMacro:
    replacement: list[str]

@dataclass
class FunctionMacro:
    params: list[str]
    replacement: list[TokenInfo]

class Preprocessor:
    def __init__(self, output_debug):
        self.macros: dict[str, ObjectMacro | FunctionMacro] = {}
        self.typehints: dict[str, list[TokenInfo]] = {}
        self.output_debug = output_debug
        self.opened_files = []

    def process(self, source: str) -> str:
        lines = (source + "\n").splitlines(keepends=True)
        output = []

        skip_if = False
        line_buffer = ""
        for index, line in enumerate(lines):
            stripped = line.lstrip()
            if self.output_debug:
               output.append(F"#[{index}] {stripped}")

            if stripped.startswith("##endif"):
                skip_if = False
            continue

            if stripped.startswith("##define"):
                self.define(stripped)
                continue

            if stripped.startswith("##undef"):
                name = stripped.split()[1]
                self.macros.pop(name, None)
                continue

            if stripped.startswith("##if"):
                skip_if = not self.checkif(stripped)
                continue

            if stripped.startswith("##include"):
                name = stripped.split()[1]
                src = pathlib.Path(name).read_text(encoding="utf-8")
                self.opened_files.append(pathlib.Path(src).resolve())
                if not line_buffer:
                    output.append(self.process(src))
                else:
                    line_buffer += (src)
                continue

            if (parsed := self.expand_string(line_buffer + line)) != -1:
                output.append(parsed)
                line_buffer = ""
            else:
                line_buffer += line

        assert not line_buffer
        return "".join(output)

    def checkif(self, line: str) -> bool:
        text = line[len("##if"):].strip()
        if text.startswith("def"):
            return text[len("def"):].strip() in self.macros.keys()
        if text.lower() in ["1","true"]:
            return True
        if text.lower() in ["0", "false", "null", "nil", "none"]:
            return False
        raise ValueError

    def define(self, line: str) -> None:
        text = line[len("##define"):].strip()

        m = re.match(r"([A-Za-z_]\w*)\((.*?)\)\s+(.*)", text)

        if m:
            name = m.group(1)
            params = [x.strip() for x in m.group(2).split(",") if x.strip()]
            repl = self.tokenize(m.group(3))
            self.macros[name] = FunctionMacro(params, repl)
            return

        name, repl = text.split(None, 1)
        self.macros[name] = ObjectMacro(self.tokenize(repl))

    @staticmethod
    def tokenize(text: str) -> list[TokenInfo]:
        try:
            return [
                tok
                for tok in tokenize.generate_tokens(io.StringIO(text).readline)
                if tok.type != token.ENDMARKER
            ]
        except tokenize.TokenError:
            return -1

    @staticmethod
    def untokenize(toks: list[TokenInfo]) -> str:
        return tokenize.untokenize(toks)

    def expand_string(self, line: str) -> str | int:
        tokens = self.tokenize(line)
        if tokens == -1: return -1

        tokens = self.expand_tokens(tokens)
        out = []
        prev = None

        for t in tokens:
            if t.type == token.ENDMARKER: continue
            s = t.string

            if prev in (token.NAME, token.NUMBER) and t.type in (token.NAME, token.NUMBER):
                out.append(" ")

            out.append(s)
            prev = t.type
        return "".join(out)

    def expand_tokens(self, toks: list[TokenInfo]) -> list[TokenInfo]:
        out: list[TokenInfo] = []
        i: int = 0
        tok: TokenInfo

        while i < len(toks):
            tok = toks[i]

            if tok.type != token.NAME:
                out.append(tok)
                i += 1
                continue

            macro = self.macros.get(tok.string)

            if macro is None:
                out.append(tok)
                i += 1
                continue

            if isinstance(macro, ObjectMacro):
                repl = self.expand_tokens(macro.replacement)
                out.extend(repl)
                i += 1
                continue

            # Function-like macro
            if i + 1 >= len(toks) or toks[i + 1].string != "(":
                out.append(tok)
                i += 1
                continue

            args, end = self.parse_args(toks, i + 1)
            mapping = {}
            for p, a in zip(macro.params, args):
                mapping[p] = a
            repl = []
            for t in macro.replacement:
                if t.type == token.NAME and t.string in mapping:
                    repl.extend(mapping[t.string])
                else:
                    repl.append(t)
            out.extend(self.expand_tokens(repl))
            i = end + 1
        return out

    @staticmethod
    def parse_args(toks: list[TokenInfo], lparen: int) -> tuple[list[TokenInfo], int]:
        #    [(, a, b, (, c, ), )]
        # -> [[a], [b], [(, c, )]]
        args: list[list[TokenInfo]] = []
        cur: list[TokenInfo] = []
        depth: int = 0
        t: TokenInfo | None = None
        i: int = lparen + 1

        while i < len(toks):
            t = toks[i]

            if t.string == "(":
                depth += 1
                cur.append(t)

            elif t.string == ")":
                if depth == 0:
                    args.append(cur)
                    return args, i
                depth -= 1
                cur.append(t)

            elif t.string == "," and depth == 0:
                args.append(cur)
                cur = []

            else:
                cur.append(t)

            i += 1

        raise SyntaxError("Unfinished macro invocation.")

def main():
    parser = argparse.ArgumentParser(
        prog="PyMacro",
        description="Preproccesser for python",
        epilog="example: ./main.py file.py -r -o newfile.py"
    )

    parser.add_argument("input", help=
                        "Source file.")
    parser.add_argument("--run", "-r", dest="run", action="store_true", help=
                        "Execute after proccessing.")
    parser.add_argument("--output", "-o", dest="output", default="", help=
                        "Place the output into file.")
    parser.add_argument("--print", "-p", dest="print", action="store_true", help=
                        "Print proccesed output to stdout")
    parser.add_argument("--verbose", "-v", dest="verbose", action="store_true", help=
                        "Print verbose output.")
    parser.add_argument("--output-debugging", "-l", dest="output_debugging", action="store_true", help=
                        "Output debugging information in the output file.")
    args = parser.parse_args()

    OUTPUTDEBUG = args.output_debugging
    VERBOSE = args.verbose
    INPUT = args.input
    OUTPUT = args.output
    RUN = args.run
    PRINT = args.print

    if not VERBOSE: disable(INFO)

    src = pathlib.Path(INPUT).read_text(encoding="utf-8")
    pp = Preprocessor(OUTPUTDEBUG)
    pp.opened_files.append(pathlib.Path(INPUT).resolve())
    expanded = pp.process(src)

    if OUTPUT:
        pathlib.Path(OUTPUT).write_text(expanded, encoding="utf-8")
    if PRINT:
        print(expanded)
    if RUN:
        exec(expanded)

    if not OUTPUT or RUN or PRINT:
        log(INFO, "No option was selected for proccessed output!")

if __name__ == "__main__":
    main()