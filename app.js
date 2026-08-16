import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Features from './components/Features';
import Announcements from './components/Announcements';
import AIChat from './components/AIChat';
import AdminPanel from './components/AdminPanel';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [announcements, setAnnouncements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnnouncements();
  }, []);

  const fetchAnnouncements = async () => {
    try {
      const response = await axios.get(`${API_URL}/announcements`);
      setAnnouncements(response.data);
    } catch (error) {
      console.error('Error fetching announcements:', error);
      // Fallback to localStorage
      const localAnnouncements = JSON.parse(localStorage.getItem('announcements') || '[]');
      setAnnouncements(localAnnouncements);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Router>
      <div className="app">
        <Navbar />
        <Routes>
          <Route path="/" element={
            <>
              <Hero />
              <Features />
              <Announcements announcements={announcements} loading={loading} />
            </>
          } />
          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
        <AIChat />
      </div>
    </Router>
  );
}

export default App;
