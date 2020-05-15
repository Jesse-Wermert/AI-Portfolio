import random
import string

targetLength = 64
class Chromosome:

    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness

    def genes_as_list(self):
        return list(self.Genes)

    def get_genes(self):
        return self.Genes

    @staticmethod
    def get_new_random_genes():
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(targetLength))

    def __str__(self):
        return self.Genes


class RoyalRoadsGA(Chromosome):
    """
    Class for RR GA and RR GA w/o intermediate levels.
    """
    def __init__(self, length, population_size, crossover_rate, mutation_rate, with_intermediate_levels, genes,
                 fitness):
        # super().__init__(genes=None, fitness=None)
        self.bitstring_size = length
        self.pop_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.intermediate_levels = with_intermediate_levels
        self.population = []
        self.building_blocks = ["11111111********************************************************",
                                "********11111111************************************************",
                                "****************11111111****************************************",
                                "************************11111111********************************",
                                "********************************11111111************************",
                                "****************************************11111111****************",
                                "************************************************11111111********",
                                "********************************************************11111111"]

    def random_bitstring(self):
        genes = []
        for x in range(self.bitstring_size):
            genes.append(str(random.randint(0, 1)))
        return Chromosome(genes, fitness=0)

    def create_population(self):
        # global ideal
        for x in range(self.pop_size):
            self.population.append(self.random_bitstring())

    def building_instances(self, chromosome):
        num_instances = 0
        for block in self.building_blocks:
            block_copy = list(block)
            chromosome_copy = chromosome.genes_as_list()
            diff = 0
            for x in range(self.bitstring_size):
                if block_copy[x] == "1" and chromosome_copy[x] != "1":
                    diff += 1
            if diff == 0:
                num_instances += 1
        return num_instances

    def rr_fitness(self):
        scores = []
        for chromosome in self.population:

            scores.append(self.building_instances(chromosome))
        return scores

    def run(self):
        pass
        # create the population
        # self.create_population()
        # determine fitness



l = 64
p = 128
x = 0.7
m = 0.005
levels = True
ga = RoyalRoadsGA(l, p, x, m, levels)
ga.create_population()
print(ga.population)
print(len(ga.population))



