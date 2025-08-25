
import React from 'react'
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import TicketNew from './pages/TicketNew'
import Navbar from './components/Navbar'

const isAuthed = () => !!localStorage.getItem('token')

const Private = ({ children }) => (isAuthed() ? children : <Navigate to="/login" />)

export default function App() {
  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', background: '#f8fafc', minHeight: '100vh' }}>
      <Navbar />
      <div style={{ maxWidth: 960, margin: '24px auto', background: '#fff', padding: 16, borderRadius: 12, boxShadow: '0 6px 24px rgba(0,0,0,.06)' }}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Private><Dashboard /></Private>} />
          <Route path="/new" element={<Private><TicketNew /></Private>} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </div>
  )
}
