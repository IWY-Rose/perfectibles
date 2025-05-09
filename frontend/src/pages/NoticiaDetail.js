import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './NoticiaDetail.css'; // Styles will be updated next

// Helper function to render individual media items
const renderMediaElement = (mediaItem) => {
  if (!mediaItem || mediaItem.media_type === 'NONE') {
    return null;
  }

  // Ensure file_url is used if available, otherwise construct from 'file' if needed
  // Based on our backend, file_url should be the absolute URL.
  const src = mediaItem.file_url || (mediaItem.file ? `http://127.0.0.1:8000/assets/${mediaItem.file}` : null);

  switch (mediaItem.media_type) {
    case 'IMAGE':
      return (
        <div key={mediaItem.id || mediaItem.order_in_article} className="embedded-media image-media">
          {mediaItem.title && <h4 className="media-title">{mediaItem.title}</h4>}
          {src && <img src={src} alt={mediaItem.alt_text || mediaItem.title || ''} crossOrigin="anonymous" />}
          {mediaItem.caption && <p className="media-caption">{mediaItem.caption}</p>}
        </div>
      );
    case 'VIDEO':
      if (mediaItem.embed_url) {
        // Basic embed for YouTube, Vimeo, etc. You might need a more robust solution for different providers
        // Or use a library like ReactPlayer
        let embedSrc = mediaItem.embed_url;
        if (mediaItem.embed_url.includes("youtube.com/watch?v=")) {
            embedSrc = mediaItem.embed_url.replace("watch?v=", "embed/");
        } else if (mediaItem.embed_url.includes("youtu.be/")) {
            embedSrc = mediaItem.embed_url.replace("youtu.be/", "youtube.com/embed/");
        }
        // Add more providers if needed
        return (
          <div key={mediaItem.id || mediaItem.order_in_article} className="embedded-media video-media">
            {mediaItem.title && <h4 className="media-title">{mediaItem.title}</h4>}
            <div className="video-responsive">
              <iframe
                width="560"
                height="315"
                src={embedSrc}
                title={mediaItem.title || 'Embedded video'}
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
            </div>
            {mediaItem.caption && <p className="media-caption">{mediaItem.caption}</p>}
          </div>
        );
      } else if (src) {
        return (
          <div key={mediaItem.id || mediaItem.order_in_article} className="embedded-media video-media">
            {mediaItem.title && <h4 className="media-title">{mediaItem.title}</h4>}
            <video controls src={src} title={mediaItem.alt_text || mediaItem.title || ''}>
              Your browser does not support the video tag.
            </video>
            {mediaItem.caption && <p className="media-caption">{mediaItem.caption}</p>}
          </div>
        );
      }
      return null;
    case 'CAROUSEL':
      // Placeholder for carousel rendering. You'll need a carousel component/library.
      // For now, it might just list images or a message.
      // This assumes carousel media items might be stored differently or need specific handling.
      // For a simple start, let's say a carousel item might have multiple 'images' in its data
      // or this mediaItem itself IS one slide of a carousel identified by its order.
      return (
        <div key={mediaItem.id || mediaItem.order_in_article} className="embedded-media carousel-media">
          {mediaItem.title && <h4 className="media-title">{mediaItem.title}</h4>}
          <p><em>Carousel content for "{mediaItem.title || 'this item'}" would go here. (src: {src})</em></p>
          {mediaItem.caption && <p className="media-caption">{mediaItem.caption}</p>}
        </div>
      );
    default:
      return null;
  }
};

// Helper function to parse cuerpo and intersperse media
const renderCuerpoWithMedia = (cuerpo, embeddedMedia) => {
  if (!cuerpo) return null;
  if (!embeddedMedia || embeddedMedia.length === 0) {
    // If no media, just return the cuerpo, split by newlines for paragraphs
    return cuerpo.split('\n').map((paragraph, index) => (
      <p key={`p-${index}`} className="detalle-paragraph">{paragraph}</p>
    ));
  }

  // Sort media by order_in_article just in case it's not already sorted
  const sortedMedia = [...embeddedMedia].sort((a, b) => a.order_in_article - b.order_in_article);
  
  let contentParts = [];
  let lastIndex = 0;

  // Regex to find placeholders like [MEDIA_1], [MEDIA_2], etc.
  const mediaPlaceholderRegex = /\[MEDIA_(\d+)]/g;
  let match;

  while ((match = mediaPlaceholderRegex.exec(cuerpo)) !== null) {
    const mediaOrder = parseInt(match[1], 10); // The number from [MEDIA_X]
    const mediaItem = sortedMedia.find(m => m.order_in_article === mediaOrder);

    // Add text before the placeholder
    if (match.index > lastIndex) {
      const textSegment = cuerpo.substring(lastIndex, match.index);
      textSegment.split('\n').forEach((paragraph, pIndex) => {
        if (paragraph.trim() !== '') { // Avoid adding empty paragraphs
          contentParts.push(<p key={`p-${lastIndex}-${pIndex}`} className="detalle-paragraph">{paragraph}</p>);
        }
      });
    }

    // Add the media element
    if (mediaItem) {
      contentParts.push(renderMediaElement(mediaItem));
    }
    
    lastIndex = mediaPlaceholderRegex.lastIndex;
  }

  // Add any remaining text after the last placeholder
  if (lastIndex < cuerpo.length) {
    const remainingText = cuerpo.substring(lastIndex);
    remainingText.split('\n').forEach((paragraph, pIndex) => {
       if (paragraph.trim() !== '') {
        contentParts.push(<p key={`p-remaining-${pIndex}`} className="detalle-paragraph">{paragraph}</p>);
      }
    });
  }
  
  return contentParts;
};


function NoticiaDetail() {
  const { id } = useParams();
  const [noticia, setNoticia] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchNoticia = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/noticias/${id}/`);
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
  }, [id]);

  if (error) {
    return <div className="detalle-page error-page">Error: {error}</div>;
  }

  if (!noticia) {
    return <div className="detalle-page loading-page">Loading...</div>;
  }

  // Ensure main_image_url is used. Fallback to constructing from main_image if necessary (though backend should provide _url)
  const mainImageUrl = noticia.main_image_url || (noticia.main_image ? `http://127.0.0.1:8000/assets/${noticia.main_image}` : null);
  const clubLogoUrl = noticia.club_logo_url || (noticia.club_logo ? `http://127.0.0.1:8000/assets/${noticia.club_logo}` : null);

  return (
    <div className="detalle-page">
      {/* Encabezado: Titulo, Bajada, Fecha */}
      <header className="detalle-header">
        <h1 className="detalle-title">{noticia.titulo}</h1>
        {noticia.bajada && <p className="detalle-bajada">{noticia.bajada}</p>}
        <div className="detalle-meta">
          <span className="detalle-fecha">{new Date(noticia.datetime).toLocaleString()}</span>
        </div>
      </header>

      {/* Imagen Principal */}
      {mainImageUrl && (
        <div className="main-image-container">
          <img src={mainImageUrl} alt={noticia.titulo} className="detalle-main-image" crossOrigin="anonymous" />
        </div>
      )}

      {/* Cuerpo de la Noticia (con media incrustada) */}
      <article className="detalle-cuerpo-container">
        {renderCuerpoWithMedia(noticia.cuerpo, noticia.embedded_media)}
      </article>

      {/* Logo del Club */}
      {clubLogoUrl && (
        <footer className="detalle-footer">
          <img src={clubLogoUrl} alt="Club Logo" className="detalle-club-logo" crossOrigin="anonymous" />
        </footer>
      )}
    </div>
  );
}

export default NoticiaDetail; 