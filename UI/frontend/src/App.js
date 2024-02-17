import React from 'react'

import { BrowserRouter as Router } from "react-router-dom";
import { Route, Routes } from "react-router-dom";
import Login from './views/pages/login/Login';
import DefaultLayout from './layout/DefaultLayout';

import './scss/style.scss'

function App() {
  return (
    <>
    <div className="app" style={{backgroundColor:"484a4d"}}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="*" element={<DefaultLayout />} />
        </Routes>
      </Router>
    </div>
    </>
  );
}

export default App;