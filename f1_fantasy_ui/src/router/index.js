import { createRouter, createWebHistory } from 'vue-router'
import MainUI from '../components/MainUI.vue'
import PositionsUI from '../components/PositionsUI.vue'
import PricesUI from '../components/PricesUI.vue'
import InputsUI from '../components/InputsUI.vue'
import GenerateUI from '../components/GenerateUI.vue'

const routes = [
  { path: '/', name: 'Main', component: MainUI},
  { path: '/positions', name: 'Positions', component: PositionsUI},
  { path: '/prices', name: 'Prices', component: PricesUI},
  { path: '/inputs', name: 'Inputs', component: InputsUI},
  { path: '/generate', name: 'Generate', component: GenerateUI},
];

const router = createRouter({
  history: createWebHistory(),
  base: process.env.BASE_URL, 
  routes,
})

export default router;

