import React, {useState, useEffect} from 'react'
import './App.css';

function App() {
  const [videos, setVideos] = useState([])
  const [prev, setPrev] = useState(null)
  const [next, setNext] = useState(null)

  
  useEffect(()=>{
    fetch('http://localhost:8002/api/ytproxy/')
    .then(d=>d.json())
    .then(d=>{
      console.log(d)
      setVideos(d['results'])
      setPrev(d['previous'])
      setNext(d['next'])
    })
  },[])

  let videos_mapped = videos.map(ele => <div>
    <img src={ele['thumbnail_url']} alt="thumbnail"/>
    <div>{ele['title']}</div>
    <div>{ele['description']}</div>
    <div>{ele['publish_time']}</div>
  </div>)
  
  return (
    <div className="App" >
      <nav className="navbar navbar-dark bg-dark" >
        <div className="navbar-brand brand-name">YT-Proxy</div>
        <ul className="navbar-nav mx-auto">
          <li className="nav-item active">
            <div className="nav-link punch-line">[ We are a backup for youtube's new videos ]</div>
          </li>
        </ul>
      </nav>

      <div>
          {videos_mapped}
      </div>
    </div>
  );
}

export default App;