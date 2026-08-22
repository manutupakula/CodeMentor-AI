import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, Bot, User, MessageSquare, CornerDownLeft } from 'lucide-react';
import { tutorAPI } from '../api/client';

export default function TutorChatPane({
  sessionId,
  problemId,
  currentCode,
  isOpen,
  onToggle
}) {
  const [messages, setMessages] = useState([
    {
      role: 'tutor',
      content: "Hello! I'm your CodeMentor tutor. Feel free to ask me clarifying questions about recursion, loops, base cases, or edge cases. I'll help you discover the answers step-by-step!",
      suggestedFollowups: [
        "Why is a base case essential in recursion?",
        "Can you trace how loops handle 0-based indices?",
        "What edge cases should I watch out for?"
      ]
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (textToSend) => {
    const query = textToSend || input;
    if (!query.trim() || loading) return;

    const userMsg = { role: 'student', content: query.trim() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await tutorAPI.chat({
        session_id: sessionId,
        problem_id: problemId,
        code: currentCode,
        message: query.trim()
      });

      const tutorMsg = {
        role: 'tutor',
        content: res.data.reply,
        suggestedFollowups: res.data.suggested_followups || []
      };
      setMessages(prev => [...prev, tutorMsg]);
    } catch (err) {
      console.error("Chat error", err);
      setMessages(prev => [
        ...prev,
        {
          role: 'tutor',
          content: "I'm having a slight connection blip with the AI tutor service, but I'm here! Try checking your loop boundary or recursion base case while I reconnect.",
          suggestedFollowups: []
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-900/90 rounded-2xl border border-slate-800 shadow-xl overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-slate-800 bg-slate-950/60 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-mentor-500/20 text-mentor-400 flex items-center justify-center border border-mentor-500/30">
            <Bot className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-white flex items-center gap-1.5">
              CodeMentor AI Tutor
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            </h3>
            <p className="text-[10px] text-slate-400">Contextual pedagogical chat</p>
          </div>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 p-4 overflow-y-auto space-y-4 text-xs">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex gap-2.5 ${m.role === 'student' ? 'justify-end' : 'justify-start'}`}
          >
            {m.role === 'tutor' && (
              <div className="w-6 h-6 rounded-md bg-mentor-500/20 text-mentor-400 flex items-center justify-center shrink-0 mt-0.5">
                <Bot className="w-3.5 h-3.5" />
              </div>
            )}

            <div className={`max-w-[85%] space-y-2`}>
              <div
                className={`p-3 rounded-xl leading-relaxed ${
                  m.role === 'student'
                    ? 'bg-mentor-600 text-slate-950 font-medium rounded-tr-none'
                    : 'bg-slate-800/80 text-slate-200 border border-slate-700/50 rounded-tl-none'
                }`}
              >
                {m.content}
              </div>

              {/* Suggested Followups */}
              {m.role === 'tutor' && m.suggestedFollowups && m.suggestedFollowups.length > 0 && (
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {m.suggestedFollowups.map((f, fIdx) => (
                    <button
                      key={fIdx}
                      onClick={() => handleSend(f)}
                      className="px-2.5 py-1 rounded-full bg-slate-950/80 hover:bg-slate-800 text-[10px] text-slate-300 border border-slate-700 transition-colors flex items-center gap-1 text-left"
                    >
                      <Sparkles className="w-2.5 h-2.5 text-amber-400 shrink-0" />
                      {f}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {m.role === 'student' && (
              <div className="w-6 h-6 rounded-md bg-slate-800 text-slate-300 flex items-center justify-center shrink-0 mt-0.5">
                <User className="w-3.5 h-3.5" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-2.5 items-center text-slate-400 text-xs">
            <div className="w-6 h-6 rounded-md bg-mentor-500/20 text-mentor-400 flex items-center justify-center">
              <Bot className="w-3.5 h-3.5 animate-spin" />
            </div>
            <span className="italic">Tutor is reflecting on your question...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Box */}
      <div className="p-3 border-t border-slate-800 bg-slate-950/60">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask your tutor a question (e.g. why is my loop infinite?)..."
            disabled={loading}
            className="flex-1 bg-slate-900 border border-slate-700/80 rounded-xl px-3.5 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-mentor-500 focus:ring-1 focus:ring-mentor-500"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="p-2 rounded-xl bg-mentor-500 hover:bg-mentor-600 disabled:opacity-50 text-slate-950 transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
