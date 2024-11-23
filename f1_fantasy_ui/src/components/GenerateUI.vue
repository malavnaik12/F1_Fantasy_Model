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
                    <button class="button" @click="submitData" v-on:keyup.enter="submitData" >Generate Team</button>
                </div>
            </div>

            <div v-if="gp_loc">
                <p class="title">Optimizer Results Summary</p>
                <div class="info">
                    {{best_team}}
                </div>
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
        };
    },
    mounted() {
        this.getRaceLocs();
    },
    methods: {
        submitData() {
            apiClient.post('/generate/generate_team/',{
                year: this.year,
                raceLoc: this.gp_loc,
            }).then(response => {
                this.best_team = response.data.entity;
            })
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
    border-right: 2px dashed #D12F2F;
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
</style>