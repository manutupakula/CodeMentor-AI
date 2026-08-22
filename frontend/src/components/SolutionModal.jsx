import React from 'react';
import { CheckCircle2, Lock, Unlock, Zap, Clock, HardDrive, Sparkles, X } from 'lucide-react';

export default function SolutionModal({
  isOpen,
  onClose,
  solutionData,
  isUnlocked
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-2xl bg-slate-900 rounded-2xl border border-slate-700/80 shadow-2xl overflow-hidden max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/40">
          <div className="flex items-center gap-3">
            <div className={`p-2 rounded-xl ${isUnlocked ? 'bg-mentor-500/20 text-mentor-400' : 'bg-red-500/20 text-red-400'}`}>
              {isUnlocked ? <Unlock className="w-5 h-5" /> : <Lock className="w-5 h-5" />}
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">
                {isUnlocked ? 'Official Solution & Pedagogical Breakdown' : 'Solution Locked'}
              </h3>
              <p className="text-xs text-slate-400">
                {isUnlocked ? solutionData?.unlocked_reason || 'Tutoring cycle completed' : 'Complete your 3 allowed attempts or solve independently to unlock'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto space-y-5 text-sm">
          {!isUnlocked ? (
            <div className="text-center py-8 space-y-4">
              <div className="w-16 h-16 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center mx-auto text-amber-400">
                <Lock className="w-8 h-8" />
              </div>
              <div className="space-y-1">
                <h4 className="text-base font-semibold text-white">Server-Side Solution Lock Active</h4>
                <p className="text-xs text-slate-400 max-w-md mx-auto">
                  To protect your learning journey, CodeMentor AI prevents revealing full code answers until you attempt the problem and engage with progressive hints.
                </p>
              </div>
            </div>
          ) : (
            <>
              {/* Solution Code */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                    Reference Python Solution
                  </span>
                  <span className="text-xs font-mono text-mentor-400 bg-mentor-500/10 px-2 py-0.5 rounded border border-mentor-500/20">
                    Validated
                  </span>
                </div>
                <pre className="p-4 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs text-emerald-300 overflow-x-auto leading-relaxed">
                  <code>{solutionData?.solution || '# Solution unlocked'}</code>
                </pre>
              </div>

              {/* Conceptual Explanation */}
              {solutionData?.explanation && (
                <div className="space-y-1.5 bg-slate-800/40 p-4 rounded-xl border border-slate-700/50">
                  <div className="flex items-center gap-2 text-slate-200 font-semibold text-xs uppercase tracking-wider">
                    <Sparkles className="w-4 h-4 text-purple-400" />
                    How It Works
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    {solutionData.explanation}
                  </p>
                </div>
              )}

              {/* Better Approach / Optimization */}
              {solutionData?.better_approach && (
                <div className="space-y-1.5 bg-slate-800/40 p-4 rounded-xl border border-slate-700/50">
                  <div className="flex items-center gap-2 text-slate-200 font-semibold text-xs uppercase tracking-wider">
                    <Zap className="w-4 h-4 text-amber-400" />
                    Optimization & Better Approach
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    {solutionData.better_approach}
                  </p>
                </div>
              )}

              {/* Complexity Metrics */}
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-center gap-3">
                  <Clock className="w-5 h-5 text-blue-400 shrink-0" />
                  <div>
                    <span className="text-[10px] text-slate-400 block uppercase font-bold">Time Complexity</span>
                    <span className="text-xs font-mono font-semibold text-slate-200">{solutionData?.time_complexity || 'O(n)'}</span>
                  </div>
                </div>
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-center gap-3">
                  <HardDrive className="w-5 h-5 text-indigo-400 shrink-0" />
                  <div>
                    <span className="text-[10px] text-slate-400 block uppercase font-bold">Space Complexity</span>
                    <span className="text-xs font-mono font-semibold text-slate-200">{solutionData?.space_complexity || 'O(1)'}</span>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-800 bg-slate-950/40 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
