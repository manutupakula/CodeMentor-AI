import React from 'react';
import { Award, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react';

export default function MasteryMeters({ conceptMastery = {} }) {
  const topics = Object.entries(conceptMastery);

  if (topics.length === 0) {
    return (
      <div className="text-center py-6 text-slate-500 text-xs">
        No concept mastery data recorded yet. Take the Knowledge Check to initialize your profile!
      </div>
    );
  }

  const getProgressColor = (score) => {
    if (score >= 0.70) return 'bg-emerald-500 text-emerald-400';
    if (score >= 0.50) return 'bg-blue-500 text-blue-400';
    return 'bg-amber-500 text-amber-400';
  };

  const getBadge = (score) => {
    if (score >= 0.70) return { label: 'Mastered', color: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' };
    if (score >= 0.50) return { label: 'Practicing', color: 'bg-blue-500/20 text-blue-300 border-blue-500/30' };
    return { label: 'Needs Focus', color: 'bg-amber-500/20 text-amber-300 border-amber-500/30' };
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
      {topics.map(([topic, score]) => {
        const pct = Math.round(score * 100);
        const badge = getBadge(score);

        return (
          <div
            key={topic}
            className="bg-slate-900/70 rounded-xl p-3.5 border border-slate-800 space-y-2.5 hover:border-slate-700 transition-colors"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-200 capitalize">
                {topic.replace('_', ' ')}
              </span>
              <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full border ${badge.color}`}>
                {badge.label}
              </span>
            </div>

            <div className="space-y-1">
              <div className="flex justify-between text-[11px] font-mono text-slate-400">
                <span>Mastery</span>
                <span className="font-bold text-slate-200">{pct}%</span>
              </div>
              <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${getProgressColor(score).split(' ')[0]}`}
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
