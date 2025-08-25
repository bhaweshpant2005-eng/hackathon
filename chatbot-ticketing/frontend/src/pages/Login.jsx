

import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'

export default function Login() {
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('admin123')
  const [error, setError] = useState('')
  const nav = useNavigate()

  const onSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const { data } = await api.post('/auth/login', { email, password })
      localStorage.setItem('token', data.token)
      localStorage.setItem('user', JSON.stringify(data.user))
      nav('/')
    } catch (e) {
      setError(e.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <form onSubmit={onSubmit} style={{ maxWidth: 420, margin: '32px auto' }}>
      <h2>Login</h2>
      <div style={{ display: 'grid', gap: 12 }}>
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button type="submit">Sign in</button>
      </div>
      {error && <p style={{ color: 'crimson' }}>{error}</p>}
      <p style={{ marginTop: 12, fontSize: 14, color: '#555' }}>Use /auth/register to create a new user in API.</p>
    </form>
  )
}
