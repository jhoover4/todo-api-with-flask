// Creates a _todo object
function Todo(id, name, created) {
    this.id = id;
    this.name = name;
    this.created = created;
    this.completed = false;
}


Vue.component('todo-item', {
    props: {
        todo: Object
    },
    data: function () {
        return {
            isEditing: false,
            editMade: false
        }
    },
    template: `
    <div class="item" :class="{ 'editing-item': isEditing, 'completed': todo.completed, 'edited': editMade }">
        <input type="checkbox" :checked="todo.completed"/>
        <span @click="markCompleted"></span>
        <label v-show="!isEditing" @click="editing">{{ todo.name }}</label>
        <input class="editing-label" v-show="isEditing" @focusout="" @blur="doneEditing(), $emit('editing-complete')" type="text" :value="todo.name"/>
        <div class="actions">
            <button @click="$emit('save')">Save</button>
            <button class="delete" @click="$emit('delete')">Delete</button>
        </div>
    </div>`,
    methods: {
        editing: function () {
            this.isEditing = !this.isEditing;
            this.editMade = true;
        },
        doneEditing: function () {
            this.isEditing = false;
        },
        markCompleted: function () {
            this.todo.completed = !this.todo.completed;
            this.editMade = true;
            this.$emit('todo-completed');
        }
    }
});

var app = new Vue({
    el: '#app',
    data: {
        todos: [],
        allTodoRoute: '/api/v1/todos',
        singleTodoRoute: '/api/v1/todos/'
    },
    methods: {
        convertToTodo: function (todoJson) {
            return new Todo(todoJson.id, todoJson.name, false);
        },
        updateTempTodo: function (todo) {
            todo.name = event.target.value;
        },
        sortTodos: function (todos) {
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
            for (i = 0; i <= this.todos.length; i++) {
                if (this.todos[i].id === id) {
                    this.todos.splice(i, 1);
                }
            }
        },
        addTodo: function () {
            const lastTodoId = this.$data.todos.slice(-1)[0].id;
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
});