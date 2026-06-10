import { Cpu } from 'lucide-react';

export default function Header() {
  return (
    <section className="rounded-3xl bg-white p-8 shadow-sm ring-1 ring-black/5 dark:bg-zinc-950 dark:ring-white/10 w-full">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-6">
        <div className="flex flex-col gap-2">
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-semibold tracking-tight text-black dark:text-zinc-50 sm:text-4xl">
              AgroGarantia IQ
            </h1>
            <span className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 ring-1 ring-emerald-600/10 dark:bg-emerald-950/50 dark:text-emerald-400 dark:ring-emerald-500/20">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
              Live Simulation
            </span>
          </div>
          <p className="text-lg leading-6 text-zinc-600 dark:text-zinc-400">
            Enterprise ESG & Global Food Security Simulation Studio
          </p>
        </div>

        <div className="flex flex-wrap gap-2.5 bg-zinc-50 dark:bg-zinc-900/50 p-3.5 rounded-2xl border border-zinc-100 dark:border-zinc-800/80 shadow-inner">
          <div className="flex items-center gap-1.5 text-xs text-zinc-500 dark:text-zinc-400 mr-1.5 font-medium">
            <Cpu size={14} className="text-purple-500 animate-pulse" />
            <span>Microsoft IQ Layer:</span>
          </div>
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium bg-purple-50 dark:bg-purple-950/45 text-purple-700 dark:text-purple-300 border border-purple-100 dark:border-purple-900/50">
            Foundry IQ
          </span>
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium bg-indigo-50 dark:bg-indigo-950/45 text-indigo-700 dark:text-indigo-300 border border-indigo-100 dark:border-indigo-900/50">
            Fabric IQ
          </span>
        </div>
      </div>
    </section>
  );
}
