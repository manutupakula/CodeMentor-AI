import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Code2, 
  LayoutDashboard, 
  BookOpen, 
  RotateCcw, 
  Sparkles, 
  User, 
  LogOut,
  GraduationCap
} from 'lucide-react';

export default function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { label: 'Practice Problems', path: '/problems', icon: BookOpen },
    { label: 'Revise Mistakes', path: '/revise-mistakes', icon: RotateCcw },
    { label: 'Custom Problem', path: '/custom-problem', icon: Sparkles },
    { label: 'Profile & Mastery', path: '/profile', icon: User },
  ];

  const getLevelBadgeColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'advanced': return 'bg-purple-500/20 text-purple-300 border-purple-500/30';
      case 'intermediate': return 'bg-blue-500/20 text-blue-300 border-blue-500/30';
      default: return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';
    }
  };

  return (
    <nav className="sticky top-0 z-40 bg-slate-900/80 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <Link to="/dashboard" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-mentor-400 to-emerald-600 flex items-center justify-center shadow-lg shadow-mentor-500/20 group-hover:scale-105 transition-transform">
              <Code2 className="w-6 h-6 text-slate-950 stroke-[2.5]" />
            </div>
            <div>
              <span className="text-xl font-bold bg-gradient-to-r from-white via-slate-100 to-mentor-300 bg-clip-text text-transparent">
                CodeMentor<span className="text-mentor-400 font-extrabold">.AI</span>
              </span>
              <span className="hidden sm:block text-[10px] text-slate-400 font-mono tracking-wider">
                ADAPTIVE CODING TUTOR
              </span>
            </div>
          </Link>

          {/* Navigation Links */}
          {user && (
            <div className="hidden md:flex items-center gap-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                const active = location.pathname === item.path;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all ${
                      active
                        ? 'bg-slate-800 text-mentor-400 border border-slate-700 shadow-sm'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    {item.label}
                  </Link>
                );
              })}
            </div>
          )}

          {/* Right User Info & Actions */}
          <div className="flex items-center gap-3">
            {user ? (
              <>
                <div className="hidden sm:flex items-center gap-2">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-semibold border ${getLevelBadgeColor(user.self_declared_level)}`}>
                    {user.self_declared_level?.toUpperCase() || 'LEARNER'}
                  </span>
                  <span className="text-xs text-slate-400 font-medium">
                    {user.name}
                  </span>
                </div>

                {!user.knowledge_check_completed && (
                  <Link
                    to="/knowledge-check"
                    className="hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-500/15 text-amber-300 border border-amber-500/30 text-xs font-semibold hover:bg-amber-500/25 transition-colors"
                  >
                    <GraduationCap className="w-3.5 h-3.5" />
                    Knowledge Check
                  </Link>
                )}

                <button
                  onClick={handleLogout}
                  title="Logout"
                  className="p-2 rounded-lg text-slate-400 hover:text-red-400 hover:bg-slate-800 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white transition-colors"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 rounded-lg bg-mentor-500 hover:bg-mentor-600 text-slate-950 font-semibold text-sm shadow-md transition-all"
                >
                  Get Started
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
