import re


class Resolver:
    @classmethod
    def resolve_variable(cls,
                         memory: dict[str, str],
                         text: str) -> str:
        def repl(match: re.Match) -> str:
            key = match.group(1)
            return memory.get(key, match.group(0))
        previous = None
        while previous != text:
            previous = text
            text = re.sub(r"\$(\w+)", repl, text)
        return text

    @classmethod
    def resolve(cls,
                memory: dict[str, str],
                path: list[str]) -> list[str]:
        fixed_path: list[str] = []
        for part in path:
            fixed_path.append(cls.resolve_variable(memory, part))
        return fixed_path
