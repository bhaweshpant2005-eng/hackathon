
import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api'
import TicketCard from '../components/TicketCard'

export default function Dashboard() {
  const [tickets, setTickets] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    (async () => {
      try {
        const { data } = await api.get('/tickets/')
        setTickets(data)
      } catch (e) {
        setError('Failed to load tickets')
      } finally {
        setLoading(false)
      }
    })()
  }, [])

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>My Tickets</h2>
        <Link to="/new">+ New Ticket</Link>
      </div>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'crimson' }}>{error}</p>}
      <div style={{ display: 'grid', gap: 12 }}>
        {tickets.map(t => <TicketCard key={t.id} ticket={t} />)}
      </div>
    </div>
  )
}

