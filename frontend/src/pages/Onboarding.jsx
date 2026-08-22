import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { GraduationCap, ArrowRight, CheckCircle2, ShieldCheck, Zap } from 'lucide-react';

export default function Onboarding() {
  const { user } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="min-h-[85vh] flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-xl bg-slate-900/90 rounded-3xl border border-slate-800 p-8 sm:p-10 shadow-2xl space-y-8 text-center">
        {/* Header Icon */}
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-400 to-mentor-500 flex items-center justify-center mx-auto shadow-xl shadow-mentor-500/20">
          <GraduationCap className="w-9 h-9 text-slate-950 stroke-[2.2]" />
        </div>

        <div className="space-y-3">
          <span className="text-xs font-mono text-mentor-400 bg-mentor-500/10 px-3 py-1 rounded-full border border-mentor-500/20 uppercase font-bold tracking-wider">
            Step 3 of Onboarding
          </span>
          <h2 className="text-3xl font-extrabold text-white tracking-tight">
            Let's check what you actually know.
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 max-w-md mx-auto leading-relaxed">
            Take an optional 5-minute baseline diagnostic to verify your self-assessment against real code challenges and unlock hyper-personalized recommendations.
          </p>
        </div>

        {/* Benefits Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-left">
          <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1.5">
            <div className="text-mentor-400 font-bold text-xs flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" /> Baseline Check
            </div>
            <p className="text-[11px] text-slate-400">
              Curated conceptual & output-prediction questions.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1.5">
            <div className="text-blue-400 font-bold text-xs flex items-center gap-1.5">
              <Zap className="w-3.5 h-3.5" /> Gap Analysis
            </div>
            <p className="text-[11px] text-slate-400">
              Compare self-declared level with actual mastery.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1.5">
            <div className="text-purple-400 font-bold text-xs flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5" /> Weakness Radar
            </div>
            <p className="text-[11px] text-slate-400">
              Target recursion, loops, or arrays precisely.
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="space-y-3 pt-2">
          <button
            onClick={() => navigate('/knowledge-check')}
            className="w-full py-3.5 rounded-xl bg-gradient-to-r from-mentor-400 to-emerald-500 hover:from-mentor-500 hover:to-emerald-600 text-slate-950 font-bold text-sm flex items-center justify-center gap-2 shadow-xl shadow-mentor-500/20 transition-all hover:scale-[1.01]"
          >
            START KNOWLEDGE CHECK
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={() => navigate('/dashboard')}
            className="w-full py-2.5 rounded-xl bg-slate-950 hover:bg-slate-800 text-slate-400 hover:text-white border border-slate-800 text-xs font-semibold transition-colors"
          >
            SKIP FOR NOW
          </button>
        </div>

        <p className="text-[11px] text-slate-500">
          You can always take or retake the Knowledge Check anytime from your Dashboard or Profile.
        </p>
      </div>
    </div>
  );
}
