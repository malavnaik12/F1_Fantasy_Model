import numpy as np
import random
import yaml
import matplotlib.pyplot as plt
import json
import os,sys

class PreprocessGA:
    def __init__(self):
        with open("inputs.yaml", "r") as file:
            inputs = yaml.safe_load(file)
            self.budget = inputs["budget"]
            self.max_generations = inputs["max_gens"]
            self.population_size = inputs["pop_size"]
            self.tournament_size = inputs["tournament_size"]
            self.crossover_prob = inputs["crossover"]
            self.mutation_prob = inputs["mutation"]
            self.max_drivers_num = inputs["max_drivers"]
            self.max_constructors_num = inputs["max_constructors"]
            file.close()
        
        with open("database.json","r") as db:
            self.db_data = json.load(db)
            db.close()
    
    def get_db_info(self):
        self.constructor_names = []; self.driver_names = {}
        for team in list(self.db_data.keys()):
            team_info = self.db_data[team]
            self.constructor_names.append(team)
            for key in team_info.keys():
                if key not in ['quali_hist', 'race_hist', 'fp', 'price']:
                    self.driver_names[key] = team

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

        while len(self.population) < self.population_size:
            drivers_selected = []; #temp = []
            constructors_selected = []; total_cost = 0
            # randomly select 5 unique drivers
            while len(drivers_selected) < self.max_drivers_num:
                driver = random.choice(list(self.driver_names.keys()))
                if driver not in drivers_selected:
                    drivers_selected.append(driver)
                    # temp.append(driver)
                    total_cost += np.nanmean(self.db_data[self.driver_names[driver]][driver]["price"])

            # randomly select 2 unique constructors
            while len(constructors_selected) < self.max_constructors_num:
                constructor = random.choice(self.constructor_names)
                if constructor not in constructors_selected:
                    constructors_selected.append(constructor)
                    total_cost += np.nanmean(self.db_data[constructor]["price"])

            # if the team is within the budget, add it to the population
            if total_cost <= self.budget:
                team = {'drivers': drivers_selected,
                        'constructors': constructors_selected,
                        'total_cost': total_cost}
                self.population.append(team)
                # print(team)

    def fitness_function(self, team):
        team_drivers = team["drivers"]
        team_constructors = team['constructors']
        team_cost = team['total_cost']

        # Calculate average qualifying, race positions, and free practice positions for the team
        driver_quali_hist = 0; driver_race_hist = 0
        constructor_quali_hist = 0; constructor_race_hist = 0
        driver_fp_hist = 0; constructor_fp_hist = 0 
        for driver in team_drivers:
            driver_quali_hist += np.nanmean(self.db_data[self.driver_names[driver]][driver]['quali_hist'])
            driver_race_hist += np.nanmean(self.db_data[self.driver_names[driver]][driver]['race_hist'])
            driver_fp_hist += np.nanmean(self.db_data[self.driver_names[driver]][driver]['fp'])
        
        for constructor in team_constructors:
            constructor_quali_hist += np.nanmean(self.db_data[constructor]['quali_hist'])
            constructor_race_hist += np.nanmean(self.db_data[constructor]['race_hist'])
            constructor_fp_hist += np.nanmean(self.db_data[constructor]['fp'])
        
        # Calculate the average positions for drivers and constructors
        avg_driver_qual = driver_quali_hist / self.max_drivers_num
        avg_driver_race = driver_race_hist / self.max_drivers_num
        avg_driver_fp = driver_fp_hist / self.max_drivers_num
        avg_constructor_qual = constructor_quali_hist / self.max_constructors_num
        avg_constructor_race = constructor_race_hist / self.max_constructors_num
        avg_constructor_fp = constructor_fp_hist / self.max_constructors_num
    
        # Calculate the fitness score using the specified formula
        driver_score = avg_driver_qual + avg_driver_race + avg_driver_fp
        constructor_score = avg_constructor_qual + avg_constructor_race + avg_constructor_fp
        fitness_score = -(driver_score + constructor_score) * team_cost
        team['fitness_val'] = fitness_score
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

        cross_flag = False
        # while not cross_flag:
        # choose a random index to split the parents
        split_index = random.randint(1, len(self.parent1) - 1)
        parent1 = self.parent1['drivers'] + self.parent1['constructors']
        parent2 = self.parent2['drivers'] + self.parent2['constructors']
        
        # create child by combining the first half of parent1 and second half of parent2
        child1 = parent1[:split_index] + parent2[split_index:]
        child2 = parent2[:split_index] + parent1[split_index:]
        
        total_cost1 = 0
        for driver in child1[:self.max_drivers_num]:
            total_cost1 += np.nanmean(self.db_data[self.driver_names[driver]][driver]["price"])
        for team in child1[self.max_drivers_num:]:
            total_cost1 += np.nanmean(self.db_data[team]["price"])
        
        total_cost2 = 0
        for driver in child2[:self.max_drivers_num]:
            total_cost2 += np.nanmean(self.db_data[self.driver_names[driver]][driver]["price"])
        for team in child2[self.max_drivers_num:]:
            total_cost2 += np.nanmean(self.db_data[team]["price"])

        if ((total_cost1 or total_cost2) > self.budget):
            self.child1 = self.parent1
            self.child2 = self.parent2
        else:
            if (((total_cost1 or total_cost2) > self.parent1['total_cost']) and ((total_cost1 or total_cost2) > self.parent2['total_cost'])):
                self.child1 = {'drivers':child1[0:5],'constructors':child1[5:],'total_cost':total_cost1}
                self.child2 = {'drivers':child2[0:5],'constructors':child2[5:],'total_cost':total_cost2}
            else:
                self.child1 = self.parent1
                self.child2 = self.parent2
                # cross_flag = True
                # elif ((len(set(self.child1['drivers'])) or len(set(self.child2['drivers'])) != 5)) or (len(set(self.child1['constructors'])) or len(set(self.child2['constructors'])) != 2):
                #     self.child1 = self.parent1
                #     self.child2 = self.parent2
    
    def mutation(self,child,mut_rate):
        child_gen = False
        temp = []
        count = 0
        while (child_gen == False):
            if random.random() < mut_rate:
                if random.random() < mut_rate:
                    popped = child['drivers'].pop(random.randint(0,4))
                    temp.append(popped)
                    for driver in child['drivers']:
                        temp.append(driver)
                    while len(child['drivers']) < self.max_drivers_num:
                        driver = random.choice(list(self.driver_names.keys()))
                        if driver not in temp:
                            child['drivers'].append(driver)
                            temp.append(driver)
                else:
                    popped = child['constructors'].pop(random.randint(0,1))
                    while len(child['constructors']) < self.max_constructors_num:
                        constructor = random.choice(self.constructor_names)
                        if constructor not in (child['constructors'] or popped):
                            child['constructors'].append(constructor)
                
                total_cost = sum([np.nanmean(self.db_data[self.driver_names[driver]][driver]["price"]) for driver in child['drivers']])
                total_cost += sum([np.nanmean(self.db_data[team]["price"]) for team in child['constructors']])
                # count+=1
                # print(child['total_cost'], total_cost,count)
                if (total_cost > self.budget):
                    child_gen = False
                # elif (total_cost <= child['total_cost']):
                #     child_gen = False
                else:
                    child_gen = True
                    child['total_cost'] = total_cost
        return child

    # main genetic algorithm function
    def genetic_algorithm(self):
        self.get_db_info()
        self.best_team_attr = {}
        self.med_team_attr = []
        self.max_team_attr = {}
        for generation in range(self.max_generations):
            self.population = []
            if generation > 0:
                self.population.append(self.best_individual)
            self.initialize_population()
            before_fitnesses = [self.fitness_function(individual) for individual in self.population]
            print(f"Generation: {generation+1}, Population Size: {len(self.population)}")
            processed_population = []
            for i in range(self.population_size):
                if random.random() < self.crossover_prob:
                    self.parent1 = self.tournament_selection(before_fitnesses)
                    self.parent2 = self.tournament_selection(before_fitnesses)
                    self.one_point_crossover()
                    if random.random() <= 0.5:
                        self.child = self.child1
                    else:
                        self.child = self.child2
                else:
                    self.child = self.population[i]
                # else:
                #     self.child1, self.child2 = self.parent1, self.parent2
                child = self.mutation(self.child, self.mutation_prob)
                # child2 = self.mutation(self.child2, self.mutation_prob)
                processed_population.append(child)
                # processed_population.append(child2)
            after_fitnesses = [self.fitness_function(individual) for individual in processed_population]

            # Population Set Attributes
            worst_fitness = max(after_fitnesses)
            worst_individual = processed_population[after_fitnesses.index(worst_fitness)]
            self.max_team_attr[generation] = worst_individual # Must do: Make this dict update operation based on generation ID, not fitness value
            self.med_team_attr.append(np.nanmedian(after_fitnesses))
            self.best_fitness = min(after_fitnesses)
            self.best_individual = processed_population[after_fitnesses.index(self.best_fitness)]
            
            self.best_team_attr[generation] = self.best_individual # Must do: Make this dict update operation based on generation ID, not fitness value
            
            self.curr_gen_info(after_fitnesses,curr_gen=generation+1)
        # for gen in self.max_team_attr.keys():
        #     fitness = self.max_team_attr[gen]['fitness_value']
        self.worst_fitness = [self.max_team_attr[gen]['fitness_val'] for gen in self.max_team_attr.keys()]
        self.best_fitness = [self.best_team_attr[gen]['fitness_val'] for gen in self.best_team_attr.keys()]
        # print("Worst:", self.max_team_attr[max(self.max_team_attr.keys())])
        # print("Best:", self.best_team_attr[min(self.best_team_attr.keys())])
        self.plot_fitness()

    def curr_gen_info(self,curr_gen_fitness_vals,curr_gen):
        if curr_gen%5 == 0:
            fig, ax = plt.subplots(1,2,figsize=(10, 6))
            fig.suptitle(f"Current Generation: {curr_gen}")
            ax[0].plot(curr_gen_fitness_vals)
            ax[0].plot(curr_gen_fitness_vals.index(self.best_fitness),self.best_fitness,'*')

            ax[1].set_axis_off()
            ax[1].text(0,0.5,f"Best Team Info:\nDrivers: {[driver for driver in self.best_individual['drivers']]}\nConstructors: {self.best_individual['constructors']}\nTotal Cost: {self.best_individual['total_cost']}")
            fig.savefig(f"./Plots/individual_plots/fitness_{curr_gen}.png")
            plt.close(fig)

    def plot_fitness(self):
        print(len(self.worst_fitness),len(list(self.med_team_attr)),len(self.best_fitness))
        plt.figure(2)
        plt.title("Fitness Function Trends per Generation")
        plt.plot(range(1,self.max_generations+1),self.worst_fitness,color='red',label='Worst')
        plt.plot(range(1,self.max_generations+1),list(self.med_team_attr),color='blue',label='Median')
        plt.plot(range(1,self.max_generations+1),self.best_fitness,color='green',label='Best')
        plt.legend()
        plt.savefig(f"./Plots/fitness_trends_{self.max_generations}g_{self.population_size}p.png")
        plt.close()
        # plt.show()

if __name__ == '__main__':
    GA = PreprocessGA()
    GA.genetic_algorithm()