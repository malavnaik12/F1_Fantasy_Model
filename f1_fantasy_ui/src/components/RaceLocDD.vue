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
        <footer class="footer">
        All Logo Copyrights belong to
        <a href="https://www.formula1.com/" target="_blank" rel="noopener"> 2003-2024 Formula One World Championship Limited</a>
        </footer>
        <footer class="footer1">
        Rest of the Content belongs to Malav Naik 2024
        </footer>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: "RaceLocDD",
    data() {
        return {
            entities: [], // Array to store entities from text file
            selectedEntity: null // The selected entity
        };
    },
    mounted() {
      // Fetch the text file content when the component is mounted
        fetch('/inputs_files/gp_list.txt')
            .then(response => response.text())
            .then(text => {
            this.entities = text.split('\n').filter(entity => entity.trim() !== '');
            });
    },
    methods: {
        submitData() {
            this.getRaceLoc();
        },
        getRaceLoc() {
            axios.post('http://localhost:8000/api/submit', 
            { raceName: this.selectedEntity })
            .then(response => {
                console.log('Response from server:', response.data)});
        }
    }
};
</script>

<style>
.footer {
position:   sticky;
padding-top: 400px;
}
.footer1 {
    position: sticky;
    padding-top: 10px;
}
</style>