<template>
    <div>
        <label for="entity-dropdown">Select Race Weekend: </label>
        <select id="entity-dropdown" v-model="selectedEntity">
        <option v-for="entity in entities" :key="entity" :value="entity">
            {{ entity }}
        </option>
        </select>
        <p></p>
        <button @click="submitData">Submit</button>
        <p>Summary: {{ returnedData }}</p>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: "RaceLocDD",
    data() {
        return {
            entities: [], // Array to store entities from text file
            selectedEntity: null, // The selected entity
            returnedData: ''
        };
    },
    mounted() {
        this.getRaceLocs();
    },
    methods: {
        submitData() {
            this.postRaceLoc();
        },
        getRaceLocs() {
            axios.get('http://localhost:8000/api/get_list/')
            // axios.get('http://10.0.0.159:8000/api/get_list/')
            .then(response => {this.entities = response.data.entity})
            .catch((err) => console.log(err));
        },
        postRaceLoc() {
            axios.post('http://localhost:8000/api/submit',
            // axios.post('http://10.0.0.159:8000/api/submit',
            { raceName: this.selectedEntity })
            .then(response => {this.returnedData = response.data.entity});
        }
    }
};
</script>

<style>

</style>