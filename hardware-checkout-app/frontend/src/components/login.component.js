import React, { useState } from 'react';
import { useNavigate } from "react-router-dom"
import axios from 'axios';
import './style.css';

export default function Login() {
  const[userId, setUserId] = useState("");
  const[password, setPassword] = useState("");
  const navigate =useNavigate();
  const handleSubmit = (event) =>{
    event.preventDefault();

    axios.post('http://localhost:5000/login',{
      userId: userId,
      password: password
    })
    .then(response => {
      console.log(response.data.success);
      if(response.data.success === true){
        navigate("/home", {state:{userId: userId}});
      }else{
        alert("incorrect userID or password")
      }
    })
    .catch(error =>{
      console.error(error);
    })
  }

    return (
      <div className="auth-wrapper">
      <div className="auth-inner">
      <form onSubmit={handleSubmit}>
        <h3>Login</h3>

        <div className="mb-3">
          <label>User ID</label>
          <input
            type="text"
            className="form-control"
            placeholder="Enter User ID"
            onChange={event => setUserId(event.target.value)}
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
            Submit
          </button>
        </div>
      </form>
      </div>
      </div>
    )
  }
