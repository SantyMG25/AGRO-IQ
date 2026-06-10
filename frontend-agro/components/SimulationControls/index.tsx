"use client";

import React from 'react';
import { Sliders, Award, Droplets, Snowflake } from 'lucide-react';
import PresetList from './PresetList';
import RangeControl from './RangeControl';
import DescriptionBlock from './DescriptionBlock';

type SimulationControlsProps = {
  irrigation: number;
  setIrrigation: (value: number) => void;
  shift: number;
  setShift: (value: number) => void;
};

const getIrrigationDescription = (irr: number) => {
  if (irr < 30) {
    return { icon: '⚠️', text: 'Low irrigation: High risk of soil drying and crop failure during dry spells.', color: 'text-red-500 dark:text-red-400' };
  }
  if (irr <= 70) {
    return { icon: '⚙️', text: 'Moderate irrigation: Medium soil protection. Yield is improved but vulnerable in peak drought.', color: 'text-amber-500 dark:text-amber-400' };
  }
  return { icon: '✨', text: 'Optimal irrigation: Fully automated drip irrigation. Maximizes soil water retention and yield.', color: 'text-emerald-500 dark:text-emerald-400' };
};

const getShiftDescription = (sh: number) => {
  if (sh < 0) {
    return { icon: '❄️', text: 'Early Planting: High danger of winter frost during the critical flowering stage.', color: 'text-sky-500 dark:text-sky-400' };
  }
  if (sh === 0) {
    return { icon: '📅', text: 'Traditional Calendar: Balanced seasonal path, standard local timelines.', color: 'text-zinc-500 dark:text-zinc-400' };
  }
  return { icon: '☀️', text: 'Delayed Planting: Shakes off winter frost risk, but increases summer heat stress during grain fill.', color: 'text-amber-500 dark:text-amber-400' };
};

export default function SimulationControls({ irrigation, setIrrigation, shift, setShift }: SimulationControlsProps) {
  const presets = [
    {
      title: '🌾 Andean Rainfed Crop',
      irr: 0,
      sh: 0,
      badge: 'High Risk',
      badgeColor: 'bg-red-500/10 text-red-700 dark:text-red-400 border border-red-500/20',
      desc: 'Traditional farming with no irrigation. Vulnerable to cold waves and droughts.',
      borderColor: 'border-red-200 dark:border-red-950/40 hover:border-red-500/30',
    },
    {
      title: '💧 Technified Mitigation',
      irr: 75,
      sh: 0,
      badge: 'Stable',
      badgeColor: 'bg-blue-500/10 text-blue-700 dark:text-blue-400 border border-blue-500/20',
      desc: '75% automated drip irrigation. Maximizes soil water retention under normal schedules.',
      borderColor: 'border-blue-200 dark:border-blue-950/40 hover:border-blue-500/30',
    },
    {
      title: '📅 Frost Avoidance Shift',
      irr: 30,
      sh: 2,
      badge: 'Balanced',
      badgeColor: 'bg-amber-500/10 text-amber-700 dark:text-amber-400 border border-amber-500/20',
      desc: 'Delays planting by 2 weeks. Postpones germination to bypass the peak winter frost season.',
      borderColor: 'border-amber-200 dark:border-amber-950/40 hover:border-amber-500/30',
    },
    {
      title: '🛡️ Optimal ESG Adaptation',
      irr: 80,
      sh: 1,
      badge: 'Best ROI',
      badgeColor: 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20',
      desc: 'Combines high irrigation with a 1-week shift. Reaches optimal water-heat balance.',
      borderColor: 'border-emerald-200 dark:border-emerald-950/40 hover:border-emerald-500/30',
    },
  ];

  const activePresetIdx = presets.findIndex((p) => p.irr === irrigation && p.sh === shift);

  const irrDesc = getIrrigationDescription(irrigation);
  const shDesc = getShiftDescription(shift);

  const applyPreset = (p: any) => {
    setIrrigation(p.irr);
    setShift(p.sh);
  };

  return (
    <section className="rounded-3xl bg-white/80 dark:bg-zinc-950/70 backdrop-blur-md p-8 shadow-md ring-1 ring-black/5 dark:ring-white/10 w-full flex flex-col gap-6 border border-zinc-100 dark:border-zinc-900/50 transition-all duration-300">
      <div className="flex items-center gap-2.5 text-emerald-600 dark:text-emerald-400 font-semibold border-b border-zinc-100 dark:border-zinc-900 pb-4">
        <Sliders size={20} className="text-emerald-500" />
        <h2 className="tracking-tight text-lg text-zinc-900 dark:text-zinc-100 font-bold">Simulation Controls</h2>
      </div>

      <PresetList presets={presets} activeIdx={activePresetIdx} onApply={applyPreset} />

      <div className="h-px bg-zinc-100 dark:bg-zinc-900 my-1" />

      <div className="flex flex-col gap-6">
        <div>
          <RangeControl
            label="Irrigation Investment"
            value={irrigation}
            min={0}
            max={100}
            icon={<Droplets size={14} className="text-blue-500" />}
            unitLabel={`${irrigation}%`}
            onChange={setIrrigation}
            gradient={'linear-gradient(to right, #ef4444 0%, #f59e0b 35%, #10b981 70%, #10b981 100%)'}
          />
          <div className="mt-3">
            <DescriptionBlock icon={irrDesc.icon} text={irrDesc.text} color={irrDesc.color} />
          </div>
        </div>

        <div>
          <RangeControl
            label="Calendar Shift"
            value={shift}
            min={-4}
            max={4}
            icon={<Snowflake size={14} className="text-sky-400" />}
            unitLabel={shift === 0 ? 'Normal' : shift > 0 ? `+${shift} weeks` : `${shift} weeks`}
            onChange={setShift}
            gradient={'linear-gradient(to right, #38bdf8 0%, #10b981 50%, #f97316 100%)'}
          />
          <div className="mt-3">
            <DescriptionBlock icon={shDesc.icon} text={shDesc.text} color={shDesc.color} />
          </div>
        </div>
      </div>
    </section>
  );
}
