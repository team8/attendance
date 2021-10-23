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
    }

    console.log("START " + present)

    return (
        <div className="App">
            <LoginForm onAdd={login}/>
            <PresentPeople present={present}/>
        </div>
    );
}