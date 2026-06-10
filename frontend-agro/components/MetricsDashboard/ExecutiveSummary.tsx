"use client";

import React from 'react';

const ExecutiveSummary = ({ summary }: { summary: any }) => {
  if (!summary) return null;
  return (
    <div className="bg-gradient-to-br from-zinc-50/70 to-zinc-100/30 dark:from-zinc-900/20 dark:to-zinc-900/5 rounded-3xl p-6 border border-zinc-200/50 dark:border-zinc-800/60 shadow-md backdrop-blur-md">
      <div className="flex items-center gap-2 mb-3 select-none">
        <span className="text-lg">🏛️</span>
        <h3 className="font-extrabold text-xs text-zinc-900 dark:text-zinc-100 uppercase tracking-widest">Executive Policy Verdict</h3>
      </div>
      <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-6 whitespace-pre-wrap font-medium">{summary.autonomous_prediction}</p>
      <div className="mt-4 pt-3.5 border-t border-zinc-200/50 dark:border-zinc-800 flex justify-between items-center select-none">
        <span className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">Strategy Auditor Verdict</span>
        <p className="text-[10px] text-indigo-600 dark:text-indigo-400 font-bold">Agent Confidence: <span className="font-mono bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/10 font-black">{(summary.agent_confidence * 100).toFixed(1)}%</span></p>
      </div>
    </div>
  );
};

export default ExecutiveSummary;
