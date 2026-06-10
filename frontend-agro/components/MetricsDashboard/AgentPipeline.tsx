"use client";

import React from 'react';
import { Zap } from 'lucide-react';

const AgentPipeline = ({ pipeline }: { pipeline: any }) => {
  if (!pipeline) return null;
  return (
    <div className="bg-gradient-to-r from-purple-500/[0.04] to-blue-500/[0.04] dark:from-purple-950/20 dark:to-blue-950/20 rounded-3xl p-5 ring-1 ring-purple-500/10 dark:ring-purple-800/20 shadow-sm backdrop-blur-md">
      <div className="flex items-center gap-2.5 mb-3 select-none">
        <div className="p-1 bg-purple-500/10 dark:bg-purple-400/10 text-purple-600 dark:text-purple-400 rounded-lg">
          <Zap size={15} className="animate-pulse" />
        </div>
        <p className="text-xs font-bold text-purple-900 dark:text-purple-300 uppercase tracking-widest">Multi-Agent Orchestration Telemetry</p>
      </div>
      <div className="grid grid-cols-2 gap-4 text-xs">
        <div className="bg-white/60 dark:bg-zinc-900/40 p-3 rounded-xl border border-zinc-100 dark:border-zinc-800/40 shadow-inner flex flex-col gap-1">
          <p className="text-[10px] text-zinc-400 dark:text-zinc-500 uppercase tracking-wider font-bold">Auditor Agent</p>
          <div className="flex justify-between items-baseline">
            <span className="font-mono text-zinc-800 dark:text-zinc-200 font-semibold">Active State</span>
            <span className="font-mono text-emerald-600 dark:text-emerald-400 font-bold">{(pipeline.auditor.confidence * 100).toFixed(0)}% trust</span>
          </div>
        </div>
        <div className="bg-white/60 dark:bg-zinc-900/40 p-3 rounded-xl border border-zinc-100 dark:border-zinc-800/40 shadow-inner flex flex-col gap-1">
          <p className="text-[10px] text-zinc-400 dark:text-zinc-500 uppercase tracking-wider font-bold">Strategy Agent</p>
          <div className="flex justify-between items-baseline">
            <span className="font-mono text-zinc-800 dark:text-zinc-200 font-semibold">Policy Evaluated</span>
            <span className="font-mono text-emerald-600 dark:text-emerald-400 font-bold">{(pipeline.strategy.confidence * 100).toFixed(0)}% trust</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentPipeline;
