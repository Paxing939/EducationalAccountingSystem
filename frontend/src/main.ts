import { createApp } from 'vue'
import App from './App.vue'

import Professions from './Professions.vue'
import Students from './Students.vue'
import Graduation from './Graduation.vue'

import Vue3EasyDataTable from 'vue3-easy-data-table';
import 'vue3-easy-data-table/dist/style.css';

const app = createApp(App);
app.component('Professions', Professions);
app.component('Students', Students);
app.component('Graduation', Graduation);
app.component('EasyDataTable', Vue3EasyDataTable);
app.mount('#app')
