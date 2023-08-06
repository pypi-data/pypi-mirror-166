from .comment import CommentParser
from .constant import SEMICOLON
from .proto_structures import Import
from .protobuf import Protobuf


class ImportParser:

    @classmethod
    def parse_and_add(cls, proto_obj: Protobuf, line, top_comment_list):
        new_import = cls.parse_import(line, top_comment_list)
        for existing_import in proto_obj.imports:
            if existing_import.value == new_import.value:
                raise Exception(f'multiple import detected: {new_import.value}!')

        proto_obj.imports.append(new_import)

    @classmethod
    def parse_import(cls, line, top_comment_list):
        value = cls._get_import_value(line)
        comments = CommentParser.create_comment(line, top_comment_list)
        n_import = Import(value, comments)
        return n_import

    @classmethod
    def _get_import_value(cls, line):
        line = line.strip()
        lindex = len('import ')
        rindex = line.index(SEMICOLON)
        value = line[lindex:rindex].strip().replace("'", '').replace('"', '')
        return value
