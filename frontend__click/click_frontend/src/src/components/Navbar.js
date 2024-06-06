import React from 'react';
import { Link } from 'react-router-dom';
import { FaHome, FaUsers, FaTrophy, FaRocket } from 'react-icons/fa'; // Бібліотека іконок

const Navbar = () => {
    return (
        <nav className="navbar">
            <ul className="navbar-list">
                <li className="navbar-item"><Link to="/"><FaHome /> Home</Link></li>
                <li className="navbar-item"><Link to="/clans"><FaUsers /> Clans</Link></li>
                <li className="navbar-item"><Link to="/leaderboard"><FaTrophy /> Leader Board</Link></li>
                <li className="navbar-item"><Link to="/bosts"><FaRocket /> Bosts</Link></li>
            </ul>
        </nav>
    );
}

export default Navbar;
