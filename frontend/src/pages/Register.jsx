import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Code2, ArrowRight, Lock, Mail, User, CheckCircle2 } from 'lucide-react';

export default function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [level, setLevel] = useState('intermediate');
  const [languages, setLanguages] = useState(['python']);
  const [selectedTopics, setSelectedTopics] = useState(['Loops', 'Arrays']);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const allTopics = [
    'Variables', 'Conditions', 'Loops', 'Functions', 
    'Arrays', 'Strings', 'Dictionaries', 'Searching', 
    'Sorting', 'Recursion', 'OOP', 'Dynamic Programming'
  ];

  const toggleTopic = (t) => {
    if (selectedTopics.includes(t)) {
      setSelectedTopics(selectedTopics.filter(item => item !== t));
    } else {
      setSelectedTopics([...selectedTopics, t]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await register(name, email, password, languages, level, selectedTopics);
      navigate('/onboarding');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create account. Please check the inputs.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[90vh] flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-lg bg-slate-900/90 rounded-2xl border border-slate-800 p-8 shadow-2xl space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-mentor-400 to-emerald-600 flex items-center justify-center mx-auto shadow-lg shadow-mentor-500/20">
            <Code2 className="w-7 h-7 text-slate-950 stroke-[2.5]" />
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Create Learner Account</h2>
          <p className="text-xs text-slate-400">Join CodeMentor AI to build genuine programming mastery</p>
        </div>

        {error && (
          <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Full Name</label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Taylor Smith"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-mentor-500"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Email</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="taylor@example.com"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-mentor-500"
                />
              </div>
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-300">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-mentor-500"
              />
            </div>
          </div>

          {/* Self-Declared Skill Level */}
          <div className="space-y-2 pt-1">
            <label className="text-xs font-semibold text-slate-300 block">
              Self-Declared Skill Level
            </label>
            <div className="grid grid-cols-3 gap-2.5">
              {[
                { id: 'beginner', title: 'Beginner', desc: 'Starting out' },
                { id: 'intermediate', title: 'Intermediate', desc: 'Loops & Data structs' },
                { id: 'advanced', title: 'Advanced', desc: 'Algorithms & Optimizations' }
              ].map((lvl) => (
                <button
                  key={lvl.id}
                  type="button"
                  onClick={() => setLevel(lvl.id)}
                  className={`p-3 rounded-xl border text-left transition-all ${
                    level === lvl.id
                      ? 'bg-mentor-500/10 border-mentor-500 text-white shadow-sm'
                      : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
                  }`}
                >
                  <div className="text-xs font-bold">{lvl.title}</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">{lvl.desc}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Familiar Topics */}
          <div className="space-y-2 pt-1">
            <label className="text-xs font-semibold text-slate-300 block">
              Topics you are familiar with
            </label>
            <div className="flex flex-wrap gap-1.5 max-h-28 overflow-y-auto p-1 bg-slate-950/40 rounded-xl border border-slate-800/80">
              {allTopics.map((topic) => {
                const isSelected = selectedTopics.includes(topic);
                return (
                  <button
                    key={topic}
                    type="button"
                    onClick={() => toggleTopic(topic)}
                    className={`px-2.5 py-1 rounded-lg text-xs transition-all flex items-center gap-1 ${
                      isSelected
                        ? 'bg-mentor-500/20 text-mentor-300 border border-mentor-500/40'
                        : 'bg-slate-900 text-slate-400 border border-slate-800 hover:bg-slate-800'
                    }`}
                  >
                    {isSelected && <CheckCircle2 className="w-3 h-3 text-mentor-400" />}
                    {topic}
                  </button>
                );
              })}
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 rounded-xl bg-mentor-500 hover:bg-mentor-600 disabled:opacity-50 text-slate-950 font-bold text-xs flex items-center justify-center gap-2 shadow-lg shadow-mentor-500/20 transition-all mt-4"
          >
            {loading ? 'Creating Profile...' : 'Complete Registration'}
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        <div className="text-center text-xs text-slate-400">
          Already have an account?{' '}
          <Link to="/login" className="text-mentor-400 hover:underline font-semibold">
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}
