/* components/common/MetricCard.tsx */
import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: React.ReactNode;
  subtitle?: string;
  icon: LucideIcon;
  bgGradient?: string; // optional custom gradient class
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  bgGradient = 'bg-white/80 dark:bg-zinc-900/30',
}) => (
  <div className={`${bgGradient} p-5 rounded-2xl border border-zinc-100 dark:border-zinc-800/40 shadow-sm hover:shadow-md transition-shadow`}>
    <div className="flex items-center justify-between mb-4 text-zinc-400">
      <p className="text-xs font-bold uppercase tracking-wider">{title}</p>
      <Icon className="w-4 h-4 text-primary-500" />
    </div>
    <p className="text-3xl font-black text-zinc-950 dark:text-zinc-50 font-mono">{value}</p>
    {subtitle && (
      <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-2 font-medium">{subtitle}</p>
    )}
  </div>
);

