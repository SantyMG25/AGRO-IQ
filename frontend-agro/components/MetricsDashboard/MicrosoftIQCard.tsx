"use client";

import React from 'react';
import { Zap } from 'lucide-react';

const MicrosoftIQCard = ({ data }: { data: any }) => {
  if (!data) return null;
  const retrievedDocuments = Array.isArray(data.foundry_iq?.retrieved_documents) ? data.foundry_iq.retrieved_documents : [];
  return (
    <div className="bg-gradient-to-br from-indigo-500/[0.03] to-purple-500/[0.03] dark:from-indigo-950/20 dark:to-purple-950/20 rounded-3xl p-6 ring-1 ring-indigo-500/10 dark:ring-indigo-800/20 shadow-sm backdrop-blur-md">
      <div className="flex items-center justify-between mb-4 border-b border-zinc-100 dark:border-zinc-900/40 pb-3 select-none">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 bg-gradient-to-br from-indigo-500 to-purple-500 text-white rounded-xl shadow-md shadow-indigo-500/20">
            <Zap size={16} className="animate-pulse" />
          </div>
          <div>
            <p className="text-xs font-extrabold text-indigo-950 dark:text-indigo-200 uppercase tracking-widest">Microsoft IQ Gateway</p>
            <p className="text-[10px] text-zinc-400 dark:text-zinc-500 font-medium">Telemetry Synchronization Layer & Agentic Knowledge Sync</p>
          </div>
        </div>
        <div className="flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-bold bg-indigo-500/10 text-indigo-700 dark:text-indigo-400 ring-1 ring-indigo-500/20 shadow-sm">
          <span className="h-1.5 w-1.5 rounded-full bg-indigo-500 animate-ping" />
          Sync Active
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        <div className="bg-white/80 dark:bg-zinc-900/30 p-4.5 rounded-2xl border border-zinc-100 dark:border-zinc-800/60 flex flex-col gap-2 shadow-sm">
          <div className="flex items-center justify-between">
            <p className="font-bold text-zinc-800 dark:text-zinc-200">Foundry IQ Retrieval (RAG)</p>
            <span className="text-[10px] text-purple-600 dark:text-purple-400 font-extrabold bg-purple-500/10 px-2 py-0.5 rounded-md border border-purple-500/10">Confidence: {(data.foundry_iq?.confidence * 100).toFixed(0)}%</span>
          </div>
          <p className="text-[10px] text-zinc-400 dark:text-zinc-500 font-bold select-none uppercase tracking-wider">Contextual FAO Climate Guidelines Synced:</p>
          <div className="flex flex-col gap-1.5 mt-1 font-mono text-[10px] text-zinc-600 dark:text-zinc-300">
            {retrievedDocuments.map((doc: string, idx: number) => (
              <div key={idx} className="flex items-center gap-2 bg-zinc-50/50 dark:bg-zinc-950/60 p-2 rounded-xl border border-zinc-100 dark:border-zinc-900/30">
                <span className="text-purple-500">📄</span>
                <span className="truncate font-semibold">{doc}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white/80 dark:bg-zinc-900/30 p-4.5 rounded-2xl border border-zinc-100 dark:border-zinc-800/60 flex flex-col gap-3 shadow-sm justify-between">
          <div className="flex flex-col gap-2">
            <div className="flex items-center justify-between">
              <p className="font-bold text-zinc-800 dark:text-zinc-200">Fabric IQ Lakehouse Sync</p>
              <span className="text-[10px] bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 px-2.5 py-0.5 rounded-md font-bold border border-emerald-500/10 uppercase">Connected</span>
            </div>
            <div className="grid grid-cols-2 gap-2.5 mt-1">
              <div className="bg-zinc-50/50 dark:bg-zinc-950/60 p-2.5 rounded-xl border border-zinc-100 dark:border-zinc-900/30">
                <p className="text-[9px] text-zinc-400 dark:text-zinc-500 uppercase font-bold tracking-wider">Lakehouse Source</p>
                <p className="font-semibold text-zinc-800 dark:text-zinc-200 font-mono tracking-tight truncate mt-0.5">{data.fabric_iq?.lakehouse}</p>
              </div>
              <div className="bg-zinc-50/50 dark:bg-zinc-950/60 p-2.5 rounded-xl border border-zinc-100 dark:border-zinc-900/30">
                <p className="text-[9px] text-zinc-400 dark:text-zinc-500 uppercase font-bold tracking-wider">Records Processed</p>
                <p className="font-extrabold text-zinc-800 dark:text-zinc-200 font-mono text-sm mt-0.5">{data.fabric_iq?.records_processed}</p>
              </div>
            </div>
          </div>
          <p className="text-[9px] text-zinc-400 dark:text-zinc-500 text-right font-mono select-none">Last Sync: {data.fabric_iq?.last_sync ? new Date(data.fabric_iq.last_sync).toLocaleTimeString() : ''}</p>
        </div>
      </div>
    </div>
  );
};

export default MicrosoftIQCard;
