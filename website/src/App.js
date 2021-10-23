import './App.css';
import LoginForm from "./components/LoginForm";
import PresentPeople from "./components/PresentPeople";
import {useState} from "react";

export default function App() {
    const [present, setPresent] = useState([])

    const login = (text) => {
        setPresent([...present, {
            name: text,
            id: text
        }])

        const request_options = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ title: 'React POST Request Example' })
        }

        fetch("http://127.0.0.1:3030/api/posts", request_options).then(r => console.log("Done"))
    }

    console.log("START " + present)

    return (
        <div className="App">
            <LoginForm onAdd={login}/>
            <PresentPeople present={present}/>
        </div>
    );
}