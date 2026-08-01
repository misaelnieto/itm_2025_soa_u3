import React from "react";
import EventsList from './components/EventsList';
import './App.css';  // Si sigues usando tu CSS personalizado

function App() {
  return (
    <div className="container">
      <h1 className="text-center my-4">Gestión de Eventos</h1>
      <EventsList />
    </div>
  );
}

export default App;

