"use client";

import React from 'react';

const DescriptionBlock = ({ icon, text, color }: { icon: string; text: string; color: string }) => {
  return (
    <div className={`text-[10px] leading-relaxed p-3.5 rounded-2xl bg-zinc-50/50 dark:bg-zinc-900/40 border border-zinc-100 dark:border-zinc-800/50 flex gap-2 shadow-inner ${color}`}>
      <span className="flex-shrink-0 text-xs">{icon}</span>
      <span className="text-zinc-600 dark:text-zinc-400 font-medium">{text}</span>
    </div>
  );
};

export default DescriptionBlock;
