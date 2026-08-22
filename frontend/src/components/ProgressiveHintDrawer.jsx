import React from 'react';
import { Lightbulb, Lock, Unlock, ChevronRight, HelpCircle, Sparkles } from 'lucide-react';

export default function ProgressiveHintDrawer({
  currentHintLevel,
  activeHint,
  onRequestHint,
  solutionUnlocked,
  attemptsUsed,
  attemptsAllowed = 3,
  loading = false
}) {
  const hints = [
    {
      level: 1,
      title: "Hint Level 1: Socratic Discovery",
      desc: "Guiding questions to discover where your logic assumption breaks down.",
      icon: HelpCircle,
      color: "border-blue-500/30 bg-blue-500/10 text-blue-300"
    },
    {
      level: 2,
      title: "Hint Level 2: Conceptual Mechanism",
      desc: "Explanation of the underlying data structures, state changes, and mechanisms.",
      icon: Lightbulb,
      color: "border-amber-500/30 bg-amber-500/10 text-amber-300"
    },
    {
      level: 3,
      title: "Hint Level 3: Code Directional Guidance",
      desc: "Concrete guidance on boundary checks, conditions, and indexing.",
      icon: Sparkles,
      color: "border-emerald-500/30 bg-emerald-500/10 text-emerald-300"
    }
  ];

  return (
    <div className="bg-slate-900/60 rounded-xl border border-slate-800 p-4 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Lightbulb className="w-5 h-5 text-amber-400" />
          <h3 className="font-semibold text-white text-sm">Progressive Hint System</h3>
        </div>
        <span className="text-xs font-mono text-slate-400 bg-slate-800 px-2.5 py-1 rounded-full border border-slate-700">
          Level {currentHintLevel} of 3
        </span>
      </div>

      <div className="space-y-3">
        {hints.map((h) => {
          const isUnlocked = currentHintLevel >= h.level || solutionUnlocked;
          const isCurrent = currentHintLevel === h.level;
          const Icon = h.icon;

          return (
            <div
              key={h.level}
              className={`rounded-lg border p-3.5 transition-all ${
                isUnlocked
                  ? `${h.color} shadow-sm`
                  : 'border-slate-800 bg-slate-950/40 text-slate-500'
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-2.5">
                  <div className={`p-1.5 rounded-md ${isUnlocked ? 'bg-slate-900/60' : 'bg-slate-900/30 text-slate-600'}`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className={`text-xs font-semibold ${isUnlocked ? 'text-slate-100' : 'text-slate-500'}`}>
                      {h.title}
                    </h4>
                    <p className="text-[11px] text-slate-400 mt-0.5">
                      {h.desc}
                    </p>
                  </div>
                </div>

                <div className="flex items-center">
                  {isUnlocked ? (
                    <Unlock className="w-4 h-4 text-mentor-400" />
                  ) : (
                    <Lock className="w-4 h-4 text-slate-600" />
                  )}
                </div>
              </div>

              {/* Show hint text if unlocked and active */}
              {isUnlocked && activeHint && isCurrent && (
                <div className="mt-3 pt-3 border-t border-slate-700/40 bg-slate-950/60 p-3 rounded-md">
                  <p className="text-xs text-slate-200 leading-relaxed font-sans">
                    💡 <span className="font-medium">{activeHint}</span>
                  </p>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Action to request next hint */}
      {currentHintLevel < 3 && !solutionUnlocked && (
        <button
          onClick={() => onRequestHint(currentHintLevel + 1)}
          disabled={loading}
          className="w-full py-2 px-3 rounded-lg bg-slate-800 hover:bg-slate-700/80 text-amber-300 border border-amber-500/30 text-xs font-semibold flex items-center justify-center gap-2 transition-all disabled:opacity-50 shadow-sm"
        >
          <Lightbulb className="w-3.5 h-3.5" />
          Request Hint Level {currentHintLevel + 1}
        </button>
      )}
    </div>
  );
}
