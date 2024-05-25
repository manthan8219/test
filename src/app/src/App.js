import "./App.css";
import logo from "./logo.svg";
import usePostTodo from "./usePostTodo.js";
import useGetTodos from "./useTodos.js";
import { useState } from "react";

export function App() {
  const [todos, loading] = useGetTodos("https://localhost:8000/todos");
  const [newTodo, setNewTodo] = useState("");
  const [postResponse, postLoading, postError, postTodo] = usePostTodo(
    "https://localhost:8000/todos",
    { title: newTodo }
  );

  console.log(newTodo);

  const handleSubmit = (e) => {
    e.preventDefault();
    postTodo();
  };

  return (
    <div className="App">
      <div>
        <h1>List of TODOs</h1>
        <li>Learn Docker</li>
        <li>Learn React</li>
      </div>
      <div>
        <h1>Create a ToDo</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label for="todo">ToDo: </label>
            <input
              type="text"
              id="todo"
              value={newTodo}
              onChange={(e) => setNewTodo(e.target.value)}
            />
          </div>
          <div style={{ marginTop: "5px" }} disabled={postLoading}>
            <button type="submit">
              {postLoading ? "Adding..." : "Add ToDo!"}
            </button>
          </div>
          <ul>
            {todos && todos.map((todo) => <li key={todo.id}>{todo.title}</li>)}
          </ul>
        </form>
      </div>
      {postError && <div>Error posting todo</div>}
      {postResponse && <div>Todo added successfully!</div>}
    </div>
  );
}

export default App;
