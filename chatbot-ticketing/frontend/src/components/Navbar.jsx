
import React from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function Navbar() {
  const nav = useNavigate()
  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    nav('/login')
  }
  return (
    <div style={{ background: '#0f172a', color: '#fff', padding: '10px 16px' }}>
      <div style={{ maxWidth: 960, margin: '0 auto', display:'flex', justifyContent:'space-between', alignItems:'center' }}>
        <Link to="/" style={{ color: '#fff', textDecoration: 'none', fontWeight: 700 }}>Chatbot Ticketing</Link>
        <div style={{ display: 'flex', gap: 12 }}>
          <Link to="/" style={{ color:'#fff' }}>Dashboard</Link>
          <Link to="/new" style={{ color:'#fff' }}>New</Link>
          <button onClick={logout}>Logout</button>
        </div>
      </div>
    </div>
  )
}
