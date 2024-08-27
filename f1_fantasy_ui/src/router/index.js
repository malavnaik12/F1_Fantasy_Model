import { createRouter, createWebHistory } from 'vue-router'
import PositionsUI from '../components/PositionsUI.vue'
import PricesUI from '../components/PricesUI.vue'
import InputsUI from '../components/InputsUI.vue'
import GenerateUI from '../components/GenerateUI.vue'

const routes = [
  { path: '/', name: 'Positions', component: PositionsUI},
  { path: '/prices', name: 'Prices', component: PricesUI},
  { path: '/inputs', name: 'Inputs', component: InputsUI},
  { path: '/generate', name: 'Generate', component: GenerateUI},
];

const router = createRouter({
    history: createWebHistory(),
  routes,
})

export default router;

