from enum import Enum
from markdown_to_blocks import markdown_to_blocks
import re


class BlockType(Enum):
    PARAGRAPH = ''
    HEADER = r'^#{1,6}\s'
    CODE = r'^```[\s\S]*\n?```$'
    QUOTE = r'^(>.*)(\n>.*)*$'
    UNORDERED_LIST = r'^(-\s.*)(\n-\s.*)*$'
    ORDERED_LIST = '123'


def is_header(s):
    return bool(re.match(r'^#{1,6}\s',s))

def is_code(s):
    if s.startswith('```') and s.endswith('```'):
        return True
    return False

def is_quote(s):
    lines = s.splitlines()
    for line in lines:
        if not line.startswith('>'):
            return False
    return True

def is_unordered_list(s):
    lines = s.splitlines()
    for line in lines:
        if not line.startswith('- '):
            return False
        if len(line) > 2 and line[2] == ' ':
            return False
    return True

def is_ordered_list(s):
    lines = s.splitlines()
    for i, line in enumerate(lines):
        if not line.startswith(f'{i + 1}. '):
            return False
        if len(line) > 2 and line[3] == ' ':
            return False
    return True


def block_to_block_type(block):

    if block == "":
        return BlockType.PARAGRAPH

    CHECKS = [
        (BlockType.HEADER, is_header),
        (BlockType.CODE, is_code),
        (BlockType.QUOTE, is_quote),
        (BlockType.UNORDERED_LIST, is_unordered_list),
        (BlockType.ORDERED_LIST, is_ordered_list),
    ]

    for b_type, check in CHECKS:
        if check(block):
            return b_type
        
    return BlockType.PARAGRAPH