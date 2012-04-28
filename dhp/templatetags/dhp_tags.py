# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django import template

register = template.Library()

@register.tag
def code(parser, token):
    """Parse our python code
    """

    nodelist = parser.parse(('endcode',))
    parser.delete_first_token()

    return CodeNode(nodelist)

class CodeNode(template.Node):
    """Node containign code
    """

    def __init__(self, nodelist):
        """nodelist does not appear to be a line-by-line list o_O
        """

        self.nodelist = nodelist

    def cleanse_code_lines(self, code_lines):
        """Take care of indents etc
        """

        clean_lines = []

        indent_char = code_lines[0][0]
        if indent_char in (' ', '\t'):
            # Determine indent
            space_count = 0
            for c in code_lines[0]:
                if c == indent_char:
                    space_count += 1
                else:
                    break

            indent = space_count * indent_char
            for line in code_lines:
                clean_lines.append(line.replace(indent, '', 1))

        return clean_lines or code_lines

    def render(self, context):
        code_block = self.nodelist[0]
        code_lines = [l for l in code_block.s.splitlines() if l.strip()]

        code_lines = self.cleanse_code_lines(code_lines)

        code = '\n'.join(code_lines)

        exec(code, context.dicts[0])

        return ''

# EOF

