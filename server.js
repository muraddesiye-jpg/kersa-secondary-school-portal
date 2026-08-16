const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

// Simple in-memory database (for testing without MongoDB)
const db = {
    students: [
        { id: 'KSS001', name: 'Ahmed Mohammed', grade: 'Grade 11', section: 'A', attendance: '95%' },
        { id: 'KSS002', name: 'Fatima Ali', grade: 'Grade 10', section: 'B', attendance: '85%' },
        { id: 'KSS003', name: 'Yusuf Ibrahim', grade: 'Grade 12', section: 'C', attendance: '75%' }
    ],
    teachers: [
        { id: 'T001', name: 'Dr. Abebe Kebede', subject: 'Mathematics', classes: 'Grade 11, 12' },
        { id: 'T002', name: 'Mrs. Sara Tesfaye', subject: 'English', classes: 'Grade 9, 10' }
    ],
    announcements: [
        { id: 1, title: 'Welcome Back!', content: 'Welcome to the new academic year.', date: '2024-08-25' },
        { id: 2, title: 'Mid-Term Exams', content: 'Mid-term examinations will be held soon.', date: '2024-10-10' }
    ]
};

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// API Routes
app.get('/api/students', (req, res) => {
    res.json(db.students);
});

app.post('/api/students', (req, res) => {
    const newStudent = req.body;
    newStudent.id = 'KSS' + String(db.students.length + 1).padStart(3, '0');
    db.students.push(newStudent);
    res.status(201).json(newStudent);
});

app.get('/api/teachers', (req, res) => {
    res.json(db.teachers);
});

app.get('/api/announcements', (req, res) => {
    res.json(db.announcements);
});

// AI Chat endpoint
app.post('/api/ai/chat', (req, res) => {
    const { message } = req.body;
    
    // Simple AI response logic
    const responses = {
        greeting: "Wa Alaikum Assalam! How can I help you with your studies today?",
        motivation: "Remember, every expert was once a beginner. Keep pushing forward! 💪",
        study: "Study tips: Break sessions into 25-minute blocks, create a quiet space, and review regularly.",
        default: "That's a great question! Could you please be more specific about what you need help with?"
    };
    
    let response;
    const msg = message.toLowerCase();
    
    if (msg.includes('hello') || msg.includes('hi') || msg.includes('salam')) {
        response = responses.greeting;
    } else if (msg.includes('motivat') || msg.includes('encourage')) {
        response = responses.motivation;
    } else if (msg.includes('study') || msg.includes('learn')) {
        response = responses.study;
    } else {
        response = responses.default;
    }
    
    res.json({ response });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Server is running on http://localhost:${PORT}`);
    console.log(`📱 Access from your phone browser at: http://localhost:${PORT}`);
});
