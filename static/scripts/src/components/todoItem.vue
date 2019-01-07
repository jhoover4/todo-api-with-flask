<template>
    <div class="item" :class="{ 'editing-item': isEditing, 'completed': todo.completed, 'edited': editMade }">
        <input type="checkbox" :checked="todo.completed"/>
        <span @click="markCompleted"></span>
        <label v-show="!isEditing" @click="editing">{{ todo.name }}</label>
        <!--suppress CommaExpressionJS -->
        <input class="editing-label" v-show="isEditing" @blur="doneEditing(), $emit('editing-complete')"
               type="text" :value="todo.name"/>
        <div class="actions">
            <button @click="$emit('save')">Save</button>
            <button class="delete" @click="$emit('delete')">Delete</button>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'TodoItem',
        props: {
            todo: Object
        },
        data() {
            return {
                isEditing: false,
                editMade: false
            }
        },
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
    }
</script>
