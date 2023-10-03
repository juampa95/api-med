export default function PatientBox({name, lastname, personal_id, code, id}){
    return(
        <article>
            <h3>{name}</h3>
            <p>{lastname}</p>
            <p>{personal_id}</p>}
            <p>{code}</p>
            <p>{id}</p>
        </article>
    )
}