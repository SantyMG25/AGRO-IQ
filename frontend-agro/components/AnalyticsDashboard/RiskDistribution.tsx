/* components/AnalyticsDashboard/RiskDistribution.tsx */
import React from 'react';
import { MetricCard } from '../common/MetricCard';
import { AnalyticsData } from '../../domain/entities';
import { Flag } from 'lucide-react'; // placeholder icon

interface RiskDistributionProps {
  analytics: AnalyticsData | null;
}

export const RiskDistribution: React.FC<RiskDistributionProps> = ({ analytics }) => {
  if (!analytics) return null;
  const total = analytics.total_simulations;
  const { low, medium, high } = analytics.risk_distribution;
  const riskItems = [
    { title: 'Low Risk', count: low, colorClass: 'bg-emerald-500/10 text-emerald-600', icon: 'bg-emerald-500' },
    { title: 'Medium Risk', count: medium, colorClass: 'bg-amber-500/10 text-amber-600', icon: 'bg-amber-500' },
    { title: 'High Risk', count: high, colorClass: 'bg-red-500/10 text-red-600', icon: 'bg-red-500' },
  ];
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {riskItems.map((item) => (
        <div
          key={item.title}
          className="text-center md:text-left p-4.5 rounded-2xl border flex flex-col justify-between h-28"
          style={{ background: `var(--card-bg-light)` }}
        >
          <div className="flex items-center justify-between mb-2 text-zinc-400">
            <span className="text-xs font-bold uppercase tracking-wider">{item.title}</span>
            <span className={`font-mono text-xs font-bold ${item.colorClass} px-2 py-0.5 rounded-full border`}>\n              {((item.count / total) * 100).toFixed(0)}%
            </span>
          </div>
          <div className="text-3xl font-black font-mono leading-none text-zinc-950 dark:text-zinc-50">
            {item.count}
          </div>
          <p className="text-[9px] text-zinc-400 dark:text-zinc-500 mt-1 font-semibold uppercase tracking-wider">
            {item.title.includes('Low') ? 'Runs resolved as safe' : item.title.includes('Medium') ? 'Runs needing oversight' : 'Runs with critical alert'}
          </p>
        </div>
      ))}
    </div>
  );
};
