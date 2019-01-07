<template>
    <div id="todos">
        <div class="list">
            <div class="add">
                <a href="#" v-on:click="addTodo">+ Add a New Task</a>
            </div>
            <todo-item
                    v-for="todo in todos"
                    v-bind:key="todo.id"
                    v-bind:todo="todo"
                    v-on:delete="deleteTodo(todo)"
                    v-on:save="saveTodo(todo)"
                    v-on:editing-complete="updateTempTodo(todo)"
                    v-on:todo-completed="sortTodos()"
            ></todo-item>
        </div>
    </div>
</template>


<script>
    import todoItem from './todoItem.vue'
    import Todo from './todo.js'

    export default {
        name: 'todos',
        components: {
            todoItem
        },
        data() {
            return {
                todos: [],
                allTodoRoute: '/api/v1/todos',
                singleTodoRoute: '/api/v1/todos/',
            }
        },
        methods: {
            convertToTodo: function (todoJson) {
                return new Todo(todoJson.id, todoJson.name, false);
            },
            updateTempTodo: function (todo) {
                todo.name = event.target.value;
            },
            sortTodos: function () {
                this.todos.sort((a, b) => ((a.completed === b.completed) ? 0 : a.completed ? 1 : -1));
            },
            createFetchHeaders: function (todo, method, username = 'jhoover', password = 'test') {
                return {
                    method: method,
                    headers: {
                        'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Authorization': 'Basic ' + btoa(username + ":" + password)
                    },
                    body: `id=${todo.id}&name=${todo.name}`
                };
            },
            getAllTodos: function () {
                fetch(this.allTodoRoute)
                    .then(response => response.json())
                    .then((jsonData) => {
                        jsonData.forEach(el => {
                            this.todos.push(this.convertToTodo(el));
                        })
                    }).catch(error => console.log('Request failed', error));
            },
            deleteTodo: function (todo) {
                if (todo.created) {
                    this.deleteTempTodo(todo.id);
                } else {
                    this.deleteServerTodo(todo.id);
                    this.deleteTempTodo(todo.id);
                }
            },
            deleteServerTodo: function (id) {
                const options = {
                    method: 'delete',
                    headers: {
                        'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    },
                };

                fetch(this.$data.singleTodoRoute + id, options)
                    .catch(err => {
                        console.error('Request failed', err)
                    })
            },
            deleteTempTodo: function (id) {
                for (let i = 0; i <= this.todos.length; i++) {
                    if (this.todos[i].id === id) {
                        this.todos.splice(i, 1);
                    }
                }
            },
            addTodo: function () {
                let lastTodoId;

                if (this.todos.length > 0) {
                    lastTodoId = this.$data.todos.slice(-1)[0].id;
                } else {
                    lastTodoId = 0
                }

                const newTodoId = lastTodoId + 1;

                const todo = new Todo(newTodoId, "New task!", true);
                this.todos.push(todo);
            },
            saveTodo: function (todo) {
                if (todo.created) {
                    this.insertTodo(todo);
                } else {
                    this.updateTodo(todo);
                }
            },
            insertTodo: function (todo) {
                const options = this.createFetchHeaders(todo, 'post');

                fetch(this.$data.allTodoRoute, options)
                    .then(response => response.json())
                    .then(jsonData => (todo = jsonData))
                    .catch(err => {
                        console.error('Request failed', err)
                    });

                todo.created = false;

                return todo;
            },
            updateTodo: function (todo) {
                const options = this.createFetchHeaders(todo, 'put');

                fetch(this.$data.singleTodoRoute + todo.id, options)
                    .then(response => response.json())
                    .catch(err => {
                        console.error('Request failed', err);
                        return false
                    });

                return true;
            },
        },
        mounted() {
            this.getAllTodos();
        }
    }
</script>
