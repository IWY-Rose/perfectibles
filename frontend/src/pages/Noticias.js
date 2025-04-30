import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './Noticias.css';

function Noticias() {
  const [featuredNoticia, setFeaturedNoticia] = useState(null);
  const [otherNoticias, setOtherNoticias] = useState([]);

  useEffect(() => {
    const fetchNoticias = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/noticias/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        const featured = data.find(noticia => noticia.is_featured === true);
        setFeaturedNoticia(featured || null);

        const sortedAllNoticias = data.sort((a, b) => {
          const dateA = new Date(a.datetime);
          const dateB = new Date(b.datetime);
          return dateB - dateA;
        });

        setOtherNoticias(sortedAllNoticias);
      } catch (error) {
        console.error('Error fetching noticias:', error);
        setFeaturedNoticia(null);
        setOtherNoticias([]);
      }
    };

    fetchNoticias();
  }, []);

  // --- Date Formatting Options ---
  const dateOptions = {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  };

  const dateTimeOptions = {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false // Use 24-hour format
  };
  // --- End Date Formatting Options ---

  return (
    <div className="noticias-page">
      <h1 className="noticias-title">Noticias Perfectibles</h1>

      {featuredNoticia && (
        <div className="featured-noticia-card">
          <Link
            to={`/noticia/${featuredNoticia.id}`}
            className="featured-noticia-link"
            style={{ backgroundImage: `url(http://127.0.0.1:8000/assets/${featuredNoticia.imagen})` }}
          >
            <div className="featured-title-container">
              <h2 className="featured-noticia-title">{featuredNoticia.titulo}</h2>
            </div>
            <div className="featured-date-container">
              {/* Format featured date: Date only */}
              <p className="featured-noticia-fecha">
                {new Date(featuredNoticia.datetime).toLocaleString(undefined, dateOptions)}
              </p>
            </div>
            <div className="featured-overlay"></div>
          </Link>
        </div>
      )}

      <div className="noticias-container">
        {otherNoticias.map((noticia) => (
          <div key={noticia.id} className="noticia-card">
            <Link to={`/noticia/${noticia.id}`} className="noticia-link-wrapper">
              <div className="noticia-item-container noticia-title-container">
                <h3 className="noticia-title">{noticia.titulo}</h3>
              </div>
              <div className="noticia-item-container noticia-image-container">
                <div className="image-wrapper">
                  <img src={`http://127.0.0.1:8000/assets/${noticia.imagen}`} alt={noticia.titulo} className="noticia-image" />
                </div>
              </div>
              <div className="noticia-item-container noticia-date-container">
                {/* Format list date: Date and 24hr Time */}
                <p className="noticia-fecha">
                  {new Date(noticia.datetime).toLocaleString(undefined, dateTimeOptions)}
                </p>
              </div>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Noticias;