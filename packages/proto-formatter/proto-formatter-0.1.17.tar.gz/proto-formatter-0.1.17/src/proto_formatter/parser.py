from .comment import CommentParser
from .detector import Detector
from .import_parser import ImportParser
from .object_parser import ObjectParser
from .option_parser import OptionParser
from .package_parser import PackageParser
from .protobuf import Protobuf
from .syntax_parser import SyntaxParser


class ProtoParser:
    PARSERS = {
        'syntax': SyntaxParser,
        'package': PackageParser,
        'option': OptionParser,
        'import': ImportParser,
        'message': ObjectParser,
        'enum': ObjectParser,
        'extend': ObjectParser,
        'service': ObjectParser,
        'oneof': SyntaxParser
    }

    def __init__(self):
        self.protobuf_obj = Protobuf()

    def load(self, fp):
        """
        Load proto from file, deserialize it as a ProtoBufStructure object.
        :param fp: The absolute file path of the proto file.
        :return: Object of ProtoBufStructure.
        """
        lines = self.read_lines(fp)
        return self._parse(lines)

    def loads(self, proto_str):
        """
        Parse proto string, return a ProtoBufStructure object.
        :param proto_str: The proto string need to pasre.
        :return: Object of ProtoBufStructure.
        """
        lines = proto_str.split('\n')
        return self._parse(lines)

    @staticmethod
    def read_lines(path):
        """
        Read data from file as line list, all blank and empty lines are removed before and after valid text.
        :param path: Absolute file path.
        :return: Line list of the striped file content.
        """
        with open(path) as f:
            content = f.read()
            content = content.strip()
            lines = content.split('\n')
            return lines

    def _parse(self, lines):
        """
        Pasre proto content lines, deserialize them as a ProtoBufStructure object.
        :param lines: the proto content lines.
        :return: an object of ProtoBufStructure.
        """
        top_comments = Detector().get_top_comments(lines)
        if len(lines) == 0:
            return self.protobuf_obj

        first_line = lines[0]
        proto_type = Detector().get_type(first_line)

        parser = self.PARSERS[proto_type]()
        if parser is None:
            return self.protobuf_obj

        if isinstance(parser, ObjectParser):
            parser.parse(lines)
            top_comments = CommentParser.create_comment(first_line, top_comments)
            all_comments = top_comments + parser.objects[0].comments
            parser.objects[0].comments = all_comments
            self.protobuf_obj.objects.extend(parser.objects)
        else:
            line = lines.pop(0)
            parser.parse_and_add(self.protobuf_obj, line, top_comments)

        if len(lines) == 0:
            return self.protobuf_obj

        return self._parse(lines)
