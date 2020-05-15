from schema import Schema
import genetic


class Hillclimber(Schema):

    def __init__(self, length, population_size, crossover_rate, mutation_rate):
        self.bitstring_size = length
        self.pop_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population = []
        self.s = Schema(self.bitstring_size)

    def initialize_population(self):
        for v in range(self.pop_size):
            self.s.gen_random_schema()
            schema = self.s.get_schema()
            self.population.append(schema)