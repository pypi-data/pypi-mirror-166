from typing import Union

import numpy as np

from pymbse.optim.design_variable.DesignVariableBase import DesignVariableBase


class GeneticDesignVariable(DesignVariableBase):
    def __init__(self,
                 xl: Union[int, float],
                 xu: Union[int, float],
                 variable: str,
                 variable_type: str,
                 bits: int,
                 _gene=None,
                 _value=None) -> None:

        super().__init__(xl=xl, xu=xu, variable=variable, variable_type=variable_type)
        self.bits = bits
        self._gene = _gene if _gene is not None else [0] * self.bits
        self._value = _value

    def __repr__(self):
        return f"GeneticDesignVariable(xl={self.xl}, xu={self.xu}, variable={self.variable}, " \
               f"variable_type={self.variable_type}, bits={self.bits})"

    def generate_random_gene(self) -> None:
        """ Method generating a random gene for int and float design variables

        :return:
        """
        gene = [int(el) for el in np.random.randint(0, 2, self.bits)]
        if self.variable_type == 'float':
            self._gene = gene
        elif self.variable_type == 'int':
            randint = np.random.randint(self.xl, self.xu + 1) - self.xl
            self._gene = self.convert_int_to_gene(randint, self.bits)
        else:
            raise AttributeError('The variable type should be either int or float, got %s.' % self.variable_type)

    @property
    def value(self) -> Union[int, float]:
        """ Method converting a gene to design variable value (either int or float):
        - for int, the value is given as lower limit + gene integer value; in case of an overflow, the upper limit is
        considered
        - for float, the value is given as the lower limit + gene integer value multiplied by variable range and divided
        by the number of binary combinations

        :return: numeric value of a gene
        """
        gene_int = GeneticDesignVariable.convert_gene_to_int(self._gene)

        # convert to value
        if self.variable_type == 'float':
            return self.xl + gene_int * (self.xu - self.xl) / (2 ** self.bits)
        elif self.variable_type == 'int':
            return min(int(self.xl + gene_int), int(self.xu))
        else:
            raise AttributeError('The variable type should be either int or float, got %s.' % self.variable_type)

    @value.setter
    def value(self, value):
        raise NotImplementedError('The value is only set by changing the gene bitstring!')

    @property
    def gene(self):
        return self._gene

    @gene.setter
    def gene(self, gene):
        if self.variable_type == 'float':
            self._gene = gene
        elif self.variable_type == 'int':
            self._gene = self._correct_int_gene_overflow(gene)
        else:
            raise AttributeError('The variable type should be either int or float, got %s.' % self.variable_type)

    def _correct_int_gene_overflow(self, gene: list) -> list:
        gene_int = GeneticDesignVariable.convert_gene_to_int(gene)
        if gene_int > (self.xu - self.xl):
            return GeneticDesignVariable.convert_int_to_gene(self.xu - self.xl, self.bits)
        else:
            return gene

    @staticmethod
    def convert_gene_to_int(gene: list) -> int:
        """ Static method converting a gene as a list into an integer

        :param gene: a list of bits representing a gene
        :return: an integer value of a gene
        """
        # convert chromosome to a string of chars
        gene_chars = ''.join([str(s) for s in gene])

        # convert string to integer
        return int(gene_chars, 2)

    @staticmethod
    def convert_int_to_gene(n: int, nbits: int) -> list:
        """ Static method converting an integer to a gene

        :param n: an integer value of a gene
        :param nbits: number of bits in binary representation
        :return: a list of bits representing a gene
        """
        bitstring = [n >> i & 1 for i in range(n.bit_length() - 1, -1, -1)]
        if len(bitstring) < nbits:
            bitstring = [0] * (nbits - len(bitstring)) + bitstring

        return bitstring
