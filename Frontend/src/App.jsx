import { useState, useEffect} from 'react'

import reactLogo from './assets/react.svg'
import { getStudents } from "./services/studentApi";


function App() {
    const [students, setStudents] = useState([]);

    useEffect(() => {
        loadStudents();
    }, []);

    const loadStudents = async () => {
        try {
          
            const response = await getStudents();
            console.log(response.data);  
            setStudents(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div>
            <h1>Student Management</h1>

            {students.map((student) => (
                <div key={student.id}>
                    <h3>{student.name}</h3>
                    <p>{student.age}</p>
                    <p>{student.course}</p>
                </div>
            ))}
        </div>
    );
}

export default App
