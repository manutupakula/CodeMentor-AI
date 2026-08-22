import React from 'react';
import { CheckCircle2, XCircle, Terminal, AlertTriangle, Clock } from 'lucide-react';

export default function TestResultsConsole({
  executionResult,
  analysisData,
  attemptNumber,
  attemptsRemaining,
  isCorrect
}) {
  if (!executionResult && !analysisData) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-slate-500 p-6 text-center text-xs">
        <Terminal className="w-8 h-8 mb-2 stroke-1 opacity-60" />
        <p className="font-medium text-slate-400">Ready for Execution</p>
        <p className="text-[11px] text-slate-500 mt-1">Submit your code to see automated test results and AI tutor diagnosis.</p>
      </div>
    );
  }

  const testResults = executionResult?.test_results || [];
  const passedCount = executionResult?.passed_count || 0;
  const totalCount = executionResult?.total_count || testResults.length;
  const stderr = executionResult?.stderr;
  const errorType = analysisData?.error_type || executionResult?.error_type;

  return (
    <div className="h-full flex flex-col bg-slate-950 font-mono text-xs overflow-hidden">
      {/* Status Bar */}
      <div className="px-4 py-2.5 bg-slate-900 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 font-sans font-bold">
            {isCorrect ? (
              <span className="flex items-center gap-1 text-emerald-400">
                <CheckCircle2 className="w-4 h-4" /> All Tests Passed!
              </span>
            ) : (
              <span className="flex items-center gap-1 text-rose-400">
                <XCircle className="w-4 h-4" /> Attempt {attemptNumber} Evaluation
              </span>
            )}
          </div>
          {errorType && errorType !== 'CORRECT' && (
            <span className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 text-[10px] uppercase tracking-wider font-semibold">
              {errorType.replace('_', ' ')}
            </span>
          )}
        </div>

        <div className="flex items-center gap-2 font-sans text-xs text-slate-400">
          <span>{passedCount}/{totalCount} Passed</span>
          <span className="text-slate-600">•</span>
          <span>{attemptsRemaining} Attempts Left</span>
        </div>
      </div>

      {/* Console Output */}
      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {/* Diagnosis Box */}
        {analysisData?.analysis && (
          <div className={`p-3.5 rounded-xl border font-sans text-xs leading-relaxed ${
            isCorrect 
              ? 'bg-emerald-950/30 border-emerald-500/30 text-emerald-200' 
              : 'bg-slate-900 border-slate-800 text-slate-200'
          }`}>
            <span className="font-bold block mb-1 text-[11px] uppercase tracking-wider text-slate-400">
              {isCorrect ? '🌟 Pedagogical Feedback' : '🔍 AI Diagnostic Analysis'}
            </span>
            {analysisData.analysis}
          </div>
        )}

        {/* Runtime Errors / Traceback */}
        {stderr && (
          <div className="p-3 rounded-lg bg-red-950/40 border border-red-500/30 text-red-300 space-y-1">
            <div className="flex items-center gap-1.5 text-[11px] font-bold uppercase text-red-400 font-sans">
              <AlertTriangle className="w-3.5 h-3.5" /> Execution Stderr
            </div>
            <pre className="text-[11px] whitespace-pre-wrap">{stderr}</pre>
          </div>
        )}

        {/* Test Cases List */}
        {testResults.length > 0 && (
          <div className="space-y-2">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider font-sans block">
              Test Case Verification
            </span>
            <div className="grid gap-2">
              {testResults.map((tc, idx) => (
                <div
                  key={idx}
                  className={`p-3 rounded-lg border flex items-start justify-between gap-4 ${
                    tc.passed
                      ? 'bg-slate-900/60 border-slate-800/80 text-slate-300'
                      : 'bg-rose-950/20 border-rose-500/30 text-rose-200'
                  }`}
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-[11px]">Case {tc.test_case_index}</span>
                      {tc.is_hidden && (
                        <span className="px-1.5 py-0.2 rounded bg-slate-800 text-[10px] text-slate-400">Hidden</span>
                      )}
                    </div>
                    {!tc.is_hidden && (
                      <div className="text-[11px] text-slate-400 space-y-0.5">
                        <div>Input: <code className="text-slate-200">{JSON.stringify(tc.input_args)}</code></div>
                        <div>Expected: <code className="text-emerald-400">{JSON.stringify(tc.expected_output)}</code></div>
                        {!tc.passed && (
                          <div>Actual: <code className="text-rose-400">{JSON.stringify(tc.actual_output)}</code></div>
                        )}
                      </div>
                    )}
                  </div>

                  <div className="shrink-0 mt-0.5">
                    {tc.passed ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    ) : (
                      <XCircle className="w-4 h-4 text-rose-400" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
