import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './Pages/HomePage';
import BoostsPage from './Pages/Bosts';
import ClanPage from './Pages/Clans';
import LeaderBoardPage from './Pages/leaderbord';
import Navbar from './components/Navbar';

function App() {
    return (
        <Router>
            <div>
                <Navbar />
                <Routes>
                    <Route exact path="/" element={<HomePage />} />
                    <Route exact path="/clans" element={<ClanPage />} />
                    <Route exact path="/leaderboard" element={<LeaderBoardPage />} />
                    <Route exact path="/bosts" element={<BoostsPage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
