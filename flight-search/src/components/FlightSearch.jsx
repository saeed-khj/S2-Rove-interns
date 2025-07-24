import { useState } from 'react'
import { Search, Plane, Calendar, MapPin, Users } from 'lucide-react'
import axios from 'axios'

const FlightSearch = () => {
  const [formData, setFormData] = useState({
    from: '',
    to: '',
    date: '',
    passengers: 1,
    cabinClass: 'economy'
  })
  
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState('')

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const searchFlights = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResults(null)

    try {
      // Note: You'll need to replace 'YOUR_RAPIDAPI_KEY' with your actual RapidAPI key
      const response = await axios.get('https://compare-flight-prices.p.rapidapi.com/getPrices', {
        params: {
          from: formData.from,
          to: formData.to,
          date: formData.date,
          passengers: formData.passengers,
          cabinClass: formData.cabinClass
        },
        headers: {
          'X-RapidAPI-Key': 'YOUR_RAPIDAPI_KEY',
          'X-RapidAPI-Host': 'compare-flight-prices.p.rapidapi.com'
        }
      })

      setResults(response.data)
    } catch (err) {
      console.error('Error searching flights:', err)
      setError('Failed to search flights. Please check your API key and try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: '800px', width: '100%' }}>
        <h2 style={{
          fontSize: '2rem',
          fontWeight: '600',
          marginBottom: '2rem',
          textAlign: 'center',
          color: '#ffffff'
        }}>
          Search Flights
        </h2>

        <form onSubmit={searchFlights}>
          <div className="grid grid-2">
            <div className="input-group">
              <label htmlFor="from">
                <MapPin size={16} style={{ marginRight: '0.5rem' }} />
                From
              </label>
              <input
                type="text"
                id="from"
                name="from"
                value={formData.from}
                onChange={handleInputChange}
                placeholder="e.g., JFK, New York"
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="to">
                <MapPin size={16} style={{ marginRight: '0.5rem' }} />
                To
              </label>
              <input
                type="text"
                id="to"
                name="to"
                value={formData.to}
                onChange={handleInputChange}
                placeholder="e.g., LAX, Los Angeles"
                required
              />
            </div>
          </div>

          <div className="grid grid-3">
            <div className="input-group">
              <label htmlFor="date">
                <Calendar size={16} style={{ marginRight: '0.5rem' }} />
                Date
              </label>
              <input
                type="date"
                id="date"
                name="date"
                value={formData.date}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="passengers">
                <Users size={16} style={{ marginRight: '0.5rem' }} />
                Passengers
              </label>
              <select
                id="passengers"
                name="passengers"
                value={formData.passengers}
                onChange={handleInputChange}
              >
                {[1, 2, 3, 4, 5, 6, 7, 8].map(num => (
                  <option key={num} value={num}>{num}</option>
                ))}
              </select>
            </div>

            <div className="input-group">
              <label htmlFor="cabinClass">
                <Plane size={16} style={{ marginRight: '0.5rem' }} />
                Cabin Class
              </label>
              <select
                id="cabinClass"
                name="cabinClass"
                value={formData.cabinClass}
                onChange={handleInputChange}
              >
                <option value="economy">Economy</option>
                <option value="premium_economy">Premium Economy</option>
                <option value="business">Business</option>
                <option value="first">First Class</option>
              </select>
            </div>
          </div>

          <div style={{ textAlign: 'center', marginTop: '2rem' }}>
            <button
              type="submit"
              className="btn"
              disabled={loading}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.5rem',
                fontSize: '1rem',
                padding: '16px 32px'
              }}
            >
              {loading ? (
                <>
                  <div style={{
                    width: '16px',
                    height: '16px',
                    border: '2px solid #000000',
                    borderTop: '2px solid transparent',
                    borderRadius: '50%',
                    animation: 'spin 1s linear infinite'
                  }} />
                  Searching...
                </>
              ) : (
                <>
                  <Search size={20} />
                  Search Flights
                </>
              )}
            </button>
          </div>
        </form>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {results && (
          <div style={{ marginTop: '2rem' }}>
            <h3 style={{
              fontSize: '1.5rem',
              fontWeight: '600',
              marginBottom: '1rem',
              color: '#ffffff'
            }}>
              Flight Results
            </h3>
            <div style={{
              background: '#1a1a1a',
              border: '1px solid #333333',
              borderRadius: '8px',
              padding: '1rem'
            }}>
              <pre style={{
                color: '#cccccc',
                fontSize: '14px',
                overflow: 'auto',
                whiteSpace: 'pre-wrap'
              }}>
                {JSON.stringify(results, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default FlightSearch 