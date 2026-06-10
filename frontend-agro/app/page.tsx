'use client';

import { useState, useEffect } from 'react';
import Header from '../components/Header';
import SimulationControls from '../components/SimulationControls';
import MetricsDashboard from '../components/MetricsDashboard';
import AnalyticsDashboard from '../components/AnalyticsDashboard';
import { HttpCropAnalysisApiAdapter } from '../adapters/outbound/http_api';

const apiService = new HttpCropAnalysisApiAdapter();

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<'simulation' | 'analytics'>('simulation');
  const [irrigation, setIrrigation] = useState(30);
  const [shift, setShift] = useState(0);
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    async function loadData() {
      const result = await apiService.fetchCropAnalysis(irrigation, shift);
      setData(result);
    }
    loadData();
  }, [irrigation, shift]);

  return (
    <div className="relative flex min-h-screen flex-col items-center justify-start bg-zinc-50/50 dark:bg-[#070708] font-sans p-8 gap-6 overflow-hidden">
      <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-emerald-500/10 dark:bg-emerald-500/[0.08] blur-[120px] pointer-events-none -z-10" />
      <div className="absolute bottom-[10%] right-[-10%] w-[500px] h-[500px] rounded-full bg-indigo-500/10 dark:bg-purple-500/[0.08] blur-[130px] pointer-events-none -z-10" />
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808008_1px,transparent_1px),linear-gradient(to_bottom,#80808008_1px,transparent_1px)] bg-[size:32px_32px] pointer-events-none -z-10" />

      <main className="flex w-full max-w-6xl flex-col gap-6 relative z-10">
        <Header />

        <div className="flex justify-center sm:justify-start mt-2">
          <div className="flex bg-zinc-200/50 dark:bg-zinc-900/60 backdrop-blur-md p-1 rounded-2xl border border-zinc-200/50 dark:border-zinc-800/40 shadow-inner w-full sm:w-auto">
            <button
              onClick={() => setActiveTab('simulation')}
              className={`flex-1 sm:flex-none px-6 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition-all duration-300 flex items-center justify-center gap-2 cursor-pointer ${
                activeTab === 'simulation'
                  ? 'bg-emerald-600 dark:bg-emerald-500 text-white shadow-md'
                  : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100/50 dark:hover:bg-zinc-900/50 hover:text-zinc-900 dark:hover:text-zinc-100'
              }`}
            >
              <span>🌾</span> Simulation Cabin
            </button>
            <button
              onClick={() => setActiveTab('analytics')}
              className={`flex-1 sm:flex-none px-6 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition-all duration-300 flex items-center justify-center gap-2 cursor-pointer ${
                activeTab === 'analytics'
                  ? 'bg-emerald-600 dark:bg-emerald-500 text-white shadow-md'
                  : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100/50 dark:hover:bg-zinc-900/50 hover:text-zinc-900 dark:hover:text-zinc-100'
              }`}
            >
              <span>📊</span> Historical Analytics
            </button>
          </div>
        </div>

        {activeTab === 'simulation' && (
          <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-start">
            <div className="md:col-span-4">
              <SimulationControls
                irrigation={irrigation}
                setIrrigation={setIrrigation}
                shift={shift}
                setShift={setShift}
              />
            </div>
            <div className="md:col-span-8">
              <MetricsDashboard data={data} />
            </div>
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="w-full">
            <AnalyticsDashboard />
          </div>
        )}
      </main>
    </div>
  );
}
