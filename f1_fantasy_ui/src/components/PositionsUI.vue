<template>
    <keep-alive>
    <div class="tab-content-grid">
        <div class="left-content">
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
            <div v-if="gp_loc" class="inputs">
                <label for="entity-dropdown">Select Session: </label>
                <select id="entity-dropdown" v-model="session" @change="getSessionInfo">
                    <option v-for="entity in sessions" :key="entity" :value="entity">
                        {{ entity }}
                    </option>
                </select>
            </div>
            <p></p>
            <div v-if="session && data_not_available" class="inputs">
                <label for="override">Override Existing Data?</label>
                <input type="checkbox" id="override" v-model="data_override" @change="postConstructor">
            </div>
            <p></p>
            <div v-if="data_override" class="inputs">
                <label for="entity-dropdown">Select Constructor: </label>
                <select id="entity-dropdown" v-model="constructor" @change="postConstructor">
                    <option v-for="entity in constructors" :key="entity" :value="entity">
                        {{ entity }}
                    </option>
                </select>
            </div>
            <p></p>
            <div  v-if="data_override && drivers_available" class="inputs">
                <label>Input Position for {{ driver1 }}: </label>
                <input type="number" id="driver1_pos" v-model="driver1_pos">
            </div>
            <p></p>
            <div  v-if="data_override && drivers_available" class="inputs">
                <label>Input Position for {{ driver2 }}: </label>
                <input type="number" id="driver2_pos" v-model="driver2_pos">
            </div>
            <p></p>
            <div v-if="data_override && drivers_available" class="inputs">
                <label for="temp_driver">Any Substitute Drivers?</label>
                <input type="checkbox" id="temp_driver" v-model="substitute_driver" >
            </div>
            <p></p>
            <div v-if="data_override && substitute_driver" class="inputs">
                <label>Input Sub Driver Name: </label>
                <input type="text" id="substitute_driver_name" v-model="substitute_driver_name">
            </div>
            <p></p>
            <div v-if="data_override && substitute_driver" class="inputs">
                <label>Input Position for Sub Driver: </label>
                <input type="number" id="substitute_driver_pos" v-model="substitute_driver_pos">
            </div>
            <p></p>
            <div class="inputs">
                <button class="button" @click="submitData" v-on:keyup.enter="submitData" >Next</button>
                <p>Summary: {{ message }}</p>
            </div>
            <div v-if="gp_loc && session" class="inputs">
                <button class="button-reload" @click="reloadSessionInfo" v-on:keyup.enter="reloadSessionInfo" >Reload Info</button>
            </div>
        </div>
        
        <div class="right-content">
            <p v-if="session" class="grid_title">{{ gp_loc }} GP {{ session }} Results</p>
            <!-- <p></p> -->
            <div v-if="session" class="session_grid">
                <div class="session_grid_right">
                    <div v-for="n in session_info_1" :key="n" class="grid-item">
                    <!-- <div v-for="n in 10" :key="n" class="grid-item"> -->
                        {{ n }}
                    </div>
                    
                </div>
                <div class="session_grid_left">
                    <div v-for="n in session_info_2" :key="n" class="grid-item">
                        {{ n }}
                    </div>
                </div>
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
            year: 2024,
            gp_locs: [], // Array to store gp_locs from text file
            gp_loc: null, // The selected entity
            sessions: [],
            session: null,
            data_not_available: false,
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
            message: '',
            session_info_1: [],
            session_info_2: [],
        };
    },
    watch: {
        gp_loc(newVal,prevVal) {
            console.log(newVal,prevVal);
            if (newVal !== prevVal) {
                this.clearFields();
                }
        },
    },
    mounted() {
        this.getRaceLocs();
        },
    methods: {
        populateSessionInfo(response) {
            if (!response) {
                this.data_not_available = true
            } else {
                this.returnedData = response.data.entity
                this.session_info_1 = response.data.entity.filter((_, index) => index % 2 === 0);
                this.session_info_2 = response.data.entity.filter((_, index) => index % 2 === 1);
            }
        },
        submitData() {
            if (this.drivers_available && !this.substitute_driver) {
                if (20 < this.driver1_pos < 0) {
                    this.driver1_pos = 0
                } else if (20 < this.driver2_pos < 0) {
                    this.driver2_pos = 0
                } else {
                    this.postDriver();
                }
            } else if (this.substitute_driver) {
                if ((20 < this.substitute_driver_pos < 0)) {
                    this.substitute_driver_pos = 0
                } else {
                    this.postDriver();
                }
            }
            this.postConstructor();
            this.getSessionInfo();
        },
        getRaceLocs() {
            apiClient.get('/api/gp_locs/')
            .then(response => {
                this.gp_locs = response.data.entity})
        },
        getSessions() {
            this.gp_loc_selected = true
            apiClient.post('/api/sessions/',{
                raceLoc: this.gp_loc
            }).then(response => {
                this.sessions = response.data.entity,
                this.getConstructors()})
        },
        getSessionInfo() {
            this.session_info_1 = Array.apply(null,Array(10));
            this.session_info_2 = Array.apply(null,Array(10));
            apiClient.post('/api/session_info/',{
                year: this.year,
                raceLoc: this.gp_loc,
                session: this.session,
            }).then(response => {
                this.populateSessionInfo(response);
            })
        },
        getConstructors() {
            apiClient.get('/api/constructors/')
            .then(response => {
                this.constructors = response.data.entity;
                // this.drivers_available = !this.drivers_available
            })
            .catch((err) => console.log(err));
        },
        checkDrivers() {
            if ((this.driver1!=="") && (this.driver2!=="") && !this.drivers_available) {
                this.drivers_available = true;
            }
        },
        postConstructor() {
            apiClient.post('/api/drivers/',
            { 
                raceLoc: this.gp_loc,
                data_override: this.data_override,
                session: this.session,
                constructor: this.constructor,
                driver1: this.driver1,
                driver2: this.driver2,
                driver1_pos: this.driver1_pos,
                driver2_pos: this.driver2_pos,
            })
            .then(response => {
                // this.returnedData = response.data,
                this.constructor = response.data.entity.constructor,
                this.driver1 = response.data.entity.driver1,
                this.driver2 = response.data.entity.driver2,
                this.checkDrivers();
            });
        },
        postDriver() {
            apiClient.post('/api/submit/',
            { 
                raceLoc: this.gp_loc,
                data_override: this.data_override,
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
                this.message = response.data.entity;
                // this.clearFields();
                // this.message = response.data.entity;
            });
        },
        clearFields() {
            this.session='',
            this.data_override=false,
            this.constructor='',
            this.driver1="",
            this.driver2="",
            this.drivers_available=false,
            this.driver1_pos=0,
            this.driver2_pos=0,
            this.substitute_driver=false,
            this.substitute_driver_name="",
            this.substitute_driver_pos=0;
        },
        reloadSessionInfo() {
            this.session_info_1 = [];
            this.session_info_2 = [];
            this.getSessionInfo()
        }
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
.reload {
    display: flex;
    justify-content:right;
    flex-direction: row;
    margin-bottom: 10px;
    flex-wrap: wrap;
    gap: 10px;
    font-size: 11pt;
}
.tab-content-grid {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Creates two equal-width columns */
    gap: 10px;
    height: 100%;
}
.grid-item {
    /* display: flex; */
    /* justify-content: center; */
    padding: 5px;
    color: black;
    /* background-color: #f5f5f5;  */
    /* border-top: 5px solid #0a0101; */
    /* width: 50%; */
    font-size: 10pt;

}
.grid-item:before {
    content: ""; /* This is necessary for the pseudo element to work. */ 
    display: block; /* This will put the pseudo element on its own line. */
    margin: 0 auto; /* This will center the border. */
    width: 50%; /* Change this to whatever width you want. */
    padding-bottom: 25px; /* This creates some space between the element and the border. */
    border-top: 5px solid white; 
}
.grid-item:before {
    content: "";  
    display: block; 
    margin: 0 auto; 
    width: 50%; 
    padding: 5px; 
    border-left: 5px solid white; 
    border-right: 5px solid white; 
    left: 0px;
    top: 25%;
    position: relative;
}
.session_grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr); /* 2 columns */
    grid-template-rows: repeat(10, auto); /* 10 rows */
    height: 100%;
}
.session_grid_right, .session_grid_left {
    display: grid;
    height: 100%;
    /* margin: 10px; */
}

.session_grid_left {
    padding: 10px;
}

.right-content {
    min-height: 250px; 
    border-left: 2px dashed #D12F2F;
    justify-content: center;
    background-color: rgb(111, 110, 110);
    border-radius: 20px;
    color: black;
    padding-bottom: 15px;
}

.button {
    border-radius: 2px;
    height: 20px;
    width: 50px;
}
.button-reload {
    border-radius: 2px;
    height: 40px;
    width: 60px;
}
.grid_title {
    justify-content: center;
}
</style>