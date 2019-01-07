// Creates a _todo object
export default function Todo(id, name, created) {
    this.id = id;
    this.name = name;
    this.created = created;
    this.completed = false;
}