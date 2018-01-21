import React from 'react';

const Card = (props) => {
  return (
    <div className="col-lg-4 col-sm-6">
      <a className="portfolio-box" href="#randomize-area" onClick={() => props.onClick(props.playlist)}>
        <img className="img-fluid" src={`img/portfolio/fullsize/${props.playlist.imageUrl}`} alt="" />
        <div className="portfolio-box-caption">
          <div className="portfolio-box-caption-content">
            <div className="project-category text-faded">
              Playlist
                </div>
            <div className="project-name">
              {props.playlist.name}
            </div>
          </div>
        </div>
      </a>
    </div>
  );
}

const PlaylistCards = (props) => {
  return (
    <section className="p-0" id="portfolio">
      <div className="container-fluid">
        <div className="row no-gutter popup-gallery">
          {props.playlists.map(playlist => <Card playlist={playlist} key={playlist.id} onClick={props.onClick}/>)}
        </div>
      </div>
    </section>
  );
}

export default PlaylistCards;
