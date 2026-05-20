import sensor
import game
import random
import math
import json
import parameters as p


class Level():

    def __init__(self, number_of_neurons: int, input_count: int, output_count: int):
        self.number_of_neurons = number_of_neurons
        self.output_count = output_count
        self.input_count = input_count
        #### [[w1n1, w2n1m ...], [w1n2, w2n2, ...]]
        self.weights = [[0 for self_neuron in range(input_count)] for input_neuron in range(number_of_neurons)]
        ### [b1, b2, ...]
        self.bias = [0 for neuron in range(number_of_neurons)]

    def randomize(self):
        """
        Randomizes every weight and bias
        """

        for neuron in range(len(self.weights)):
            for index in range(len(self.weights[neuron])):
                self.weights[neuron][index] = random.random()*2 - 1

        for bias in range(len(self.bias)):
            self.bias[bias] = random.random()*2 - 1
    
    def mutate(self, amount: float):
        """
        Randomizes every weight and bias by an amount
        
        :param self: Description
        :param amount: How much the previous weight gets close to a new random value
        :type amount: float
        """

        for neuron in range(len(self.weights)):
            for index in range(len(self.weights[neuron])):
                new_value = random.random()*2 - 1
                prev_value = self.weights[neuron][index]
                self.weights[neuron][index] = prev_value + (new_value - prev_value) * amount

        for bias in range(len(self.bias)):
            new_value = random.random()*2 - 1
            prev_value = self.bias[bias]
            self.bias[bias] = prev_value + (new_value - prev_value) * amount

    def send(self, inputs: list[float]):
        
        output = [bias for bias in self.bias]

        for neuron_index, neuron in enumerate(self.weights):
            for w_index, weight in enumerate(neuron):
                output[neuron_index] += inputs[w_index] * weight
        
        for index in range(len(output)):
            if output[index] <= 0:
                output[index] = -1
            else:
                output[index] = 1
        
        return output

    

class Brain():

    def __init__(self, sensor: sensor.Sensor, 
                 paddle: game.Paddle, 
                 ball: game.Ball,
                 number_of_levels: int, 
                 neurons_per_level: int):
        
        self.sensor = sensor
        self.paddle = paddle
        self.ball = ball
        self.number_of_levels = number_of_levels
        self.neurons_per_level = neurons_per_level
        self.simulation = 0

        self.hits = 0
        self.max_hits_path = ''

        self.create_network()
    
    def create_network(self):

        # Rays + Paddle Position + Ball X position + Ball Y position
        inputs = len(self.sensor.t_values) + 5
        # inputs = 5
        
        self.levels = [Level(self.neurons_per_level, inputs, self.neurons_per_level)]
        for i in range(self.number_of_levels - 1):
            self.levels.append(Level(self.neurons_per_level, self.neurons_per_level, self.neurons_per_level))
        

        for level in self.levels:
            level.randomize()

        self.out = Level(2, self.neurons_per_level, self.neurons_per_level)
        self.out.randomize()


    def randomize(self):
        for level in self.levels:
            level.randomize()
        self.out.randomize()

    def mutate(self):
        amount = p.MUTATE_AMOUNT
        for level in self.levels:
            level.mutate(amount)
        self.out.mutate(amount)

    
    def read(self):

        # Get relative position of the paddle
        paddle_pos = self.paddle.y / p.SCREEN_HEIGHT
        # Get Relative X of the Ball
        ball_x = self.ball.x / p.SCREEN_WIDTH
        # Get Relative Y of the Ball
        ball_y = self.ball.y / p.SCREEN_HEIGHT
        # Get X Speed (1 or -1)
        ball_x_speed = 1 if self.ball.x_speed > 0 else -1
        # Get Y Speed (1 or -1)
        ball_y_speed = 1 if self.ball.y_speed > 0 else -1

        # Insert all into inputs
        inputs = [paddle_pos, ball_x, ball_y, ball_x_speed, ball_y_speed]

        # Insert sensor
        inputs = inputs + self.sensor.t_values

        received = self.levels[0].send(inputs)
        if len(self.levels) > 1:
            for level in self.levels[1:]:
                received = level.send(received)

        # Transform received into a Command
        received = self.out.send(received)

        return received
    

    def new_hits(self, hits):
        if hits > self.hits:
            print("SAVING", hits, "HITS")
            self.hits = hits
            self.max_hits_path = p.NETWORK_FOLDER + f'save_{self.hits}.json'
            self.save_network()
        elif hits < self.hits and not p.GENETIC_TRAIN:
            self.load_network(self.max_hits_path)
        if p.GENETIC_TRAIN:
            self.randomize()
        else:
            self.mutate()

    
    def save_network(self):
        path = p.NETWORK_FOLDER + f'save_{self.hits}.json'
        save = {}
        for level_index, level in enumerate(self.levels):
            save[level_index] = {}
            save[level_index]['weights'] = level.weights
            save[level_index]['bias'] = level.bias
        save['out'] = {}
        save['out']['weights'] = self.out.weights
        save['out']['bias'] = self.out.bias

        save['hits'] = self.hits

        print("Saving", path)
        with open(path, 'w') as file:
            json.dump(save, file, indent=4)

    def load_network(self, path):
        print("Loading", path, "| Simulation:", self.simulation)
        self.simulation += 1

        self.max_hits_path = path

        with open(path, 'r') as file:
            save = json.load(file)

        for i in save:

            if i != 'out' and i != 'hits':
                index = int(i)
                self.levels[index].weights = save[i]['weights']
                self.levels[index].bias = save[i]['bias']
            elif i == 'out':
                self.out.weights = save['out']['weights']
                self.out.bias = save['out']['bias']
            elif i == 'hits':
                self.hits = save['hits']

