import React, { useEffect, useState, useCallback } from 'react';
import { Link } from 'react-router-dom';
import './Noticias.css';

const AUTO_SLIDE_INTERVAL = 7000; // 7 seconds

function Noticias() {
  const [allFeaturedNoticiasData, setAllFeaturedNoticiasData] = useState([]); // Stores the direct API response
  const [currentFeaturedIndex, setCurrentFeaturedIndex] = useState(0);
  // currentFeaturedItem will now be the 'noticia' object from allFeaturedNoticiasData[currentFeaturedIndex].noticia
  const [currentDisplayNoticia, setCurrentDisplayNoticia] = useState(null);
  const [otherNoticias, setOtherNoticias] = useState([]);

  useEffect(() => {
    const fetchFeaturedNoticias = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/featured-noticias/'); // New endpoint
        if (!response.ok) {
          throw new Error(`HTTP error fetching featured! status: ${response.status}`);
        }
        const featuredData = await response.json(); // Array of { noticia: {...}, added_datetime: ..., custom_order: ... }
        
        setAllFeaturedNoticiasData(featuredData);
        if (featuredData.length > 0 && featuredData[0].noticia) {
          setCurrentDisplayNoticia(featuredData[0].noticia);
          setCurrentFeaturedIndex(0);
        } else {
          setCurrentDisplayNoticia(null);
        }
      } catch (error) {
        console.error('Error fetching featured noticias:', error);
        setCurrentDisplayNoticia(null);
        setAllFeaturedNoticiasData([]);
      }
    };

    const fetchAllNoticiasList = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/noticias/');
        if (!response.ok) {
          throw new Error(`HTTP error fetching all news! status: ${response.status}`);
        }
        const data = await response.json(); // Array of Noticia objects
        // Already sorted by -datetime from backend if view is set up that way
        setOtherNoticias(data);
      } catch (error) {
        console.error('Error fetching all noticias list:', error);
        setOtherNoticias([]);
      }
    };

    fetchFeaturedNoticias();
    fetchAllNoticiasList();
  }, []);

  const goToNextFeatured = useCallback(() => {
    if (allFeaturedNoticiasData.length === 0) return;
    const nextIndex = (currentFeaturedIndex + 1) % allFeaturedNoticiasData.length;
    setCurrentFeaturedIndex(nextIndex);
    if (allFeaturedNoticiasData[nextIndex] && allFeaturedNoticiasData[nextIndex].noticia) {
      setCurrentDisplayNoticia(allFeaturedNoticiasData[nextIndex].noticia);
    }
  }, [currentFeaturedIndex, allFeaturedNoticiasData]);

  const goToPrevFeatured = () => {
    if (allFeaturedNoticiasData.length === 0) return;
    const prevIndex = (currentFeaturedIndex - 1 + allFeaturedNoticiasData.length) % allFeaturedNoticiasData.length;
    setCurrentFeaturedIndex(prevIndex);
    if (allFeaturedNoticiasData[prevIndex] && allFeaturedNoticiasData[prevIndex].noticia) {
      setCurrentDisplayNoticia(allFeaturedNoticiasData[prevIndex].noticia);
    }
  };

  useEffect(() => {
    if (allFeaturedNoticiasData.length > 1) {
      const timer = setInterval(goToNextFeatured, AUTO_SLIDE_INTERVAL);
      return () => clearInterval(timer);
    }
  }, [allFeaturedNoticiasData, goToNextFeatured]);

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

      {/* Display the currentDisplayNoticia which is the 'noticia' object */}
      {currentDisplayNoticia && (
        <div className="featured-noticia-card">
          <Link
            to={`/noticia/${currentDisplayNoticia.id}`} // Use the actual Noticia ID
            className="featured-noticia-link"
            style={{ backgroundImage: `url(http://127.0.0.1:8000/assets/${currentDisplayNoticia.imagen})` }}
          >
            <div className="featured-title-container">
              <h2 className="featured-noticia-title">{currentDisplayNoticia.titulo}</h2>
            </div>
            <div className="featured-date-container">
              {/* Displaying the original Noticia's datetime, or you can use allFeaturedNoticiasData[currentFeaturedIndex].added_datetime */}
              <p className="featured-noticia-fecha">
                {new Date(currentDisplayNoticia.datetime).toLocaleString(undefined, dateOptions)}
              </p>
            </div>
            <div className="featured-overlay"></div>
          </Link>

          {allFeaturedNoticiasData.length > 1 && (
            <>
              <button onClick={goToPrevFeatured} className="carousel-arrow prev-arrow" aria-label="Previous slide">&#10094;</button>
              <button onClick={goToNextFeatured} className="carousel-arrow next-arrow" aria-label="Next slide">&#10095;</button>
            </>
          )}
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