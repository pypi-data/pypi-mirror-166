from .comment import CommentParser
from .constant import EQUAL_SIGN, SEMICOLON
from .proto_structures import Option
from .protobuf import Protobuf


class OptionParser:

    @classmethod
    def parse_and_add(cls, proto_obj: Protobuf, line, top_comment_list):
        option = cls.parse_option(line, top_comment_list)
        cls.add_options(proto_obj, option)

    @classmethod
    def add_options(cls, proto_obj: Protobuf, new_option):
        for option in proto_obj.options:
            if option.name == new_option.name:
                raise Exception(f'multiple option detected: {new_option.name}!')
        proto_obj.options.append(new_option)

    @classmethod
    def parse_option(cls, line, top_comment_list):
        name, value = cls._get_option_value(line)
        comments = CommentParser.create_comment(line, top_comment_list)
        option = Option(name, value, comments)
        return option

    @classmethod
    def _get_option_value(cls, line):
        line = line.strip()
        lindex = len('option ')
        equal_sign_index = line.index(EQUAL_SIGN)
        semicolon_index = line.index(SEMICOLON)
        name = line[lindex:equal_sign_index].strip().replace('"', "").replace("'", "")
        value = line[equal_sign_index + 1:semicolon_index].strip().replace('"', "").replace("'", "")

        return name, value
