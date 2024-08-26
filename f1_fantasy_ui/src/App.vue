<template>
  <img alt="Vue logo" src="./assets/F1_logo.png">
  <h1>F1 Fantasy Team Builder App</h1>
  <h2>[Under Development]</h2>
  <MainF1UI>

  </MainF1UI>
  <footer class="footer">
    All Logo Copyrights belong to
    <a href="https://www.formula1.com/" target="_blank" rel="noopener"> 2003-2024 Formula One World Championship Limited</a>
    </footer>
  <footer class="footer1">
    Rest of the Content belongs to Malav Naik 2024
  </footer>
  <footer class="footer1">
    Fastapi-based backend implemeted in Python also hosted on Render.
    <a href="https://f1-fantasy-model-backend.onrender.com/docs" target="_blank" rel="noopener"> Link to FastAPI docs page</a>.
  </footer>
</template>

<script>
// import MainUI from './components/MainUI.vue';
import MainF1UI from './components/MainF1UI.vue';

export default {
  name: 'App',
  components: {
    MainF1UI
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
  margin-top: 0px;
}
.footer {
  position:   sticky;
  padding-top: 300px;
}
.footer1 {
  position: sticky;
  padding-top: 10px;
}
</style>
