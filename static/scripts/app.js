// Creates a tdo object
function Todo(id, name) {
    this.id = id;
    this.name = name;
    this.edited = false;
    this.completed = false;
}


Vue.component('todo-item', {
    props: {
        todo: Object
    },
    template: `
    <div class="item">
        <input type="checkbox" v-on:click="markCompleted"/>
        <span></span>
        <label v-on:click="editing"></label>
        <input class="editing-label" type="text" v-bind:value="todo.name"/>
        <div class="actions">
            <a href="" v-on:click="updateTodo(todo.id, todo.name)">Save</a>
            <a href="" class="delete" v-on:click="deleteTodo(todo.id)">Delete</a>
        </div>
    </div>`,
    methods: {
        editing: function () {

        },
        markCompleted: function () {

        }
    }
});

var app = new Vue({
    el: '#app',
    data: {
        todos: [],
        currentTodo: null,
        allTodoRoute: '/api/v1/todos',
        singleTodoRoute: '/api/v1/todo/'
    },
    methods: {
        convertToTodo: function (todoJson) {
            let todo = new Todo(todoJson.id, todoJson.name);

            return todo;
        },
        getAllTodos: function () {
            fetch(this.allTodoRoute)
                .then(response => response.json())
                .then(jsonData => (jsonData.forEach(el => {
                    this.todos.push(this.convertToTodo(el));
                })).catch(error => console.log('Request failed', error)));
        },
        getSingleTodo: function (id) {
            let todo;

            fetch(this.$data.singleTodoRoute + id)
                .then(response => response.json())
                .then(jsonData => (todo = jsonData))
                .catch(error => console.log('Request failed', error));

            return todo;
        },
        updateTodo: function (id, name) {
            let todo;
            const options = {
                method: 'put',
                headers: {
                    'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
                },
                body: `id=${id}&name=${name}`
            };

            fetch(this.$data.singleTodoRoute + id, options)
                .then(response => response.json())
                .then(jsonData => (todo = jsonData))
                .catch(err => {
                    console.error('Request failed', err)
                });

            return todo;
        },
        deleteTodo: function (id) {
            let todo;
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
            this.todos.splice(index, 1);
        },
        saveTodos: function () {
            let filteredTodos = this.todos.filter(function (todo) {
                if (todo.edited) {
                    return todo;
                }
            });
            filteredTodos.forEach(function (todo) {
                if (todo.id) {
                    this.updateTodo(todo.id)
                } else {
                    this.createTodo(todo.id)
                }
            });
        },
        addTodo: function () {
            this.$data.todos.push({})
        },
        addTodoAPI: function () {
            let todo;
            const options = {
                method: 'post',
                headers: {
                    'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
                },
                body: `id=${id}&name=${name}`
            };

            fetch(this.$data.singleTodoRoute + id, options)
                .then(response => response.json())
                .then(jsonData => (todo = jsonData))
                .catch(err => {
                    console.error('Request failed', err)
                });

            return todo;
        }
    },
    mounted() {
        this.getAllTodos();
    }
});