﻿import itertools
from operator import contains
import typing
from xmlrpc.client import TRANSPORT_ERROR
import tools
from enum import Enum, StrEnum
from typing import Iterator, Self
import re
from itertools import tee
import functools
from copy import deepcopy

class Pipe:
    def __init__(self, parse_char:str, print_char:str, name:str, has_W:bool, has_E:bool, has_N:bool, has_S:bool):
        self.parse_char = parse_char
        self.print_char = print_char
        self.name = name
        self.has_E = has_E
        self.has_W = has_W
        self.has_N = has_N
        self.has_S = has_S
            
    def __repr__(self) -> str:
        return self.print_char    

PIPE_VERTICAL = Pipe('|', '┃', 'N-S', False, False, True, True) # is a vertical pipe connecting north and south.
PIPE_HORIZONTAL = Pipe('-', '━', 'W-E', True, True, False, False) # is a horizontal pipe connecting east and west.
PIPE_BEND_N_E = Pipe('L', '┖', 'N-E', False, True, True, False) # is a 90-degree bend connecting north and east.
PIPE_BEND_N_W = Pipe('J', '┛', 'N-W', True, False, True, False) # is a 90-degree bend connecting north and west.
PIPE_BEND_S_W = Pipe('7', '┒', 'S-W', True, False, False, True) # is a 90-degree bend connecting south and west.
PIPE_BEND_S_E = Pipe('F', '┎', 'S-E', False, True, False, True) # is a 90-degree bend connecting south and east.
PIPE_NO_PIPE = Pipe('.', '·', 'empty', False, False, False, False) # is ground; there is no pipe in this tile.
PIPE_START = Pipe('S', 'S', 'start', None, None, None, None) # is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

ALL_PIPES = [ PIPE_VERTICAL,PIPE_HORIZONTAL,PIPE_BEND_N_E ,PIPE_BEND_N_W ,PIPE_BEND_S_W ,PIPE_BEND_S_E ,PIPE_NO_PIPE ,PIPE_START ]

def parse_pipe(c:str) -> Pipe:
    for p in ALL_PIPES:
        if p.parse_char == c:
            return p
    raise ValueError('Unknown pipe', c)

# None used to make Start connect to anything
def can_connect_horizontal(left:Pipe, right:Pipe) -> bool:
    return (left.has_E is None or left.has_E) and (right.has_W is None or right.has_W)
def can_connect_vertical(top:Pipe, bottom:Pipe) -> bool:
    return (top.has_S is None or top.has_S) and (bottom.has_N is None or bottom.has_N)
    

Node = typing.NewType('Node', None)

class Field:
    def __init__(self, field_matrix : list[list[Node]] = None):
        self.field = field_matrix        

        self.len_Y = len(self.field)
        self.len_X = len(self.field[0])

    def assert_coord_valid(self, x, y):
        assert x >= 0 and y>= 0, f'Coordinate ({x},{y}) outside field'
        assert self.len_X > x, f'Coordinate ({x},{y}) outside field'
        assert self.len_Y > y, f'Coordinate ({x},{y}) outside field'

    def get(self, x:int, y:int) -> Node:
        self.assert_coord_valid(x, y)
        return self.field[y][x]

    def set(self, x:int, y:int, n:Node) -> None:
        self.assert_coord_valid(x, y)
        self.field[y][x] = n
        
    def all_nodes(self) -> list[Node]:
        #return list(itertools.chain(self.field))
        return functools.reduce(lambda xs, ys: xs+ys, self.field)

    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        def y_to_str(ls: list[Node]) -> str:
            return ''.join(map(lambda n: n.value.print_char, ls))
        lines = list(map(y_to_str, self.field))
        return '\n'.join(lines)
    
    def get_start_pos(self) -> Node:
        return next(filter(lambda n: n.value == PIPE_START, self.all_nodes()), None)
    
class Node:
    def __init__(self, field:Field, value:Pipe, x:int, y:int):
        self.field = field
        self.value = value
        self.x = x
        self.y = y
        self.tag = None
       
    def __str__(self) -> str:
        return f'Node [{self.x},{self.y}] {self.value}'

    def __repr__(self) -> str:
        return f'Node [{self.x},{self.y}] {self.value}'
    
    @staticmethod
    def clear_tags(thing) -> None:
        if isinstance(thing, Node):
            thing.tag = None
        else:
            for n in thing:
                Node.clear_tags(n)

    def move(self, dir:str) -> Self:
        if dir == 'N': return self.move_N()
        if dir == 'S': return self.move_S()
        if dir == 'E': return self.move_E()
        if dir == 'W': return self.move_W()
        raise ValueError(f'Innvalid direction {dir}')

    def move_W(self) -> Self:
        if self.x == 0: return None
        return self.field.get(self.x-1, self.y)
    def move_E(self) -> Self:
        if self.x+1 == self.field.len_X : return None
        return self.field.get(self.x+1, self.y)
    def move_N(self) -> Self:
        if self.y == 0: return None
        return self.field.get(self.x, self.y-1)
    def move_S(self) -> Self:
        if self.y+1 == self.field.len_Y : return None
        return self.field.get(self.x, self.y+1)

    def can_move_W(self)->bool:
        n = self.move_W()
        return not n is None and can_connect_horizontal(n.value, self.value)
    def can_move_E(self)->bool:
        n = self.move_E()
        return not n is None and can_connect_horizontal(self.value, n.value)
    def can_move_N(self)->bool:
        n = self.move_N()
        return not n is None and can_connect_vertical(n.value, self.value)
    def can_move_S(self)->bool:
        n = self.move_S()
        return not n is None and can_connect_vertical(self.value, n.value)
    
    def can_move(self, dir:str) -> Self:
        if dir == 'N': return self.can_move_N()
        if dir == 'S': return self.can_move_S()
        if dir == 'E': return self.can_move_E()
        if dir == 'W': return self.can_move_W()
        raise ValueError(f'Innvalid direction {dir}')
    
    def coonnected_neighbors(self) -> list[Self]:
        valid_dir = list( filter( lambda d: self.can_move(d), 'NSEW'))
        return list(map( lambda d: self.move(d), valid_dir))
    
def ParseField(str_field:str) -> Field:
    lines = str_field.split('\n')
    y_len = len(lines)
    x_len = len(lines[0])
    field = Field(list(map(lambda _: [None]*x_len, [None]*y_len)))
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            p = parse_pipe(lines[y][x])
            n = Node(field, p, x, y)
            field.set(x, y, n)
    return field

def find_loop(start:Node) -> list[Node]:
    Node.clear_tags(start.field.all_nodes())
    
    loop = []
    n = start
    while True:
        loop.append(n)
        n.tag = True
        neighbors = n.coonnected_neighbors()
        # nexts = list(filter(lambda n: not n.tag, neighbors))
        
        next_node = next(filter(lambda n: not n.tag, neighbors), None)
        if next_node is None:
            if contains(neighbors, start): # has looped
                break
            raise ValueError('Could not move away from node ', n)
        n = next_node
        
    return loop
        
    