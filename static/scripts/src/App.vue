<template>
    <div id="app">
        <div id="nav">
            <router-link v-if="authenticated" to="/login" v-on:click.native="logout()" replace>Logout</router-link>
        </div>
        <router-view @authenticated="setAuthenticated"/>
    </div>
</template>


<script>
    import Login from './components/login.vue'
    import Todos from './components/todos.vue'

    export default {
        name: 'App',
        components: {
            Login,
            Todos
        },
        data() {
            return {
                authenticated: false,
                mockAccount: {
                    username: "jhoover",
                    password: "test"
                },
                authorizationToken: ''
            }
        },
        methods: {
            setAuthenticated(status) {
                this.authenticated = status;
            },
            logout() {
                this.authenticated = false;
            }
        },
        mounted() {
            if (!this.authenticated) {
                this.$router.replace({name: "login"});
            }
        }
    }
</script>
