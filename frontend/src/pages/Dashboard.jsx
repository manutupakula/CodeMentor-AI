import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { learnerAPI, sessionsAPI } from '../api/client';
import MasteryMeters from '../components/MasteryMeters';
import { 
  GraduationCap, 
  Sparkles, 
  ArrowRight, 
  RotateCcw, 
  CheckCircle, 
  BookOpen, 
  AlertTriangle,
  Award,
  Flame,
  Lightbulb,
  Zap,
  Target
} from 'lucide-react';

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [startingSessionId, setStartingSessionId] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [profRes, recsRes] = await Promise.all([
          learnerAPI.getProfile(),
          learnerAPI.getRecommendations(4)
        ]);
        setProfile(profRes.data);
        setRecommendations(recsRes.data);
      } catch (err) {
        console.error("Failed to load dashboard data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  const handleStartProblem = async (problemId) => {
    setStartingSessionId(problemId);
    try {
      const res = await sessionsAPI.create(problemId);
      navigate(`/workspace/${res.data.id}`);
    } catch (err) {
      console.error("Failed to start session", err);
      navigate('/problems');
    } finally {
      setStartingSessionId(null);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center space-y-3">
        <div className="w-10 h-10 border-2 border-mentor-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-xs text-slate-400">Personalizing your learning dashboard...</p>
      </div>
    );
  }

  const weakTopics = profile?.weak_topics || [];
  const strongTopics = profile?.strong_topics || [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-in fade-in duration-200">
      {/* Knowledge Check Alert Banner if not completed */}
      {!user?.knowledge_check_completed && (
        <div className="bg-gradient-to-r from-amber-500/15 via-amber-500/10 to-slate-900 border border-amber-500/30 rounded-2xl p-4 sm:p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3.5">
            <div className="p-3 rounded-xl bg-amber-500/20 text-amber-300 border border-amber-500/30 shrink-0">
              <GraduationCap className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-sm sm:text-base font-bold text-white">Improve your recommendations</h3>
              <p className="text-xs text-slate-300 mt-0.5">
                Take the 5-minute Knowledge Check to assess your strengths and tailor adaptive problem recommendations.
              </p>
            </div>
          </div>
          <Link
            to="/knowledge-check"
            className="px-4 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs flex items-center gap-1.5 shrink-0 shadow-md transition-colors"
          >
            Take Knowledge Check
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      )}

      {/* Top Learner Overview Card */}
      <div className="bg-gradient-to-br from-slate-900 via-slate-900 to-slate-950 rounded-3xl border border-slate-800 p-6 sm:p-8 shadow-2xl space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono text-mentor-400 uppercase font-bold tracking-wider">
                LEARNER PROFILE
              </span>
              <span className="text-xs text-slate-500">•</span>
              <span className="text-xs text-slate-400 font-medium capitalize">
                Assessed Level: <strong className="text-white">{profile?.overall_level}</strong>
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
              Welcome back, {user?.name}!
            </h1>
            <p className="text-xs sm:text-sm text-slate-400">
              CodeMentor AI has mapped your concept strengths and areas for targeted improvement.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              to="/revise-mistakes"
              className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-2 border border-slate-700 transition-colors"
            >
              <RotateCcw className="w-4 h-4 text-amber-400" />
              Revise Mistakes
            </Link>
            <Link
              to="/problems"
              className="px-4 py-2.5 rounded-xl bg-mentor-500 hover:bg-mentor-600 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-lg shadow-mentor-500/20 transition-all"
            >
              <BookOpen className="w-4 h-4" />
              Browse Problems
            </Link>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
          <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Problems Solved</span>
            <div className="text-2xl font-bold text-white font-mono">{profile?.problems_solved || 0}</div>
            <span className="text-[10px] text-emerald-400 font-medium flex items-center gap-1">
              <CheckCircle className="w-3 h-3" /> {profile?.independent_solves || 0} independent
            </span>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Total Attempts</span>
            <div className="text-2xl font-bold text-white font-mono">{profile?.recent_performance?.total_attempts || 0}</div>
            <span className="text-[10px] text-slate-400">Across sessions</span>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Hints Requested</span>
            <div className="text-2xl font-bold text-amber-300 font-mono">{profile?.hints_used || 0}</div>
            <span className="text-[10px] text-slate-400">Progressive guidance</span>
          </div>

          <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Diagnostic Score</span>
            <div className="text-2xl font-bold text-mentor-400 font-mono">
              {profile?.knowledge_check_score !== null && profile?.knowledge_check_score !== undefined
                ? `${Math.round(profile.knowledge_check_score * 100)}%`
                : 'Pending'}
            </div>
            <span className="text-[10px] text-slate-400">Baseline accuracy</span>
          </div>
        </div>
      </div>

      {/* Weak Topics Notification Card */}
      {weakTopics.length > 0 && (
        <div className="bg-amber-950/20 border border-amber-500/30 rounded-2xl p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-amber-500/20 text-amber-300 border border-amber-500/30 shrink-0">
              <Target className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xs font-bold text-amber-300 uppercase tracking-wider">Priority Skill Gap Detected</div>
              <h4 className="text-sm font-semibold text-white capitalize mt-0.5">
                {weakTopics.join(', ')} — Needs Practice
              </h4>
              <p className="text-xs text-slate-400 mt-0.5">
                Recommended exercises below are optimized to build mental models for your priority topics.
              </p>
            </div>
          </div>
          <Link
            to="/revise-mistakes"
            className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-amber-300 border border-amber-500/30 text-xs font-semibold transition-colors shrink-0"
          >
            Practice Focus Topics
          </Link>
        </div>
      )}

      {/* Main Grid: Personalized Recommendations + Concept Mastery */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left 2 Cols: Personalized Problem Recommendations */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-mentor-400" />
              <h2 className="text-base font-bold text-white">Recommended For You</h2>
            </div>
            <Link to="/problems" className="text-xs text-mentor-400 hover:underline font-semibold flex items-center gap-1">
              View all problems <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="grid gap-3.5">
            {recommendations.map((rec) => (
              <div
                key={rec.problem_id}
                className="bg-slate-900/80 rounded-2xl p-5 border border-slate-800 hover:border-slate-700 transition-all space-y-3"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-300 border border-slate-700">
                        {rec.topic}
                      </span>
                      <span className="text-[10px] font-mono text-slate-500 uppercase">
                        {rec.difficulty}
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-white hover:text-mentor-400 transition-colors">
                      {rec.title}
                    </h3>
                  </div>

                  <button
                    onClick={() => handleStartProblem(rec.problem_id)}
                    disabled={startingSessionId === rec.problem_id}
                    className="px-4 py-2 rounded-xl bg-mentor-500 hover:bg-mentor-600 disabled:opacity-50 text-slate-950 font-bold text-xs flex items-center gap-1.5 shadow-md transition-all shrink-0"
                  >
                    {startingSessionId === rec.problem_id ? 'Starting...' : 'Solve with Tutor'}
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>

                {/* Natural language recommendation reason */}
                <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-start gap-2 text-xs text-slate-300">
                  <Lightbulb className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />
                  <span className="italic leading-relaxed">{rec.recommendation_reason}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right 1 Col: Concept Mastery Radar & Progress */}
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Award className="w-5 h-5 text-purple-400" />
            <h2 className="text-base font-bold text-white">Concept Mastery</h2>
          </div>

          <div className="bg-slate-900/80 rounded-2xl p-5 border border-slate-800 space-y-4">
            <MasteryMeters conceptMastery={profile?.concept_mastery || {}} />
          </div>
        </div>
      </div>
    </div>
  );
}
