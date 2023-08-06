from __future__ import annotations

import ast
import builtins
from random import choice
from base64 import b64encode

class Obfuscator:
    def __init__(self, code: str) -> None:
        self.tree = ast.parse(code)
    
    def getCode(self) -> str:
        return ast.unparse(self.tree)
    
    def getTree(self) -> str:
        return ast.dump(self.tree, indent=2)
    
    def getRandomName(self, names: dict[str, str]) -> str:
        while (name := "O" + "".join(choice("O0") for _ in range(10))) in names:
            pass
        return name
    
    def iterateTree(self, node: ast.AST) -> list[ast.AST]:
        nodes = [node]
        for child in ast.iter_child_nodes(node):
            nodes.extend(self.iterateTree(child))
        if isinstance(node, ast.Call):
            for arg in node.args:
                nodes.extend(self.iterateTree(arg))
        return nodes
    
    def changeNames(self) -> Obfuscator:
        names: dict[str, str] = {}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.alias):
                if node.asname is not None:
                    names.setdefault(node.asname, node.asname)
                else:
                    node.asname = self.getRandomName(names)
                    names.setdefault(node.name, node.asname)
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Name) and node.id not in dir(builtins) and not (node.id.startswith("__") and node.id.endswith("__")):
                node.id = names.setdefault(node.id, self.getRandomName(names))
            if isinstance(node, ast.FunctionDef) and node.name not in dir(builtins) and not (node.name.startswith("__") and node.name.endswith("__")):
                node.name = names.setdefault(node.name, self.getRandomName(names))
            # if isinstance(node, ast.Attribute) and node.attr not in dir(builtins) and not (node.attr.startswith("__") and node.attr.endswith("__")):
            #     node.attr = names.setdefault(node.attr, uuid4().hex)
        return self
    
    def removeDots(self) -> Obfuscator:
        self.tree = _DotRemover().visit(self.tree)
        return self
    
    def base64encode(self) -> Obfuscator:
        self.tree = ast.parse(f"exec(__import__('base64').b64decode(b'{b64encode(ast.unparse(self.tree).encode('utf-8')).decode('utf-8')}'))")
        return self
    
    def changeStrings(self):
        self.tree = _StringChanger().visit(self.tree)
        return self
    
    def changeBytes(self):
        self.tree = _BytesChanger().visit(self.tree)
        return self
    
    def changeIntsToStrings(self):
        self.tree = _IntStringifier().visit(self.tree)
        return self
    
    def changeInts(self):
        self.tree = _IntChanger().visit(self.tree)
        return self

class _DotRemover(ast.NodeTransformer):
    def visit_Assign(self, node: ast.Assign) -> ast.AST:
        self.generic_visit(node)
        if isinstance(node.targets[0], ast.Attribute):
            return ast.Expr(value=ast.Call(func=ast.Name(id="setattr", ctx=ast.Load()), args=[node.targets[0].value, ast.Constant(value=node.targets[0].attr), node.value], keywords=[]))
        return node
    
    def visit_Attribute(self, node: ast.Attribute) -> ast.AST:
        self.generic_visit(node)
        if isinstance(node.ctx, ast.Load):
            return ast.Call(func=ast.Name(id="getattr", ctx=ast.Load()), args=[node.value, ast.Constant(value=node.attr)], keywords=[])
        return node

class _StringChanger(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        self.generic_visit(node)
        if isinstance(node.value, str):
            return ast.Call(
                func=ast.Attribute(
                value=ast.Call(
                    func=ast.Name(id='bytes', ctx=ast.Load()),
                    args=[
                    ast.List(
                        elts=[
                        ast.Constant(value=ord(c)) for c in node.value],
                        ctx=ast.Load())],
                    keywords=[]),
                attr='decode',
                ctx=ast.Load()),
                args=[],
                keywords=[])
        return node

class _BytesChanger(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        self.generic_visit(node)
        if isinstance(node.value, bytes):
            return ast.Call(
                func=ast.Name(id='bytes', ctx=ast.Load()),
                args=[
                ast.List(
                    elts=[
                    ast.Constant(value=int(b)) for b in node.value],
                    ctx=ast.Load())],
                keywords=[])
        return node

class _IntStringifier(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        self.generic_visit(node)
        if isinstance(node.value, int):
            return ast.Call(
                func=ast.Name(id='int', ctx=ast.Load()),
                args=[ast.Constant(value=str(node.value))],
                keywords=[])
        return node

class _IntChanger(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        self.generic_visit(node)
        if isinstance(node.value, int):
            res = node
            if node.value == 0:
                res = ast.BinOp(
                    left=ast.Compare(
                        left=ast.List(elts=[], ctx=ast.Load()),
                        ops=[ast.Eq()],
                        comparators=[ast.List(elts=[], ctx=ast.Load())]
                    ),
                    op=ast.Sub(),
                    right=ast.Compare(
                        left=ast.List(elts=[], ctx=ast.Load()),
                        ops=[ast.Eq()],
                        comparators=[ast.List(elts=[], ctx=ast.Load())]
                    )
                )
            else:
                value = abs(node.value)
                res = ast.Compare(
                    left=ast.List(elts=[], ctx=ast.Load()),
                    ops=[ast.Eq()],
                    comparators=[ast.List(elts=[], ctx=ast.Load())]
                )
                for _ in range(value - 1):
                    res = ast.BinOp(
                        left=res,
                        op=ast.Add(),
                        right=ast.Compare(
                            left=ast.List(elts=[], ctx=ast.Load()),
                            ops=[ast.Eq()],
                            comparators=[ast.List(elts=[], ctx=ast.Load())]
                        )
                    )
                if node.value < 0:
                    ast.UnaryOp(
                        op=ast.USub(),
                        operand=res
                    )
            return res
        return node
