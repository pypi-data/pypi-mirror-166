"""
Subclass of the
`built-in function type <https://docs.python.org/3/library/operator.html>`__
for representing algebraic operators (that are typically associated with
algebraic structures and algebraic circuits) as immutable, hashable, sortable,
and callable objects.

Instances of the class exported by this library can be used as gate operations
within circuits as they are implemented within the
`circuit <https://pypi.org/project/circuit>`__ library. This library is intended
to complement the `logical <https://pypi.org/project/logical>`__ library for
logical operations.
"""
from __future__ import annotations
from typing import Any, Tuple
import doctest
import operator

class algebraical(type(operator)):
    """
    Class for representing algebraic operators. This class is derived from
    the type of the built-in functions found in the :obj:`operator` library.
    Thus, it is possible to invoke these operators on values of
    `numeric <https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex>`__
    types and on objects that define the special
    `methods <https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types>`__
    associated with these built-in operators.

    >>> algebraical.add_(1, 2)
    3

    The name and arity of an instance can be retrieved.

    >>> algebraical.mul_.name()
    'mul'
    >>> algebraical.mul_.arity()
    2

    Instances can be compared according to their precedence.

    >>> pow_ > mul_
    True
    >>> pow_ < add_
    False
    >>> sorted([pow_, mul_, add_]) # From lowest to highest precedence.
    [add_, mul_, pow_]

    Instances are also hashable and can be used as members of :obj:`set`
    instances and as keys within :obj:`dict` instances.

    >>> from algebraical import *
    >>> {add_, add_, add_}
    {add_}
    >>> sorted({add_: 0, mul_: 1}.items())
    [(add_, 0), (mul_, 1)]
    """
    names: dict = None
    """Typical concise names for operators."""

    arities: dict = None
    """Arities of operators."""

    def __init__(
            self: algebraical,
            function: operator, # pylint: disable=redefined-outer-name
            name: str
        ):
        """
        Create an instance given a built-in operator object.
        """
        super().__init__(name)

        # Store the original function for use in :obj:`__call__`.
        self.function = function

    def __call__(
            self: algebraical,
            *arguments: Tuple[Any, ...]
        ) -> Any:
        """
        Apply the function represented by this instance to zero or more
        arguments.

        >>> algebraical.add_(1, 2)
        3
        """
        return self.function(*arguments)

    def name(self: algebraical) -> str:
        """
        Return the canonical concise name for this operator.

        >>> algebraical.mul_.name()
        'mul'
        """
        return algebraical.names[self] # pylint: disable=unsubscriptable-object

    def arity(self: algebraical) -> int:
        """
        Return the arity of this operator.

        >>> algebraical.mul_.arity()
        2
        >>> algebraical.neg_.arity()
        1
        """
        return algebraical.arities[self] # pylint: disable=unsubscriptable-object

    def __repr__(self: algebraical) -> str:
        """
        String representation of this instance.

        >>> algebraical.mul_
        mul_
        """
        return algebraical.names[self] + '_' # pylint: disable=unsubscriptable-object

    def __str__(self: algebraical) -> str:
        """
        String representation of this instance.

        >>> str(algebraical.mul_)
        'mul_'
        """
        return repr(self)

    def _precedence(self: algebraical):
        """
        Return an integer that represents the precedence of an operator
        (with a higher integer representing a higher precedence).
        """
        if self == algebraical.abs_:
            return 3
        if self == algebraical.pow_:
            return 2
        if self in (
            algebraical.mul_,
            algebraical.matmul_,
            algebraical.truediv_,
            algebraical.floordiv_,
            algebraical.mod_
        ):
            return 1

        return 0

    def __lt__(self: algebraical, other: algebraical) -> bool:
        """
        Compare two operators according to their precedence, where an operator
        with lower precedence is *less than* an operator with higher precedence.

        >>> add_ < mul_
        True
        >>> add_ < pow_
        True
        >>> pow_ < mul_
        False
        >>> add_ > abs_
        False

        Operators that have the same precedence are not *less than* one another.

        >>> mul_ < mul_
        False
        >>> sub_ > add_
        False
        """
        return self._precedence() < other._precedence()

    def __le__(self: algebraical, other: algebraical) -> bool:
        """
        Compare two operators according to their precedence, where an operator
        with lower precedence is *less than or equal to* an operator with
        higher precedence.

        >>> add_ <= mul_
        True
        >>> add_ <= pow_
        True
        >>> mul_ >= pow_
        False
        >>> mul_ >= mul_
        True
        """
        return self._precedence() <= other._precedence()

    pos_: algebraical = None
    """
    Identity operator.

    >>> pos_(2)
    2
    """

    neg_: algebraical = None
    """
    Negation operator.

    >>> neg_(2)
    -2
    """

    abs_: algebraical = None
    """
    Absolute value operator.

    >>> abs(-2)
    2
    """

    add_: algebraical = None
    """
    Addition operator.

    >>> add_(1, 2)
    3
    """

    sub_: algebraical = None
    """
    Subtraction operator.

    >>> sub_(3, 2)
    1
    """

    mul_: algebraical = None
    """
    Multiplication operator.

    >>> mul_(2, 3)
    6
    """

    matmul_: algebraical = None
    """
    Alternative multiplication operator.

    >>> class free(tuple):
    ...     def __matmul(self, other):
    ...         return free((self, other))
    >>> isinstance(matmul_(free(), free()), free)
    True
    """

    truediv_: algebraical = None
    """
    Division operator.

    >>> truediv_(4, 2)
    2
    """

    floordiv_: algebraical = None
    """
    Integer division operator.

    >>> floordiv_(3, 2)
    1
    """

    mod_: algebraical = None
    """
    Modulus operator.

    >>> mod_(7, 4)
    3
    """

    pow_: algebraical = None
    """
    Exponentiation operator.

    >>> pow_(2, 3)
    8
    """

# All operators as named class constants.
algebraical.pos_ = algebraical(operator.pos, 'pos')
algebraical.neg_ = algebraical(operator.neg, 'neg')
algebraical.abs_ = algebraical(operator.abs, 'abs')
algebraical.add_ = algebraical(operator.add, 'add')
algebraical.sub_ = algebraical(operator.add, 'sub')
algebraical.mul_ = algebraical(operator.mul, 'mul')
algebraical.matmul_ = algebraical(operator.matmul, 'matmul')
algebraical.truediv_ = algebraical(operator.truediv, 'truediv')
algebraical.floordiv_ = algebraical(operator.floordiv, 'floordiv')
algebraical.mod_ = algebraical(operator.mod, 'mod')
algebraical.pow_ = algebraical(operator.pow, 'pow')

# All operators as top-level constants.
pos_: algebraical = algebraical.pos_
neg_: algebraical = algebraical.neg_
abs_: algebraical = algebraical.abs_
add_: algebraical = algebraical.add_
sub_: algebraical = algebraical.sub_
mul_: algebraical = algebraical.mul_
matmul_: algebraical = algebraical.matmul_
truediv_: algebraical = algebraical.truediv_
floordiv_: algebraical = algebraical.floordiv_
mod_: algebraical = algebraical.mod_
pow_: algebraical = algebraical.pow_

# Operator names.
algebraical.names: dict = {
    algebraical.pos_: 'pos',
    algebraical.neg_: 'neg',
    algebraical.abs_: 'abs',
    algebraical.add_: 'add',
    algebraical.sub_: 'sub',
    algebraical.mul_: 'mul',
    algebraical.matmul_: 'matmul',
    algebraical.truediv_: 'truediv',
    algebraical.floordiv_: 'floordiv',
    algebraical.mod_: 'mod',
    algebraical.pow_: 'pow'
}

# Operator arities.
algebraical.arities: dict = {
    algebraical.pos_: 1,
    algebraical.neg_: 1,
    algebraical.abs_: 1,
    algebraical.add_: 2,
    algebraical.sub_: 2,
    algebraical.mul_: 2,
    algebraical.matmul_: 2,
    algebraical.truediv_: 2,
    algebraical.floordiv_: 2,
    algebraical.mod_: 2,
    algebraical.pow_: 2
}

if __name__ == '__main__':
    doctest.testmod() # pragma: no cover
