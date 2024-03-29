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

import sys
import io 
import z3
from functools import reduce
from . import ast, int


class SymState(object):
    def __init__(self, solver=None):
        # environment mapping variables to symbolic constants
        self.env = dict()
        # path condition
        self.path = list()
        self._solver = solver
        if self._solver is None:
            self._solver = z3.Solver()

        # true if this is an error state
        self._is_error = False

    def add_pc(self, *exp):
        """Add constraints to the path condition"""
        self.path.extend(exp)
        self._solver.append(exp)

    def is_error(self):
        return self._is_error

    def mk_error(self):
        self._is_error = True

    def is_empty(self):
        """Check whether the current symbolic state has any concrete states"""
        res = self._solver.check()
        return res == z3.unsat

    def pick_concerete(self):
        """Pick a concrete state consistent with the symbolic state.
           Return None if no such state exists"""
        res = self._solver.check()
        if res != z3.sat:
            return None
        model = self._solver.model()
        st = int.State()
        for (k, v) in self.env.items():
            st.env[k] = model.eval(v)
        return st

    def fork(self):
        """Fork the current state into two identical states that can evolve separately"""
        child = SymState()
        child.env = dict(self.env)
        child.add_pc(*self.path)

        return (self, child)

    def __repr__(self):
        return str(self)

    def to_smt2(self):
        """Returns the current state as an SMT-LIB2 benchmark"""
        return self._solver.to_smt2()

    def __str__(self):
        buf = io.StringIO()
        for k, v in self.env.items():
            buf.write(str(k))
            buf.write(': ')
            buf.write(str(v))
            buf.write('\n')
        buf.write('pc: ')
        buf.write(str(self.path))
        buf.write('\n')

        return buf.getvalue()
    
    def addcond_isSolvable(self, cond):
        self.add_pc(cond)
        return not self.is_empty()


class SymExec(ast.AstVisitor):
    def __init__(self):
        pass

    def run(self, ast, state):
        # set things up and call
        self.visit (ast, state=state)
        return self.visit(ast, state=state)
        # if not state.is_empty ():
        #     for out in self.visit (ast, state=state):
        #         return out
        pass

    def visit_IntVar(self, node, *args, **kwargs):
        return kwargs['state'].env[node.name]

    def visit_BoolConst(self, node, *args, **kwargs):
        return z3.BoolVal(node.val)

    def visit_IntConst(self, node, *args, **kwargs):
        return z3.IntVal(node.val)

    def visit_RelExp(self, node, *args, **kwargs):
        lhs = self.visit(node.arg(0), *args, **kwargs)
        rhs = self.visit(node.arg(1), *args, **kwargs)
        if node.op == '<=': return lhs <= rhs
        if node.op == '<': return lhs < rhs
        if node.op == '=': return lhs == rhs
        if node.op == '>=': return lhs >= rhs
        if node.op == '>': return lhs > rhs
        # assert True

    def visit_BExp(self, node, *args, **kwargs):
        kids = [self.visit(a, *args, **kwargs) for a in node.args]
        if node.op == 'not':
            assert node.is_unary()
            assert len(kids) == 1
            return z3.Not(kids[0])
        
        fn = None
        base = None
        if node.op == 'and':
            fn = lambda x, y :z3.And(x,y)
            base = z3.BoolVal(True)
        elif node.op == 'or':
            fn = lambda x, y : z3.Or(x,y)
            base = z3.BoolVal(False)

        assert fn is not None
        return reduce (fn, kids, base)
        pass

    def visit_AExp(self, node, *args, **kwargs):
        kids = [self.visit(a, *args, **kwargs) for a in node.args]

        fn = None
        if node.op == '+':
            fn = lambda x, y: x + y
        elif node.op == '-':
            fn = lambda x, y: x - y
        elif node.op == '*':
            fn = lambda x, y: x * y
        elif node.op == '/':
            fn = lambda x, y: x / y

        assert fn is not None
        return reduce(fn, kids)
        pass

    def visit_SkipStmt(self, node, *args, **kwargs):
        return [kwargs['state']]
        pass

    def visit_PrintStateStmt(self, node, *args, **kwargs):
        print(kwargs['state'])
        return [kwargs['state']]
        pass

    def visit_AsgnStmt(self, node, *args, **kwargs):
        
        val = self.visit (node.rhs, *args, **kwargs)
        st = kwargs['state']
        name = node.lhs.name
        sym_val = z3.FreshInt (name)
        st.env [name] = sym_val
        st.add_pc (sym_val == val)
        yield st
        pass

    def visit_IfStmt(self, node, *args, **kwargs):
        
        cond_val = self.visit (node.cond, *args, **kwargs)

        st = kwargs['state']
        then_branch, else_branch = st.fork ()
        then_branch.add_pc (cond_val)

        if not then_branch.is_empty ():
            # cover all path under then branch
            nkwargs = dict (kwargs)
            nkwargs['state'] = then_branch
            for out in self.visit (node.then_stmt, *args, **nkwargs):
                yield out

        else_branch.add_pc (z3.Not (cond_val))
        if not else_branch.is_empty ():
            if node.has_else ():
                nkwargs = dict (kwargs)
                nkwargs['state'] = else_branch
                for out in self.visit (node.else_stmt, *args, **nkwargs):
                   yield out

            else:
                yield else_branch
        pass

    def visit_WhileStmt(self, node, *args, **kwargs):
       done = []
       while_states = [kwargs['state']]

       executed_time = 1

       while(len(while_states) != 0 and executed_time <= 10):
            executed_time += 1
            updated_while_states = []
            for state in while_states:
                cond = self.visit(node.cond, state=state) 
                cond_fork = state.fork()

                # if after adding condition, state is still solvable, visit node.body,
                # and extend returned state-list
                if cond_fork[0].addcond_isSolvable(cond):
                    updated_while_states.extend(self.visit(node.body, state=cond_fork[0]))
                # if after adding not condition, state is still solvable, append the termination state into returning states
                if cond_fork[1].addcond_isSolvable(z3.Not(cond)):
                    done.append(cond_fork[1])
            while_states = updated_while_states
       return done



    def visit_AssertStmt(self, node, *args, **kwargs):
                
        st = kwargs['state']
        cond_val = self.visit (node.cond, *args, **kwargs)
        true_state, false_state = st.fork ()
        false_state.add_pc (z3.Not (cond_val))
        if not false_state.is_empty ():
            print ('[symexec]: Error at', node, 'with', false_state)
            print ('[symexec]: Concrete state', false_state.pick_concerete())
            false_state.mk_error ()

        true_state.add_pc (cond_val)
        if not true_state.is_empty ():
            yield true_state
        pass

    def visit_AssumeStmt(self, node, *args, **kwargs):
                
        st = kwargs['state']
        cond_val = self.visit (node.cond, *args, **kwargs)
        st.add_pc (cond_val)
        if not st.is_empty ():
            yield st
        pass

    def visit_HavocStmt(self, node, *args, **kwargs):
        state = kwargs['state']
        for var in node.vars:
            state.env[var.name] = z3.FreshInt(var.name)
        return [state]
        pass

    def visit_StmtList(self, node, *args, **kwargs):
        
        st = kwargs['state']
        for out in self._run_Stmts (node.stmts, st):
            yield out
        pass

    def _run_Stmts (self, stmts, st):
        """Recursively run a sequential list of statements"""

        # empty sequence is just like a skip
        if len (stmts) == 0:
            yield st

        # a single statement is simply executed
        elif len (stmts) == 1:
            for out in self.run (stmts [0], st):
                yield out

        # for every output state of executing the first statement,
        # execute the rest of the sequence
        else:
            for out1 in self.run (stmts [0], st):
                for out2 in self._run_Stmts (stmts[1:], out1):
                    yield out2

def _parse_args():
    import argparse
    ap = argparse.ArgumentParser(prog='sym',
                                 description='WLang Interpreter')
    ap.add_argument('in_file', metavar='FILE',
                    help='WLang program to interpret')
    args = ap.parse_args()
    return args

    

def main():
    args = _parse_args()
    prg = ast.parse_file(args.in_file)
    st = SymState()
    sym = SymExec (loop_bound=args.bound)

    states = sym.run(prg, st)
    if states is None:
        print('[symexec]: no output states')
    else:
        count = 0
        for out in states:
            count = count + 1
            print('[symexec]: symbolic state reached')
            print(out)
        print('[symexec]: found', count, 'symbolic states')
    return 0


if __name__ == '__main__':
    sys.exit(main())
