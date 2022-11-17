import logo from './logo.svg';
import './App.css';
import io from 'socket.io-client';
import {useState, useEffect} from 'react';

const socket = io("localhost:5000/hello");

function App() {
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [lastPong, setLastPong] = useState(null);
  
  useEffect(() => {
    socket.on('connect', (data) => {
      setIsConnected(true);
      console.log(data);
    });

    socket.on('disconnect', (data) => {
      setIsConnected(false);
      console.log(data);
    });

    // socket.on('pong', () => {
    //   setLastPong(new Date().toISOString());
    // });

    return () => {
      socket.off('connect');
      socket.off('disconnect');
      // socket.off('pong');
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
