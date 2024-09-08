<template>
    <keep-alive>
    <div>
            <div class="inputs">
                <label for="entity-dropdown">Select Race Weekend: </label>
            <select id="entity-dropdown" v-model="gp_loc">
                <option v-for="entity in gp_locs" :key="entity" :value="entity">
                    {{ entity }}
                </option>
            </select>
        </div>
        <p></p>
        <div v-if="gp_loc" class="inputs">
            <label for="override">Override Existing Data?</label>
            <input type="checkbox" id="override" v-model="data_override" @change="override" >
        </div>
        <p></p>
        <div v-if="data_override" class="inputs">
            <label for="entity-dropdown">Select Session: </label>
            <select id="entity-dropdown" v-model="session">
                <option v-for="entity in sessions" :key="entity" :value="entity">
                    {{ entity }}
                </option>
            </select>
        </div>
        <p></p>
        <div v-if="data_override" class="inputs">
            <label for="entity-dropdown">Select Constructor: </label>
            <select id="entity-dropdown" v-model="constructor">
                <option v-for="entity in constructors" :key="entity" :value="entity">
                    {{ entity }}
                </option>
            </select>
        </div>
        <p></p>
        <div  v-if="drivers_available" class="inputs">
            <label>Input Position for {{ driver1 }}: </label>
            <input type="number" ref="driver1_pos">
        </div>
        <p></p>
        <div  v-if="drivers_available" class="inputs">
            <label>Input Position for {{ driver2 }}: </label>
            <input type="number" ref="driver2_pos">
        </div>
        <p></p>
        <div class="inputs">
            <button @click="submitData" v-on:keyup.enter="submitData" >Next</button>
            <p>Summary: {{ returnedData }}</p>
            <div v-if="message" class="inputs">
                <p>Message? {{ message }}</p>
            </div>
        </div>
    </div>
    </keep-alive>
</template>

<script>
import apiClient from '../axios';
export default {
    name: "PositionsUI",
    data() {
        return {
            gp_locs: [], // Array to store gp_locs from text file
            gp_loc: null, // The selected entity
            sessions: [],
            session: null,
            data_override: false,
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
            message: ''
        };
    },
    mounted() {
        this.getRaceLocs();
        // this.getSessions();
        // this.getConstructors();
        // this.checkDrivers();
        },
    // watch: {
    //     override_check(data_override){
    //         if (data_override) {
    //             this.getConstructors();
    //         }
    //     }
    // },
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
        override() {
            // this.data_override = !this.data_override;
            // this.getConstructors();
            this.getSessions();
        },
        submitData() {
            if (this.drivers_available) {
                if ((20 >= this.$refs.driver1_pos.value >= 1) && (20 >= this.$refs.driver2_pos.value >= 1)) {
                    this.driver1_pos = this.$refs.driver1_pos.value
                    this.driver2_pos = this.$refs.driver2_pos.value
                    this.postDriver();
                }
            }
            this.postConstructor();
        },
        getRaceLocs() {
            apiClient.get('/api/gp_locs/')
            .then(response => {this.gp_locs = response.data.entity})
            .catch((err) => console.log(err));
        },
        getSessions() {
            apiClient.post('/api/sessions/',{
                raceLoc: this.gp_loc
            })
            .then(response => {
                this.sessions = response.data.entity,
                this.getConstructors()})
            .catch((err) => console.log(err));
        },
        getConstructors() {
            apiClient.get('/api/constructors/')
            .then(response => {this.constructors = response.data.entity})
            .catch((err) => console.log(err));
        },
        checkDrivers() {
            if ((this.driver1!=="") && (this.driver2!=="") && !this.drivers_available) {
                this.drivers_available = true;
            }
        },
        // setPos() {
        //     this.driver1_pos = this.$refs.driver1_pos.value
        //     this.driver2_pos = this.$refs.driver2_pos.value
            // console.log(this.driver1_pos,this.driver2_pos)
        // },
        postConstructor() {
            apiClient.post('/api/drivers/',
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
                this.constructor = response.data.entity.constructor;
                this.driver1 = response.data.entity.driver1,
                this.driver2 = response.data.entity.driver2,
                this.checkDrivers();
            });
        },
        postDriver() {
            apiClient.post('/api/submit/',
            { 
                raceLoc: this.gp_loc,
                session: this.session,
                constructor: this.constructor,
                driver1: this.driver1,
                driver2: this.driver2,
                driver1_pos: this.driver1_pos,
                driver2_pos: this.driver2_pos,
                substitute_driver: this.substitute_driver,
                substitute_driver_name: this.substitute_driver_name,
                substitute_driver_pos: this.substitute_driver_pos,
            })
            .then(response => {
                this.returnedData = response.data,
                this.message = response.data.entity;
            });
        }
    }
};
</script>

<style scoped>
.inputs {
    display: flex;
    flex-direction: row;
    justify-content:left;
    margin-bottom: 10px;
    flex-wrap: wrap;
    gap: 10px;
    font-size: 11pt;
}
/* .inputs-drivers {
    display:flex;
    flex-direction: row;
    place-content:left;
    margin-bottom: 10px;
    flex-wrap: wrap;
    gap: 10px;
} */
/* position: relative; */
/* padding: 15px; */
</style>