import React, { useState } from 'react';
import Editor from '@monaco-editor/react';
import { tutorAPI } from '../api/client';
import ProgressiveHintDrawer from '../components/ProgressiveHintDrawer';
import { Sparkles, Play, Lightbulb, Bot, Terminal, CheckCircle2, AlertCircle } from 'lucide-react';

export default function CustomProblem() {
  const [title, setTitle] = useState('Find the First Duplicate Element');
  const [description, setDescription] = useState('Given a list of numbers, return the first integer that occurs more than once in the list. If no duplicate exists, return -1.');
  const [code, setCode] = useState('def find_first_duplicate(nums):\n    # Write your own code to analyze\n    for i in range(len(nums)):\n        for j in range(i + 1, len(nums)):\n            if nums[i] == nums[j]:\n                return nums[j]\n    return -1\n');
  const [hintLevel, setHintLevel] = useState(1);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!title.trim() || !code.trim() || loading) return;
    setLoading(true);
    setError('');

    try {
      const res = await tutorAPI.customProblem({
        problem_title: title,
        problem_description: description,
        student_code: code,
        language: 'python',
        hint_level: hintLevel
      });
      setAnalysisResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze custom problem.');
    } finally {
      setLoading(false);
    }
  };

  const handleRequestHint = (newLevel) => {
    setHintLevel(newLevel);
    if (analysisResult) {
      // Re-trigger analysis with new hint level
      setTimeout(() => {
        handleAnalyze();
      }, 50);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="space-y-1">
        <div className="flex items-center gap-2 text-xs font-mono text-purple-400 font-bold uppercase tracking-wider">
          <Sparkles className="w-4 h-4" /> Open Tutoring Workspace
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
          Bring Your Own Problem
        </h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Paste any coding assignment or custom problem to receive progressive hints, misconception analysis, and pedagogical guidance.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Problem Input & Progressive Hints (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 space-y-4 shadow-xl">
            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                Problem Title
              </label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Invert Binary Tree"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-mentor-500"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                Problem Statement / Requirements
              </label>
              <textarea
                rows={4}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe what the problem requires, inputs, and outputs..."
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-mentor-500 resize-none"
              />
            </div>
          </div>

          {/* Progressive Hint Drawer */}
          <ProgressiveHintDrawer
            currentHintLevel={hintLevel}
            activeHint={analysisResult?.hint}
            onRequestHint={handleRequestHint}
            solutionUnlocked={false}
            attemptsUsed={hintLevel}
            attemptsAllowed={3}
            loading={loading}
          />
        </div>

        {/* Right Column: Code Editor & AI Diagnosis (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="bg-slate-900/90 rounded-2xl border border-slate-800 overflow-hidden shadow-xl flex flex-col">
            <div className="px-4 py-2.5 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-300">Your Python Solution</span>
              <span className="text-[10px] font-mono text-slate-500">Hint Level {hintLevel}</span>
            </div>

            <div className="h-64 relative">
              <Editor
                height="100%"
                defaultLanguage="python"
                theme="vs-dark"
                value={code}
                onChange={(val) => setCode(val || '')}
                options={{
                  fontSize: 13,
                  fontFamily: 'Fira Code, monospace',
                  minimap: { enabled: false },
                  lineNumbers: 'on',
                  tabSize: 4,
                  automaticLayout: true,
                }}
              />
            </div>

            <div className="p-3 bg-slate-950 border-t border-slate-800 flex justify-end">
              <button
                onClick={handleAnalyze}
                disabled={loading || !code.trim()}
                className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-mentor-400 to-emerald-500 hover:from-mentor-500 hover:to-emerald-600 disabled:opacity-50 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-lg shadow-mentor-500/20 transition-all"
              >
                {loading ? (
                  <>
                    <div className="w-3.5 h-3.5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
                    Diagnosing Code...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 fill-slate-950 stroke-none" />
                    Analyze with Tutor
                  </>
                )}
              </button>
            </div>
          </div>

          {/* AI Analysis Feedback Panel */}
          {analysisResult && (
            <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-6 space-y-4 shadow-xl animate-in fade-in duration-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="p-2 rounded-xl bg-mentor-500/20 text-mentor-400">
                    <Bot className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">AI Tutor Diagnostic Feedback</h3>
                    <span className="text-xs text-slate-400">Concept: {analysisResult.concept}</span>
                  </div>
                </div>

                <span className={`px-2.5 py-1 rounded-full text-xs font-bold font-mono uppercase border ${
                  analysisResult.is_correct
                    ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
                    : 'bg-rose-500/20 text-rose-300 border-rose-500/30'
                }`}>
                  {analysisResult.error_type?.replace('_', ' ')}
                </span>
              </div>

              {/* Diagnosis text */}
              <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 text-xs text-slate-200 leading-relaxed">
                <span className="font-bold text-slate-400 uppercase tracking-wider block mb-1 text-[11px]">
                  Analysis
                </span>
                {analysisResult.analysis}
              </div>

              {/* Active Progressive Hint */}
              {analysisResult.hint && (
                <div className="p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 text-xs text-amber-200 leading-relaxed flex items-start gap-2.5">
                  <Lightbulb className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold text-amber-300 block mb-0.5">
                      Hint Level {analysisResult.hint_level}:
                    </span>
                    {analysisResult.hint}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
