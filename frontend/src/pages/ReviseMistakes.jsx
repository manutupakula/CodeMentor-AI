import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { learnerAPI, sessionsAPI } from '../api/client';
import { RotateCcw, AlertTriangle, Lightbulb, ArrowRight, CheckCircle2, Sparkles, BookOpen } from 'lucide-react';

export default function ReviseMistakes() {
  const [revisions, setRevisions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [startingId, setStartingId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchRevisions = async () => {
      try {
        const res = await learnerAPI.getReviseMistakes();
        setRevisions(res.data || []);
      } catch (err) {
        console.error("Failed to load mistake revisions", err);
      } finally {
        setLoading(false);
      }
    };
    fetchRevisions();
  }, []);

  const handleStartProblem = async (problemId) => {
    setStartingId(problemId);
    try {
      const res = await sessionsAPI.create(problemId);
      navigate(`/workspace/${res.data.id}`);
    } catch (err) {
      console.error("Failed to create session", err);
      navigate('/problems');
    } finally {
      setStartingId(null);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center space-y-3">
        <div className="w-10 h-10 border-2 border-mentor-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-xs text-slate-400">Analyzing your recurring mistake history...</p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-in fade-in duration-200">
      {/* Header */}
      <div className="space-y-2">
        <div className="flex items-center gap-2 text-xs font-mono text-amber-400 font-bold uppercase tracking-wider">
          <RotateCcw className="w-4 h-4" /> Misconception Analysis & Revision
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
          Revise My Mistakes
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 max-w-2xl">
          CodeMentor AI tracks your repeated conceptual and logical stumbling blocks to generate personalized corrective practice.
        </p>
      </div>

      {revisions.length === 0 ? (
        <div className="bg-slate-900/60 rounded-3xl border border-slate-800 p-12 text-center space-y-4">
          <div className="w-16 h-16 rounded-2xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center mx-auto border border-emerald-500/20">
            <CheckCircle2 className="w-8 h-8" />
          </div>
          <div className="space-y-1">
            <h3 className="text-base font-bold text-white">No Recurring Mistakes Detected!</h3>
            <p className="text-xs text-slate-400 max-w-md mx-auto">
              You haven't accumulated recurring error patterns yet. Continue solving practice problems and CodeMentor AI will keep track of any growth opportunities.
            </p>
          </div>
          <button
            onClick={() => navigate('/problems')}
            className="px-5 py-2.5 rounded-xl bg-mentor-500 hover:bg-mentor-600 text-slate-950 font-bold text-xs inline-flex items-center gap-1.5 shadow-md transition-all"
          >
            <BookOpen className="w-4 h-4" />
            Explore Practice Challenges
          </button>
        </div>
      ) : (
        <div className="grid gap-4">
          {revisions.map((rev, idx) => (
            <div
              key={idx}
              className="bg-slate-900/90 rounded-2xl p-6 border border-slate-800 space-y-4 hover:border-slate-700 transition-all shadow-xl"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="p-3 rounded-xl bg-amber-500/20 text-amber-300 border border-amber-500/30 shrink-0">
                    <AlertTriangle className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-base font-bold text-white">
                        {rev.mistake_type}
                      </h3>
                      <span className="px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-bold font-mono">
                        {rev.count} occurrence{rev.count > 1 ? 's' : ''}
                      </span>
                    </div>
                    <span className="text-xs text-slate-400">Concept: {rev.concept}</span>
                  </div>
                </div>

                {rev.recommended_problem && (
                  <button
                    onClick={() => handleStartProblem(rev.recommended_problem.problem_id)}
                    disabled={startingId === rev.recommended_problem.problem_id}
                    className="px-4 py-2 rounded-xl bg-mentor-500 hover:bg-mentor-600 disabled:opacity-50 text-slate-950 font-bold text-xs flex items-center gap-1.5 shadow-md transition-all shrink-0 self-start sm:self-auto"
                  >
                    {startingId === rev.recommended_problem.problem_id ? 'Opening...' : 'Practice Corrective Problem'}
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>

              {/* Advice Callout */}
              <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800/80 flex items-start gap-2.5 text-xs text-slate-300">
                <Lightbulb className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold text-white block mb-0.5">Tutor Conceptual Guidance:</span>
                  <span className="leading-relaxed">{rev.advice}</span>
                </div>
              </div>

              {/* Matched Targeted Problem Preview */}
              {rev.recommended_problem && (
                <div className="pt-2 flex items-center justify-between text-xs text-slate-400 border-t border-slate-800/60">
                  <span className="flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-purple-400" />
                    Target Challenge: <strong className="text-slate-200">{rev.recommended_problem.title}</strong> ({rev.recommended_problem.difficulty})
                  </span>
                  <span className="text-[11px] italic text-slate-500 hidden sm:inline">
                    {rev.recommended_problem.recommendation_reason}
                  </span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
