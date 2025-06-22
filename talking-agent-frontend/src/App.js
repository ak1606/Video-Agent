import React from 'react';
import TalkingAgent from './components/TalkingAgent';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Talking Agent</h1>
      </header>
      <main>
        <TalkingAgent />
      </main>
    </div>
  );
}

export default App;