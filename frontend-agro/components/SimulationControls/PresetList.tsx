"use client";

import React from 'react';
import PresetButton from './PresetButton';

const PresetList = ({ presets, activeIdx, onApply }: { presets: any[]; activeIdx: number; onApply: (p: any) => void }) => {
  return (
    <div className="flex flex-col gap-3.5">
      <h3 className="text-xs font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-widest flex items-center gap-1.5 select-none">
        Quick Preset Scenarios
      </h3>
      <div className="grid grid-cols-1 gap-3">
        {presets.map((preset, idx) => (
          <PresetButton key={idx} preset={preset} isActive={idx === activeIdx} onApply={onApply} />
        ))}
      </div>
    </div>
  );
};

export default PresetList;
