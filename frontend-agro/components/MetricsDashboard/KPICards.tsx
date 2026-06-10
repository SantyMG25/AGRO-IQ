"use client";

import React from 'react';
import { ShieldAlert, TrendingUp, DollarSign } from 'lucide-react';

const KPICards = ({ metrics }: { metrics: any }) => {
  return (
    <>
      <article className="rounded-3xl bg-white/80 dark:bg-zinc-950/70 backdrop-blur-md p-6 shadow-md ring-1 ring-black/5 dark:ring-white/10 flex flex-col justify-between border border-zinc-100 dark:border-zinc-900/50 hover:shadow-lg hover:scale-[1.01] transition-all duration-300">
        <div className="flex flex-col gap-2 w-full">
          <p className="text-[10px] font-extrabold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 flex items-center gap-1.5 select-none">
            <ShieldAlert size={13} className="text-red-500" />
            Food Security
          </p>
          <p className="text-2xl font-black text-zinc-900 dark:text-zinc-100 font-mono leading-none">{metrics.food_security_index}%</p>
        </div>
        <div className="w-full mt-4">
          <div className="w-full bg-zinc-100 dark:bg-zinc-900 h-2 rounded-full overflow-hidden">
            <div className={`h-full rounded-full transition-all duration-500 ${
              metrics.food_security_index >= 75
                ? 'bg-emerald-500'
                : metrics.food_security_index >= 50
                ? 'bg-amber-500'
                : 'bg-red-500'
            }`} style={{ width: `${metrics.food_security_index}%` }}></div>
          </div>
          <div className="flex justify-between items-center mt-2 text-[9px] text-zinc-500 dark:text-zinc-400 font-bold uppercase tracking-wider">
            <span>Status</span>
            <span className={
              metrics.food_security_index >= 75
                ? 'text-emerald-600 dark:text-emerald-400'
                : metrics.food_security_index >= 50
                ? 'text-amber-600 dark:text-amber-400'
                : 'text-red-600 dark:text-red-400'
            }>
              {metrics.food_security_index >= 75 ? 'Secured' : metrics.food_security_index >= 50 ? 'Moderate' : 'At Risk'}
            </span>
          </div>
        </div>
      </article>

      <article className="rounded-3xl bg-white/80 dark:bg-zinc-950/70 backdrop-blur-md p-6 shadow-md ring-1 ring-black/5 dark:ring-white/10 flex flex-col justify-between border border-zinc-100 dark:border-zinc-900/50 hover:shadow-lg hover:scale-[1.01] transition-all duration-300">
        <div className="flex flex-col gap-2 w-full">
          <p className="text-[10px] font-extrabold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 flex items-center gap-1.5 select-none">
            <TrendingUp size={13} className="text-emerald-500" />
            Projected Yield
          </p>
          <div className="flex items-baseline gap-1">
            <p className="text-2xl font-black text-zinc-900 dark:text-zinc-100 font-mono leading-none">{metrics.projected_yield_tons}</p>
            <span className="text-[9px] text-zinc-400 font-bold uppercase font-mono tracking-wider">Tons / HA</span>
          </div>
        </div>
        <div className="flex items-center gap-2.5 mt-4 bg-emerald-500/5 dark:bg-emerald-950/10 p-2.5 rounded-2xl border border-emerald-500/10 shadow-inner">
          <span className="text-sm select-none">🌾</span>
          <div className="flex flex-col">
            <span className="text-[10px] font-bold text-emerald-700 dark:text-emerald-400 leading-tight">{metrics.projected_yield_tons > 3.0 ? 'High Yield Profile' : 'Stable Yield Profile'}</span>
            <span className="text-[8px] text-zinc-400 dark:text-zinc-500 font-mono mt-0.5">Base Target: 2.5 Tons</span>
          </div>
        </div>
      </article>

      <article className="rounded-3xl bg-white/80 dark:bg-zinc-950/70 backdrop-blur-md p-6 shadow-md ring-1 ring-black/5 dark:ring-white/10 flex flex-col justify-between border border-zinc-100 dark:border-zinc-900/50 hover:shadow-lg hover:scale-[1.01] transition-all duration-300">
        <div className="flex flex-col gap-2 w-full">
          <p className="text-[10px] font-extrabold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 flex items-center gap-1.5 select-none">
            <DollarSign size={13} className="text-blue-500" />
            Loss Mitigated
          </p>
          <p className="text-2xl font-black text-zinc-900 dark:text-zinc-100 font-mono leading-none">${metrics.economic_loss_prevented_usd.toLocaleString()}</p>
        </div>
        <div className="flex items-center gap-2.5 mt-4 bg-blue-500/5 dark:bg-blue-950/10 p-2.5 rounded-2xl border border-blue-500/10 shadow-inner">
          <span className="text-sm select-none">💰</span>
          <div className="flex flex-col">
            <span className="text-[10px] font-bold text-blue-700 dark:text-blue-400 leading-tight">Financial Protection</span>
            <span className="text-[8px] text-zinc-400 dark:text-zinc-500 font-mono mt-0.5">ESG Net Benefit</span>
          </div>
        </div>
      </article>
    </>
  );
};

export default KPICards;
