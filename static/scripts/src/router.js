import Vue from 'vue'
import Router from 'vue-router'
import Login from './components/login.vue'
import Todos from './components/todos.vue'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            redirect: {
                name: 'login'
            }
        },
        {
            path: '/login',
            name: 'login',
            component: Login
        },
        {
            path: '/todos',
            name: 'todos',
            component: Todos
        }
    ]
})
