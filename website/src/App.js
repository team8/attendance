import './App.css';
import LoginForm from "./components/LoginForm";
import PresentPeople from "./components/PresentPeople";
import {useState} from "react";

export default function App() {
    const [present, setPresent] = useState([])

    const login = (text) => {
        console.log("Requesting to add " + text);

        const request_options = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ id: parseInt(text) })
        }

        fetch("http://127.0.0.1:3030/api/login", request_options)
            .then(response => response.json())
            .then(data => {
                if (data.valid) {
                    if (data.leaving) {
                    } else {
                        setPresent([...present, {
                            name: data.name,
                            id: parseInt(text)
                        }])
                    }
                }
            })
    }

    console.log("START " + present)

    return (
        <div className="App">
            <LoginForm onAdd={login}/>
            <PresentPeople present={present}/>
        </div>
    );
}