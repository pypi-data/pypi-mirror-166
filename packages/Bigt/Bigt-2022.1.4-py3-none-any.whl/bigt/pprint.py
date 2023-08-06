from bigt.dictext import DictExt

try:
    from rich.console import Console
    from rich.pretty import ReprHighlighter

    def pp(full, missed, changed, indent=0):
        result = ""
        if isinstance(full, dict):
            result += "{\n"
            indent += 4
            for k, v in full.items():
                if isinstance(k, str):
                    kk = f"{' ' * indent}'{k}'"
                if k in changed and 'old' in changed[k]:
                    result += "[on #632725][#fd3c3c]-[/#fd3c3c]" + \
                        f"{' ' * (indent-1)}'{k}': " + \
                        f"{pp(changed[k]['old'], {}, {}, indent)}" \
                        ",[/on #632725]\n"
                    result += "[on #1d5e2b][#06da06]+[/#06da06]" + \
                        f"{' ' * (indent-1)}'{k}': " + \
                        f"{pp(changed[k]['new'], {}, {}, indent)}" \
                        ",[/on #1d5e2b]\n"
                else:
                    result += f"{kk}: "
                    result += pp(v,
                                 missed.get(k, {}),
                                 changed.get(k, {}),
                                 indent)
                    result += ",\n"
            for k, v in missed.items():
                if k not in full:
                    result += "[on #254263][#06da06]+[/#06da06]" + \
                        f"{' ' * (indent-1)}'{k}': " + \
                        f"{pp(v, {}, {}, indent)},[/on #254263]\n"
                else:
                    pass
                    # print(k, v)
            indent -= 4
            result += f"{' ' * indent}}}"
        elif isinstance(full, list):
            result += "[\n"
            indent += 4
            for i, x in enumerate(full):
                m, c = {}, {}
                if i < len(missed):
                    m = missed[i]
                if i < len(changed):
                    c = changed[i]
                result += f"{' ' * indent}{pp(x, m, c, indent)},\n"
            if i < len(missed):
                for m in missed:
                    result += "[on #632725][#fd3c3c]-[/#fd3c3c]" + \
                        f"{' ' * (indent-1)}{pp(m, {}, {}, indent)}" \
                        ",[/on #632725]\n"
            indent -= 4
            result += f"{' ' * indent}]"
        elif isinstance(full, str):
            result += f"'{full}'"
        else:
            result += f"{full}"
        return result

    def assert_issubset(a, b, regex_mask=False, skip=[], weights={}):
        if pprint(a, b, regex_mask, skip, weights, False):
            raise AssertionError("Difference found. "
                                 "Please find more details above.")

    def pprint(a, b, regex_mask=False, skip=[], weights={},
               print_if_equal=True):
        r, m, c = DictExt(b).issubset(a, regex_mask, skip, weights)
        if not r or print_if_equal:
            console = Console()
            console.print(
                ReprHighlighter()
                (console.render_str(pp(a, m, c)))
                .with_indent_guides(4))
        return not r
except ImportError:
    import json

    def pprint(a, b, regex_mask=False, skip=[], weights={},
               print_if_equal=True):
        r, m, c = DictExt(b).issubset(a, regex_mask, skip, weights)
        print(json.dumps({"missed": m, "changed": c}, indent=4))
        return not r

    def assert_issubset(a, b, regex_mask=False, skip=[], weights={}):
        if pprint(a, b, regex_mask, skip, weights, False):
            raise AssertionError("Difference found. "
                                 "Please find more details above.")
