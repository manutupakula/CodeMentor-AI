import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import Onboarding from './pages/Onboarding';
import KnowledgeCheck from './pages/KnowledgeCheck';
import Dashboard from './pages/Dashboard';
import ProblemsList from './pages/ProblemsList';
import Workspace from './pages/Workspace';
import ReviseMistakes from './pages/ReviseMistakes';
import CustomProblem from './pages/CustomProblem';
import Profile from './pages/Profile';

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-950 text-slate-400 text-xs">
        <div className="w-8 h-8 border-2 border-mentor-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

function AppRoutes() {
  return (
    <div className="min-h-screen bg-slate-950 flex flex-col font-sans">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          <Route path="/onboarding" element={
            <ProtectedRoute>
              <Onboarding />
            </ProtectedRoute>
          } />
          
          <Route path="/knowledge-check" element={
            <ProtectedRoute>
              <KnowledgeCheck />
            </ProtectedRoute>
          } />
          
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />

          <Route path="/problems" element={
            <ProtectedRoute>
              <ProblemsList />
            </ProtectedRoute>
          } />

          <Route path="/workspace/:sessionId" element={
            <ProtectedRoute>
              <Workspace />
            </ProtectedRoute>
          } />

          <Route path="/revise-mistakes" element={
            <ProtectedRoute>
              <ReviseMistakes />
            </ProtectedRoute>
          } />

          <Route path="/custom-problem" element={
            <ProtectedRoute>
              <CustomProblem />
            </ProtectedRoute>
          } />

          <Route path="/profile" element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          } />

          {/* Default Fallback */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}
