import React, { useRef, useEffect } from 'react';
import { Play, Loader } from 'lucide-react';
import './VideoPlayer.css';

const VideoPlayer = ({ videoUrl, isProcessing }) => {
  const videoRef = useRef(null);

  useEffect(() => {
    if (videoUrl && videoRef.current) {
      videoRef.current.load();
      videoRef.current.play().catch(error => {
        console.error('Error playing video:', error);
      });
    }
  }, [videoUrl]);

  return (
    <div className="video-player">
      <div className="video-player__container">
        {isProcessing ? (
          <div className="video-player__loading">
            <Loader className="spinner" size={48} />
            <p>Generating response...</p>
          </div>
        ) : videoUrl ? (
          <video
            ref={videoRef}
            className="video-player__video"
            controls
            autoPlay
            muted
          >
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        ) : (
          <div className="video-player__placeholder">
            <Play size={48} />
            <p>AI Agent will appear here</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoPlayer;