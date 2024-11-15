<!-- Enter Maximum number of Generations: 150 -->
<!-- Enter Size of the Population Set: 50 -->
<!-- Enter Crossover Probability: 0.8 -->
<!-- Enter Mutation Rate:  0.9-->
<!-- Enter Elitism Rate:  1-->
<!-- Enter Tournament Size Proportion: 0.9-->
<!-- Enter The Number of Current Race Week: Not needed-->
<!-- Enter The Maximum Number of Drivers Allowed: 5 -->
<!-- Enter The Maximum Number of Constructors Allowed: 2 -->
<!-- Enter the Weekly Budget: 100 -->
<template>
    <keep-alive>
        <div>
            <div class="inputs">
                <label>F1 Season Year: </label>
                <input type="number" id="driver1_pos" v-model="year">
            </div>
            <p></p>
            <div class="inputs">
                <label for="entity-dropdown">Select Race Weekend: </label>
                <select id="entity-dropdown" v-model="gp_loc" @change="getSessions">
                    <option v-for="entity in gp_locs" :key="entity" :value="entity">
                        {{ entity }}
                    </option>
                </select>
            </div>
            <p></p>
            <button @click="submitData" v-on:keyup.enter="submitData" >Next</button>
            <p>Summary: {{ returnedData }}</p>
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
            gp_locs: [], // Array to store gp_locs from text file
            gp_loc: null, // The selected entity
            sessions: [],
            session: null,
            // constructors: [],
            // constructor: null,
            // session_info_full: [],
            // session_info_1: [],
            // session_info_2: [],
            // session_prices: Array(20).fill(null),
            // loading_info: false,
            // constructor_prices: Array(10).fill(null),
        };
    },
    watch: {
        gp_loc(newVal,prevVal) {
            console.log(newVal,prevVal);
            // if (newVal !== prevVal) {
            //     this.session='';
            //     this.session_prices=Array(20).fill(null);
            //     this.constructor_prices=Array(10).fill(null);
            //     }
        },
        session(newVal,prevVal) {
            console.log(newVal,prevVal);
            // if (newVal !== prevVal) {
            //     this.session_prices=Array(20).fill(null);
            //     this.constructor_prices=Array(10).fill(null);
            //     }
        }
    },
    mounted() {
        this.getRaceLocs();
    },
    methods: {
        submitData() {
            apiClient.post('/inputs/prices_submit/',{
                year: this.year,
                raceLoc: this.gp_loc,
                session: this.session,
                // drivers: this.session_info_full,
                // driver_prices: this.session_prices,
                // constructors: this.constructors,
                // constructor_prices: this.constructor_prices
            }).then(response => {
                console.log(response);
            })
        },
        getRaceLocs() {
            apiClient.get('/inputs/gp_locs/')
            .then(response => {this.gp_locs = response.data.entity})
        },
        getSessions() {
            apiClient.post('/inputs/sessions/',{
                raceLoc: this.gp_loc
            }).then(response => {
                this.sessions = response.data.entity})
        },
    }
};
</script>

<style scoped>
.inputs {
    display: flex;
    justify-content:left;
    flex-direction: row;
    margin-bottom: 10px;
    flex-wrap: wrap;
    gap: 10px;
    font-size: 11pt;
}
</style>