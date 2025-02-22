import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './NoticiaDetail.css'; // You can reuse the same CSS

function NoticiaDetail() {
  const { id } = useParams();
  const [noticia, setNoticia] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchNoticia = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/noticias/${id}/`); // Fetch noticia by ID
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setNoticia(data);
      } catch (error) {
        setError(error.message);
        console.error('Error fetching noticia:', error);
      }
    };

    fetchNoticia();
  }, [id]); // Fetch when the component mounts or when the ID changes

  if (error) {
    return <div>Error: {error}</div>; // Display error message
  }

  if (!noticia) {
    return <div>Loading...</div>; // Display loading state
  }

  return (
    <div className="detalle-page">
      <div className='encabezado-container'>
        <div className='titulo-container'>
          <h2 className="detalle-title">{noticia.titulo}</h2>
          <p className="detalle-bajada">{noticia.bajada}</p>
        </div>
        <div className="detalle-fecha">{new Date(noticia.datetime).toLocaleString()}</div>
        <div className='image-wrapper'>
          <img src={`http://127.0.0.1:8000/assets/${noticia.imagen}`} alt={noticia.titulo} className="detalle-image" />
        </div>
      </div>
      <p className="detalle-cuerpo">{noticia.cuerpo}</p>
      
    </div>
  );
}

export default NoticiaDetail; 