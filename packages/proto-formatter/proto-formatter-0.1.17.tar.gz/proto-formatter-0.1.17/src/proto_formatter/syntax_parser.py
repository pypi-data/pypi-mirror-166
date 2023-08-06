from .comment import CommentParser
from .protobuf import Protobuf
from .proto_structures import Syntax


class SyntaxParser:

    @classmethod
    def parse_and_add(cls, proto_obj: Protobuf, line, top_comment_list):
        if proto_obj.syntax is not None:
            raise 'multiple syntax detected!'

        proto_obj.syntax = cls.parse_syntax(line, top_comment_list)

    @classmethod
    def parse_syntax(cls, line, top_comment_list):
        value = cls._get_syntax_value(line)
        comments = CommentParser.create_comment(line, top_comment_list)
        syntax = Syntax(value, comments)
        return syntax

    @classmethod
    def _get_syntax_value(cls, line):
        line = line.strip().replace(' ', '')
        lindex = len('syntax=')
        rindex = line.index(';')
        value = line[lindex:rindex].strip().replace('"', "").replace("'", "")

        return value
