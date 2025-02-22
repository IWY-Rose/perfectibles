import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './Noticias.css';

function Noticias() {
  const [noticias, setNoticias] = useState([]);

  useEffect(() => {
    const fetchNoticias = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/noticias/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const sortedNoticias = data.sort((a, b) => a.id - b.id);
        setNoticias(sortedNoticias);
      } catch (error) {
        console.error('Error fetching noticias:', error);
      }
    };

    fetchNoticias();
  }, []);

  return (
    <div className="noticias-page">
      <h1 className="noticias-title">Noticias Perfectibles</h1>
      <div className="noticias-container">
        {noticias.map((noticia) => (
          <div key={noticia.id} className="noticia-card">
            <Link to={`/noticia/${noticia.id}`} className="noticia-title">
              {noticia.titulo}
            </Link>
            <div className="image-wrapper">
              <img src={`http://127.0.0.1:8000/assets/${noticia.imagen}`} alt={noticia.titulo} className="noticia-image" />
            </div>
            <p className="noticia-fecha">{new Date(noticia.datetime).toLocaleString()}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Noticias;