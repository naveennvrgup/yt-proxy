import React, { useState, useEffect } from 'react'
import './App.css';

function App() {
  const [videos, setVideos] = useState([])
  const [prev, setPrev] = useState(null)
  const [next, setNext] = useState(null)
  const [pageNo, setPageNo] = useState(1)
  const [pageSize, setPageSize] = useState('10')


  const fetch_videos = (pgno, psize) => {
    fetch(`http://localhost:8002/api/ytproxy/?page=${pgno}&page_size=${psize}`)
      .then(d => d.json())
      .then(d => {
        setVideos(d['results'])
        setPrev(d['previous'])
        setNext(d['next'])
        setPageNo(pgno)
        setPageSize(psize)
      })
  }

  const previousPageChangeHandler = () => {
    fetch_videos(pageNo - 1, pageSize)
  }

  const nextPageChangeHandler = () => {
    fetch_videos(pageNo + 1, pageSize)
  }

  const pageSizeChangeHandler = e => {
    fetch_videos(1, e.target.value)
  }

  useEffect(() => {
    fetch_videos(1)
  }, [])


  const Pagination = (props) => {
    return <div className='d-flex align-items-center my-3 align-content-around'>
      <button onClick={previousPageChangeHandler} disabled={prev === null} className="btn btn-sm btn-outline-">previous</button>
      <div className="mx-3">{pageNo}</div>
      <button onClick={nextPageChangeHandler} disabled={next === null} className="btn btn-sm btn-outline-default">next</button>
      {props.pageSizeSelector ? <select className='form-control mx-3' value={pageSize} onChange={pageSizeChangeHandler}>
        <option value="10">10</option>
        <option value="5">5</option>
        <option value="20">20</option>
        <option value="50">50</option>
      </select> : null}
    </div>
  }

  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

  let videos_mapped = videos.map((ele, i) => {
    let timestamp = new Date(ele['publish_time'])

    return <div key={i} className='video'>
      <img src={ele['thumbnail_url']} alt="thumbnail" />
      <div className='title'>{ele['title'].slice(0, 50)}...</div>
      <div className='desc'>{ele['description'].slice(0, 180)}</div>
      <div className='time'>{monthNames[timestamp.getMonth()]} {timestamp.getDate()}, {timestamp.getHours() % 12==0?12:timestamp.getHours() % 12} {timestamp.getHours() >= 12 && timestamp.getHours() <24 ? "PM" : "AM"}</div>
    </div>
  })

  return (
    <div className="App bg" >
      <nav className="navbar navbar-dark bg-dark" >
        <div className="navbar-brand brand-name">YT-Proxy</div>
        <ul className="navbar-nav mx-auto">
          <li className="nav-item active">
            <div className="nav-link punch-line">[ We are a backup for youtube's news videos ]</div>
          </li>
        </ul>
      </nav>

      <div className='container'>
        <div className="m-5 px-5 py-3 wrapper">
          <div className="d-flex justify-content-center flex-wrap">
            <Pagination pageSizeSelector={true} />
          </div>
          <div className="d-flex justify-content-center flex-wrap">
            {videos_mapped}
          </div>
          <div className="d-flex justify-content-center flex-wrap">
            <Pagination />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;