"use client";

import React from 'react';
import { AlertTriangle, ShieldCheck } from 'lucide-react';

interface Alert {
    id?: number;
    src_ip: string;
    dst_ip: string;
    type: string;
    timestamp: number;
    time_str: string;
    details: any;
}

interface Props {
    alerts: Alert[];
}

const AlertTable: React.FC<Props> = ({ alerts }) => {
    return (
        <div className="overflow-x-auto">
            <table className="min-w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-md rounded-lg overflow-hidden">
                <thead className="bg-gray-50 dark:bg-gray-700">
                    <tr>
                        <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Time</th>
                        <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Type</th>
                        <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Source IP</th>
                        <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Destination IP</th>
                        <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Details</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                    {alerts.length === 0 ? (
                        <tr>
                            <td colSpan={5} className="py-4 px-4 text-center text-gray-500 dark:text-gray-400">
                                <div className="flex flex-col items-center justify-center">
                                    <ShieldCheck className="w-8 h-8 text-green-500 mb-2" />
                                    <span>No threats detected recently. System is secure.</span>
                                </div>
                            </td>
                        </tr>
                    ) : (
                        alerts.map((alert, idx) => (
                            <tr key={idx} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                                <td className="py-3 px-4 text-sm text-gray-700 dark:text-gray-300 whitespace-nowrap">{alert.time_str}</td>
                                <td className="py-3 px-4 text-sm font-bold text-red-600 dark:text-red-400 flex items-center gap-2">
                                    <AlertTriangle className="w-4 h-4" />
                                    {alert.type}
                                </td>
                                <td className="py-3 px-4 text-sm text-gray-700 dark:text-gray-300 font-mono">{alert.src_ip}</td>
                                <td className="py-3 px-4 text-sm text-gray-700 dark:text-gray-300 font-mono">{alert.dst_ip}</td>
                                <td className="py-3 px-4 text-sm text-gray-500 dark:text-gray-400">
                                    <details className="cursor-pointer">
                                        <summary>View Features</summary>
                                        <pre className="text-xs mt-2 bg-gray-100 dark:bg-gray-900 p-2 rounded overflow-auto max-w-xs">
                                            {JSON.stringify(alert.details, null, 2)}
                                        </pre>
                                    </details>
                                </td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default AlertTable;
