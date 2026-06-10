"use client";

import React from 'react';

const PresetButton = ({ preset, isActive, onApply }: { preset: any; isActive: boolean; onApply: (p: any) => void }) => {
  return (
    <button
      onClick={() => onApply(preset)}
      className={`flex flex-col text-left p-4 rounded-2xl border transition-all duration-300 text-xs gap-2 cursor-pointer group relative overflow-hidden ${
        isActive
          ? 'border-emerald-500 dark:border-emerald-400 bg-emerald-50/40 dark:bg-emerald-950/20 shadow-md shadow-emerald-500/5 scale-[1.02]'
          : `${preset.borderColor} bg-zinc-50/50 dark:bg-zinc-900/30 hover:bg-zinc-100/30 dark:hover:bg-zinc-900/50 hover:scale-[1.01]`
      }`}
    >
      {isActive && (
        <div className="absolute top-0 right-0 h-16 w-16 pointer-events-none overflow-hidden">
          <div className="absolute transform rotate-45 bg-emerald-500 text-white text-[8px] font-bold py-1 px-4 right-[-24px] top-[12px] text-center w-24 uppercase tracking-widest shadow-sm">Active</div>
        </div>
      )}

      <div className="flex justify-between font-semibold text-zinc-800 dark:text-zinc-200 items-center pr-8 w-full">
        <span className={`group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors flex items-center gap-1.5 ${isActive ? 'text-emerald-600 dark:text-emerald-400' : ''}`}>{preset.title}</span>
        <span className={`text-[9px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider ${preset.badgeColor}`}>{preset.badge}</span>
      </div>
      <p className="text-zinc-500 dark:text-zinc-400 text-[10px] leading-relaxed">{preset.desc}</p>
    </button>
  );
};

export default PresetButton;
