import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import HomePage from './Pages/HomePage';
import Navbar from './components/Navbar';

function App() {
    return (
        <Router>
            <Navbar />
                <Route exact path="/home_pages" component={HomePage} />
        </Router>
    );
}

export default App;
