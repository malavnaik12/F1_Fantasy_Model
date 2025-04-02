import os
import json
import yaml
import random
import numpy as np
from team_parse import getDrivers, getTeams
import matplotlib.pyplot as plt


class MainGA:
    def __init__(self):
        with open("./input_files/positions_schema.yaml", "r") as file:
            self.race_weekend_sessions = list(yaml.safe_load(file))
        self.race_weekend_sessions.pop(
            self.race_weekend_sessions.index("race_weekend_type")
        )
        self.race_weekend_sessions.pop(self.race_weekend_sessions.index("Constructor"))

    def initalize(self, year: int):
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
            self.budget = inputs["weekly_budget"]
            self.max_generations = inputs["max_gens"]
            self.population_size = inputs["pop_size"]
            self.tournament_size_prop = inputs["tournament_size_prop"]
            self.crossover_prob = inputs["crossover"]
            self.mutation_prob = inputs["mutation"]
            self.elitism = inputs["elitism"]
            self.max_drivers_num = inputs["max_drivers"]
            self.max_constructors_num = inputs["max_constructors"]

        # with open("./input_files/prices.yaml") as prices_file:
        #     prices = yaml.safe_load(prices_file)

        with open("./database_files/database_main.json", "r") as db:
            db_data = json.load(db)
        self.db_data = db_data[str(year)]

        # Initialization of variables used to store team attributes
        self.best_team_attr = {}
        self.med_team_attr = []
        self.max_team_attr = {}

        # Output Plots Folder Initialization
        self.ind_folder = "individual_files"
        os.makedirs("./Plots/", exist_ok=True)
        os.makedirs(f"./Plots/{self.ind_folder}/", exist_ok=True)
        os.makedirs("./ga_output_files/", exist_ok=True)
        os.makedirs(f"./ga_output_files/{self.ind_folder}/", exist_ok=True)

    def get_db_info(self, constructors=[], drivers={}):
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
        for team in getTeams():
            constructors.append(team)
            for driver in getDrivers(team):
                drivers[driver] = team
        return constructors, drivers

    def initialize_population(self, pop_list, db_data, raceLoc):
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
            temp = []
            # randomly select 5 unique drivers
            while len(drivers_selected) < self.max_drivers_num:
                driver = random.choice(list(self.driver_names.keys()))
                if driver not in drivers_selected:
                    drivers_selected.append(driver)
                    try:
                        total_cost += np.nanmean(
                            db_data[self.driver_names[driver]][driver]["prices"][
                                raceLoc
                            ]
                        )
                    except KeyError:
                        drivers_selected.pop(drivers_selected.index(driver))
            while len(constructors_selected) < self.max_constructors_num:
                constructor = random.choice(self.constructor_names)
                if constructor not in constructors_selected:
                    try:
                        constructors_selected.append(constructor)
                        total_cost += np.nanmean(
                            db_data[constructor]["prices"][raceLoc]
                        )
                    except KeyError:
                        continue
            # if the team is within the budget, add it to the population
            if total_cost <= self.budget:
                team = {
                    "drivers": drivers_selected,
                    "constructors": constructors_selected,
                    "total_cost": total_cost,
                }
                pop_list.append(team)
        return pop_list

    def get_avg_attr_drivers(self, db_data, team_items, session, avg_val=0):
        for item in team_items:
            # print(session, item)
            filtered_item_list = [
                item
                for item in db_data[self.driver_names[item]][item][session]
                if item is not None
            ]
            result = np.nanmean(filtered_item_list)
            try:
                int(result)
            except ValueError:
                result = 0
            avg_val += result
        return avg_val

    def get_avg_attr_constructors(self, db_data, team_items, session, avg_val=0):
        for item in team_items:
            filtered_item_list = [
                item for item in db_data[item][session] if item is not None
            ]
            avg_val += np.nanmean(filtered_item_list)
        return avg_val

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
        driver_score = 0
        constructor_score = 0
        for session in self.race_weekend_sessions:
            driver_score += self.get_avg_attr_drivers(db_data, team["drivers"], session)
            # print(session, driver_score)
            constructor_score = self.get_avg_attr_constructors(
                db_data, team["constructors"], session
            )

        # Calculate the fitness score using the specified formula
        driver_part = driver_score / self.max_drivers_num
        constructor_part = constructor_score / self.max_constructors_num
        fitness_score = (driver_part + constructor_part) / team["total_cost"]
        # print(driver_part, constructor_part, team["total_cost"])
        # input()
        team["fitness_val"] = fitness_score
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
        participants = random.sample(
            range(len(fitness_vals)),
            int(self.tournament_size_prop * self.population_size),
        )

        # Determine the fitness values of the participants
        participant_fitness = [fitness_vals[i] for i in participants]

        # Find the index of the participant with the best fitness value
        best_index = participants[participant_fitness.index(max(participant_fitness))]

        return best_index  # Return the best individual from the tournament

    def get_crossed_team(self, team, db_data, raceLoc):
        drivers = team[: self.max_drivers_num]
        constructors = team[self.max_drivers_num :]
        total_cost = 0
        for driver in drivers:
            try:
                total_cost += np.nanmean(
                    db_data[self.driver_names[driver]][driver]["prices"][raceLoc]
                )
            except KeyError:
                drivers.pop(drivers.index(driver))
                temp = [driver]
                while len(driver) < self.max_drivers_num:
                    temp_driver = random.choice(list(self.driver_names.keys()))
                    if temp_driver not in temp:
                        team["drivers"].append(driver)
                        temp.append(driver)
                        total_cost += np.nanmean(
                            db_data[self.driver_names[driver]][driver]["prices"][
                                raceLoc
                            ]
                        )
        for team in constructors:
            total_cost += np.nanmean(db_data[team]["prices"][raceLoc])
        return total_cost

    def one_point_crossover(self, team1, team2, db_data, raceLoc):
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
        parent1 = team1["drivers"] + team1["constructors"]
        parent2 = team2["drivers"] + team2["constructors"]

        # create child by combining the first half of parent1 and second half of parent2
        child1 = parent1[:split_index] + parent2[split_index:]
        child2 = parent2[:split_index] + parent1[split_index:]

        total_cost1 = self.get_crossed_team(child1, db_data, raceLoc)
        total_cost2 = self.get_crossed_team(child2, db_data, raceLoc)

        if (total_cost1 or total_cost2) > self.budget:
            out_child1 = team1
            out_child2 = team2
        else:
            out_child1 = {
                "drivers": child1[0:5],
                "constructors": child1[5:],
                "total_cost": total_cost1,
            }
            out_child2 = {
                "drivers": child2[0:5],
                "constructors": child2[5:],
                "total_cost": total_cost2,
            }
            self.fitness_function(out_child1, db_data=db_data)
            self.fitness_function(out_child2, db_data=db_data)
            if (
                (out_child1["fitness_val"] or out_child2["fitness_val"])
                >= team1["fitness_val"]
            ) and (
                (out_child1["fitness_val"] or out_child2["fitness_val"])
                >= team2["fitness_val"]
            ):
                out_child1 = team1
                out_child2 = team2
        if out_child1["fitness_val"] <= out_child2["fitness_val"]:
            child = out_child1
        else:
            child = out_child2
        return child

    def mutation(self, team, mut_rate, db_data, raceLoc):
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
        old_team_fitness = team["fitness_val"]
        while team_gen == False:
            if random.random() < mut_rate:
                if random.random() < mut_rate:
                    temp = []
                    popped = team["drivers"].pop(random.randint(0, 4))
                    temp.append(popped)
                    while len(team["drivers"]) < self.max_drivers_num:
                        driver = random.choice(list(self.driver_names.keys()))
                        if driver not in temp:
                            team["drivers"].append(driver)
                            temp.append(driver)
                else:
                    popped = team["constructors"].pop(random.randint(0, 1))
                    while len(team["constructors"]) < self.max_constructors_num:
                        constructor = random.choice(self.constructor_names)
                        if constructor not in (team["constructors"] or popped):
                            team["constructors"].append(constructor)
                try:
                    total_cost = sum(
                        [
                            np.nanmean(
                                db_data[self.driver_names[driver]][driver]["prices"][
                                    raceLoc
                                ]
                            )
                            for driver in team["drivers"]
                        ]
                    )
                    total_cost += sum(
                        [
                            np.nanmean(db_data[team]["prices"][raceLoc])
                            for team in team["constructors"]
                        ]
                    )
                    if total_cost > self.budget:
                        team_gen = False
                    elif team["fitness_val"] < old_team_fitness:
                        team_gen = True
                    else:
                        team_gen = True
                        team["total_cost"] = total_cost
                except KeyError:
                    team_gen = False
        return team

    def curr_gen_info(self, curr_gen_fitness_vals, curr_gen):
        save_folder = f"./Plots/{self.ind_folder}/{self.max_generations}g_{self.population_size}p/"
        os.makedirs(save_folder, exist_ok=True)
        if (curr_gen + 1) % 5 == 0:
            fig, ax = plt.subplots(1, 2, figsize=(10, 6))
            fig.suptitle(f"Current Generation: {curr_gen+1}")
            ax[0].plot(range(1, self.population_size + 1), curr_gen_fitness_vals)
            ax[0].plot(
                curr_gen_fitness_vals.index(min(curr_gen_fitness_vals)) + 1,
                min(curr_gen_fitness_vals),
                "*",
            )

            ax[1].set_axis_off()
            ax[1].text(
                -0.5,
                0.5,
                f"""
                                Best Team Info:\n
                                Drivers: {self.best_team_attr[curr_gen]['drivers']}\n
                                Constructors: {self.best_team_attr[curr_gen]['constructors']}\n
                                Total Cost: {self.best_team_attr[curr_gen]['total_cost']}
                                """,
            )
            fig.savefig(f"{save_folder}fitness_{curr_gen+1}.png")
            plt.close(fig)

    def plot_fitness(self):
        plt.figure(2)
        plt.title("Fitness Function Trends per Generation")
        plt.plot(
            range(1, self.max_generations + 1),
            self.worst_fitness,
            color="red",
            label="Worst",
        )
        plt.plot(
            range(1, self.max_generations + 1),
            list(self.med_team_attr),
            color="blue",
            label="Median",
        )
        plt.plot(
            range(1, self.max_generations + 1),
            self.best_fitness,
            color="green",
            label="Best",
        )
        plt.legend()
        fig_name = f"fitness_trends_{self.max_generations}g_{self.population_size}p.png"
        plt.savefig(f"./Plots/{fig_name}")
        plt.close()
        try:
            os.rename(
                f"./Plots/{fig_name}",
                f"../f1_fantasy_ui/src/assets/ga_results.png",
            )
        except FileExistsError:
            os.remove(f"../f1_fantasy_ui/src/assets/ga_results.png")
            os.rename(
                f"./Plots/{fig_name}",
                f"../f1_fantasy_ui/src/assets/ga_results.png",
            )

    # main genetic algorithm function
    def genetic_algorithm(self, item):
        """
        The main function carrying out all Genetic Algorithm operations

        Args:
            item: A dictionary containing Season year and Current Race Week location

        Returns:
            The best team from the GA computations
        """
        self.initalize(item["year"])
        # final_summary_file = open(f"./ga_output_files/best_team.txt", "w")
        self.constructor_names, self.driver_names = self.get_db_info()
        best_fitness_val = []
        for generation in range(self.max_generations):
            population = []
            if self.elitism > 0:
                if generation > 0:
                    population.append(self.best_team_attr[generation - 1])
                    processing_indx = 1
                else:
                    processing_indx = 0
            else:
                processing_indx = 0
            population = self.initialize_population(
                population, db_data=self.db_data, raceLoc=item["raceLoc"]
            )
            before_fitnesses = [
                self.fitness_function(individual, db_data=self.db_data)
                for individual in population
            ]
            processed_population = []
            if processing_indx == 1:
                processed_population.append(population[0])
            print(f"Generation: {generation+1}, Population Size: {len(population)}")
            for i in range(processing_indx, self.population_size):
                if random.random() < (self.crossover_prob / 1):  # (generation + 100)):
                    parent1_index = self.tournament_selection(before_fitnesses)
                    parent2_index = self.tournament_selection(before_fitnesses)
                    parent1 = population[parent1_index]
                    parent2 = population[parent2_index]
                    child = self.one_point_crossover(
                        team1=parent1,
                        team2=parent2,
                        db_data=self.db_data,
                        raceLoc=item["raceLoc"],
                    )
                else:
                    child = population[i]
                mutated_child = self.mutation(
                    child,
                    self.mutation_prob / (generation + 100),
                    db_data=self.db_data,
                    raceLoc=item["raceLoc"],
                )
                processed_population.append(mutated_child)
            after_fitnesses = [
                self.fitness_function(individual, db_data=self.db_data)
                for individual in processed_population
            ]

            # Population Set Attributes
            best_fitness_val.append(min(after_fitnesses))
            self.max_team_attr[generation] = processed_population[
                after_fitnesses.index(max(after_fitnesses))
            ]
            # print(self.max_team_attr[generation])
            self.med_team_attr.append(np.nanmedian(after_fitnesses))
            self.best_team_attr[generation] = processed_population[
                after_fitnesses.index(min(after_fitnesses))
            ]
            # self.curr_gen_info(after_fitnesses, curr_gen=generation)

        self.worst_fitness = [
            self.max_team_attr[gen]["fitness_val"] for gen in self.max_team_attr.keys()
        ]
        self.best_fitness = [
            self.best_team_attr[gen]["fitness_val"]
            for gen in self.best_team_attr.keys()
        ]
        self.plot_fitness()
        # final_summary_file.close()
        best_team_file = open(f"./ga_output_files/best_team_per_gen.txt", "w+")
        out_string = f"Generation: {best_fitness_val.index(min(best_fitness_val))+1}\n"
        out_string += f"\tDrivers: {self.best_team_attr[best_fitness_val.index(min(best_fitness_val))]['drivers']}\n"
        out_string += f"\tConstructors: {self.best_team_attr[best_fitness_val.index(min(best_fitness_val))]['constructors']}\n"
        out_string += f"\tTeam Cost: {self.best_team_attr[best_fitness_val.index(min(best_fitness_val))]['total_cost']}\n"
        out_string += f"\tFitness: {self.best_team_attr[best_fitness_val.index(min(best_fitness_val))]['fitness_val']}\n"
        best_team_file.write(out_string)
        best_team_file.close()
        return self.best_team_attr[best_fitness_val.index(min(best_fitness_val))]


if __name__ == "__main__":
    GA = MainGA()
    print(GA.genetic_algorithm(item={"year": 2024, "raceLoc": "Brazil"}))
    # Need to populate info for a recent race, run rr_to_dbmain conversion, and then run ga - Done
    # Need to check if driver is still a driver
    #   if so, then get most recent race they participated in and corresponding price
    #   if not, then bump them from the team and update the team with a new driver
