import ast

from mutpy.operators.base import MutationOperator, copy_node, MutationResign


class DecoratorDeletion(MutationOperator):
    @copy_node
    def mutate_FunctionDef(self, node):
        if node.decorator_list:
            node.decorator_list = []
            return node
        else:
            raise MutationResign()

    @classmethod
    def name(cls):
        return 'DDL'


class AbstractMethodDecoratorInsertionMutationOperator(MutationOperator):
    @copy_node
    def mutate_FunctionDef(self, node):
        if not isinstance(node.parent, ast.ClassDef):
            raise MutationResign()
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                decorator_name = decorator.func.id
            elif isinstance(decorator, ast.Attribute):
                decorator_name = decorator.value.id
            else:
                decorator_name = decorator.id
            if decorator_name == self.get_decorator_name():
                raise MutationResign()
        if node.decorator_list:
            lineno = node.decorator_list[-1].lineno
        else:
            lineno = node.lineno
        decorator = ast.Name(id=self.get_decorator_name(), ctx=ast.Load(), lineno=lineno)
        self.shift_lines(node.body, 1)
        node.decorator_list.append(decorator)
        return node

    def get_decorator_name(self):
        raise NotImplementedError()


class ClassmethodDecoratorInsertion(AbstractMethodDecoratorInsertionMutationOperator):
    def get_decorator_name(self):
        return 'classmethod'


class StaticmethodDecoratorInsertion(AbstractMethodDecoratorInsertionMutationOperator):
    def get_decorator_name(self):
        return 'staticmethod'
