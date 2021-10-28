import React from "react";
import {useState} from "react";
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';


const LoginForm = ({onAdd}) => {
    const [text, setText] = useState('')
    const [error, setError] = useState(false)

    const isValid = (t) => {
        let valid = /^\d+$/.test(t);
        valid &= t.length === 8
        valid |= t.length === 0
        if (!valid) {
            setError(true);
            setText(t);
            alert("invalid");
            return false;
        } else {
            alert("valid");
            setError(false);
            setText(t);
            return true;
        }
    }

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();

            if (isValid(text)) {
                onAdd(text)
            }
            setText('')
        }
    }

    return (
        <Box
            component="form"
            sx={{
                '& .MuiTextField-root': { m: 1, width: '25ch' },
            }}
            noValidate
            autoComplete="off"
        >
            <div>
                <TextField
                    error={error}
                    id="outlined-error"
                    label="Student ID"
                    defaultValue={text}
                    value={text}
                    onKeyUp={handleKeyDown}

                    onChange={s => isValid(s.target.value)}
                />
            </div>
        </Box>
    )
}

export default LoginForm;