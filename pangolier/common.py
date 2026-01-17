from textwrap import indent


def bracket(body: str, pretty: bool) -> str:
    if pretty:
        return '(\n' + indent_body(body) + '\n)'
    return '(' + body + ')'


def indent_body(body: str) -> str:
    return indent(body, ' ' * 4)


def format_modifier(
    name: str,
    args: list[str],
    force_bracket: bool = False,
    pretty: bool = False,
) -> str:
    if not args:
        if force_bracket:
            return '%s()' % name
        return name

    body = ', '.join(args)

    if pretty:
        return '%s(\n%s\n)' % (
            name,
            indent_body(body)
        )

    return '%s(%s)' % (name, body)
