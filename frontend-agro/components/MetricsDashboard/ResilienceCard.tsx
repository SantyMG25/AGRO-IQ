"use client";

import React from 'react';
import { Zap } from 'lucide-react';

const ResilienceCard = ({ resilience }: { resilience: number }) => {
  return (
    <article className="rounded-3xl bg-white/80 dark:bg-zinc-950/70 backdrop-blur-md p-6 shadow-md ring-1 ring-black/5 dark:ring-white/10 flex flex-col items-center justify-between border border-zinc-100 dark:border-zinc-900/50 hover:shadow-lg hover:scale-[1.01] transition-all duration-300 min-h-[180px]">
      <p className="text-[10px] font-extrabold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 flex items-center gap-1.5 select-none self-start">
        <Zap size={13} className="text-purple-500" />
        Resilience
      </p>

      <div className="relative flex items-center justify-center w-24 h-24 my-2">
        <svg className="w-full h-full transform -rotate-90">
          <circle cx="48" cy="48" r="38" className="stroke-zinc-100 dark:stroke-zinc-900" strokeWidth="7" fill="transparent" />
          <circle cx="48" cy="48" r="38"
            className={`${
              resilience >= 75
                ? 'stroke-emerald-500 drop-shadow-[0_0_6px_rgba(16,185,129,0.4)]'
                : resilience >= 55
                ? 'stroke-amber-500 drop-shadow-[0_0_6px_rgba(245,158,11,0.4)]'
                : 'stroke-red-500 drop-shadow-[0_0_6px_rgba(239,68,68,0.4)]'
            }`}
            strokeWidth="7" fill="transparent"
            strokeDasharray="238"
            strokeDashoffset={238 - (238 * resilience) / 100}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute font-mono text-base font-black text-zinc-900 dark:text-zinc-100">{resilience}%</div>
      </div>

      <span className={`text-[9px] px-2.5 py-0.5 rounded-full font-bold uppercase tracking-wider ${
        resilience >= 75
          ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20'
          : resilience >= 55
          ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20'
          : 'bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/20'
      }`}>
        {resilience >= 75 ? 'OPTIMAL' : resilience >= 55 ? 'STABLE' : 'CRITICAL'}
      </span>
    </article>
  );
};

export default ResilienceCard;
