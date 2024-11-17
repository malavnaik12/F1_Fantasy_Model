<!-- DONE: Enter the Weekly Budget: 100 -->
<!-- DONE: Enter Maximum number of Generations: 150 -->
<!-- DONE: Enter Size of the Population Set: 50 -->
<!-- DONE: Enter Crossover Probability: 0.8 -->
<!-- DONE: Enter Mutation Rate:  0.9-->
<!-- DONE: Enter Elitism Rate:  1-->
<!-- DONE: Enter Tournament Size Proportion: 0.9-->
<!-- NOT NEEDED: Enter The Number of Current Race Week: -->
<!-- DONE: Enter The Maximum Number of Drivers Allowed: 5 -->
<!-- DONE: Enter The Maximum Number of Constructors Allowed: 2 -->
<template>
    <keep-alive>
        <div class="tab-content-grid">
            <div class="left-content">
                <p class="title">Optimizer Inputs</p>
                <div class="inputs">
                    <label>F1 Season Year: </label>
                    <input type="number" class="text" v-model="year">
                </div>
                <p></p>
                <div class="inputs">
                    <label for="entity-dropdown">Select Race Weekend: </label>
                    <select id="entity-dropdown" v-model="gp_loc">
                    <!-- </select> @change="getSessions"> -->
                        <option v-for="entity in gp_locs" :key="entity" :value="entity">
                            {{ entity }}
                        </option>
                    </select>
                </div>
                <p></p>
                <div v-if = "gp_loc" class="inputs">
                    <label>Enter Available Weekly Budget (millions): </label>
                    <input type="number" class="text" v-model="budget">
                </div>
                <p></p>
                <div v-if = "gp_loc" class="inputs">
                    <label>Enter Maximum Optimizer Evolutions: </label>
                    <input type="number" class="text" v-model="max_gens">
                </div>
                <p></p>
                <div v-if = "gp_loc" class="inputs">
                    <label>Enter Population Set Size: </label>
                    <input type="number" class="text" v-model="pop_set">
                </div>
                <p></p>
                <div v-if = "gp_loc" class="inputs">
                    <label>Enter Crossover Rate: </label>
                    <input type="number" class="text" v-model="cross_rate">
                </div>
                <p></p>
                <div v-if = "gp_loc" class="inputs">
                    <label>Enter Mutation Rate: </label>
                    <input type="number" class="text" v-model="mut_rate">
                </div>
                <p></p>
                <div v-if = "gp_loc" class="inputs">
                    <label>Enter Desired Number of Elites: </label>
                    <input type="number" class="text" v-model="elite_count">
                </div>
                <p></p>
                <div v-if = "gp_loc" class="inputs">
                    <label>Enter Tournament Size: </label>
                    <input type="number" class="text" v-model="tournament_size">
                </div>
                <p></p>
                <div v-if = "gp_loc" class="inputs">
                    <label>Enter Maximum Driver Count: </label>
                    <input type="number" class="text" v-model="drivers_num">
                </div>
                <p></p>
                <div v-if = "gp_loc" class="inputs">
                    <label>Enter Maximum Constructor Count: </label>
                    <input type="number" class="text" v-model="construtors_num">
                </div>
                <p></p>
                <div v-if = "gp_loc" class="inputs">
                    <button class="button" @click="submitData" v-on:keyup.enter="submitData" >Submit Inputs</button>
                    <!-- <p>Summary: {{ returnedData }}</p> -->
                </div>
            </div>

            <div v-if="gp_loc">
                <p class="title">Optimizer Inputs Information</p>
                <div class="info">
                    <p><span class="underline">Year:</span> Current Year of the F1 Season</p>
                    <p><span class="underline">Race Weekend:</span> Location name in which the Race is taking place</p>
                    <p><span class="underline">Available Budget:</span> The budget available for the given week (in millions)</p>
                    <p><span class="underline">Maximum Optimizer Evolutions:</span> The number of evolutions for which the optimizer will execute </p>
                    <p><span class="underline">Population Set Size:</span> Number of candidate solutions in a Evolution</p>
                    <p><span class="underline">Crossover Rate:</span> Probability of creating sub-canditates (childern) based on candidates (parents)</p>
                    <p><span class="underline">Mutation Rate:</span> Probability of random changes in candidate solutions' attributes</p>
                    <p><span class="underline">Elitism Count:</span> Number of top solutions directly passed to the next Evolution</p>
                    <p><span class="underline">Tournament Size:</span> Number of candidates competing for selection during Crossover Operations</p>
                    <p><span class="underline">Maximum Number of Drivers:</span> Maximum drivers allowed on a given F1 Fantasy Team</p>
                    <p><span class="underline">Maximum Number of Constructors:</span> Maximum constructors allowed on a given F1 Fantasy Team</p>
                </div>
            </div>
        </div>
    </keep-alive>
</template>

<script>
import apiClient from '../axios';
export default {
    name: "InputsUI",
    data() {
        return {
            year: 2024,
            gp_locs: [], 
            gp_loc: null,
            budget: 100,
            max_gens: 150,
            pop_set: 50,
            cross_rate: 0.8,
            mut_rate: 0.5,
            elite_count: 1,
            tournament_size: 40,
            drivers_num: 5,
            construtors_num: 2
        };
    },
    // watch: {
    //     gp_loc(newVal,prevVal) {
    //     },
    // },
    mounted() {
        this.getRaceLocs();
    },
    methods: {
        submitData() {
            apiClient.post('/inputs/inputs_submit/',{
                year: this.year,
                raceLoc: this.gp_loc,
                budget: this.budget,
                max_gens: this.max_gens,
                pop_set: this.pop_set,
                crossover_rate: this.cross_rate,
                mutation_rate: this.mut_rate,
                elite_counts: this.elite_count,
                tournament_size: this.tournament_size,
                max_drivers_num: this.drivers_num,
                max_constructors_num: this.construtors_num,
            }).then(response => {
                console.log(response.data);
            })
        },
        getRaceLocs() {
            apiClient.get('/inputs/gp_locs/')
            .then(response => {this.gp_locs = response.data.entity})
        },
    }
};
</script>

<style scoped>
.tab-content-grid {
    display: grid;
    grid-template-columns: 50% 50%;
    gap: 10px;
    height: 100%;
}
.left-content {
    border-right: 2px dashed #D12F2F;
}
.title {
    justify-content: center;
    padding-left: 2px;
    font-size: 16pt;
}
.info {
    text-align: left;
    padding-left: 2px;
    font-size: 12pt;
}
.underline {
    text-decoration: underline;
}
.inputs {
    display: flex;
    justify-content:left;
    flex-direction: row;
    margin-bottom: 10px;
    flex-wrap: wrap;
    gap: 10px;
    font-size: 11pt;
}
.text {
    width: 50px;
    justify-content: right;
}
</style>