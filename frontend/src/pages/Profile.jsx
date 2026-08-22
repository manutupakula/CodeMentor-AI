import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { learnerAPI, profileAPI } from '../api/client';
import MasteryMeters from '../components/MasteryMeters';
import { 
  User, 
  Award, 
  RotateCcw, 
  GraduationCap, 
  Clock, 
  CheckCircle2, 
  XCircle, 
  AlertTriangle,
  History,
  ShieldCheck
} from 'lucide-react';

export default function Profile() {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const [profRes, histRes] = await Promise.all([
          learnerAPI.getProfile(),
          learnerAPI.getHistory(15)
        ]);
        setProfile(profRes.data);
        setHistory(histRes.data || []);
      } catch (err) {
        console.error("Failed to load profile", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfileData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center space-y-3">
        <div className="w-10 h-10 border-2 border-mentor-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-xs text-slate-400">Loading your comprehensive learner profile...</p>
      </div>
    );
  }

  const recurringMistakes = Object.entries(profile?.recurring_mistakes || {});

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-in fade-in duration-200">
      {/* Top Profile Header */}
      <div className="bg-gradient-to-br from-slate-900 to-slate-950 rounded-3xl border border-slate-800 p-8 shadow-2xl space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-mentor-500/20 text-mentor-400 flex items-center justify-center border border-mentor-500/30 font-bold text-2xl">
              {user?.name?.charAt(0) || 'U'}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-bold text-white">{user?.name}</h1>
                <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-mentor-500/20 text-mentor-300 border border-mentor-500/30 uppercase">
                  {profile?.overall_level}
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">{user?.email}</p>
            </div>
          </div>

          <Link
            to="/knowledge-check"
            className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-2 border border-slate-700 transition-colors shrink-0"
          >
            <GraduationCap className="w-4 h-4 text-amber-400" />
            {user?.knowledge_check_completed ? 'Retake Knowledge Check' : 'Take Knowledge Check'}
          </Link>
        </div>

        {/* Info Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1">
            <span className="text-[10px] text-slate-500 uppercase font-bold">Self Assessment</span>
            <div className="text-base font-bold text-white capitalize">{profile?.self_assessment || 'Intermediate'}</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1">
            <span className="text-[10px] text-slate-500 uppercase font-bold">Diagnostic Score</span>
            <div className="text-base font-bold text-mentor-400 font-mono">
              {profile?.knowledge_check_score !== null && profile?.knowledge_check_score !== undefined
                ? `${Math.round(profile.knowledge_check_score * 100)}%`
                : 'Not Taken'}
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1">
            <span className="text-[10px] text-slate-500 uppercase font-bold">Problems Solved</span>
            <div className="text-base font-bold text-white font-mono">{profile?.problems_solved || 0}</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1">
            <span className="text-[10px] text-slate-500 uppercase font-bold">Independent Solves</span>
            <div className="text-base font-bold text-emerald-400 font-mono">{profile?.independent_solves || 0}</div>
          </div>
        </div>
      </div>

      {/* Grid: Mastery + Recurring Mistakes */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Concept Mastery Meters (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="flex items-center gap-2">
            <Award className="w-5 h-5 text-mentor-400" />
            <h2 className="text-base font-bold text-white">Concept Mastery Radar</h2>
          </div>

          <div className="bg-slate-900/80 rounded-2xl p-5 border border-slate-800">
            <MasteryMeters conceptMastery={profile?.concept_mastery || {}} />
          </div>
        </div>

        {/* Right: Recurring Mistakes Log (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-amber-400" />
              <h2 className="text-base font-bold text-white">Recurring Misconceptions</h2>
            </div>
            <Link to="/revise-mistakes" className="text-xs text-mentor-400 hover:underline font-semibold">
              Revise All
            </Link>
          </div>

          <div className="bg-slate-900/80 rounded-2xl p-5 border border-slate-800 space-y-3">
            {recurringMistakes.length === 0 ? (
              <div className="text-center py-6 text-slate-500 text-xs">
                No repeated misconceptions recorded yet. Keep practicing!
              </div>
            ) : (
              <div className="space-y-2">
                {recurringMistakes.map(([mistake, count], idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 flex items-center justify-between"
                  >
                    <span className="text-xs font-semibold text-slate-200 capitalize">
                      {mistake.replace(/_/g, ' ')}
                    </span>
                    <span className="px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-mono font-bold">
                      {count}x
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Learning History Log */}
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <History className="w-5 h-5 text-blue-400" />
          <h2 className="text-base font-bold text-white">Recent Learning Sessions</h2>
        </div>

        <div className="bg-slate-900/80 rounded-2xl border border-slate-800 overflow-hidden shadow-xl">
          {history.length === 0 ? (
            <div className="text-center py-8 text-slate-500 text-xs">
              No learning session history found. Start your first problem from the catalog!
            </div>
          ) : (
            <div className="divide-y divide-slate-800/80">
              {history.map((h, idx) => (
                <div key={idx} className="p-4 flex items-center justify-between gap-4 text-xs hover:bg-slate-850/40 transition-colors">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-white text-sm">{h.problem_title}</span>
                      <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-800 text-slate-300 border border-slate-700">
                        {h.topic}
                      </span>
                    </div>
                    <div className="text-slate-400 flex items-center gap-3 text-[11px]">
                      <span>{h.attempts_used} attempt{h.attempts_used > 1 ? 's' : ''}</span>
                      <span>•</span>
                      <span>{h.hints_used} hint{h.hints_used > 1 ? 's' : ''} used</span>
                      <span>•</span>
                      <span>{new Date(h.started_at).toLocaleDateString()}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold font-mono uppercase border ${
                      h.status === 'solved_independently'
                        ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
                        : h.status === 'solved_with_hints'
                        ? 'bg-blue-500/20 text-blue-300 border-blue-500/30'
                        : 'bg-slate-800 text-slate-400 border-slate-700'
                    }`}>
                      {h.status?.replace(/_/g, ' ')}
                    </span>
                    <Link
                      to={`/workspace/${h.session_id}`}
                      className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition-colors"
                    >
                      Open
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
