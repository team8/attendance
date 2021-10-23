import React from "react";
import {useState} from "react";

const LoginForm = ({onAdd}) => {
    const [text, setText] = useState('')

    const onSubmit = (e) => {
        e.preventDefault()

        if (!text) {
            alert('Please add valid student ID')
            setText('')
            return;
        }
        let valid = /^\d+$/.test(text);
        valid &= text.length === 8
        if (!valid) {
            alert('Please add valid student ID')
            setText('')
            return
        }

        onAdd(text)
        setText('')
    }

    return (
        <form className='add-form' onSubmit={onSubmit}>
            <label>Login </label>
            <input type='text' placeholder='Student ID' value={text}
                   onChange={(e) => setText(e.target.value)}/>

            <input type='submit' placeholder='Login'/>
        </form>
    )
}

export default LoginForm;