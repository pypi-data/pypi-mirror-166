import ast as py_ast

import hy
import vyper.ast.nodes as vy_nodes
from hy import models

from .builtins import parse_builtin
from .core import (parse_attribute, parse_call, parse_contract,
                   parse_declarations, parse_do_body, parse_fn, parse_struct, parse_subscript, parse_tuple)
from .ops import (BIN_FUNCS, BOOL_OPS, COMP_FUNCS, UNARY_OPS, parse_binop,
                  parse_boolop, parse_comparison, parse_unary)
from .stmt import parse_assignment, parse_if, parse_return
from .utils import next_node_id_maker, next_nodeid

BUILTIN_FUNCS = BIN_FUNCS + COMP_FUNCS + UNARY_OPS + BOOL_OPS

NAME_CONSTS = ["True", "False"]

MACROS = []

def parse_expr(expr):

    match expr:
        case models.Keyword(name), models.Integer(length):
            if str(name) == "string":
                value_node = parse_node(models.Symbol("String"))
            elif str(name) == "bytes":
                value_node = parse_node(models.Symbol("Bytes"))
            else:
                value_node = parse_node(models.Symbol(str(name)))
            annotation = vy_nodes.Subscript(ast_type='Subscript', node_id=next_nodeid(), slice=vy_nodes.Index(ast_type='Index', node_id=next_nodeid(), value=parse_node(length)), value=value_node)
            annotation._children.add(value_node)
            return annotation

    
    cmd_str = str(expr[0])

    if cmd_str in BIN_FUNCS:
        return parse_binop(expr)
    if cmd_str in COMP_FUNCS:
        return parse_comparison(expr)
    if cmd_str in UNARY_OPS:
        return parse_unary(expr)
    if cmd_str in BOOL_OPS:
        return parse_boolop(expr)

    match cmd_str:
        case "defcontract":
            return parse_contract(expr)
        case "defmacro":
            hy.eval(expr)
            MACROS.append(str(expr[1]))
        case str(cmd) if cmd in MACROS:
            new_node = hy.macroexpand_1(expr)
            return parse_node(new_node)
        case 'defn':
            return parse_fn(expr)
        case 'return':
            return parse_return(expr)
        case 'quote':
            return parse_tuple(expr)
        case 'tuple':
            return parse_tuple(expr)
        case '.':
            return parse_attribute(expr)
        case 'setv':
            return parse_assignment(expr)
        case 'if':
            return parse_if(expr)
        case 'defvar':
            return parse_declarations(expr)
        case 'defstruct':
            return parse_struct(expr)
        case 'subscript':
            return parse_subscript(expr)
        case 'get-in':
            return parse_subscript(expr)
        case 'public' | 'immutable' | 'constant':
            return parse_call(expr)
        case 'do':
            return parse_do_body(expr)
        case _:
            return parse_call(expr, wrap_expr=False)


def parse_node(node):
    match node:
        case models.Expression(node):
            return parse_expr(node)
        case models.Integer(node):
            value_node = vy_nodes.Int(value=int(node), node_id=next_nodeid(), ast_type='Int')
            return value_node
        case models.Float(node):
            raise Exception("Floating point not supported (yet)")
            # value_node = vy_nodes.Decimal(value=Decimal(float(node)), node_id=next_nodeid(), ast_type='Decimal')
            # return value_node
        case models.String(node):
            value_node = vy_nodes.Str(value=str(node), node_id=next_nodeid(), ast_type='Str')
            return value_node
        case models.Symbol(node) if str(node) in BUILTIN_FUNCS:
            return parse_builtin(node)
        case models.Symbol(node) if str(node) in NAME_CONSTS:
            return vy_nodes.NameConstant(value=py_ast.literal_eval(str(node)), id=next_nodeid(), ast_type='NameConstant')
        case models.Symbol(node) if str(node).startswith('0x'):
            return vy_nodes.Hex(id=next_nodeid(), ast_type='Hex', value=str(node))
        case models.Symbol(node) if "/" in str(node):
            target, attr = str(node).split('/')
            replacement_node = models.Expression((models.Symbol('.'), models.Symbol(target), models.Symbol(attr)))
            return parse_node(replacement_node)
        case models.Symbol(node) | models.Keyword(node):
            name_node = vy_nodes.Name(id=str(node), node_id=next_nodeid(), ast_type='Name')
            return name_node
        case models.Bytes(byt):
            bytes_node = vy_nodes.Bytes(node_id=next_nodeid(), ast_type='Byte', value=byt)
            return bytes_node
        case None:
            return None
        case _:
            raise Exception(f"No match for node {node}")

def parse_src(src: str):
    mod_node = vy_nodes.Module(body=[], name="", doc_string="", ast_type='Module', node_id=next_nodeid())

    vars = []
    fs = []
    for element in hy.read_many(src):
        ast = parse_node(element)

        if isinstance(ast, vy_nodes.Module):
            mod_node = ast
        elif isinstance(ast, vy_nodes.VariableDecl):
            vars.append(ast)
        elif isinstance(ast, vy_nodes.StructDef):
            vars.append(ast)
        elif isinstance(ast, vy_nodes.FunctionDef):
            fs.append(ast)
        elif isinstance(ast, list):
            for v in ast:
                vars.append(v)
        elif ast is None:
            # macro declarations return None
            pass
        else:
            raise Exception(f"Unrecognized top-level form {element} {ast}")

    for e in vars + fs:
        mod_node.add_to_body(e)


    return mod_node

with open("dasy/parser/macros.hy", encoding="utf-8") as f:
    code = f.read()
    for expr in hy.read_many(code):
        parse_node(expr)
