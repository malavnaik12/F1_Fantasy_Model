<template>
  <img alt="Vue logo" src="./assets/F1_logo.png">
  <h1>F1 Fantasy Team Builder App</h1>
  <MainUI> 
    
  </MainUI>
</template>

<script>
import MainUI from './components/MainUI.vue';

export default {
  name: 'App',
  components: {
    MainUI
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
