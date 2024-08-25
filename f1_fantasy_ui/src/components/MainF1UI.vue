<template>
    <div>
        <div class="customDropdown" >
            <label for="entity-dropdown">Select Race Weekend: </label>
            <select id="entity-dropdown" v-model="gp_loc">
                <option v-for="entity in gp_locs" :key="entity" :value="entity">
                    {{ entity }}
                </option>
            </select>
        </div>
        <p></p>
        <div class="customDropdown">
            <label for="entity-dropdown">Select Race Weekend Session: </label>
            <select id="entity-dropdown" v-model="session">
                <option v-for="entity in sessions" :key="entity" :value="entity">
                    {{ entity }}
                </option>
            </select>
        </div>
        <p></p>
        <div class="customDropdown">
            <label for="entity-dropdown">Select Constructor: </label>
            <select id="entity-dropdown" v-model="constructor">
                <option v-for="entity in constructors" :key="entity" :value="entity">
                    {{ entity }}
                </option>
            </select>
            <!-- <button @click="submitConstructor" v-on:keyup.enter="submitConstructor" class="customDropdown">Next</button> -->
        </div>
        <p></p>
        <div class="customDropdown" v-if="drivers_available">
            <!-- <li>
            </li> -->
                <label>Input Position for {{ driver1 }}: </label>
                <input type="number" ref="driver1_pos">
                 <!-- v-on:keyup.enter="submitData"> -->
                <p></p>
                <label>Input Position for {{ driver2 }}: </label>
                <input type="number" ref="driver2_pos">
                 <!-- v-on:keyup.enter="submitData"> -->
                <!-- <button @click="postDriverPos" v-on:keyup.enter="postDriverPos" class="customDropdown">Set Positions</button> -->
        </div>
        <p></p>
        <!-- <input type="text" ref="userText" v-on:keyup.enter="submitData()"> -->
        <button @click="submitData" v-on:keyup.enter="submitData" class="customDropdown">Next</button>
        <p>Summary: {{ returnedData }}</p>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: "MainF1UI",
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
            drivers_available: false,
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
        this.getConstructors();
        // this.checkDrivers();
        },
    // watch: {
    //         driver1_pos(val){
    //             if (val>20 && val<1) {
    //                 this.driver1_pos = 20;
    //             }
    //         },
    //         driver2_pos(val){
    //             if (val>20 && val<1) {
    //                 this.driver2_pos = 20;
    //             }
    //         }
    //     },
    methods: {
        submitData() {
            if (this.drivers_available) {
                if ((20 >= this.$refs.driver1_pos.value >= 1) && (20 >= this.$refs.driver2_pos.value >= 1)) {
                    this.driver1_pos = this.$refs.driver1_pos.value
                    this.driver2_pos = this.$refs.driver2_pos.value
                }
            }
            this.postInputs();
        },
        getRaceLocs() {
            axios.get('https://f1-fantasy-model-backend.onrender.com/api/gp_locs/')
            // axios.get('http://10.0.0.159:8000/api/gp_locs/')
            .then(response => {this.gp_locs = response.data.entity})
            .catch((err) => console.log(err));
        },
        getSessions() {
            axios.get('https://f1-fantasy-model-backend.onrender.com/api/sessions/')
            // axios.get('http://10.0.0.159:8000/api/sessions/')
            .then(response => {this.sessions = response.data.entity})
            .catch((err) => console.log(err));
        },
        getConstructors() {
            axios.get('https://f1-fantasy-model-backend.onrender.com/api/constructors/')
            // axios.get('http://10.0.0.159:8000/api/sessions/')
            .then(response => {this.constructors = response.data.entity})
            .catch((err) => console.log(err));
        },
        checkDrivers() {
            if ((this.driver1!=="") && (this.driver2!=="") && !this.drivers_available) {
                this.drivers_available = true;
            }
        },
        setPos() {
            this.driver1_pos = this.$refs.driver1_pos.value
            this.driver2_pos = this.$refs.driver2_pos.value
            console.log(this.driver1_pos,this.driver2_pos)
        },
        // axios.post('https://f1-fantasy-model-backend.onrender.com/api/selected_constructor/',
        // {constructor: this.constructor})
        // // .then(response => {this.returnedData = response.data});
        postInputs() {
            axios.post('https://f1-fantasy-model-backend.onrender.com/api/submit/',
            // axios.post('http://10.0.0.159:8000/api/submit',
            { 
                raceLoc: this.gp_loc,
                session: this.session,
                constructor: this.constructor,
                driver1: this.driver1,
                driver2: this.driver2,
                driver1_pos: this.driver1_pos,
                driver2_pos: this.driver2_pos,
            })
            .then(response => {
                this.returnedData = response.data,
                this.driver1 = response.data.entity.driver1,
                this.driver2 = response.data.entity.driver2,
                this.checkDrivers();
            });
        }
    }
};
</script>

<style scoped>
  .customDropdown {
    /* border: 1.5px dashed red;
    background-color: rgb(244, 171, 171); */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    /* align-content: right; */
    /* margin: 0;
    position: relative */
  }
</style>