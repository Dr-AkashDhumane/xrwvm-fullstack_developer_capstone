import LoginPanel from "./components/Login/Login";
import RegisterPanel from "./components/Register/Register";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      {/* React login page */}
      <Route path="/login" element={<LoginPanel />} />

      {/* React registration page */}
      <Route path="/register" element={<RegisterPanel />} />

      {/* You can add more React pages here */}
    </Routes>
  );
}

export default App;
