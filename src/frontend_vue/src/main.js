import './assets/main.css'
import { createAuth0 } from '@auth0/auth0-vue';

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)
app.use(
    createAuth0({
        domain: "dev-z7katmlnvcvupi8a.us.auth0.com",
        clientId: "6G6xwuYGBMwu2mgQ56EkJ6B9KqwZ0Emc",
        authorizationParams: {
            redirect_uri: window.location.origin
        }
    })
);

app.mount('#app')
