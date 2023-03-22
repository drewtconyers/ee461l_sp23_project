import React, { Component, useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css'

export default function SignUp() {
    const [userId, setUserId] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
  
    const handleSubmit = (event) =>{
      event.preventDefault();

      axios.post('http://localhost:5000/signup',{
        userId: userId,
        username: username,
        password: password
      })
      .then(response => {
        console.log(response.data);
      })
      .catch(error =>{
        console.error(error);
      })
    }
    return (
      <form onSubmit={handleSubmit}> 
        <h3>Sign Up</h3>

        <div className="mb-3">
          <label>User ID</label>
          <input
            type="text"
            className="form-control"
            placeholder="Enter User ID"
            onChange={event => setUserId(event.target.value)}
          />
        </div>

        <div className='mb-3'>
          <label>Username</label>
          <input 
            type="text" 
            className="form-control"
            placeholder="Enter Username"
            onChange={event => setUsername(event.target.value)}
            />
        </div>

        <div className="mb-3">
          <label>Password</label>
          <input
            type="password"
            className="form-control"
            placeholder="Enter password"
            onChange={event => setPassword(event.target.value)}
          />
        </div>

        <div className="d-grid">
          <button type="submit" className="btn btn-primary">
            Sign Up
          </button>
        </div>
      </form>
    );
}
