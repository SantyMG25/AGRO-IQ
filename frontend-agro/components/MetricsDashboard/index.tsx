"use client";

import AgentPipeline from './AgentPipeline';
import MicrosoftIQCard from './MicrosoftIQCard';
import ResilienceCard from './ResilienceCard';
import KPICards from './KPICards';
import ActionCard from './ActionCard';
import ExecutiveSummary from './ExecutiveSummary';
import React from 'react';

export default function MetricsDashboard({ data }: { data: any }) {
  if (!data) {
    return (
      <div className="text-center p-12 text-zinc-400 w-full bg-white dark:bg-zinc-950 rounded-3xl ring-1 ring-black/5 dark:ring-white/10">Connecting to Python agent engine...</div>
    );
  }

  if (data.status === 'error') {
    return (
      <div className="text-center p-12 text-red-500 w-full bg-white dark:bg-zinc-950 rounded-3xl ring-1 ring-black/5 dark:ring-white/10">{data.message || 'Agent orchestration error'}</div>
    );
  }

  const resilience = data.dashboard_metrics?.resilience_score || 0;
  const actionCards = Array.isArray(data.action_cards) ? data.action_cards : [];

  return (
    <section className="flex flex-col gap-6 w-full relative">
      {data.agent_pipeline && <AgentPipeline pipeline={data.agent_pipeline} />}
      {data.microsoft_iq && <MicrosoftIQCard data={data.microsoft_iq} />}

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <ResilienceCard resilience={resilience} />
        <KPICards metrics={data.dashboard_metrics} />
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {actionCards.map((card: any) => (
          <ActionCard key={card.id} card={card} />
        ))}
      </div>

      {data.executive_summary && <ExecutiveSummary summary={data.executive_summary} />}
    </section>
  );
}
