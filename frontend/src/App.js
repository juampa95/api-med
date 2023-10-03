import {useEffect, useState} from "react";
import PatientBox from "./components/PatientsBox";

function App() {
  const [patients, setPatients]= useState([])
  useEffect(()=>{
    fetch('http://localhost:8000/patient/list')
        .then(res => res.json())
        .then(res => setPatients(res))
  }, [])
  return (
      <main>
        <h1>Medical app</h1>
          {
              patients.map(patients => (
                  <PatientBox name={patients.name} lastname={patients.lastname}
                              personal_id={patients.personal_id} code={patients.code}
                              key={patients.id} />

              ))
          }

      </main>
  );
}

export default App;
