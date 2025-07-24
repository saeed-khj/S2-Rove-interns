import { useState } from 'react'
import './App.css'
import FlightSearch from './components/FlightSearch'
import Header from './components/Header'

function App() {
  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <FlightSearch />
      </main>
    </div>
  )
}

export default App
