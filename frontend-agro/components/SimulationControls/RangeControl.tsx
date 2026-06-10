"use client";

import React from 'react';

const RangeControl = ({
  label,
  value,
  min,
  max,
  icon,
  unitLabel,
  onChange,
  gradient,
}: {
  label: string;
  value: number | string;
  min: number;
  max: number;
  icon: React.ReactNode;
  unitLabel: React.ReactNode;
  onChange: (v: number) => void;
  gradient?: string;
}) => {
  return (
    <div className="flex flex-col gap-3">
      <label className="text-xs font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 flex justify-between select-none">
        <span className="flex items-center gap-1.5 text-zinc-700 dark:text-zinc-300 font-bold">{icon} {label}</span>
        <span className="font-mono text-emerald-600 dark:text-emerald-400 font-extrabold text-xs bg-emerald-50 dark:bg-emerald-950/40 px-2 py-0.5 rounded-lg border border-emerald-100 dark:border-emerald-900/30">{unitLabel}</span>
      </label>
      <div className="relative flex items-center group w-full px-1">
        <input
          type="range"
          min={String(min)}
          max={String(max)}
          value={String(value)}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full h-2 rounded-lg appearance-none bg-zinc-100 dark:bg-zinc-800/80 cursor-pointer accent-emerald-600 focus:outline-none transition-all duration-300"
          style={{ background: gradient }}
        />
      </div>
    </div>
  );
};

export default RangeControl;
