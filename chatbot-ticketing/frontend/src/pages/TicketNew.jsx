
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'

export default function TicketNew() {
  const [subject, setSubject] = useState('Internet not working')
  const [description, setDescription] = useState('WiFi down in hostel room 23')
  const [priority, setPriority] = useState('medium')
  const nav = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    await api.post('/tickets/', { subject, description, priority })
    nav('/')
  }

  return (
    <form onSubmit={submit} style={{ display: 'grid', gap: 12 }}>
      <h2>New Ticket</h2>
      <input value={subject} onChange={e=>setSubject(e.target.value)} placeholder="Subject" />
      <textarea value={description} onChange={e=>setDescription(e.target.value)} placeholder="Describe your issue" rows={5} />
      <select value={priority} onChange={e=>setPriority(e.target.value)}>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
      <button type="submit">Create</button>
    </form>
  )
}

