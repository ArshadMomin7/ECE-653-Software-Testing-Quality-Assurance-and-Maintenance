# The MIT License (MIT)
# Copyright (c) 2016 Arie Gurfinkel

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from . import ast


class UndefVisitor(ast.AstVisitor):
    """Computes all variables that are used before being defined"""

    def __init__(self):
        super(UndefVisitor, self).__init__()
        self.undefined = set()
        pass

    def check(self, node):
        """Check for undefined variables starting from a given AST node"""
        # do the necessary setup/arguments and call self.visit (node, args)
        self.visit(node, defined=set())
        pass

    def get_undefs(self):
        """Return the set of all variables that are used before being defined
        in the program.  Available only after a call to check()
        """
        return self.undefined
        pass

    def visit_StmtList(self, node, *args, **kwargs):
        for st in node.stmts:
            self.visit(st, *args, **kwargs)
        pass

    def visit_IntVar(self, node, *args, **kwargs):
        if node.name not in kwargs["defined"]:
            self.undefined.add(node)
        pass

    def visit_Const(self, node, *args, **kwargs):
        pass

    def visit_Stmt(self, node, *args, **kwargs):
        pass

    def visit_AsgnStmt(self, node, *args, **kwargs):
        self.visit(node.rhs, *args, **kwargs)
        kwargs['defined'].add(node.lhs.name)
        pass

    def visit_Exp(self, node, *args, **kwargs):
        for arg in node.args:
            self.visit(arg, *args, **kwargs)
        pass

    def visit_HavocStmt(self, node, *args, **kwargs):
        for var in node.vars:
            kwargs["defined"].add(var.name)
        pass

    def visit_AssertStmt(self, node, *args, **kwargs):
        self.visit(node.cond, *args, **kwargs)
        pass

    def visit_AssumeStmt(self, node, *args, **kwargs):
        self.visit(node.cond, *args, **kwargs)
        pass

    def visit_IfStmt(self, node, *args, **kwargs):
        self.visit(node.cond, *args, **kwargs)
        local_defined_then = set(kwargs["defined"])
        self.visit(node.then_stmt, defined=local_defined_then)
        if node.has_else():
            local_defined_else = set(kwargs["defined"])
            self.visit(node.else_stmt, defined=local_defined_then)
            defined_both_then_else = local_defined_else & local_defined_then
            kwargs['defined'] |= defined_both_then_else
        pass

    def visit_WhileStmt(self, node, *args, **kwargs):
        self.visit(node.cond, *args, **kwargs)
        local_defined_do = set(kwargs["defined"])
        self.visit(node.body, defined=local_defined_do)
        pass
