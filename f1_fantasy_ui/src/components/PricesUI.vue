<template>
    <keep-alive>
    <div class="tab-content-grid">
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
            <div v-if="gp_loc" class="inputs">
                <label for="entity-dropdown">Select Session: </label>
                <select id="entity-dropdown" v-model="session" @change="getSessionInfo">
                    <option v-for="entity in sessions" :key="entity" :value="entity">
                        {{ entity }}
                    </option>
                </select>
            </div>
            <p></p>
            <div v-if="!session_prices.includes(null)" class="inputs">
                <button class="button" @click="submitData" v-on:keyup.enter="submitData" >Next</button>
            </div>
        </div>

        <div class="right-content">
            <p v-if="session" class="grid_title">{{ gp_loc }} GP {{ session }} Results</p>
            <div v-if="session" class="session_grid">
                <div class="session_grid_right">
                    <div v-for="(driver, index) in session_info_1" :key="driver" class="grid-item">
                        {{ driver }}
                        <p></p>
                        <label>Price:</label>
                        <input class="price_input" type="number" v-model.number="session_prices[2*index]">
                    </div>
                    
                </div>
                <div class="session_grid_left">
                    <div v-for="(driver, index) in session_info_2" :key="driver" class="grid-item">
                        {{ driver }}
                        <p></p>
                        <label>Price: </label>
                        <input class="price_input" type="number" v-model.number="session_prices[2*index+1]">
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
    name: "PricesUI",
    data() {
        return {
            year: 2024,
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
            session_info_full: [],
            session_info_1: [],
            session_info_2: [],
            session_prices: Array(20).fill(null),
        };
    },
    mounted() {
        this.getRaceLocs();
        },
    methods: {
        submitData() {
            apiClient.post('/prices/prices_submit/',{
                year: this.year,
                raceLoc: this.gp_loc,
                session: this.session,
                drivers: this.session_info_full,
                prices: this.session_prices
            }).then(response => {
                console.log(response);
            })
        },
        getRaceLocs() {
            apiClient.get('/prices/gp_locs/')
            .then(response => {this.gp_locs = response.data.entity})
            .catch((err) => console.log(err));
        },
        getSessions() {
            console.log(this.gp_loc)
            apiClient.post('/prices/sessions/',{
                raceLoc: this.gp_loc
            }).then(response => {
                this.sessions = response.data.entity})
        },
        getSessionInfo() {
            this.session_info_1 = Array.apply(null,Array(10));
            this.session_info_2 = Array.apply(null,Array(10));
            console.log(this.year,this.raceLoc,this.session)
            apiClient.post('/prices/session_info/',{
                year: this.year,
                raceLoc: this.gp_loc,
                session: this.session,
            }).then(response => {
                this.populateSessionInfo(response);
            })
        },
        populateSessionInfo(response) {
            if (response) {
                this.session_info_full = response.data.entity
                this.session_info_1 = response.data.entity.filter((_, index) => index % 2 === 0);
                this.session_info_2 = response.data.entity.filter((_, index) => index % 2 === 1);
            }
        },
        getConstructors() {
            apiClient.get('/prices/constructors/')
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
        postInputs() {
            apiClient.post('/prices/submit/',
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
.tab-content-grid {
    display: grid;
    grid-template-columns: 40% 40% 20%;
    gap: 10px;
    height: 100%;
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
.right-content {
        min-height: 250px; 
        border-left: 2px dashed #D12F2F;
        border-right: 2px dashed #D12F2F;
        justify-content: center;
        background-color: rgb(111, 110, 110);
        border-radius: 20px;
        color: black;
        padding-bottom: 15px;
}
.grid-item {
    padding: 5px;
    color: black;
    font-size: 10pt;

}
.grid-item:before {
    content: "";  
    display: block; 
    margin: 0 auto; 
    width: 50%; 
    padding: 5px; 
    padding-bottom: 25px;
    border-top: 5px solid white;
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
}
.session_grid_left {
    padding: 10px;
}
.grid_title {
    justify-content: center;
}
.price_input {
    width: 50px;           /* Set the width */
    /* height: 40px;           Set the height */
    /* padding: 10px;          Add padding */
    /* font-size: 12px;        Adjust font size */
    border-radius: 5px;
    /* border: 2px solid #ccc; /* Add border */
    /* background-color: #f9f9f9;  Background color */
    /* color: #333;            Text color */ 
}

.price_input:focus {
    border-color: #007bff;  /* Change border color on focus */
    outline: none;          /* Remove default outline */
}
</style>