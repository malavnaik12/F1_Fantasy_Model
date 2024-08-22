<template>
    <div>
        <label for="entity-dropdown">Select Race Weekend: </label>
        <select id="entity-dropdown" v-model="gp_loc">
        <option v-for="entity in gp_locs" :key="entity" :value="entity">
            {{ entity }}
        </option>
        </select>
        <p></p>
        <label for="entity-dropdown">Select Race Weekend Session: </label>
        <select id="entity-dropdown" v-model="session">
        <option v-for="entity in sessions" :key="entity" :value="entity">
            {{ entity }}
        </option>
        </select>
        <p></p>
        <!-- <input type="text" ref="userText" v-on:keyup.enter="submitData()"> -->
        <button @click="submitData" v-on:keyup.enter="submitData">Submit</button>
        <p>Summary: {{ returnedData }}</p>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: "RaceLocDD",
    data() {
        return {
            gp_locs: [], // Array to store gp_locs from text file
            gp_loc: null, // The selected entity
            sessions: [],
            session: null,
            data_override: true,
            constructors: [],
            constructor: null,
            driver1: "",
            driver2: "",
            driver1_pos: 0,
            driver2_pos: 0,
            substitute_driver: false,
            substitute_driver_name: "",
            substitute_driver_pos: 0,
            returnedData: '',
        };
    },
    mounted() {
        this.getRaceLocs();
        this.getSessions();
    },
    methods: {
        submitData() {
            this.postRaceLoc();
        },
        getRaceLocs() {
            //axios.get('http://localhost:8000/api/gp_locs/')
            axios.get('http://10.0.0.159:8000/api/gp_locs/')
            .then(response => {this.gp_locs = response.data.entity})
            .catch((err) => console.log(err));
        },
        getSessions() {
            // axios.get('http://localhost:8000/api/sessions/')
            axios.get('http://10.0.0.159:8000/api/sessions/')
            .then(response => {this.sessions = response.data.entity})
            .catch((err) => console.log(err));
        },
        postRaceLoc() {
            // axios.post('http://localhost:8000/api/submit',
            axios.post('http://10.0.0.159:8000/api/submit',
            { raceLoc: this.gp_loc , session: this.session})
            .then(response => {this.returnedData = response.data});
        }
    }
};
</script>

<style>

</style>