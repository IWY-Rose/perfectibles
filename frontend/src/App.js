import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import '@fortawesome/fontawesome-free/css/all.min.css';
import './App.css';
import logo from './assets/perfectible1.jpg';

import Inicio from './pages/Inicio';
import Historia from './pages/Historia';
import Noticias from './pages/Noticias';
import Contacto from './pages/Contacto';
import Proyectos from './pages/Proyectos';
import Eventos from './pages/Eventos';
import NoticiaDetail from './pages/NoticiaDetail';


function App() {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setIsVisible(false);
      } else {
        setIsVisible(true);
      }
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <Router>
      <div className="App">
        <header className={`top-bar ${isVisible ? '' : 'hidden'}`}>
          <Link to="/">
            <img src={logo} alt="Perfectibles FC Logo" className="logo" />
          </Link>
          <nav className="nav-tabs">
            <a href="/">Inicio</a>
            <a href="/historia">Historia</a>
            <a href="/noticias">Noticias</a>
            <a href="/contacto">Contacto</a>
            <a href="/proyectos">Proyectos</a>
            <a href="/eventos">Eventos</a>
          </nav>
          
          {/* Instagram button */}
          <a 
            href="https://www.instagram.com/perfectibles.fc?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==" 
            target="_blank" 
            rel="noopener noreferrer"
            className="instagram-button"
            title="Síguenos en Instagram"
          >
            <i className="fab fa-instagram"></i>
          </a>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<Inicio />} />
            <Route path="/historia" element={<Historia />} />
            <Route path="/noticias" element={<Noticias />} />
            <Route path="/noticia/:id" element={<NoticiaDetail />} />
            <Route path="/contacto" element={<Contacto />} />
            <Route path="/proyectos" element={<Proyectos />} />
            <Route path="/eventos" element={<Eventos />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}


export default App;

