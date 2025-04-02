<template>
  <div class="app-container">
    <img alt="logo" src="./assets/F1_logo.png">
    <h1>F1 Fantasy Team Builder App</h1>
    <h2>[Under Development]</h2>
  <div class="app-container">
    <nav class="nav-tabs">
      <router-link to="/positions" class="tab" active-class="active-tab">Positions</router-link>
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
      Fastapi-based backend implemeted in Python also hosted on Render.
      <a href="https://f1-fantasy-model-backend.onrender.com/docs" target="_blank" rel="noopener"> Link to FastAPI docs page</a>.
    </footer>
    <footer class="app-container">
      Rest of the Content belongs to Malav Naik 2024. Code hosted on
      <a href="https://github.com/malavnaik12/F1_Fantasy_Model" target="_blank" rel="noopener"> GitHub</a>.
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
  padding: 2.5px; /* Consistent padding */
  max-width: 100%; /* Full width for mobile */
  text-align: center;
  background-color: #ffffff; /* Light gray background */
  /* border-radius: 5px; */
}

.nav-tabs {
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin-bottom: 15px;
  border-bottom: 2px solid #666; /* Softer dark gray bottom border */
  flex-wrap: wrap; /* Allows tabs to wrap on smaller screens */
}

.tab {
  padding: 10px 20px;
  margin: 5px; /* Adds margin for better spacing on mobile */
  text-decoration: none;
  color: #666; /* Soft dark gray text color */
  font-weight: bold;
  border-radius: 5px;
  background-color: #ddd; /* Light gray background */
  transition: background-color 0.3s, color 0.3s;
  flex: 1; /* Ensures tabs are evenly spaced on mobile */
  text-align: center; /* Center text in tabs */
}

.tab:hover {
  background-color: #D12F2F; /* Matte scarlet on hover */
  color: #fff; /* White text on hover */
}

.active-tab {
  background-color: #D12F2F; /* Matte scarlet for active tab */
  color: white;
  border-bottom: 2px solid #D12F2F; /* Match active tab border with background */
}

.tab-content {
  padding: 25px;
  background-color: #ffffff; /* White background for content */
  border: 1px solid #ccc; /* Soft light gray border */
  border-radius: 15px;
  /* border-left: 12px solid #666; */
  /* border: 2px solid #D12F2F;
  grid-row: 1/2; */
  min-height: 200px;
  color: #333; /* Softer dark gray text for content */
}

@media (max-width: 768px) {
  .tab {
    padding: 10px; /* Adjust padding for smaller screens */
    font-size: 14px; /* Slightly smaller font on mobile */
  }
  
  .tab-content {
    padding: 15px; /* Adjust content padding for mobile */
  }
}
</style>
