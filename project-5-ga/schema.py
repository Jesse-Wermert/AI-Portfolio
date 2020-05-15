import random


class Schema:

    # def __init__(self, genes, fitness):

    def __init__(self, num_bits):
        self.genes = ""
        self.size = num_bits
        self.fitness = 0

    def royal_road(self, other):
        cs = self.order()
        sigma = self.sigma_s_of_x(other)
        self.fitness += cs * sigma
        # self.fitness += fitness

    def num_ones(self):
        s_copy = list(self.genes)
        num_ones = 0
        for x in s_copy:
            if x == "1":
                num_ones += 1
        return num_ones

    def num_zeros(self):
        s_copy = list(self.genes)
        num_zeros = 0
        for x in s_copy:
            if x == "0":
                num_zeros += 1
        return num_zeros

    def order(self):
        order = 0
        for x in range(len(self.genes)):
            if self.genes[x] != "*":
                order += 1
        return order

    def def_length(self):
        schema_copy = list(self.genes)
        return self.get_last_fixed_ind(schema_copy) - self.get_first_fixed_ind(schema_copy)

    def get_first_fixed_ind(self, a_list):
        if a_list[0] != "*":
            return 0
        else:
            for x in range(len(a_list)):
                if a_list[x] != "*":
                    return x

    def get_last_fixed_ind(self, a_list):
        if a_list[-1] != "*":
            return len(self.genes) - 1
        else:
            size = len(self.genes) - 1
            ind = size
            for x in range(len(a_list)):
                if a_list[ind] != "*":
                    return ind + 1
                else:
                    ind -= 1

    def rand_schema_population(self, pop_size):
        pop = []
        for i in range(pop_size):
            self.gen_random_schema()
            pop.append(self.genes)
        return pop

    def gen_random_schema(self):
        l = []
        symbols = ["0", "1", "*"]
        for i in range(0, self.size):
            l.append(random.choice(symbols))
        self.genes = ''.join(l)

    def gen_rand_bits_only(self):
        l = []
        for i in range(0, self.size):
            l.append(str(random.randint(0, 1)))
        self.genes = ''.join(l)

    def convert_str_2_int(self):
        v = int(self.genes)
        return v

    def phenotype(self):
        x = self.convert_str_2_int()
        binary = x
        decimal, i, n = 0, 0, 0
        while binary != 0:
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary // 10
            i += 1
        return decimal

    def set_schema(self, schema):
        self.genes = schema

    def __str__(self):
        return self.genes

    def sigma_s_of_x(self, other):
        copy = list(self.genes)
        # other = Schema(other)
        other_copy = list(other.genes)
        for i in range(len(copy)):
            if other_copy[i] == "*" and copy[i] == "0" or copy[i] == "1":
                pass
            if other_copy[i] == "0" and copy[i] != "0":
                return 0
            if other_copy[i] == "1" and copy[i] != "1":
                return 0
        return 1

    def get_list_of_schemas(self):
        return ["11111111********************************************************",
                "********11111111************************************************",
                "****************11111111****************************************",
                "************************11111111********************************",
                "********************************11111111************************",
                "****************************************11111111****************",
                "************************************************11111111********",
                "********************************************************11111111",
                "1111111111111111************************************************",
                "****************1111111111111111********************************",
                "********************************1111111111111111****************",
                "************************************************1111111111111111",
                "11111111111111111111111111111111********************************",
                "********************************11111111111111111111111111111111",
                "1111111111111111111111111111111111111111111111111111111111111111"]

    def get_genes(self):
        return self.genes


s1 = "11111111********************************************************"
s2 = "********11111111************************************************"
s3 = "****************11111111****************************************"
s4 = "************************11111111********************************"
s5 = "********************************11111111************************"
s6 = "****************************************11111111****************"
s7 = "************************************************11111111********"
s8 = "********************************************************11111111"
s9 = "1111111111111111************************************************"
s10 = "****************1111111111111111********************************"
s11 = "********************************1111111111111111****************"
s12 = "************************************************1111111111111111"
s13 = "11111111111111111111111111111111********************************"
s14 = "********************************11111111111111111111111111111111"
s15 = "1111111111111111111111111111111111111111111111111111111111111111"
# schema = Schema(64)
# schema.gen_random_schema()
# print(schema.__str__())

"""
schema1 = Schema(64)
schema1.set_schema(s1)
print("c1:" + str(schema1.order()))
# print(schema1.__str__())
# schema1.instances()
# print(schema1.__str__())
schema2 = Schema(64)
schema2.set_schema(s2)
print("c2:" + str(schema2.order()))
schema3 = Schema(64)
schema3.set_schema(s3)
print("c3:" + str(schema3.order()))
schema4 = Schema(64)
schema4.set_schema(s4)
print("c4:" + str(schema4.order()))
schema5 = Schema(64)
schema5.set_schema(s5)
print("c5:" + str(schema5.order()))
schema6 = Schema(64)
schema6.set_schema(s6)
print("c6:" + str(schema6.order()))
schema7 = Schema(64)
schema7.set_schema(s7)
print("c7:" + str(schema7.order()))
schema8 = Schema(64)
schema8.set_schema(s8)
print("c8:" + str(schema8.order()))
schema9 = Schema(64)
schema9.set_schema(s9)
print("c9:" + str(schema9.order()))
schema10 = Schema(64)
schema10.set_schema(s10)
print("c10:" + str(schema10.order()))
schema11 = Schema(64)
schema11.set_schema(s11)
print("c11:" + str(schema11.order()))
schema12 = Schema(64)
schema12.set_schema(s12)
print("c12:" + str(schema12.order()))
schema13 = Schema(64)
schema13.set_schema(s13)
print("c13:" + str(schema13.order()))
schema14 = Schema(64)
schema14.set_schema(s14)
print("c14:" + str(schema14.order()))
schema15 = Schema(64)
schema15.set_schema(s15)
print("c15:" + str(schema15.order()))
basic = Schema(4)
basic.set_schema("0*1*")
i1 = Schema(4)
i2 = Schema(4)
i3 = Schema(4)
i4 = Schema(4)
n1 = Schema(4)
n2 = Schema(4)
n3 = Schema(4)
n1.set_schema("1010")
n2.set_schema("0000")
n3.set_schema("1111")
i1.set_schema("0010")
i2.set_schema("0011")
i3.set_schema("0110")
i4.set_schema("0111")
print(i1.sigma_s_of_x(basic))
print(basic.sigma_s_of_x(i2))
print(basic.sigma_s_of_x(i3))
print(basic.sigma_s_of_x(i4))
print(basic.sigma_s_of_x(n1))
print(basic.sigma_s_of_x(n2))
print(basic.sigma_s_of_x(n3))
"""
