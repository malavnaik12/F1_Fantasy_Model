import numpy as np
import pandas as pd
import random

class ModelGA:
    def __init__(self):

        self.drivers = [
            {'team':'Red Bull','name': 'Max Verstappen',
                'qualifying_position': np.nanmean([1,15]),
                'race_position': np.nanmean([1,2]),
                'curr_week_fp_pos': np.nanmean([1,1,1]),
                'price': np.nanmean(27)},
            {'team':'Red Bull','name': 'Sergio Perez',
                'qualifying_position': np.nanmean([2,1]),
                'race_position': np.nanmean([2,1]),
                'curr_week_fp_pos': np.nanmean([2,2,2]),
                'price': np.nanmean(18.1)},
            {'team':'Aston Martin','name': 'Fernando Alonso',
                'qualifying_position': np.nanmean([5,2]),
                'race_position': np.nanmean([3,3]),
                'curr_week_fp_pos': np.nanmean([3,3,3]),
                'price': np.nanmean(8.5)},
            {'team':'Aston Martin','name': 'Lance Stroll',
                'qualifying_position': np.nanmean([8,5]),
                'race_position': np.nanmean([6,20]),
                'curr_week_fp_pos': np.nanmean([4,4,4]),
                'price': np.nanmean(7.6)},
            {'team':'Mercedes','name': 'George Russell',
                'qualifying_position': np.nanmean([6,3]),
                'race_position': np.nanmean([7,4]),
                'curr_week_fp_pos': np.nanmean([5,5,5]),
                'price': np.nanmean(18.6)},
            {'team':'Mercedes','name': 'Lewis Hamilton',
                'qualifying_position': np.nanmean([7,7]),
                'race_position': np.nanmean([5,5]),
                'curr_week_fp_pos': np.nanmean([6,6,6]),
                'price': np.nanmean(23.7)},
            {'team':'Ferrari','name': 'Charles Leclerc',
                'qualifying_position': np.nanmean([3,12]),
                'race_position': np.nanmean([19,7]),
                'curr_week_fp_pos': np.nanmean([7,7,7]),
                'price': np.nanmean(21.1)},
            {'team':'Ferrari','name': 'Carlos Sainz',
                'qualifying_position': np.nanmean([4,4]),
                'race_position': np.nanmean([4,6]),
                'curr_week_fp_pos': np.nanmean([8,8,8]),
                'price': np.nanmean(17.2)},
            {'team':'Alpine','name': 'Pierre Gasly',
                'qualifying_position': np.nanmean([20,9]),
                'race_position': np.nanmean([9,9]),
                'curr_week_fp_pos': np.nanmean([9,9,9]),
                'price': np.nanmean(8.2)},
            {'team':'Alpine','name': 'Esteban Ocon',
                'qualifying_position': np.nanmean([9,6]),
                'race_position': np.nanmean([18,8]),
                'curr_week_fp_pos': np.nanmean([10,10,10]),
                'price': np.nanmean(9.3)},
            {'team':'Haas','name': 'Nico Hulkenburg',
                'qualifying_position': np.nanmean([10,10]),
                'race_position': np.nanmean([15,12]),
                'curr_week_fp_pos': np.nanmean([11,11,11]),
                'price': np.nanmean(4.2)},
            {'team':'Haas','name': 'Kevin Magnessun',
                'qualifying_position': np.nanmean([17,13]),
                'race_position': np.nanmean([13,10]),
                'curr_week_fp_pos': np.nanmean([12,12,12]),
                'price': np.nanmean(6.7)},
            {'team':'Alfa Romeo','name': 'Valteri Bottas',
                'qualifying_position': np.nanmean([12,14]),
                'race_position': np.nanmean([8,19]),
                'curr_week_fp_pos': np.nanmean([13,13,13]),
                'price': np.nanmean(7.8)},
            {'team':'Alfa Romeo','name': 'Guanyu Zhou',
                'qualifying_position': np.nanmean([13,11]),
                'race_position': np.nanmean([16,13]),
                'curr_week_fp_pos': np.nanmean([14,14,14]),
                'price': np.nanmean(4.9)},
            {'team':'Mclaren','name': 'Lando Norris',
                'qualifying_position': np.nanmean([11,19]),
                'race_position': np.nanmean([17,17]),
                'curr_week_fp_pos': np.nanmean([15,15,15]),
                'price': np.nanmean(11.1)},
            {'team':'Mclaren','name': 'Oscar Pisatri',
                'qualifying_position': np.nanmean([18,8]),
                'race_position': np.nanmean([20,15]),
                'curr_week_fp_pos': np.nanmean([16,16,16]),
                'price': np.nanmean(6.9)},
            {'team':'AlphaTauri','name': 'Nyck de Vries',
                'qualifying_position': np.nanmean([19,18]),
                'race_position': np.nanmean([14,14]),
                'curr_week_fp_pos': np.nanmean([17,17,17]),
                'price': np.nanmean(5.0)},
            {'team':'AlphaTauri','name': 'Yuki Tsunoda',
                'qualifying_position': np.nanmean([14,16]),
                'race_position': np.nanmean([11,11]),
                'curr_week_fp_pos': np.nanmean([18,18,18]),
                'price': np.nanmean(4.8)},
            {'team':'Williams','name': 'Alex Albon',
                'qualifying_position': np.nanmean([15,17]),
                'race_position': np.nanmean([10,19]),
                'curr_week_fp_pos': np.nanmean([19,19,19]),
                'price': np.nanmean(5.5)},
            {'team':'Williams','name': 'Logan Sargeant',
                'qualifying_position': np.nanmean([16,20]),
                'race_position': np.nanmean([12,15]),
                'curr_week_fp_pos': np.nanmean([20,20,20]),
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
            print(f"Updated Teams: {team}")

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
        
        return 1 / fitness_score

    def one_point_crossover(self,parent1, parent2):
        # choose a random index to split the parents
        split_index = random.randint(1, len(parent1) - 1)
        
        # create child by combining the first half of parent1 and second half of parent2
        child = parent1[:split_index] + parent2[split_index:]
        
        return child

    def mutation(self,individual, mutation_rate):
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                # randomly change one attribute of the individual
                if i < 5:
                    attribute = 'driver'
                else:
                    attribute = 'constructor'
                individual[i][attribute] = random.choice(self.drivers) if attribute == 'driver' else random.choice(self.constructors)
        
        return individual

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
    
    def tournament_selection(self):
        # Randomly select individuals from the population to participate in the tournament
        participants = random.sample(range(len(self.population)), self.tournament_size)
        # Determine the fitness values of the participants
        participant_fitness = [self.fitnesses[i] for i in participants]
        # Find the index of the participant with the best fitness value
        best_index = participants[participant_fitness.index(max(participant_fitness))]
        # Return the best individual from the tournament
        return self.population[best_index]

    # main genetic algorithm function
    def genetic_algorithm(self):
        self.driver_names = [self.drivers[ii]['name'] for ii in range(0,len(self.drivers))]
        self.constructor_names = [self.constructors[ii]['name'] for ii in range(0,len(self.constructors))]
        self.num_drivers = len(self.driver_names)
        self.num_constructors = len(self.constructor_names)
        self.budget = 100
        self.max_generations = 100
        self.population_size = 100
        self.tournament_size = 5
        self.crossover_prob = 0.8
        self.mutation_prob = 0.05
        self.initialize_population()
        self.fitnesses = [self.fitness_function(individual) for individual in self.population]
        best_individual = self.population[self.fitnesses.index(min(self.fitnesses))]
        print(best_individual)
        for generation in range(self.max_generations):
            next_population = []
            for i in range(self.population_size):
                parent1 = self.tournament_selection()
                parent2 = self.tournament_selection()
                print(parent1,parent2)
                input()
        #         if random.random() < crossover_prob:
        #             child1, child2 = self.one_point_crossover(parent1, parent2)
        #         else:
        #             child1, child2 = parent1, parent2
        #         child1 = self.mutation(child1, mutation_prob)
        #         child2 = self.mutation(child2, mutation_prob)
        #         next_population.append(child1)
        #         next_population.append(child2)
        #     population = next_population
        #     fitnesses = [self.fitness_function(individual, driver_data, constructor_data, budget) for individual in population]
        #     best_fitness = min(fitnesses)
        #     best_individual = population[fitnesses.index(best_fitness)]

if __name__ == '__main__':
    GA = ModelGA()
    GA.genetic_algorithm()


    # def calculate_fitness(self,drivers, constructors, budget):
    #     driver_qualifying_avg = sum(driver['qualifying_position'] for driver in drivers) / len(drivers)
    #     driver_race_avg = sum(driver['race_position'] for driver in drivers) / len(drivers)
    #     constructor_qualifying_avg = sum(constructor['qualifying_position'] for constructor in constructors) / len(constructors)
    #     constructor_race_avg = sum(constructor['race_position'] for constructor in constructors) / len(constructors)
    #     team_cost = sum(driver['price'] for driver in drivers) + sum(constructor['price'] for constructor in constructors)
        
    #     if team_cost > budget:
    #         return 0  # team is too expensive, return fitness score of 0
        
    #     return (driver_qualifying_avg + driver_race_avg + constructor_qualifying_avg + constructor_race_avg) * team_cost
    # def selection(self,population, num_parents):
    # #     # sort population by fitness score in descending order
    #     sorted_population = sorted(population, key=lambda x: x['fitness'], reverse=True)
        
    #     # select the top num_parents as parents for reproduction
    #     parents = sorted_population[:num_parents]
        
    #     return parents