'use client';
import React from 'react';
import type { ChartViewType } from './AnalyticsDashboard';

type NavTabProps = {
  chartView: ChartViewType;
  setChartView: React.Dispatch<React.SetStateAction<ChartViewType>>;
};

export default function NavTab({ chartView, setChartView }: NavTabProps) {
  const getTabClass = (view: ChartViewType) => {
    const baseClass = "px-5 py-2.5 rounded-xl font-bold transition-all duration-300 text-xs cursor-pointer select-none";
    const activeClass = "bg-emerald-600 dark:bg-emerald-500 text-white shadow-md";
    const inactiveClass = "text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100/50 dark:hover:bg-zinc-900/50 hover:text-zinc-950 dark:hover:text-zinc-100";
    return `${baseClass} ${chartView === view ? activeClass : inactiveClass}`;
  };

  return (
    <div className="flex bg-zinc-200/50 dark:bg-zinc-900/60 backdrop-blur-md p-1 rounded-2xl border border-zinc-200/50 dark:border-zinc-800/40 shadow-inner w-fit">
      <button onClick={() => setChartView('trends')} className={getTabClass('trends')}>Performance Trends</button>
      <button onClick={() => setChartView('correlation')} className={getTabClass('correlation')}>Risk Correlation Plot</button>
      <button onClick={() => setChartView('roi')} className={getTabClass('roi')}>ROI Analysis</button>
    </div>
  );
}