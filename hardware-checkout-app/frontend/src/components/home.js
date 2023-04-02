import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Projects({ username }) {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    const response = await axios.get('http://localhost:5000/api/projects');
    setProjects(response.data);
  };

  

  const joinProject = async (projectId) => {
    try {
      const response = await axios.post(`http://localhost:5000/api/projects/${projectId}/join`, { username });
      alert(response.data.message);
    } catch (error) {
      console.error('Error joining project:', error);
    }
  };

  const leaveProject = async (projectId) => {
    try {
      const response = await axios.post(`http://localhost:5000/api/projects/${projectId}/leave`, { username });
      alert(response.data.message);
    } catch (error) {
      console.error('Error leaving project:', error);
    }
  };


  // const [hardwareQty, setHardwareQty] = useState('');

  const handleCheckIn = async (projectId) => {
    try {
        const response = await axios.post(`http://localhost:5000/api/projects/${projectId}/check-in`, { qty: parseInt(hardwareQtys[projectId]) });
        if (response.data.error) {
            alert(response.data.error);
        } else {
            alert(`${response.data.qty} hardware checked in`);
        }
    } catch (error) {
        console.error('Error checking in hardware:', error);
    }
};

const handleCheckOut = async (projectId) => {
      try {
        const response = await axios.post(`http://localhost:5000/api/projects/${projectId}/check-out`, { qty: parseInt(hardwareQtys[projectId]) });
        if (response.data.error) {
            alert(response.data.error);
        } else {
            alert(`${response.data.qty} hardware checked in`);
        }
    } catch (error) {
        console.error('Error checking in hardware:', error);
    }
};

  const [hardwareQtys, setHardwareQtys] = useState({});

  const handleInputChange = (projectId, value) => {
      setHardwareQtys({ ...hardwareQtys, [projectId]: value });
  };

  return (
    <div>
      {projects.map(project => (
        <div key={project._id}>
          <h2>{project.name}</h2>
          <p>Hardware Quantity: {project.hardware_qty}</p>
          <p>Hardware Capacity: {project.hardware_cap}</p>
          <button onClick={() => joinProject(project._id)}>Join</button>
          <button onClick={() => leaveProject(project._id)}>Leave</button>
          <input
            type="number"
            value={hardwareQtys[project._id] || ''}
            onChange={(e) => handleInputChange(project._id, e.target.value)}
            placeholder="Enter hardware quantity"
        />
        <button onClick={() => handleCheckIn(project._id)}>Check In</button>
        <button onClick={() => handleCheckOut(project._id)}>Check Out</button>
      </div>
      ))}
    </div>
  );
};

export default function HomePage() {
    return(
    <div>
        <Projects projects={"test"} />
      </div>
    );
  }