from textwrap import indent


def indent_body(body: str) -> str:
    return indent(body, ' ' * 4)


def format_modifier(name: str, args: list[str], pretty: bool) -> str:
    if not args:
        return name

    body = ', '.join(args)

    if pretty:
        return '%s(\n%s\n)' % (
            name,
            indent_body(body)
        )

    return '%s(%s)' % (name, body)
