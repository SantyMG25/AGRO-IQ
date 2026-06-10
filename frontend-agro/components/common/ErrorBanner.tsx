/* components/common/ErrorBanner.tsx */
import React from 'react';
import { AlertTriangle } from 'lucide-react';

export const ErrorBanner: React.FC<{ message: string }> = ({ message }) => (
  <div className="w-full p-6 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/50 rounded-3xl flex items-center gap-3">
    <AlertTriangle className="w-5 h-5 text-red-600" />
    <p className="text-red-700 dark:text-red-400 font-medium">{message}</p>
  </div>
);
