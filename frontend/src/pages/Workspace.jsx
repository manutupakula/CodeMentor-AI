import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import { sessionsAPI, problemsAPI } from '../api/client';
import ProgressiveHintDrawer from '../components/ProgressiveHintDrawer';
import SolutionModal from '../components/SolutionModal';
import TutorChatPane from '../components/TutorChatPane';
import TestResultsConsole from '../components/TestResultsConsole';
import { 
  Play, 
  Lightbulb, 
  RotateCcw, 
  Lock, 
  Unlock, 
  MessageSquare, 
  Sparkles, 
  CheckCircle2, 
  ArrowLeft,
  ChevronDown,
  Terminal,
  Code
} from 'lucide-react';

export default function Workspace() {
  const { sessionId } = useParams();
  const navigate = useNavigate();

  const [session, setSession] = useState(null);
  const [problem, setProblem] = useState(null);
  const [code, setCode] = useState('');
  const [activeHint, setActiveHint] = useState(null);
  const [executionResult, setExecutionResult] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [solutionData, setSolutionData] = useState(null);
  const [isSolutionModalOpen, setIsSolutionModalOpen] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [hintLoading, setHintLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch session & problem
  useEffect(() => {
    const initWorkspace = async () => {
      try {
        const sessRes = await sessionsAPI.get(sessionId);
        const sessData = sessRes.data;
        setSession(sessData);

        const probRes = await problemsAPI.getById(sessData.problem_id);
        const probData = probRes.data;
        setProblem(probData);
        setCode(probData.starter_code || '# Write your code here\n');

        // If solution is already unlocked, fetch solution details
        if (sessData.solution_unlocked) {
          try {
            const solRes = await sessionsAPI.getSolution(sessionId);
            setSolutionData(solRes.data);
          } catch (e) {}
        }
      } catch (err) {
        console.error("Workspace init error", err);
        setError("Failed to load workspace session.");
      } finally {
        setLoading(false);
      }
    };
    initWorkspace();
  }, [sessionId]);

  // Submit Code Attempt
  const handleSubmitAttempt = async () => {
    if (!code.trim() || submitting) return;
    setSubmitting(true);
    setError('');

    try {
      const res = await sessionsAPI.submitAttempt(sessionId, code, 'python');
      const data = res.data;
      
      setExecutionResult(data.execution_result);
      setAnalysisData(data);
      setActiveHint(data.hint);

      // Update session state locally
      setSession(prev => ({
        ...prev,
        attempts_used: data.attempt_number,
        attempts_remaining: data.attempts_remaining,
        current_hint_level: data.hint_level,
        solution_unlocked: data.solution_unlocked,
        status: data.is_correct ? 'solved' : (data.solution_unlocked ? 'exhausted' : 'in_progress')
      }));

      // If solution unlocked, store solution details
      if (data.solution_unlocked && data.solution) {
        setSolutionData({
          problem_id: problem.id,
          solution: data.solution,
          explanation: data.explanation,
          better_approach: data.better_approach,
          time_complexity: data.time_complexity,
          space_complexity: data.space_complexity,
          unlocked_reason: data.is_correct ? 'Solved successfully!' : 'Unlocked after allowed attempts'
        });
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze code.');
    } finally {
      setSubmitting(false);
    }
  };

  // Request Next Hint
  const handleRequestHint = async (targetLevel) => {
    setHintLoading(true);
    try {
      const res = await sessionsAPI.requestHint(sessionId, targetLevel);
      setActiveHint(res.data.hint_text);
      setSession(prev => ({
        ...prev,
        current_hint_level: res.data.hint_level,
        hints_used: Math.max(prev.hints_used || 0, res.data.hint_level)
      }));
    } catch (err) {
      console.error("Hint request error", err);
    } finally {
      setHintLoading(false);
    }
  };

  // View Solution (with server-side check)
  const handleOpenSolutionModal = async () => {
    if (session?.solution_unlocked && !solutionData) {
      try {
        const solRes = await sessionsAPI.getSolution(sessionId);
        setSolutionData(solRes.data);
      } catch (e) {
        console.error("Fetch solution error", e);
      }
    }
    setIsSolutionModalOpen(true);
  };

  const handleResetCode = () => {
    if (problem?.starter_code) {
      setCode(problem.starter_code);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center space-y-3">
        <div className="w-10 h-10 border-2 border-mentor-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-xs text-slate-400">Preparing coding workspace and tutor environment...</p>
      </div>
    );
  }

  if (error && !problem) {
    return (
      <div className="max-w-md mx-auto my-16 text-center space-y-4 p-8 bg-slate-900 rounded-2xl border border-slate-800">
        <div className="text-rose-400 text-sm font-semibold">{error}</div>
        <button
          onClick={() => navigate('/problems')}
          className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs"
        >
          Return to Problems
        </button>
      </div>
    );
  }

  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col overflow-hidden bg-slate-950">
      {/* Top Problem Toolbar */}
      <div className="px-4 py-2.5 bg-slate-900 border-b border-slate-800 flex items-center justify-between gap-4 shrink-0">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/problems')}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            title="Back to Catalog"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-300 border border-slate-700">
              {problem?.topic}
            </span>
            <h1 className="text-sm font-bold text-white truncate max-w-xs sm:max-w-md">
              {problem?.title}
            </h1>
          </div>
        </div>

        {/* Right Controls */}
        <div className="flex items-center gap-3">
          {/* Attempt Badge */}
          <div className="px-3 py-1 rounded-full bg-slate-950 border border-slate-800 text-xs font-mono text-slate-300 flex items-center gap-1.5">
            <span className="text-slate-500">Attempt</span>
            <strong className="text-white">{session?.attempts_used || 0}</strong>
            <span className="text-slate-500">of</span>
            <strong className="text-white">{session?.attempts_allowed || 3}</strong>
          </div>

          {/* Solution Status Button */}
          <button
            onClick={handleOpenSolutionModal}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 border transition-all ${
              session?.solution_unlocked
                ? 'bg-purple-500/20 text-purple-300 border-purple-500/40 hover:bg-purple-500/30'
                : 'bg-slate-800/80 text-slate-400 border-slate-700 hover:text-slate-200'
            }`}
          >
            {session?.solution_unlocked ? (
              <>
                <Unlock className="w-3.5 h-3.5 text-purple-400" />
                View Solution
              </>
            ) : (
              <>
                <Lock className="w-3.5 h-3.5 text-slate-500" />
                Solution Locked
              </>
            )}
          </button>

          {/* AI Chat Drawer Toggle */}
          <button
            onClick={() => setIsChatOpen(!isChatOpen)}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 border transition-all ${
              isChatOpen
                ? 'bg-mentor-500 text-slate-950 font-bold border-mentor-400'
                : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700'
            }`}
          >
            <MessageSquare className="w-3.5 h-3.5" />
            Tutor Chat
          </button>
        </div>
      </div>

      {/* Main Split Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Column: Problem Description & Progressive Hints (40% width) */}
        <div className="w-[42%] border-r border-slate-800 p-5 overflow-y-auto space-y-6 bg-slate-950/60">
          <div className="space-y-3">
            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-400 font-mono capitalize">
                Difficulty: <strong className="text-slate-200">{problem?.difficulty}</strong>
              </span>
              <span className="text-slate-500 font-mono text-[11px]">
                Concept: {problem?.subconcept?.replace('_', ' ')}
              </span>
            </div>

            <div className="text-xs sm:text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
              {problem?.description}
            </div>
          </div>

          {/* Examples */}
          {problem?.examples?.length > 0 && (
            <div className="space-y-3">
              <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">Examples</h3>
              <div className="space-y-2">
                {problem.examples.map((ex, idx) => (
                  <div key={idx} className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono space-y-1">
                    <div><span className="text-slate-500">Input:</span> <span className="text-slate-200">{ex.input_str}</span></div>
                    <div><span className="text-slate-500">Output:</span> <span className="text-emerald-400">{ex.output_str}</span></div>
                    {ex.explanation && (
                      <div className="text-[11px] text-slate-400 pt-1 border-t border-slate-800/60 font-sans">
                        {ex.explanation}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Constraints */}
          {problem?.constraints?.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">Constraints</h3>
              <ul className="list-disc list-inside text-xs font-mono text-slate-400 space-y-1">
                {problem.constraints.map((c, idx) => (
                  <li key={idx}>{c}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Progressive Hint Drawer */}
          <div className="pt-2">
            <ProgressiveHintDrawer
              currentHintLevel={session?.current_hint_level || 0}
              activeHint={activeHint}
              onRequestHint={handleRequestHint}
              solutionUnlocked={session?.solution_unlocked}
              attemptsUsed={session?.attempts_used || 0}
              attemptsAllowed={session?.attempts_allowed || 3}
              loading={hintLoading}
            />
          </div>
        </div>

        {/* Middle/Right: Code Editor & Test Results (58% width) */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Editor Header */}
          <div className="px-4 py-2 bg-slate-900/90 border-b border-slate-800 flex items-center justify-between shrink-0">
            <div className="flex items-center gap-2">
              <Code className="w-4 h-4 text-mentor-400" />
              <span className="text-xs font-semibold text-slate-300">Solution Editor (Python 3)</span>
            </div>
            <button
              onClick={handleResetCode}
              className="text-[11px] text-slate-400 hover:text-white flex items-center gap-1 transition-colors"
            >
              <RotateCcw className="w-3 h-3" />
              Reset Starter Code
            </button>
          </div>

          {/* Monaco Editor Container (60% height) */}
          <div className="h-[55%] relative">
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
                scrollBeyondLastLine: false,
                lineNumbers: 'on',
                tabSize: 4,
                automaticLayout: true,
              }}
            />

            {/* Floating Run & Analyze Button */}
            <div className="absolute bottom-3 right-4 z-10 flex items-center gap-2">
              <button
                onClick={handleSubmitAttempt}
                disabled={submitting}
                className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-mentor-400 to-emerald-500 hover:from-mentor-500 hover:to-emerald-600 disabled:opacity-50 text-slate-950 font-extrabold text-xs flex items-center gap-2 shadow-xl shadow-mentor-500/20 transition-all hover:scale-[1.02]"
              >
                {submitting ? (
                  <>
                    <div className="w-3.5 h-3.5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
                    Diagnosing...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 fill-slate-950 stroke-none" />
                    Submit & Analyze
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Bottom Pane: Test Results & AI Diagnosis (45% height) */}
          <div className="h-[45%] border-t border-slate-800 overflow-hidden">
            <TestResultsConsole
              executionResult={executionResult}
              analysisData={analysisData}
              attemptNumber={session?.attempts_used || 0}
              attemptsRemaining={session?.attempts_remaining ?? 3}
              isCorrect={analysisData?.is_correct}
            />
          </div>
        </div>

        {/* Collapsible Tutor Chat Drawer */}
        {isChatOpen && (
          <div className="w-96 border-l border-slate-800 h-full shrink-0 animate-in slide-in-from-right duration-200">
            <TutorChatPane
              sessionId={sessionId}
              problemId={problem?.id}
              currentCode={code}
              isOpen={isChatOpen}
              onToggle={() => setIsChatOpen(false)}
            />
          </div>
        )}
      </div>

      {/* Solution Reveal Modal */}
      <SolutionModal
        isOpen={isSolutionModalOpen}
        onClose={() => setIsSolutionModalOpen(false)}
        solutionData={solutionData}
        isUnlocked={session?.solution_unlocked}
      />
    </div>
  );
}
