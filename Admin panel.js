import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const AdminPanel = () => {
  const [students, setStudents] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [announcements, setAnnouncements] = useState([]);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [token, setToken] = useState(localStorage.getItem('token'));

  const [studentForm, setStudentForm] = useState({ name: '', grade: '', section: '' });
  const [teacherForm, setTeacherForm] = useState({ name: '', subject: '' });
  const [announcementForm, setAnnouncementForm] = useState({ title: '', content: '' });

  useEffect(() => {
    if (token) {
      fetchStudents();
      fetchTeachers();
      fetchAnnouncements();
    }
  }, [token]);

  const login = async () => {
    try {
      const response = await axios.post(`${API_URL}/auth/login`, {
        email: 'admin@kersaschool.edu.et',
        password: 'admin123'
      });
      setToken(response.data.token);
      localStorage.setItem('token', response.data.token);
    } catch (error) {
      alert('Login failed. Please check credentials.');
    }
  };

  const fetchStudents = async () => {
    try {
      const response = await axios.get(`${API_URL}/students`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStudents(response.data);
    } catch (error) {
      // Fallback to localStorage
      setStudents(JSON.parse(localStorage.getItem('students') || '[]'));
    }
  };

  const fetchTeachers = async () => {
    try {
      const response = await axios.get(`${API_URL}/teachers`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTeachers(response.data);
    } catch (error) {
      setTeachers(JSON.parse(localStorage.getItem('teachers') || '[]'));
    }
  };

  const fetchAnnouncements = async () => {
    try {
      const response = await axios.get(`${API_URL}/announcements`);
      setAnnouncements(response.data);
    } catch (error) {
      setAnnouncements(JSON.parse(localStorage.getItem('announcements') || '[]'));
    }
  };

  const addStudent = async () => {
    if (!studentForm.name) return;
    
    const newStudent = { ...studentForm, id: Date.now() };
    
    try {
      await axios.post(`${API_URL}/students`, newStudent, {
        headers: { Authorization: `Bearer ${token}` }
      });
    } catch (error) {
      // Save to localStorage
      const students = JSON.parse(localStorage.getItem('students') || '[]');
      students.push(newStudent);
      localStorage.setItem('students', JSON.stringify(students));
    }
    
    setStudentForm({ name: '', grade: '', section: '' });
    fetchStudents();
  };

  const addAnnouncement = async () => {
    if (!announcementForm.title || !announcementForm.content) return;
    
    const newAnnouncement = {
      ...announcementForm,
      date: new Date().toISOString().split('T')[0],
      id: Date.now()
    };
    
    try {
      await axios.post(`${API_URL}/announcements`, newAnnouncement, {
        headers: { Authorization: `Bearer ${token}` }
      });
    } catch (error) {
      const announcements = JSON.parse(localStorage.getItem('announcements') || '[]');
      announcements.unshift(newAnnouncement);
      localStorage.setItem('announcements', JSON.stringify(announcements));
    }
    
    setAnnouncementForm({ title: '', content: '' });
    fetchAnnouncements();
  };

  if (!token) {
    return (
      <div className="admin-login">
        <h2>Admin Login</h2>
        <p>Default: admin@kersaschool.edu.et / admin123</p>
        <button onClick={login}>Login as Admin</button>
      </div>
    );
  }

  return (
    <div className="admin-panel">
      <div className="admin-sidebar">
        <h3>Admin Panel</h3>
        <button onClick={() => setActiveTab('dashboard')}>Dashboard</button>
        <button onClick={() => setActiveTab('students')}>Students</button>
        <button onClick={() => setActiveTab('teachers')}>Teachers</button>
        <button onClick={() => setActiveTab('announcements')}>Announcements</button>
      </div>
      
      <div className="admin-content">
        {activeTab === 'dashboard' && (
          <div>
            <h2>Dashboard</h2>
            <div className="stats-grid">
              <div className="stat-card">
                <h3>{students.length}</h3>
                <p>Students</p>
              </div>
              <div className="stat-card">
                <h3>{teachers.length}</h3>
                <p>Teachers</p>
              </div>
              <div className="stat-card">
                <h3>{announcements.length}</h3>
                <p>Announcements</p>
              </div>
            </div>
          </div>
        )}
        
        {activeTab === 'students' && (
          <div>
            <h2>Student Management</h2>
            <div className="form-group">
              <input
                type="text"
                placeholder="Student Name"
                value={studentForm.name}
                onChange={(e) => setStudentForm({...studentForm, name: e.target.value})}
              />
              <select
                value={studentForm.grade}
                onChange={(e) => setStudentForm({...studentForm, grade: e.target.value})}
              >
                <option>Grade 9</option>
                <option>Grade 10</option>
                <option>Grade 11</option>
                <option>Grade 12</option>
              </select>
              <select
                value={studentForm.section}
                onChange={(e) => setStudentForm({...studentForm, section: e.target.value})}
              >
                <option>A</option>
                <option>B</option>
                <option>C</option>
              </select>
              <button onClick={addStudent}>Add Student</button>
            </div>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Grade</th>
                  <th>Section</th>
                </tr>
              </thead>
              <tbody>
                {students.map(student => (
                  <tr key={student.id}>
                    <td>{student.name}</td>
                    <td>{student.grade}</td>
                    <td>{student.section}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        
        {activeTab === 'announcements' && (
          <div>
            <h2>Announcement Management</h2>
            <div className="form-group">
              <input
                type="text"
                placeholder="Title"
                value={announcementForm.title}
                onChange={(e) => setAnnouncementForm({...announcementForm, title: e.target.value})}
              />
              <textarea
                placeholder="Content"
                value={announcementForm.content}
                onChange={(e) => setAnnouncementForm({...announcementForm, content: e.target.value})}
              />
              <button onClick={addAnnouncement}>Post Announcement</button>
            </div>
            <div className="announcements-list">
              {announcements.map(announcement => (
                <div key={announcement.id} className="announcement-item">
                  <h4>{announcement.title}</h4>
                  <p>{announcement.content}</p>
                  <small>{announcement.date}</small>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminPanel;
