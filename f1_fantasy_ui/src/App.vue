<template>
  <div class="app-container">
    <img alt="Vue logo" src="./assets/F1_logo.png">
    <h1>F1 Fantasy Team Builder App</h1>
    <h2>[Under Development]</h2>
  <div class="app-container">
    <nav class="nav-tabs">
      <router-link to="/" class="tab" active-class="active-tab">Positions</router-link>
      <router-link to="/prices" class="tab" active-class="active-tab">Prices</router-link>
      <router-link to="/inputs" class="tab" active-class="active-tab">Optimizer Inputs</router-link>
      <router-link to="/generate" class="tab" active-class="active-tab">Generate Team</router-link>
    </nav>
    <div class="tab-content">
      <router-view></router-view>
    </div>
  </div>
    <footer class="app-container">
      All Logo Copyrights belong to
      <a href="https://www.formula1.com/" target="_blank" rel="noopener"> 2003-2024 Formula One World Championship Limited</a>
    </footer>
    <footer class="app-container">
      Rest of the Content belongs to Malav Naik 2024
    </footer>
    <footer class="app-container">
      Fastapi-based backend implemeted in Python also hosted on Render.
      <a href="https://f1-fantasy-model-backend.onrender.com/docs" target="_blank" rel="noopener"> Link to FastAPI docs page</a>.
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {
  }
}
</script>

<style scoped>
.app-container {
  font-family: 'Titillium Web', sans-serif;
  margin: 0 auto;
  padding: 5px; /* Softer padding */
  max-width: 800px;
  text-align: center;
  background-color: #ffffff; /* Soft light gray background */
}

.nav-tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  border-bottom: 2px solid #666; /* Softer dark gray bottom border */
}

.tab {
  padding: 10px 20px;
  margin: 0 5px;
  text-decoration: none;
  color: #666; /* Soft dark gray text color */
  font-weight: bold;
  border-radius: 5px 5px 0 0;
  background-color: #ddd; /* Light gray background */
  transition: background-color 0.3s, color 0.3s;
}

.tab:hover {
  background-color: #D12F2F; /* Softened red for hover state */
  color: #fff; /* White text on hover */
}

.active-tab {
  background-color: #D12F2F; /* Softer red for active tab */
  color: white;
  border-bottom: 2px solid #D12F2F; /* Match active tab border with background */
}

.tab-content {
  padding: 20px;
  background-color: #ffffff; /* White background for content */
  border: 1px solid #ccc; /* Soft light gray border */
  border-radius: 5px;
  min-height: 200px;
  color: #333; /* Softer dark gray text for content */
}
</style>
