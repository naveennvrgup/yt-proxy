import React, { useState, useEffect, Fragment } from 'react'
import './App.css';

// flexible base url for dev/prod
let baseurl=''
if(process.env.NODE_ENV === 'development'){
  baseurl='http://localhost:5557'
}


function App() {
  // states
  const [videos, setVideos] = useState([])
  const [prev, setPrev] = useState(null)
  const [next, setNext] = useState(null)
  const [pageNo, setPageNo] = useState(1)
  const [searchText, setSearchText] = useState('')
  const [orderBy, setOrderBy] = useState('-publish_time')
  const [pageSize, setPageSize] = useState('10')


  const fetch_videos = (pgno, psize, orderby, stext) => {
    const ordering = orderby.length===0?'':`&ordering=${orderby}`
    const searching = stext.length===0?'':`&search=${stext}`

    fetch(`${baseurl}/api/ytproxy/?page=${pgno}&page_size=${psize}${ordering}${searching}`)
      .then(d => d.json())
      .then(d => {
        setVideos(d['results'])
        setPrev(d['previous'])
        setNext(d['next'])
        setPageNo(pgno)
        setPageSize(psize)
        setOrderBy(orderby)
        setSearchText(stext)
      })
  }

  const previousPageChangeHandler = () => {
    fetch_videos(pageNo - 1, pageSize, orderBy,searchText)
  }

  const nextPageChangeHandler = () => {
    fetch_videos(pageNo + 1, pageSize, orderBy,searchText)
  }

  const pageSizeChangeHandler = e => {
    fetch_videos(1, e.target.value, orderBy,searchText)
  }

  const orderByChangeHandler = e => {
    fetch_videos(1, pageSize, e.target.value,searchText)
  }

  const onSearchHandler = e => {
    e.preventDefault();
    fetch_videos(1,pageSize,orderBy,searchText)
  }

  useEffect(() => {
    fetch_videos(1,10,orderBy,'')
  }, [])


  const filtering = <form className='d-flex justify-content-between align-items-center'>
      <input 
        onChange={e => setSearchText(e.target.value)}
        onSubmit={onSearchHandler}
        value={searchText}
        type='text' 
        placeholder='search by title' 
        className='ml-3 form-control' /> 
      <button 
        onClick={onSearchHandler}
        className='btn btn-primary ml-3'>Search</button>
      <select className='form-control ml-3' value={orderBy} onChange={orderByChangeHandler}>
        <option value="-publish_time">time (dsc)</option>
        <option value="+publish_time">time (asc)</option>
        <option value="+title">title (asc)</option>
        <option value="-title">title (dsc)</option>
        <option value="+description">description (asc)</option>
        <option value="-description">description (dsc)</option>
      </select>
      <select className='form-control ml-3' value={pageSize} onChange={pageSizeChangeHandler}>
        <option value="10">10</option>
        <option value="5">5</option>
        <option value="20">20</option>
        <option value="50">50</option>
      </select>
  </form>


  const Pagination = <div className='d-flex align-items-center my-3 align-content-around'>
      <button onClick={previousPageChangeHandler} disabled={prev === null} className="btn btn-sm btn-outline-">previous</button>
      <div className="mx-3">{pageNo}</div>
      <button onClick={nextPageChangeHandler} disabled={next === null} className="btn btn-sm btn-outline-default">next</button>
    </div>

  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

  let videos_mapped = videos.map((ele, i) => {
    let timestamp = new Date(ele['publish_time'])

    return <div key={i} className='video'>
      <img src={ele['thumbnail_url']} alt="thumbnail" />
      <div className='title'>{ele['title'].slice(0, 50)}...</div>
      <div className='desc'>{ele['description'].slice(0, 180)}</div>
      {/* building custom date format */}
      <div className='time'>{monthNames[timestamp.getMonth()]} {timestamp.getDate()}, {timestamp.getHours() % 12===0?12:timestamp.getHours() % 12} {timestamp.getHours() >= 12 && timestamp.getHours() <24 ? "PM" : "AM"}</div>
    </div>
  })

  return (
    <div className="App bg" >
      <nav className="navbar navbar-dark bg-dark" >
        <div className="navbar-brand brand-name">YT-Proxy</div>
        <ul className="navbar-nav mx-auto">
          <li className="nav-item">
            <span className="nav-link punch-line">[ We are a backup for youtube's news videos ]</span>
          </li>
        </ul>
        <a className="nav-link btn btn-success btn-sm" href='/docs/'>Swagger docs</a>
        <a className="nav-link btn btn-primary btn-sm ml-3" href='/admin/'>Django Admin</a>
      </nav>

      <div className='container'>
        <div className="m-5 px-5 py-3 wrapper">
          <div className="d-flex justify-content-between flex-wrap mx-3 mr-5">
            {filtering}
            {Pagination}
          </div>
          <div className="d-flex justify-content-center flex-wrap">
            {videos_mapped}
          </div>
          <div className="d-flex justify-content-center flex-wrap">
            {Pagination}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;