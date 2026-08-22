import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { problemsAPI, sessionsAPI } from '../api/client';
import { BookOpen, Search, Filter, Clock, ArrowRight, Sparkles, CheckCircle2 } from 'lucide-react';

export default function ProblemsList() {
  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [startingId, setStartingId] = useState(null);
  const navigate = useNavigate();

  const topics = [
    'Variables', 'Conditions', 'Loops', 'Functions', 
    'Arrays', 'Strings', 'Dictionaries', 'Searching', 
    'Sorting', 'Recursion', 'OOP', 'Dynamic Programming'
  ];

  const difficulties = ['beginner', 'intermediate', 'advanced'];

  useEffect(() => {
    const fetchProblems = async () => {
      setLoading(true);
      try {
        const params = {};
        if (selectedTopic) params.topic = selectedTopic;
        if (selectedDifficulty) params.difficulty = selectedDifficulty;
        if (search) params.search = search;

        const res = await problemsAPI.list(params);
        setProblems(res.data || []);
      } catch (err) {
        console.error("Failed to load problems", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProblems();
  }, [selectedTopic, selectedDifficulty, search]);

  const handleStart = async (problemId) => {
    setStartingId(problemId);
    try {
      const res = await sessionsAPI.create(problemId);
      navigate(`/workspace/${res.data.id}`);
    } catch (err) {
      console.error("Failed to create session", err);
    } finally {
      setStartingId(null);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-mentor-400 font-bold uppercase tracking-wider">
            <BookOpen className="w-4 h-4" /> Practice Catalog
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Coding Challenges</h1>
          <p className="text-xs sm:text-sm text-slate-400">
            Select a problem to practice with your adaptive AI programming tutor.
          </p>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="bg-slate-900/80 rounded-2xl border border-slate-800 p-4 space-y-3">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {/* Search Box */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search problems by title..."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-mentor-500"
            />
          </div>

          {/* Topic Dropdown */}
          <select
            value={selectedTopic}
            onChange={(e) => setSelectedTopic(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white focus:outline-none focus:border-mentor-500"
          >
            <option value="">All Topics</option>
            {topics.map(t => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>

          {/* Difficulty Dropdown */}
          <select
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white focus:outline-none focus:border-mentor-500 capitalize"
          >
            <option value="">All Difficulties</option>
            {difficulties.map(d => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Problems Grid */}
      {loading ? (
        <div className="min-h-[40vh] flex flex-col items-center justify-center space-y-3">
          <div className="w-8 h-8 border-2 border-mentor-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-xs text-slate-400">Loading problems catalog...</p>
        </div>
      ) : problems.length === 0 ? (
        <div className="text-center py-12 bg-slate-900/40 rounded-2xl border border-slate-800 space-y-2">
          <BookOpen className="w-8 h-8 text-slate-600 mx-auto" />
          <h3 className="text-sm font-semibold text-slate-300">No problems found</h3>
          <p className="text-xs text-slate-500">Try adjusting your search filters.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {problems.map((p) => {
            const diffColor = p.difficulty === 'beginner' 
              ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
              : p.difficulty === 'intermediate'
              ? 'text-blue-400 bg-blue-500/10 border-blue-500/20'
              : 'text-purple-400 bg-purple-500/10 border-purple-500/20';

            return (
              <div
                key={p.id}
                className="bg-slate-900/80 rounded-2xl p-5 border border-slate-800 hover:border-slate-700 transition-all flex flex-col justify-between space-y-4 hover:shadow-xl hover:shadow-mentor-500/5 group"
              >
                <div className="space-y-2.5">
                  <div className="flex items-center justify-between gap-2">
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-slate-800 text-slate-300 border border-slate-700">
                      {p.topic}
                    </span>
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase border ${diffColor}`}>
                      {p.difficulty}
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-white group-hover:text-mentor-400 transition-colors">
                    {p.title}
                  </h3>

                  <div className="flex items-center gap-3 text-xs text-slate-400">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 text-slate-500" />
                      ~{p.estimated_time} mins
                    </span>
                    <span className="text-slate-600">•</span>
                    <span className="font-mono text-[11px] text-slate-400">
                      {p.subconcept?.replace('_', ' ')}
                    </span>
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between">
                  <div className="flex flex-wrap gap-1">
                    {p.tags?.slice(0, 2).map((tag, tIdx) => (
                      <span key={tIdx} className="text-[10px] text-slate-500">
                        #{tag}
                      </span>
                    ))}
                  </div>

                  <button
                    onClick={() => handleStart(p.id)}
                    disabled={startingId === p.id}
                    className="px-3.5 py-1.5 rounded-lg bg-mentor-500/15 hover:bg-mentor-500 text-mentor-300 hover:text-slate-950 border border-mentor-500/30 text-xs font-bold flex items-center gap-1.5 transition-all shadow-sm"
                  >
                    {startingId === p.id ? 'Opening...' : 'Start'}
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
