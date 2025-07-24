import { Plane } from 'lucide-react'

const Header = () => {
  return (
    <header style={{
      padding: '2rem',
      borderBottom: '1px solid #333333',
      background: 'rgba(0, 0, 0, 0.8)',
      backdropFilter: 'blur(10px)'
    }}>
      <div className="container">
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1rem'
        }}>
          <Plane size={32} color="#ffffff" />
          <h1 style={{
            fontSize: '1.8rem',
            fontWeight: '700',
            color: '#ffffff',
            margin: 0
          }}>
            FlightSearch
          </h1>
        </div>
        <p style={{
          marginTop: '0.5rem',
          color: '#cccccc',
          fontSize: '1rem'
        }}>
          Find the best flight deals with real-time price comparison
        </p>
      </div>
    </header>
  )
}

export default Header 