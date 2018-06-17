import React from 'react';
import { Link } from "react-scroll";

const Card = (props) => {
  return (
    <div className="col-lg-4 col-sm-6">
      <Link className="portfolio-box" href="" smooth={true} to="getstarted" onClick={() => props.onClick(props.playlist)}>
        <img className="img-fluid" src={props.playlist.imageUrl} alt="" />
        <div className="portfolio-box-caption">
          <div className="portfolio-box-caption-content">
            <div className="project-category text-faded">
              Playlist
                </div>
            <div id={`playlistSelectorItem${props.rowId}`} className="project-name">
              {props.playlist.displayName}
            </div>
          </div>
        </div>
      </Link>
    </div>
  );
}

const PlaylistCards = (props) => {
  return (
    <section className="p-0" id="playlists">
      <div className="container-fluid">
        <div className="row no-gutter popup-gallery">
          {props.playlists.map(playlist => <Card playlist={playlist} key={playlist.id} rowId={playlist.id} onClick={props.onClick}/>)}
        </div>
      </div>
    </section>
  );
}

export default PlaylistCards;
