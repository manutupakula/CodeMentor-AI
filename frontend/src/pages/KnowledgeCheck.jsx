import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { assessmentAPI } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { 
  GraduationCap, 
  CheckCircle2, 
  XCircle, 
  ArrowRight, 
  ArrowLeft, 
  Sparkles, 
  TrendingUp, 
  ShieldAlert, 
  HelpCircle,
  Award
} from 'lucide-react';

export default function KnowledgeCheck() {
  const { user, updateUser } = useAuth();
  const navigate = useNavigate();

  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const res = await assessmentAPI.start();
        setQuestions(res.data.questions || []);
      } catch (err) {
        setError('Failed to load assessment questions. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    fetchQuestions();
  }, []);

  const handleSelectOption = (option) => {
    const currentQ = questions[currentIndex];
    setSelectedAnswers(prev => ({
      ...prev,
      [currentQ.question_id]: option
    }));
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setError('');

    const formattedAnswers = questions.map(q => ({
      question_id: q.question_id,
      selected_answer: selectedAnswers[q.question_id] || ''
    }));

    try {
      const res = await assessmentAPI.submit(formattedAnswers);
      setResult(res.data);
      updateUser({ knowledge_check_completed: true });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to evaluate assessment.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center space-y-3">
        <div className="w-10 h-10 border-2 border-mentor-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-xs text-slate-400">Loading curated Knowledge Check questions...</p>
      </div>
    );
  }

  // Diagnostic Results Screen
  if (result) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8 space-y-8 animate-in fade-in duration-300">
        {/* Header Banner */}
        <div className="bg-gradient-to-br from-slate-900 to-slate-950 rounded-3xl p-8 border border-slate-800 shadow-2xl space-y-6">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-6 text-center sm:text-left">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-2xl bg-mentor-500/20 text-mentor-400 flex items-center justify-center border border-mentor-500/30">
                <Award className="w-9 h-9" />
              </div>
              <div>
                <span className="text-xs font-mono text-mentor-400 uppercase font-bold tracking-wider">
                  Diagnostic Baseline Complete
                </span>
                <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
                  Knowledge Check Results
                </h1>
              </div>
            </div>

            <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 text-center min-w-[140px]">
              <span className="text-[10px] text-slate-400 block uppercase font-bold">Verified Score</span>
              <span className="text-3xl font-extrabold text-mentor-400 font-mono">
                {result.score_percentage}%
              </span>
            </div>
          </div>

          {/* Self-Declared vs Actual Level Comparison */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1">
              <span className="text-[11px] text-slate-400 font-bold uppercase block">Self-Declared Level</span>
              <div className="text-lg font-bold text-slate-200 capitalize">
                {result.self_declared_level}
              </div>
              <p className="text-[11px] text-slate-500">Your initial estimate during signup</p>
            </div>

            <div className="p-4 rounded-xl bg-mentor-950/20 border border-mentor-500/30 space-y-1">
              <span className="text-[11px] text-mentor-400 font-bold uppercase block">Calculated Level</span>
              <div className="text-lg font-bold text-white capitalize flex items-center gap-2">
                {result.calculated_level}
                <CheckCircle2 className="w-4 h-4 text-mentor-400" />
              </div>
              <p className="text-[11px] text-mentor-300/80">Determined through diagnostic question bank</p>
            </div>
          </div>

          {/* Gap Explanation */}
          <div className="p-5 rounded-2xl bg-slate-950/70 border border-slate-800 space-y-2">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-200 uppercase tracking-wider">
              <Sparkles className="w-4 h-4 text-purple-400" />
              AI Gap & Learning Path Analysis
            </div>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
              {result.gap_summary}
            </p>
          </div>

          {/* Strong vs Weak Breakdown */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
              <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 uppercase tracking-wider">
                <CheckCircle2 className="w-4 h-4" /> Strong Foundations
              </div>
              <div className="flex flex-wrap gap-1.5">
                {result.strong_topics?.length > 0 ? (
                  result.strong_topics.map(t => (
                    <span key={t} className="px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 text-xs font-medium border border-emerald-500/30 capitalize">
                      {t}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-400 italic">No dominant strengths yet.</span>
                )}
              </div>
            </div>

            <div className="p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 space-y-2">
              <div className="flex items-center gap-2 text-xs font-bold text-amber-400 uppercase tracking-wider">
                <ShieldAlert className="w-4 h-4" /> Priority Focus Areas
              </div>
              <div className="flex flex-wrap gap-1.5">
                {result.weak_topics?.length > 0 ? (
                  result.weak_topics.map(t => (
                    <span key={t} className="px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-300 text-xs font-medium border border-amber-500/30 capitalize">
                      {t}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-400 italic">All baseline topics mastered!</span>
                )}
              </div>
            </div>
          </div>

          {/* Continue Action */}
          <button
            onClick={() => navigate('/dashboard')}
            className="w-full py-3.5 rounded-xl bg-gradient-to-r from-mentor-400 to-emerald-500 hover:from-mentor-500 hover:to-emerald-600 text-slate-950 font-bold text-sm flex items-center justify-center gap-2 shadow-xl shadow-mentor-500/20 transition-all hover:scale-[1.01]"
          >
            Go to Personalized Dashboard
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    );
  }

  const currentQ = questions[currentIndex];
  const answeredCount = Object.keys(selectedAnswers).length;
  const progressPct = Math.round(((currentIndex + 1) / questions.length) * 100);

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">
      {/* Progress & Stepper */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs font-semibold text-slate-400">
          <span>Question {currentIndex + 1} of {questions.length}</span>
          <span className="font-mono">{answeredCount} of {questions.length} Answered</span>
        </div>
        <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden border border-slate-800">
          <div
            className="h-full bg-gradient-to-r from-mentor-500 to-emerald-400 rounded-full transition-all duration-300"
            style={{ width: `${progressPct}%` }}
          />
        </div>
      </div>

      {/* Question Card */}
      {currentQ && (
        <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-6 sm:p-8 shadow-2xl space-y-6">
          <div className="flex items-center justify-between">
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-slate-800 border border-slate-700 text-slate-300">
              {currentQ.topic} ({currentQ.subconcept?.replace('_', ' ')})
            </span>
            <span className="text-xs font-mono text-slate-500 uppercase">
              {currentQ.difficulty}
            </span>
          </div>

          <div className="text-sm sm:text-base font-medium text-slate-100 whitespace-pre-wrap leading-relaxed">
            {currentQ.question}
          </div>

          {/* Options */}
          <div className="space-y-3 pt-2">
            {currentQ.options?.map((opt, optIdx) => {
              const isSelected = selectedAnswers[currentQ.question_id] === opt;
              return (
                <button
                  key={optIdx}
                  type="button"
                  onClick={() => handleSelectOption(opt)}
                  className={`w-full p-4 rounded-xl border text-left text-xs sm:text-sm font-medium transition-all flex items-center justify-between ${
                    isSelected
                      ? 'bg-mentor-500/15 border-mentor-500 text-white shadow-md'
                      : 'bg-slate-950/60 border-slate-800 text-slate-300 hover:border-slate-700 hover:bg-slate-950'
                  }`}
                >
                  <span className="pr-4">{opt}</span>
                  <div className={`w-5 h-5 rounded-full border flex items-center justify-center shrink-0 ${
                    isSelected ? 'border-mentor-500 bg-mentor-500 text-slate-950' : 'border-slate-700'
                  }`}>
                    {isSelected && <CheckCircle2 className="w-4 h-4 stroke-[3]" />}
                  </div>
                </button>
              );
            })}
          </div>

          {error && (
            <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
              {error}
            </div>
          )}

          {/* Footer Controls */}
          <div className="flex items-center justify-between pt-4 border-t border-slate-800">
            <button
              onClick={handlePrev}
              disabled={currentIndex === 0}
              className="px-4 py-2 rounded-xl bg-slate-950 hover:bg-slate-800 disabled:opacity-30 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              Previous
            </button>

            {currentIndex === questions.length - 1 ? (
              <button
                onClick={handleSubmit}
                disabled={submitting}
                className="px-6 py-2.5 rounded-xl bg-mentor-500 hover:bg-mentor-600 disabled:opacity-50 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-lg shadow-mentor-500/20 transition-all"
              >
                {submitting ? 'Evaluating...' : 'Submit Assessment'}
                <CheckCircle2 className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={handleNext}
                className="px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs flex items-center gap-1.5 transition-colors"
              >
                Next Question
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
