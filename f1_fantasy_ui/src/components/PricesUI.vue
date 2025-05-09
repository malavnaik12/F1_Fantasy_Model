<template>
    <keep-alive>
    <div class="tab-content-grid">
        <div class="left-content">
            <div class="inputs">
                <label>F1 Season Year: </label>
                <input type="number" class="text" v-model="year">
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
            <div v-if="!session_prices.includes(null) || !constructor_prices.includes(null)" class="inputs">
                <button class="button" @click="submitData" v-on:keyup.enter="submitData" >Submit Prices</button>
            </div>
            <div v-if="loading_info" class="spinner">
                Loading...
            </div>
        </div>

        <div class="middle-content">
            <p v-if="session" class="grid_title">{{ gp_loc }} GP {{ session }} Results</p>
            <div v-if="session" class="session_grid">
                <div class="session_grid_right">
                    <div v-for="(driver, index) in session_info_1" :key="driver" class="grid-item">
                        P{{ 2*index+1 }}
                        <div>
                            {{ driver }}
                        </div>
                        <p></p>
                        <label>Price:</label>
                        <input class="price_input" type="number" v-model.number="session_prices[2*index]">
                    </div>
                    
                </div>
                <div class="session_grid_left">
                    <div v-for="(driver, index) in session_info_2" :key="driver" class="grid-item">
                        P{{ 2*index+2 }}
                        <div>
                            {{ driver }}
                        </div>
                        <p></p>
                        <label>Price: </label>
                        <input class="price_input" type="number" v-model.number="session_prices[2*index+1]">
                    </div>
                </div>
            </div>
        </div>

        <div class="right-content">
            <p v-if="session" class="grid_title">{{ gp_loc }} GP Race Week Constructor Price </p>
            <div v-if="session" class="constructor_grid">
                <div v-for="(key,index) in constructors" :key="key" class="team-item">
                    {{ key }}
                    <p></p>
                    <label>Price: </label>
                    <input class="price_input" type="number" v-model.number="constructor_prices[index]">
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
            constructors: [],
            constructor: null,
            session_info_full: [],
            session_info_1: [],
            session_info_2: [],
            session_prices: Array(20).fill(null),
            loading_info: false,
            constructor_prices: Array(10).fill(null),
        };
    },
    watch: {
        gp_loc(newVal,prevVal) {
            console.log(newVal,prevVal);
            if (newVal !== prevVal) {
                this.session='';
                this.session_prices=Array(20).fill(null);
                this.constructor_prices=Array(10).fill(null);
                }
        },
        session(newVal,prevVal) {
            console.log(newVal,prevVal);
            if (newVal !== prevVal) {
                this.session_prices=Array(20).fill(null);
                this.constructor_prices=Array(10).fill(null);
                }
        }
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
                driver_prices: this.session_prices,
                constructors: this.constructors,
                constructor_prices: this.constructor_prices
            }).then(response => {
                console.log(response);
            })
        },
        getRaceLocs() {
            apiClient.get('/prices/gp_locs/')
            .then(response => {this.gp_locs = response.data.entity})
        },
        getSessions() {
            apiClient.post('/prices/sessions/',{
                raceLoc: this.gp_loc
            }).then(response => {
                this.sessions = response.data.entity})
        },
        getSessionInfo() {
            this.loading_info = true
            this.session_info_1 = Array.apply(null,Array(10));
            this.session_info_2 = Array.apply(null,Array(10));
            apiClient.post('/prices/session_info/',{
                year: this.year,
                raceLoc: this.gp_loc,
                session: this.session,
            }).then(response => {
                console.log(response)
                this.populateSessionInfo(response);
            }).finally(this.loading_info = false)
        },
        populateSessionInfo(response) {
            if (response) {
                if (response.data.entity.driver_prices)
                    this.session_prices = response.data.entity.driver_prices
                this.session_info_full = response.data.entity.driver_positions
                this.session_info_1 = this.session_info_full.filter((_, index) => index % 2 === 0);
                this.session_info_2 = this.session_info_full.filter((_, index) => index % 2 === 1);
                if (Object.keys(response.data.entity.constructor_prices).length !== 0) {
                    this.constructors = response.data.entity.constructor_order
                    this.constructor_prices = response.data.entity.constructor_prices
                } else {
                    this.getConstructors();
                }
            }
        },
        getConstructors() {
            apiClient.get('/prices/constructors/')
            .then(response => {
                this.constructors = response.data.entity;
            })
        },
    }
};
</script>

<style scoped>
.spinner {
    font-size: 18px;
    font-weight: bold;
    color: #333;
    margin-top: 10px;
}
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
.left-content {
    border-right: 2px dashed #D12F2F;
}
.right-content {
    border-left: 2px dashed #D12F2F;
    justify-content: center;
}
.constructor_grid {
    text-align: center;
    height: 100%;
}
.team-item {
    padding: 15px;
    color: black;
    font-size: 10pt;
}
.team-item:before {
    content: "";  
    display: block; 
    margin: 0 auto; 
    width: 50%; 
    padding-bottom: 25px;
    border-top: 5px solid black;
    border-left: 5px solid black; 
    border-right: 5px solid black; 
    left: 0px;
    top: 25%;
    position: relative;
}
.middle-content {
    min-height: 250px; 
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
    width: 50px;
    border-radius: 5px;
}

.price_input:focus {
    border-color: #007bff; 
    outline: none;          
}
.text {
    width: 50px;
    justify-content: right;
}
</style>