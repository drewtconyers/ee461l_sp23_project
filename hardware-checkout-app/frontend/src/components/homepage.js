import React, {useState} from 'react';
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import './style.css';
import {useLocation} from 'react-router-dom';
import axios from 'axios';

function Projects(props){
  const { projects, id, hwSet } = props;
  return (
    <div>
      {projects.map(project => (
        <ProjectCard key={project.id} project={project} userId={id} hwSet={hwSet}/>
      ))}
    </div>
  );
}

function ProjectCard(props){
  const { project, userId, hwSet} = props;
  const id = project.id;
  const [availableHardware, setAvailableHardware] = useState(hwSet);
  const [isMember, setIsMember] = useState(project.isMember);
  


  const handleJoin = (event) =>{
    setIsMember(true);
    event.preventDefault();
    axios.post('http://localhost:5000/join',{
      projectId: id,
      userId: userId
    })
    .then(response => {
      console.log(response.data);
    })
    .catch(error =>{
      console.error(error);
    })
  }

  const handleLeave = (event) => {
    setIsMember(false);

    event.preventDefault();
    axios.post('http://localhost:5000/leave',{
      projectId: id,
      userId: userId
    })
    .then(response => {
      console.log(response.data);
    })
    .catch(error =>{
      console.error(error);
    })

  }

  return(
    <Card variant="outlined">
    <CardContent>
      <ProjectTitle title={project.name} />
      <ProjectAuthorized authorized={project.Users} />
      <ProjectHardware hardware={availableHardware} isMember={isMember}/>
      <ProjectButtons isMember={isMember} onJoin={handleJoin} onLeave={handleLeave} />
    </CardContent>
  </Card>
  );
}


function ProjectTitle(props) {
  const { title } = props;
  return <Typography variant="h5" component="h2">{title}</Typography>;
}

function ProjectAuthorized(props) {
  const { authorized } = props;
  const list = authorized.join(', ');
  return <Typography variant="body2" component="p">{list}</Typography>;
}

function ProjectHardware(props) {
  const {hardware, isMember} = props;
  return(
    <div>
          {hardware.map(item =>(
              <HardwareItem key ={item} name ={item} isMember ={isMember}/>
          ))}
    </div>
  );
}

function HardwareItem(props){
  const {name, isMember} = props;
  const [numHardware, setNumHardware] = useState();
  const [availHardware, setAvailHardware] = useState();
  const [change, setChange] = useState(0);

  axios.post('http://localhost:5000/getnumhardware',{
    name: name
  })
  .then(response =>{
    console.log(response.data);
    const arr = response.data;
    setNumHardware(arr[0]);
    setAvailHardware(arr[1]);
  })
  .catch(error => {
    console.log(error);
  });

  const handleCheckout = (event) =>{
    if(isMember){
      event.preventDefault();
      axios.post('http://localhost:5000/checkouthardware',{
        change: change,
        name: name
      })
      .then(response =>{
        console.log(response.data);
        if(response.data.status === true){
          setAvailHardware(response.data.number);
        }else{
          alert("Check-out request exceeds available amount")
        }
      })
      .catch(error => {
        console.log(error);
      });
    }
  }

  const handleCheckin = (event) =>{
    if(isMember){
      // setAvailHardware(parseInt(availHardware) + parseInt(change));
      event.preventDefault();
      axios.post('http://localhost:5000/checkin',{
        change: change,
        name: name
      })
      .then(response =>{
        console.log(response.data);
        if(response.data.status === true){
          setAvailHardware(response.data.number);
        }else{
          alert("Check-in request exceeds the capacity")
        }
      })
      .catch(error => {
        console.log(error);
      });
    }
  }
  
  const handleChange = (event) =>{
    setChange(event.target.value);
  }

  return(
    <div>
      <span style={{ fontWeight: 'bold' }}>{name}:</span>
      {availHardware}/{numHardware}
      <input
      type="number"
      id='qty'
      name='qty'
      onChange={handleChange}
      />
      <Button  type='submit' variant='outlined' color='primary' onClick={handleCheckin}>
        Check In
      </Button>
      <Button type='submit' variant='outlined' color='primary' onClick={handleCheckout}>
        Check Out
      </Button>
    </div>
  );
}

function ProjectButtons(props) {
  const { isMember, onJoin, onLeave } = props;

  if (isMember) {
    return (
      <Button variant="contained" color="secondary" onClick={onLeave}>
        Leave
      </Button>
    );
  }

  return (
    <Button variant="contained" color="primary" onClick={onJoin}>
      Join
    </Button>
  );
}

export default function HomePage() {
  const [joinProject, setJoinProject] = useState("");
  const location = useLocation();
  const [data, setData] = useState([]);
  const [hwset, setHwset] = useState([]);
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [id, setId] = useState('');
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  const handleButton = (event) =>{
    event.preventDefault();
    axios.post('http://localhost:5000/home',{
      userId: location.state.userId
    })
    .then(response => {
      console.log(response.data);
      setData(JSON.parse(response.data));
      console.log(data);
    })
    .catch(error =>{
      console.error(error);
    })
    axios.post('http://localhost:5000/gethardware')
    .then(response =>{
      setHwset(response.data);
    })
    .catch(error => {
      console.log(error);
    });
  }
  const handleSubmit = (event) =>{
    event.preventDefault();
    axios.post('http://localhost:5000/join',{
      projectId: joinProject,
      userId: location.state.userId
    })
    .then(response => {
      console.log(response.data);
      if(response.data.success === true){
        alert("Joined Project ID:" + joinProject + " successfully\nClick LOAD PROJECTS to see the project");
      }
    })
    .catch(error =>{
      console.error(error);
    })
    setJoinProject('');
  }
  const handleButtonClick = (event) =>{
    event.preventDefault();
    setIsPopupOpen(true);
  }
  const handleCreateProject = (event) =>{
    event.preventDefault();
    axios.post('http://localhost:5000/create',{
      id: id,
      name: name,
      description: description
    })
    .then(response => {
      console.log(response.data);
    })
    .catch(error =>{
      console.error(error);
    })
    setId('');
    setName('');
    setDescription('');
  }
      
  return(
  <div>
      <Typography variant="h3" component="h1"> {location.state.userId}'s Projects</Typography>
      <center>
      <form onSubmit={handleSubmit} className="form-inline">
      <div className="body">
          <label>Join Project</label>
          <input
            type="text"
            className="form-control"
            value={joinProject}
            placeholder="Enter Project ID"
            onChange={event => setJoinProject(event.target.value)}
          />
          <Button  type='submit' variant='outlined' color='primary' onClick={handleSubmit}>
            Join
          </Button>
        </div>
      </form>
      <br/>
      <div>
      <Button variant='contained' color='primary' onClick={handleButtonClick}>
        Create a new Project
      </Button>
      {isPopupOpen && (
        <div className="popup">
        <form onSubmit={handleCreateProject}>
          <div>
          <label>
            <input
              type="text"
              className="form-control"
              placeholder="Enter Project ID"
              value={id}
              onChange={(event) => setId(event.target.value)}
            />
          </label>
          </div>
          <div>
          <label>
            <input
              type="text"
              className="form-control"
              placeholder="Enter Project Name"
              value={name}
              onChange={(event) => setName(event.target.value)}
            />
          </label>
          </div>
          <div>
          <label>
            <input
              type="text"
              className="form-control"
              placeholder="Enter Project Description"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
            />
          </label>
          </div>
          <button type="submit">Submit</button>
            <button type="button" onClick={() => setIsPopupOpen(false)}>
              Close
            </button>
          </form>
          </div>
      )}
      </div>
      <br/>
      <Button variant="contained" color="primary" onClick={handleButton}>
      Load Projects
      </Button> 
      </center>
      <Projects projects={data} id={location.state.userId} hwSet={hwset} />
    </div>
  );
}