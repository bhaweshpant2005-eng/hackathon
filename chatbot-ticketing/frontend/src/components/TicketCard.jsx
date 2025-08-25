
import React from 'react'

export default function TicketCard({ ticket }) {
  return (
    <div style={{ border: '1px solid #e5e7eb', padding: 12, borderRadius: 10 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <strong>{ticket.subject}</strong>
        <span>{ticket.status}</span>
      </div>
      <p style={{ color: '#555' }}>{ticket.description}</p>
      <small>Priority: {ticket.priority} • Category: {ticket.category}</small>
    </div>
  )
}

