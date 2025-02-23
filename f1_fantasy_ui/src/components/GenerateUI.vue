<template>
    <keep-alive>
        <div class="tab-content-grid">
            <div class="left-content">
                <p class="title">Optimizer Execution Inputs</p>
                <div class="inputs">
                    <label>F1 Season Year: </label>
                    <input type="number" class="text" v-model="year">
                </div>
                <p></p>
                <div class="inputs">
                    <label for="entity-dropdown">Current Race Weekend: </label>
                    <select id="entity-dropdown" v-model="gp_loc">
                        <option v-for="entity in gp_locs" :key="entity" :value="entity">
                            {{ entity }}
                        </option>
                    </select>
                </div>
                <p></p>
                <div v-if = "gp_loc" class="inputs">
                    <button class="button" @click="submitData" :disabled="loading">
                        Generate Team
                    </button>
                </div>
                <p></p>
                <div v-if="loading && gp_loc" class="spinner-container">
                    <div class="car-wrapper">
                        <img src="../assets/F1_car.png" alt="F1 Car" class="f1-car">
                    </div>
                </div>
            </div>

            <div class="right-content">
                <p class="title">Optimizer Results Summary</p>
                <div class="right-content-top" v-if="best_drivers.length>0">
                    <div class="team-item">
                        {{ best_drivers.at(0) }}        {{ best_drivers.at(1) }}        {{ best_drivers.at(2) }}
                    </div>
                    <p></p>
                    <div>
                                        {{ best_drivers.at(3) }}        {{ best_drivers.at(4) }}
                    </div>
                </div>
                    
                <div class="right-content-middle" v-if="best_constrs.length>0">
                    <div class="team-item">
                        {{ best_constrs.at(0) }}        {{ best_constrs.at(1) }}
                    </div>
                    <p></p>
                    <div class="team-item" v-if="best_price>0">
                        Total Team Cost of Best Team: {{ best_price }}
                    </div>
                </div>

                <!-- <div class="right-content-bottom" v-if="best_price>0">
                    <img src="../assets/ga_results.png" alt="ga_out_plot">
                </div> -->

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
            best_team: '',
            best_drivers: [],
            best_constrs: [],
            best_price: 0,
            loading: false,
        };
    },
    mounted() {
        this.getRaceLocs();
    },
    methods: {
        extract_team_info(team) {
            this.best_drivers = team.drivers
            this.best_constrs = team.constructors
            this.best_price = team.total_cost
        },
        async submitData() {
            this.loading = true;
            console.log(this.loading)
            apiClient.post('/generate/generate_team/',{
                year: this.year,
                raceLoc: this.gp_loc,
            }).then(response => {
                this.best_team = response.data.entity;
                this.loading=false;
                this.extract_team_info(this.best_team);
            })
            console.log(this.loading)
        },
        getRaceLocs() {
            apiClient.get('/generate/gp_locs/')
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
    /* border-right: 2px dashed #D12F2F; */
}
.right-content {
    display: grid;
    grid-template-rows: 40% 40% 20%;/*40% 40% 20%;*/
    /* height: 100%; */
    border-left: 2px dashed #D12F2F;
}
.right-content-top {
    border: 1px dashed #D12F2F;
    font-size: 12px;
    /* min-height: 50px;  */
    /* justify-content: center; */
    /* background-color: rgb(111, 110, 110); */
    /* border-radius: 20px; */
    color: black;
    /* padding-bottom: 15px; */
}
.right-content-middle {
    border: 1px dashed #D12F2F;
    font-size: 12px;
    /* min-height: 50px;  */
    /* justify-content: center; */
    /* background-color: rgb(111, 110, 110); */
    /* border-radius: 20px; */
    color: black;
    /* padding-bottom: 15px; */
}
.team-item {
    padding: 5px;
    color: black;
    font-size: 10pt;
}
/* .team-item:before {
    content: "";  
    display: block; 
    margin: 0 auto; 
    width: 50%; 
    padding: 5px; 
    padding-bottom: 25px;
    border-top: 5px solid red;
    border-left: 5px solid red; 
    border-right: 5px solid red; 
    left: 0px;
    top: 25%;
    position: relative;
} */
.right-content-bottom {
    border: 1px dashed #D12F2F;
    /* min-height: 50px;  */
    /* justify-content: center; */
    /* background-color: rgb(111, 110, 110); */
    /* border-radius: 20px; */
    color: black;
    /* padding-bottom: 15px; */
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
.spinner-container {
  /* position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 150px; 
  height: 150px;
  border: 20px solid black; 
  border-radius: 50%;  */
}

.car-wrapper {
  position: fixed;
  top: 50%; /* Start at the top of the circle */
  left: 50%; /* Center horizontally */
  transform: translate(-0%, 0); /* Align horizontally */
  transform-origin: center 100px; /* Pivot at the center of the circle */
  animation: spin 3s linear infinite;
}

.f1-car {
  width: 50px; 
  height: auto;
  transform: rotate(0deg); /* Keep it aligned along the path */
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>