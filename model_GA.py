import numpy as np
import random
import yaml
import matplotlib.pyplot as plt

class ModelGA:
    def __init__(self):

        with open("inputs.yaml", "r") as file:
            inputs = yaml.safe_load(file)
            self.budget = inputs["budget"]
            self.max_generations = inputs["max_gens"]
            self.population_size = inputs["pop_size"]
            self.tournament_size = inputs["tournament_size"]
            self.crossover_prob = inputs["crossover"]
            self.mutation_prob = inputs["mutation"]

        self.drivers = [
            {'team':'Red Bull','name': 'Max Verstappen',
                'qualifying_position': np.nanmean([1,15]),
                'race_position': np.nanmean([1,2]),
                'curr_week_fp_pos': np.nanmean([1,1,1]),
                'price': np.nanmean(27)},
            {'team':'Red Bull','name': 'Sergio Perez',
                'qualifying_position': np.nanmean([2,1]),
                'race_position': np.nanmean([2,1]),
                'curr_week_fp_pos': np.nanmean([2,3,2]),
                'price': np.nanmean(18.1)},
            {'team':'Aston Martin','name': 'Fernando Alonso',
                'qualifying_position': np.nanmean([5,2]),
                'race_position': np.nanmean([3,3]),
                'curr_week_fp_pos': np.nanmean([3,2,3]),
                'price': np.nanmean(8.5)},
            {'team':'Aston Martin','name': 'Lance Stroll',
                'qualifying_position': np.nanmean([8,5]),
                'race_position': np.nanmean([6,20]),
                'curr_week_fp_pos': np.nanmean([4,7,4]),
                'price': np.nanmean(7.6)},
            {'team':'Mercedes','name': 'George Russell',
                'qualifying_position': np.nanmean([6,3]),
                'race_position': np.nanmean([7,4]),
                'curr_week_fp_pos': np.nanmean([5,5,11]),
                'price': np.nanmean(18.6)},
            {'team':'Mercedes','name': 'Lewis Hamilton',
                'qualifying_position': np.nanmean([7,7]),
                'race_position': np.nanmean([5,5]),
                'curr_week_fp_pos': np.nanmean([6,11,5]),
                'price': np.nanmean(23.7)},
            {'team':'Ferrari','name': 'Charles Leclerc',
                'qualifying_position': np.nanmean([3,12]),
                'race_position': np.nanmean([19,7]),
                'curr_week_fp_pos': np.nanmean([11,9,6]),
                'price': np.nanmean(21.1)},
            {'team':'Ferrari','name': 'Carlos Sainz',
                'qualifying_position': np.nanmean([4,4]),
                'race_position': np.nanmean([4,6]),
                'curr_week_fp_pos': np.nanmean([7,10,10]),
                'price': np.nanmean(17.2)},
            {'team':'Alpine','name': 'Pierre Gasly',
                'qualifying_position': np.nanmean([20,9]),
                'race_position': np.nanmean([9,9]),
                'curr_week_fp_pos': np.nanmean([8,6,9]),
                'price': np.nanmean(8.2)},
            {'team':'Alpine','name': 'Esteban Ocon',
                'qualifying_position': np.nanmean([9,6]),
                'race_position': np.nanmean([18,8]),
                'curr_week_fp_pos': np.nanmean([12,4,14]),
                'price': np.nanmean(9.3)},
            {'team':'Haas','name': 'Nico Hulkenburg',
                'qualifying_position': np.nanmean([10,10]),
                'race_position': np.nanmean([15,12]),
                'curr_week_fp_pos': np.nanmean([15,27,13]),
                'price': np.nanmean(4.2)},
            {'team':'Haas','name': 'Kevin Magnessun',
                'qualifying_position': np.nanmean([17,13]),
                'race_position': np.nanmean([13,10]),
                'curr_week_fp_pos': np.nanmean([16,15,17]),
                'price': np.nanmean(6.7)},
            {'team':'Alfa Romeo','name': 'Valteri Bottas',
                'qualifying_position': np.nanmean([12,14]),
                'race_position': np.nanmean([8,19]),
                'curr_week_fp_pos': np.nanmean([18,20,18]),
                'price': np.nanmean(7.8)},
            {'team':'Alfa Romeo','name': 'Guanyu Zhou',
                'qualifying_position': np.nanmean([13,11]),
                'race_position': np.nanmean([16,13]),
                'curr_week_fp_pos': np.nanmean([19,16,12]),
                'price': np.nanmean(4.9)},
            {'team':'Mclaren','name': 'Lando Norris',
                'qualifying_position': np.nanmean([11,19]),
                'race_position': np.nanmean([17,17]),
                'curr_week_fp_pos': np.nanmean([20,12,7]),
                'price': np.nanmean(11.1)},
            {'team':'Mclaren','name': 'Oscar Pisatri',
                'qualifying_position': np.nanmean([18,8]),
                'race_position': np.nanmean([20,15]),
                'curr_week_fp_pos': np.nanmean([14,19,8]),
                'price': np.nanmean(6.9)},
            {'team':'AlphaTauri','name': 'Nyck de Vries',
                'qualifying_position': np.nanmean([19,18]),
                'race_position': np.nanmean([14,14]),
                'curr_week_fp_pos': np.nanmean([13,17,20]),
                'price': np.nanmean(5.0)},
            {'team':'AlphaTauri','name': 'Yuki Tsunoda',
                'qualifying_position': np.nanmean([14,16]),
                'race_position': np.nanmean([11,11]),
                'curr_week_fp_pos': np.nanmean([10,13,19]),
                'price': np.nanmean(4.8)},
            {'team':'Williams','name': 'Alex Albon',
                'qualifying_position': np.nanmean([15,17]),
                'race_position': np.nanmean([10,19]),
                'curr_week_fp_pos': np.nanmean([9,14,15]),
                'price': np.nanmean(5.5)},
            {'team':'Williams','name': 'Logan Sargeant',
                'qualifying_position': np.nanmean([16,20]),
                'race_position': np.nanmean([12,15]),
                'curr_week_fp_pos': np.nanmean([17,18,16]),
                'price': np.nanmean(4.0)}
            ]

        self.constructors = [
            {'name': 'Red Bull',
                'qualifying_position': 2,
                'race_position': 1,
                'curr_week_fp_pos': 3,
                'price': np.nanmean(27.3)},
            {'name': 'Aston Martin',
                'qualifying_position': 2,
                'race_position': 1,
                'curr_week_fp_pos': 3,
                'price': np.nanmean(6.8)},
            {'name': 'Mercedes',
                'qualifying_position': 1,
                'race_position': 2,
                'curr_week_fp_pos': 3,
                'price': np.nanmean(25.1)},
            {'name': 'Ferrari',
                'qualifying_position': 2,
                'race_position': 1,
                'curr_week_fp_pos': 3,
                'price': np.nanmean(22.1)},
            {'name': 'Alpine',
                'qualifying_position': 2,
                'race_position': 1,
                'curr_week_fp_pos': 3,
                'price': np.nanmean(10.0)},
            {'name': 'Alfa Romeo',
                'qualifying_position': 2,
                'race_position': 1,
                'curr_week_fp_pos': 3,
                'price': np.nanmean(6.2)},
            {'name': 'AlphaTauri',
                'qualifying_position': 2,
                'race_position': 1,
                'curr_week_fp_pos': 3,
                'price': np.nanmean(6.3)},
            {'name': 'Williams',
                'qualifying_position': 2,
                'race_position': 1,
                'curr_week_fp_pos': 3,
                'price': np.nanmean(5.1)},
            {'name': 'Mclaren',
                'qualifying_position': 2,
                'race_position': 1,
                'curr_week_fp_pos': 3,
                'price': np.nanmean(9.0)},
            {'name': 'Haas',
                'qualifying_position': 2,
                'race_position': 1,
                'curr_week_fp_pos': 3,
                'price': np.nanmean(5.3)},
            ]
    
        for team in self.constructors:
            race = 0; quali = 0; fp_pos = 0
            for driver in self.drivers:
                if driver['team'] == team['name']:
                    race += driver['race_position']
                    quali += driver['qualifying_position']
                    fp_pos += driver['curr_week_fp_pos']
            team['race_position'] = int(race/2)
            team['qualifying_position'] = int(quali/2)
            team['curr_week_fp_pos'] = int(fp_pos/2)
            # print(f"Updated Teams: {team}")

    def initialize_population(self):
        """
        Initialize a population of teams for the genetic algorithm.

        Args:
        - num_teams (int): the size of the population
        - drivers (dict): a dictionary containing information about the drivers
        - constructors (dict): a dictionary containing information about the constructors
        - budget (float): the maximum budget for a team

        Returns:
        - population (list): a list of teams, where each team is a dictionary containing
                            information about the drivers, constructors, and total cost
        """
        self.population = []

        while len(self.population) < self.population_size:
            drivers_selected = []
            constructors_selected = []
            # randomly select 5 unique drivers
            while len(drivers_selected) < 5:
                driver = random.choice(self.driver_names)
                if driver not in drivers_selected:
                    drivers_selected.append(driver)

            # randomly select 2 unique constructors
            while len(constructors_selected) < 2:
                constructor = random.choice(self.constructor_names)
                if constructor not in constructors_selected:
                    constructors_selected.append(constructor)
            # print(drivers_selected,constructors_selected)
            drivers_indx = [self.driver_names.index(driver) for driver in drivers_selected]
            constructors_indx = [self.constructor_names.index(constructor) for constructor in constructors_selected]
            # calculate the total cost of the team
            total_cost = sum([self.drivers[index_d]['price'] for index_d in drivers_indx] +
                            [self.constructors[index_c]['price'] for index_c in constructors_indx])

            # if the team is within the budget, add it to the population
            if total_cost <= self.budget:
                team = {'drivers': drivers_selected,
                        'constructors': constructors_selected,
                        'total_cost': total_cost}
                self.population.append(team)

    def fitness_function(self, team):
        # Calculate average qualifying, race positions, and free practice positions for the team
        
        drivers_indx = [self.driver_names.index(driver) for driver in team['drivers']]
        constructors_indx = [self.constructor_names.index(constructor) for constructor in team['constructors']]
            
        driver_qual = [self.drivers[d]['qualifying_position'] for d in drivers_indx]
        constructor_qual = [self.constructors[c]['qualifying_position'] for c in constructors_indx]
        driver_race = [self.drivers[d]['race_position'] for d in drivers_indx]
        constructor_race = [self.constructors[c]['race_position'] for c in constructors_indx]
        driver_fp = [self.drivers[d]['curr_week_fp_pos'] for d in drivers_indx]
        constructor_fp = [self.constructors[c]['curr_week_fp_pos'] for c in constructors_indx]
        
        # Calculate the average positions for drivers and constructors
        avg_driver_qual = sum(driver_qual) / len(driver_qual)
        avg_constructor_qual = sum(constructor_qual) / len(constructor_qual)
        avg_driver_race = sum(driver_race) / len(driver_race)
        avg_constructor_race = sum(constructor_race) / len(constructor_race)
        avg_driver_fp = sum(driver_fp) / len(driver_fp)
        avg_constructor_fp = sum(constructor_fp) / len(constructor_fp)
        # print(avg_driver_qual,avg_driver_race)
        # print(avg_constructor_qual,avg_constructor_race)
    
        # # Calculate the fitness score using the specified formula
        fitness_score = (avg_driver_qual + avg_constructor_qual + avg_driver_race + avg_constructor_race + avg_driver_fp + avg_constructor_fp) * team['total_cost']
        # print(fitness_score)
        # input()
        
        return fitness_score

    def tournament_selection(self,fitness_vals):
        # Randomly select individuals from the population to participate in the tournament
        participants = random.sample(range(len(self.population)), self.tournament_size)
        # Determine the fitness values of the participants
        participant_fitness = [fitness_vals[i] for i in participants]
        # Find the index of the participant with the best fitness value
        best_index = participants[participant_fitness.index(max(participant_fitness))]
        # Return the best individual from the tournament
        return self.population[best_index]

    def one_point_crossover(self):
        # choose a random index to split the parents
        split_index = random.randint(1, len(self.parent1) - 1)

        parent1 = self.parent1['drivers'] + self.parent1['constructors']
        parent2 = self.parent2['drivers'] + self.parent2['constructors']
        
        # create child by combining the first half of parent1 and second half of parent2

        child1 = parent1[:split_index] + parent2[split_index:]
        child2 = parent2[:split_index] + parent1[split_index:]

        drivers_indx1 = [self.driver_names.index(driver) for driver in child1[0:5]]
        constructors_indx1 = [self.constructor_names.index(constructor) for constructor in child1[5:]]
        
        drivers_indx2 = [self.driver_names.index(driver) for driver in child2[0:5]]
        constructors_indx2 = [self.constructor_names.index(constructor) for constructor in child2[5:]]

        # calculate the total cost of the team
        total_cost1 = sum([self.drivers[index_d]['price'] for index_d in drivers_indx1] +
                        [self.constructors[index_c]['price'] for index_c in constructors_indx1])
        
        
        total_cost2 = sum([self.drivers[index_d]['price'] for index_d in drivers_indx2] +
                        [self.constructors[index_c]['price'] for index_c in constructors_indx2])
        
        if ((total_cost1 or total_cost2) >= self.budget):
            self.child1 = self.parent1
            self.child2 = self.parent2
        else:
            self.child1 = {'drivers':child1[0:5],'constructors':child1[5:],'total_cost':total_cost1}
            self.child2 = {'drivers':child2[0:5],'constructors':child2[5:],'total_cost':total_cost2}
            if ((len(set(self.child1['drivers'])) or len(set(self.child2['drivers'])) != 5)) or (len(set(self.child1['constructors'])) or len(set(self.child2['constructors'])) != 2):
                self.child1 = self.parent1
                self.child2 = self.parent2
    
    def mutation(self,child,mut_rate):
        child_gen = False
        while (child_gen == False):
            if random.random() < mut_rate:
                if random.random() < 0.8:
                    popped = child['drivers'].pop(random.randint(0,4))
                    while len(child['drivers']) < 5:
                        driver = random.choice(self.driver_names)
                        if driver not in (child['drivers'] or popped):
                            child['drivers'].append(driver)
                else:
                    popped = child['constructors'].pop(random.randint(0,1))
                    while len(child['constructors']) < 2:
                        constructor = random.choice(self.constructor_names)
                        if constructor not in (child['constructors'] or popped):
                            child['constructors'].append(constructor)
                drivers_indx1 = [self.driver_names.index(driver) for driver in child['drivers']]
                constructors_indx1 = [self.constructor_names.index(constructor) for constructor in child['constructors']]
                total_cost = sum([self.drivers[index_d]['price'] for index_d in drivers_indx1] +
                            [self.constructors[index_c]['price'] for index_c in constructors_indx1])
                if(total_cost > self.budget):
                    child_gen = False
                else:
                    child_gen = True
                    child['total_cost'] = total_cost
        return child

    # main genetic algorithm function
    def genetic_algorithm(self):
        self.driver_names = [self.drivers[ii]['name'] for ii in range(0,len(self.drivers))]
        self.constructor_names = [self.constructors[ii]['name'] for ii in range(0,len(self.constructors))]
        self.num_drivers = len(self.driver_names)
        self.num_constructors = len(self.constructor_names)
        self.initialize_population()
        fitnesses = [self.fitness_function(individual) for individual in self.population]
        best_individual = self.population[fitnesses.index(min(fitnesses))]
        self.best_team_attr = {}
        for generation in range(self.max_generations):
            print(f"Generation: {generation}")
            next_population = []
            for i in range(self.population_size):
                self.parent1 = self.tournament_selection(fitnesses)
                self.parent2 = self.tournament_selection(fitnesses)
                if random.random() < self.crossover_prob:
                    self.one_point_crossover()
                else:
                    self.child1, self.child2 = self.parent1, self.parent2
                child1 = self.mutation(self.child1, self.mutation_prob)
                child2 = self.mutation(self.child2, self.mutation_prob)
                next_population.append(child1)
                next_population.append(child2)
            population = next_population
            self.fitnesses = [self.fitness_function(individual) for individual in population]
            best_fitness = min(self.fitnesses)
            best_individual = population[self.fitnesses.index(best_fitness)]
            self.best_team_attr[best_fitness] = best_individual
        # print(self.best_team_attr[min(self.best_team_attr.keys())])
        self.plot_fitness()

    def plot_fitness(self):
        plt.figure(1)
        plt.plot(list(self.best_team_attr.keys()))
        plt.show()

if __name__ == '__main__':
    GA = ModelGA()
    GA.genetic_algorithm()