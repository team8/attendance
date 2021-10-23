import React from "react";

const PresentPeople = (props) => {
    console.log(props.present + "END")
    return (
        <div>
            <h2>People at Lab</h2>
            {props.present.map((person) => <p key={person.id}> {person.name} </p>)}
        </div>
    )
}

export default PresentPeople