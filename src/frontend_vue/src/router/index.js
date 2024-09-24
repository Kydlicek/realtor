import { createRouter, createWebHistory } from 'vue-router';
import HomeComponent from '../views/HomeView.vue';
import ListingsComponent from '../views/ListingsView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeComponent,
  },
  {
    path: '/listings',
    name: 'listings',
    component: ListingsComponent,
    props: true, // Enable passing route params as props
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
