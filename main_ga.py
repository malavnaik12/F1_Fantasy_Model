import numpy as np
import random
import yaml
import matplotlib.pyplot as plt
import json
import os

class PreprocessGA:
    def __init__(self):
        pass
    
    def initalize(self):
        """
        Initialize various inputs from the inputs.yaml, load the database into memory, and create the output plots folder.

        Args:
            None
        
        Returns: Loads data into class constructor
        - db_data (dict): The main source of the drivers and constructors information
        - The inputs from the inputs.yaml (float or int) 
        """
        with open("./input_files/inputs.yaml", "r") as file:
            inputs = yaml.safe_load(file)
            self.max_generations = inputs["max_gens"]
            self.population_size = inputs["pop_size"]
            self.tournament_size_prop = inputs["tournament_size_prop"]
            self.crossover_prob = inputs["crossover"]
            self.mutation_prob = inputs["mutation"]
            self.elitism_prob = inputs["elitism"]
            self.max_drivers_num = inputs["max_drivers"]
            self.max_constructors_num = inputs["max_constructors"]
            
        with open("./input_files/prices.yaml") as prices_file:
            prices = yaml.safe_load(prices_file)
            self.budget = prices["weekly_budget"]
        
        with open("./database_files/database.json","r") as db:
            self.db_data = json.load(db)
            db.close()
        
        # Initialization of variables used to store team attributes 
        self.best_team_attr = {}
        self.med_team_attr = []
        self.max_team_attr = {}

        # Output Plots Folder Initialization
        self.ind_folder = "individual_files"
        os.makedirs("./Plots/",exist_ok=True)
        os.makedirs(f"./Plots/{self.ind_folder}/",exist_ok=True)
        os.makedirs("./ga_output_files/",exist_ok=True)
        os.makedirs(f"./ga_output_files/{self.ind_folder}/",exist_ok=True)
    
    def get_db_info(self, db_data, constructors = [], drivers = {}):
        """
        From the database that gets loaded from database.json, extract team and driver info and save to variables.

        Args:
        - db_data (dict): A dictionary containing raw data from database.json
        - drivers (dict): An empty dictionary to house driver names and corresponding team that the driver belongs to
        - constructors (list): An empty list containing information about the constructor names

        Returns:
        - drivers (dict): A populated dictionary housing driver names and corresponding team that the driver belongs to
        - constructors (list): A populated list containing the constructor names
        """
        for team in list(db_data.keys()):
            team_info = db_data[team]
            constructors.append(team)
            for key in team_info.keys():
                if key not in ['quali_hist', 'race_hist', 'fp', 'price']:
                    drivers[key] = team
        return constructors, drivers

    def initialize_population(self, pop_list, db_data):
        """
        Initialize a population of teams for the genetic algorithm.

        Args:
        - db_data (dict): A dictionary containing raw data from database.json
        - self.drivers_names (dict): A dictionary containing driver names and their corresponding teams
        - self.constructors (list): A dictionary containing constructor names
        - self.budget (float): The maximum budget for a team
        - self.max_drivers_num (int): The maximum number of drivers allowed per team
        - self.max_constructors_num (int): The maximum number of constructors allowed per team

        Returns:
        - population (list): a list of teams, where each team is a dictionary containing
                            information about the drivers, constructors, and total cost
        """

        while len(pop_list) < self.population_size:
            drivers_selected = []
            constructors_selected = []
            total_cost = 0
            
            # randomly select 5 unique drivers
            while len(drivers_selected) < self.max_drivers_num:
                driver = random.choice(list(self.driver_names.keys()))
                if driver not in drivers_selected:
                    drivers_selected.append(driver)
                    # temp.append(driver)
                    total_cost += np.nanmean(db_data[self.driver_names[driver]][driver]["price"])

            # randomly select 2 unique constructors
            while len(constructors_selected) < self.max_constructors_num:
                constructor = random.choice(self.constructor_names)
                if constructor not in constructors_selected:
                    constructors_selected.append(constructor)
                    total_cost += np.nanmean(db_data[constructor]["price"])

            # if the team is within the budget, add it to the population
            if total_cost <= self.budget:
                team = {'drivers': drivers_selected,
                        'constructors': constructors_selected,
                        'total_cost': total_cost}
                pop_list.append(team)
        return pop_list

    def fitness_function(self, team, db_data):
        """
        Calculate the fitness value based on the particular population individual (team) supplied via the function input

        Args:
        - db_data (dict): A dictionary containing raw data from database.json
        - team (dict): A dict containing the driver, constructor, and cost information for a given population individual

        Returns:
        - fitness_score (float): The fitness score of a supplied team. 
                                - The value of the fitness_score is multiplied by -1, the lower the value, the better the quality of the team.
        """
        team_drivers = team["drivers"]
        team_constructors = team['constructors']
        team_cost = team['total_cost']

        # Calculate average qualifying, race positions, and free practice positions for the team
        driver_quali_hist = 0; driver_race_hist = 0
        constructor_quali_hist = 0; constructor_race_hist = 0
        driver_fp_hist = 0; constructor_fp_hist = 0 
        for driver in team_drivers:
            driver_quali_hist += np.nanmean(db_data[self.driver_names[driver]][driver]['quali_hist'])
            driver_race_hist += np.nanmean(db_data[self.driver_names[driver]][driver]['race_hist'])
            driver_fp_hist += np.nanmean(db_data[self.driver_names[driver]][driver]['fp'])
        
        for constructor in team_constructors:
            constructor_quali_hist += np.nanmean(db_data[constructor]['quali_hist'])
            constructor_race_hist += np.nanmean(db_data[constructor]['race_hist'])
            constructor_fp_hist += np.nanmean(db_data[constructor]['fp'])
        
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

    def tournament_selection(self, fitness_vals):
        """
        Based on the fitness values of the initial population set, run tournament selection and find index of best (lowest) fitness value.

        Args:
        - fitness_vals (list): A list containing fitness values for each of the individuals in the populations set.
        - self.tournament_size_prop (int): The number of individuals using which a subset of the population set is created
                                        - Must be less than or equal to self.population_size

        Returns:
        - best_index (int): The index of the population individual with the best fitness score within the population subset generated via self.tournament_size_prop 
        """
        # Randomly select individuals from the population to participate in the tournament
        participants = random.sample(range(len(fitness_vals)), int(self.tournament_size_prop*self.population_size))

        # Determine the fitness values of the participants
        participant_fitness = [fitness_vals[i] for i in participants]

        # Find the index of the participant with the best fitness value
        best_index = participants[participant_fitness.index(max(participant_fitness))]
        
        return best_index # Return the best individual from the tournament

    def one_point_crossover(self, team1, team2, db_data):
        """
        If invoked, create children teams based on the two parent teams supplied in function input.
        The goal here is to create two children teams that may better tend towards the desired team budget while also yielding better fitness than the parents.

        Args:
        - db_data (dict): A dictionary containing raw data from database.json
        - team1 (dict): One of the parent teams, selected from tournament_selection, a dict containing the driver, constructor, and cost information for a given population individual
        - team2 (dict): The other parent team, selected from tournament_selection, a dict containing the driver, constructor, and cost information for a given population individual
        
        Returns:
        - child (dict): The resulting child team created based on crossover using the supplied two parents
                        - A dict containing the driver, constructor, and cost information for a given population individual
        """

        # choose a random index to split the parents
        split_index = random.randint(1, len(team1) - 1)
        parent1 = team1['drivers'] + team1['constructors']
        parent2 = team2['drivers'] + team2['constructors']
        
        # create child by combining the first half of parent1 and second half of parent2
        child1 = parent1[:split_index] + parent2[split_index:]
        child2 = parent2[:split_index] + parent1[split_index:]
        
        total_cost1 = 0
        for driver in child1[:self.max_drivers_num]:
            total_cost1 += np.nanmean(db_data[self.driver_names[driver]][driver]["price"])
        for team in child1[self.max_drivers_num:]:
            total_cost1 += np.nanmean(db_data[team]["price"])
        
        total_cost2 = 0
        for driver in child2[:self.max_drivers_num]:
            total_cost2 += np.nanmean(db_data[self.driver_names[driver]][driver]["price"])
        for team in child2[self.max_drivers_num:]:
            total_cost2 += np.nanmean(db_data[team]["price"])
        
        if ((total_cost1 or total_cost2) > self.budget):
            out_child1 = team1
            out_child2 = team2
        else:
            out_child1 = {'drivers':child1[0:5],'constructors':child1[5:],'total_cost':total_cost1}
            out_child2 = {'drivers':child2[0:5],'constructors':child2[5:],'total_cost':total_cost2}
            self.fitness_function(out_child1, db_data=db_data)
            self.fitness_function(out_child2, db_data=db_data)
            if (((out_child1['fitness_val'] or out_child2['fitness_val']) >= team1['fitness_val']) and ((out_child1['fitness_val'] or out_child2['fitness_val']) >= team2['fitness_val'])):
                out_child1 = team1
                out_child2 = team2
        if out_child1['fitness_val'] <= out_child2['fitness_val']:
            child = out_child1
        else:
            child = out_child2
        return child
    
    def mutation(self, team, mut_rate, db_data):
        """
        If invoked, mutate supplied team.
        The goal here is to randomly mutate the drivers or constructors and create a mutated team that has a better fitness value than the supplied team.

        Args:
        - db_data (dict): A dictionary containing raw data from database.json
        - mut_rate (float): A float value, to be used to assess if supplied team should undergo any mutation
        - team (dict): A dict containing the driver, constructor, and cost information for a given population individual to be mutated

        Returns:
        - team (dict): The mutated team, a dict containing the driver, constructor, and cost information for a given population individual to be mutated
        """

        team_gen = False
        temp = []
        old_team_fitness = team['fitness_val']
        while (team_gen == False):
            if random.random() < mut_rate:
                if random.random() < mut_rate:
                    popped = team['drivers'].pop(random.randint(0,4))
                    temp.append(popped)
                    for driver in team['drivers']:
                        temp.append(driver)
                    while len(team['drivers']) < self.max_drivers_num:
                        driver = random.choice(list(self.driver_names.keys()))
                        if driver not in temp:
                            team['drivers'].append(driver)
                            temp.append(driver)
                else:
                    popped = team['constructors'].pop(random.randint(0,1))
                    while len(team['constructors']) < self.max_constructors_num:
                        constructor = random.choice(self.constructor_names)
                        if constructor not in (team['constructors'] or popped):
                            team['constructors'].append(constructor)
                total_cost = sum([np.nanmean(db_data[self.driver_names[driver]][driver]["price"]) for driver in team['drivers']])
                total_cost += sum([np.nanmean(db_data[team]["price"]) for team in team['constructors']])

                if (total_cost > self.budget):
                    team_gen = False
                elif (team['fitness_val'] < old_team_fitness):
                    team_gen = True
                else:
                    team_gen = True
                    team['total_cost'] = total_cost
        return team

    def curr_gen_info(self, curr_gen_fitness_vals, curr_gen):
        save_folder = f"./Plots/{self.ind_folder}/{self.max_generations}g_{self.population_size}p/"
        os.makedirs(save_folder,exist_ok=True)
        if (curr_gen+1)%5 == 0:
            fig, ax = plt.subplots(1,2,figsize=(10, 6))
            fig.suptitle(f"Current Generation: {curr_gen+1}")
            ax[0].plot(range(1,self.population_size+1),curr_gen_fitness_vals)
            ax[0].plot(curr_gen_fitness_vals.index(min(curr_gen_fitness_vals))+1,min(curr_gen_fitness_vals),'*')

            ax[1].set_axis_off()
            ax[1].text(-0.5,0.5,f"""
                                Best Team Info:\n
                                Drivers: {self.best_team_attr[curr_gen]['drivers']}\n
                                Constructors: {self.best_team_attr[curr_gen]['constructors']}\n
                                Total Cost: {self.best_team_attr[curr_gen]['total_cost']}
                                """)
            fig.savefig(f"{save_folder}fitness_{curr_gen+1}.png")
            plt.close(fig)

    def plot_fitness(self):
        plt.figure(2)
        plt.title("Fitness Function Trends per Generation")
        plt.plot(range(1,self.max_generations+1),self.worst_fitness,color='red',label='Worst')
        plt.plot(range(1,self.max_generations+1),list(self.med_team_attr),color='blue',label='Median')
        plt.plot(range(1,self.max_generations+1),self.best_fitness,color='green',label='Best')
        plt.legend()
        plt.savefig(f"./Plots/fitness_trends_{self.max_generations}g_{self.population_size}p.png")
        plt.close()

    # main genetic algorithm function
    def genetic_algorithm(self):
        """
        The main function carrying out all Genetic Algorithm operations

        Args:
            None
        
        Returns:
            None        
        """
        self.initalize()
        best_team_file = open(f"./ga_output_files/best_team_per_gen.txt","w")
        final_summary_file = open(f"./ga_output_files/best_team.txt","w")
        self.constructor_names, self.driver_names = self.get_db_info(db_data=self.db_data)
        best_fitness_val = []
        for generation in range(self.max_generations):
            population = []
            if random.random() < self.elitism_prob*(generation/self.max_generations):
                if generation > 0:
                    population.append(self.best_team_attr[generation-1])
                    processing_indx = 1
            else:
                processing_indx = 0
            population = self.initialize_population(population, db_data=self.db_data)
            before_fitnesses = [self.fitness_function(individual,db_data=self.db_data) for individual in population]
            processed_population = []
            if processing_indx == 1:
                processed_population.append(population[0])
            print(f"Generation: {generation+1}, Population Size: {len(population)}")
            for i in range(processing_indx, self.population_size):
                if random.random() < (self.crossover_prob/(generation+100)):
                    parent1_index = self.tournament_selection(before_fitnesses)
                    parent2_index = self.tournament_selection(before_fitnesses)
                    parent1 = population[parent1_index]
                    parent2 = population[parent2_index]
                    child = self.one_point_crossover(team1 = parent1, team2 = parent2, db_data=self.db_data)
                else:
                    child = population[i]
                mutated_child = self.mutation(child, self.mutation_prob/(generation+100), db_data=self.db_data)
                processed_population.append(mutated_child)
            after_fitnesses = [self.fitness_function(individual, db_data=self.db_data) for individual in processed_population]

            # Population Set Attributes
            best_fitness_val.append(min(after_fitnesses))
            self.max_team_attr[generation] = processed_population[after_fitnesses.index(max(after_fitnesses))]
            self.med_team_attr.append(np.nanmedian(after_fitnesses))            
            self.best_team_attr[generation] = processed_population[after_fitnesses.index(min(after_fitnesses))]
            self.curr_gen_info(after_fitnesses,curr_gen=generation)
            best_team_file.write(f"""
Generation: {generation+1}\n
\tDrivers: {self.best_team_attr[generation]['drivers']}\n
\tConstructors: {self.best_team_attr[generation]['constructors']}\n
\tTeam Cost: {self.best_team_attr[generation]['total_cost']}\n
\tFitness: {self.best_team_attr[generation]['fitness_val']}\n
            """)

        best_overall_team_index = best_fitness_val.index(min(best_fitness_val))
        final_summary_file.write(f"""
Generation: {best_overall_team_index+1}\n
\tDrivers: {self.best_team_attr[best_overall_team_index]['drivers']}\n
\tConstructors: {self.best_team_attr[best_overall_team_index]['constructors']}\n
\tTeam Cost: {self.best_team_attr[best_overall_team_index]['total_cost']}\n
\tFitness: {self.best_team_attr[best_overall_team_index]['fitness_val']}\n
            """)
        final_summary_file.write(f"""
Generation: {generation+1}\n
\tDrivers: {self.best_team_attr[generation]['drivers']}\n
\tConstructors: {self.best_team_attr[generation]['constructors']}\n
\tTeam Cost: {self.best_team_attr[generation]['total_cost']}\n
\tFitness: {self.best_team_attr[generation]['fitness_val']}\n
            """)
        
        self.worst_fitness = [self.max_team_attr[gen]['fitness_val'] for gen in self.max_team_attr.keys()]
        self.best_fitness = [self.best_team_attr[gen]['fitness_val'] for gen in self.best_team_attr.keys()]
        self.plot_fitness()
        final_summary_file.close()
        best_team_file.close()

if __name__ == '__main__':
    GA = PreprocessGA()
    GA.genetic_algorithm()