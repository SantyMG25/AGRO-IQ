'use client';

import { useState, useEffect } from 'react';
import Header from './Header';
import SimulationControls from './SimulationControls';
import MetricsDashboard from './MetricsDashboard';
import { fetchCropAnalysis } from '../lib/api';

export default function HomePage() {
  const [irrigation, setIrrigation] = useState(30);
  const [shift, setShift] = useState(0);
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    async function loadData() {
      const result = await fetchCropAnalysis(irrigation, shift);
      setData(result);
    }
    loadData();
  }, [irrigation, shift]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-start bg-zinc-50 font-sans dark:bg-black p-8 gap-6">
      <main className="flex w-full max-w-5xl flex-col gap-6">
        <Header />
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
      </main>
    </div>
  );
}