import { createApp } from 'vue'
import App from '@/App.vue'
import { Quasar } from 'quasar'
import quasarUserOptions from './quasar-user-options'
import VueResizeObserver from "vue-resize-observer"
import { createPinia } from 'pinia'
import './assets/set-operations/css/Glyphter.css'

const app = createApp(App)

app.use(Quasar, quasarUserOptions, createPinia())
app.use(createPinia())
app.use(VueResizeObserver)
app.mount('#app')


