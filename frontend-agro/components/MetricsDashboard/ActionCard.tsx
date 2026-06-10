"use client";

import React from 'react';

const ActionCard = ({ card }: { card: any }) => {
  const isRed = card.visual_indicator === 'red';
  const isAmber = card.visual_indicator === 'amber';
  return (
    <div
      key={card.id}
      className={`rounded-3xl p-6 shadow-md border ring-1 ring-black/5 dark:ring-white/5 transition-all duration-300 hover:scale-[1.01] hover:shadow-lg flex flex-col justify-between relative overflow-hidden bg-white/80 dark:bg-zinc-950/70 backdrop-blur-md ${
        isRed
          ? 'border-l-4 border-l-red-500 border-zinc-100 dark:border-zinc-900'
          : isAmber
          ? 'border-l-4 border-l-amber-500 border-zinc-100 dark:border-zinc-900'
          : 'border-l-4 border-l-emerald-500 border-zinc-100 dark:border-zinc-900'
      }`}
    >
      <div>
        <h4 className="font-bold text-xs flex items-center gap-2 mb-2 select-none uppercase tracking-wider">
          <span className={`h-2 w-2 rounded-full ${card.visual_indicator === 'emerald' ? 'bg-emerald-500' : card.visual_indicator === 'amber' ? 'bg-amber-500' : 'bg-red-500'} animate-pulse`} />
          <span className={isRed ? 'text-red-900 dark:text-red-200' : 'text-zinc-900 dark:text-zinc-100'}>{card.title}</span>
        </h4>
        <p className="text-xs leading-5 text-zinc-500 dark:text-zinc-400 mb-3">{card.description}</p>
      </div>

      <div className="flex flex-col gap-1.5 mt-2 pt-2.5 border-t border-zinc-100 dark:border-zinc-900/50">
        {card.resilience_contribution && (
          <p className="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold font-mono">Resilience Boost: {card.resilience_contribution}</p>
        )}
        {card.executive_priority && (
          <p className="text-[10px] text-purple-600 dark:text-purple-400 font-bold font-mono">Priority Score: {card.executive_priority}</p>
        )}
        {Array.isArray(card.decision_triggers) && card.decision_triggers.length > 0 && (
          <div className="mt-1 text-[10px] font-bold space-y-1">
            {card.decision_triggers.map((trigger: string, idx: number) => (
              <p key={idx} className="text-red-500 dark:text-red-400 flex items-center gap-1">
                <span>⚠️</span>
                <span>{trigger}</span>
              </p>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ActionCard;
