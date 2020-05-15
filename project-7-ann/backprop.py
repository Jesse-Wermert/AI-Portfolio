import random
import string
import math


"""
Complete this implementation of backpropagation learning for
feedforward networks.
"""


# ------------------------------------------------------------------------------


def pretty(values):
    return ' '.join(['%.3f' % v for v in values])


# ------------------------------------------------------------------------------


class Unit:
    """
    A Unit object represents a node in a network.  It keeps track of
    the node's current activation value (between 0.0 and 1.0), as well
    as all of the connections from other units into this unit, and all
    of the connections from this unit to other units in the network.
    """

    def __init__(self, activation=0.0):
        assert 0.0 <= activation <= 1.0, 'activation out of range'
        self.activation = activation
        self.incoming_connections = []
        self.outgoing_connections = []
        self.delta = 0

    def sigmoid_function(self, x):
        try:
            x = 1 / (1 + math.exp(-x))
        except:
            x = float('inf')
        return x

    def deriv(self, x):
        try:
            x = 1 * (1.0 - x)
        except:
            x = float('inf')
        return x

    def rectified_linear_unit(self):
        pass


# ----------------------------------------------------------------------------------------------------------------------------------------------------------


class Connection:
    """
    A Connection object represents a connection between two units of a
    network. The connection strength (weight, w) is initialized to a small random
    value. The connection object keeps track of the unit that the connection
    is coming from, as well as the unit that the connection is going to.
    """

    def __init__(self, from_unit, to_unit):
        self.from_unit = from_unit
        self.to_unit = to_unit
        self.randomize()
        self.increment = 0

    def randomize(self):
        self.weight = random.uniform(-0.1, +0.1)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------


class Network:
    """
    A Network object represents a three-layer feedforward network with
    a given number of input, hidden, and output units.
    """

    def __init__(self, num_inputs, num_hiddens, num_outputs):
        # create the units
        self.output_layer = [Unit() for i in range(num_outputs)]
        self.hidden_layer = [Unit() for j in range(num_hiddens)]
        self.input_layer = [Unit() for k in range(num_inputs)]

        # wire up the network
        self.all_connections = []
        self.connect_layers(self.input_layer, self.hidden_layer)
        self.connect_layers(self.hidden_layer, self.output_layer)

        # connect the bias units
        output_bias = Unit(1.0)
        self.connect_to_layer(output_bias, self.output_layer)
        hidden_bias = Unit(1.0)
        self.connect_to_layer(hidden_bias, self.hidden_layer)

        # set the learning parameters
        self.learning_rate = 0.3
        self.tolerance = 0.25
        self.num_units = num_hiddens + num_inputs + num_outputs

    def connect(self, from_unit, to_unit):
        c = Connection(from_unit, to_unit)
        from_unit.outgoing_connections.append(c)
        to_unit.incoming_connections.append(c)
        self.all_connections.append(c)

    def connect_to_layer(self, unit, layer):
        for other_unit in layer:
            self.connect(unit, other_unit)

    def connect_layers(self, from_layer, to_layer):
        for unit in from_layer:
            self.connect_to_layer(unit, to_layer)

    def test(self):
        print('weights =', pretty([c.weight for c in self.all_connections]))
        for pattern in self.inputs:
            output = pretty(self.propagate(pattern))
            hidden_rep = pretty([h.activation for h in self.hidden_layer])
            print('%s -> [%s] -> output %s' % (pattern, hidden_rep, output))
        print()

    def propagate(self, pattern):
        """
        This method takes an input pattern, represented as a list of
        floating-point values, propagates the pattern through the
        network, and returns the resulting output pattern as a list of
        floating-point values.  This method should update the
        activation values of all input, hidden, and output units in
        the network as a side effect.

        It ensures that given pattern is the appropriate length and
        that the values are in the range 0-1.
        """
        # Input layer
        for i in range(len(self.input_layer)):
            self.input_layer[i].activation = pattern[i]
        # Hidden layer
        for h in self.hidden_layer:
            bias = h.incoming_connections[-1].from_unit.activation
            bias_weight = h.incoming_connections[-1].weight  # this line is the line that was added
            weighted_sum = 0
            for i in range(len(h.incoming_connections) - 1):
                weighted_sum += pattern[i] * h.incoming_connections[i].weight
            h.activation = h.sigmoid_function(weighted_sum + (bias * bias_weight))
        # Output layer
        outputs = []
        for o in self.output_layer:
            bias = o.incoming_connections[-1].from_unit.activation
            bias_weight = o.incoming_connections[-1].weight  # this is the line that was also added
            weighted_sum = 0
            for j in range(len(o.incoming_connections) - 1):  # for the number of hiddens (i.e., num_hiddens = 3 for XOR)
                weighted_sum += o.incoming_connections[j].weight * \
                                o.incoming_connections[j].from_unit.activation
            o.activation = o.sigmoid_function(weighted_sum +
                                              (bias * bias_weight))
            outputs.append(o.activation)
        return outputs

    def compute_error(self):
        """
        This method evaluates the network's performance on the
        patterns stored in self.inputs with answers stored in
        self.targets, returning a tuple of the form

        (correct, total, score, error)

        where total is the total number of individual values in the
        target patterns, correct is the number of these that the
        network got right (to within self.tolerance), score is the
        percentage (0-100) of correct values, and error is the total
        sum squared error across all values.
        """
        total = len(self.targets) * len(self.targets[0])
        correct = 0
        # total_error = 0.0
        output_activation_vals = [self.output_layer[x].activation for x in range(len(self.output_layer))]
        error = []
        for x in range(len(self.targets)):
            for y in range(len(self.targets[0])):
                self.propagate(self.inputs[x])
                if self.targets[x][y] == 0:
                    # total_error += (self.targets[x][y] - output_activation_vals[y])**2
                    error.append((self.targets[x][y] - output_activation_vals[y]) ** 2)
                    temp = output_activation_vals[y] - self.tolerance
                    if temp <= 0:
                        correct += 1
                elif self.targets[x][y] == 1:
                    # total_error += (self.targets[x][y] - output_activation_vals[y])**2
                    error.append((self.targets[x][y] - output_activation_vals[y]) ** 2)
                    temp = output_activation_vals[y] + self.tolerance
                    if temp >= 1:
                        correct += 1
        score = (correct/total) * 100
        total_error = sum(error)/total
        return correct, total, score, total_error

    def teach_pattern(self, pattern, target):
        """
        Modifies the weights according to the back-propagation
        learning rule using the given input pattern and associated
        target pattern.

        This method should begin by forward propagating activations.
        Next it should backward propagate error as follows:
        1. Update the deltas associated with every unit in the output layer.
        2. Update the deltas associated with every unit in the hidden layer.
        3. Update the increments associated with every connection in the
           network and then use these to update all weights in the network.
        """
        # Begin by forward propagating activations
        outputs = self.propagate(pattern)
        errors = [target[i] - outputs[i] for i in range(len(target))]
        # Back-propagate errors, update deltas
        for o in range(len(self.output_layer)):
            self.output_layer[o].delta = self.output_layer[o].deriv(self.output_layer[o].activation) * errors[o]
        for _ in reversed(range(len(self.all_connections)-len(self.output_layer))):
            weighted_sum = 0
            for x in range(len(self.all_connections[_].from_unit.outgoing_connections)-1):
                weighted_sum += self.all_connections[_].from_unit.outgoing_connections[x].to_unit.delta * \
                                self.all_connections[_].from_unit.outgoing_connections[x].weight
            self.all_connections[_].from_unit.delta = \
                self.all_connections[_].from_unit.deriv(self.all_connections[_].from_unit.activation) * weighted_sum
        for _ in reversed(range(len(self.all_connections))):
            self.all_connections[_].increment = self.learning_rate * \
                                                 self.all_connections[_].from_unit.activation * \
                                                 self.all_connections[_].to_unit.delta
        for conn in self.all_connections:
            conn.weight += conn.increment

    def teach_dataset(self):
        """
        Performs one learning sweep through the training set. Patterns
        are randomly reordered on each sweep.
        """
        assert len(self.inputs) > 0, 'no training data'
        dataset = list(zip(self.inputs, self.targets))
        random.shuffle(dataset)
        for (pattern, target) in dataset:
            # print '   teaching %s -> %s' % (pattern, target)
            self.teach_pattern(pattern, target)

    def train(self, cycles=2000):
        """
        Trains the network for the given number of training cycles
        (with a default of 10000).  This method repeatedly calls
        teachDataset, displaying the current cycle number and
        performance of the network after each call.
        """
        assert len(self.inputs) > 0, 'no training data'
        (correct, total, score, error) = self.compute_error()
        print('Epoch #    0: TSS error %7.4f, %d/%d correct (%.1f%%)' % (error, correct, total, score))
        for t in range(1, cycles + 1):
            self.teach_dataset()
            (correct, total, score, error) = self.compute_error()
            print('Epoch #%5d: TSS error %7.4f, %d/%d correct (%.1f%%)' % (t, error, correct, total, score))
            if correct == total:
                print('All patterns learned')
                break


# ------------------------------------------------------------------------------
# XOR function

x = Network(2, 3, 1)

x.inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
x.targets = [[0], [1], [1], [0]]

# x.test()
# x.train()
# x.test()

# ------------------------------------------------------------------------------
# auto-association

a = Network(8, 3, 8)

a.inputs = [[1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1]]

a.targets = a.inputs

a.test()
a.train()
a.test()
