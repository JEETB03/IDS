"use client";

import React, { useEffect, useState } from 'react';
import api from '@/lib/api';
import AlertTable from './AlertTable';
import MatrixBackground from './MatrixBackground';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Shield, Activity, AlertOctagon, AlertTriangle, FileText } from 'lucide-react';
import Link from 'next/link';

export default function Dashboard() {
    const [alerts, setAlerts] = useState([]);
    const [stats, setStats] = useState({ total: 0, benign: 0, malicious: 0 });
    const [chartData, setChartData] = useState<any[]>([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await api.get('/alerts');
                setAlerts(res.data);

                // Calculate stats
                const malicious = res.data.length; // Assuming API only returns alerts (malicious)
                setStats({ total: malicious, benign: 0, malicious });

                // Update chart data (mocking traffic flow for demo if no real data)
                setChartData(prev => {
                    const now = new Date().toLocaleTimeString();
                    const newData = [...prev, { name: now, threats: malicious }];
                    if (newData.length > 20) newData.shift();
                    return newData;
                });

            } catch (error) {
                console.error("Error fetching alerts:", error);
            }
        };

        const interval = setInterval(fetchData, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="relative min-h-screen bg-gray-900 overflow-hidden text-gray-100">
            <MatrixBackground />

            <div className="relative z-10 p-6 space-y-6">
                <header className="mb-8 flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-green-500 flex items-center gap-3">
                            <Shield className="w-10 h-10 text-green-500" />
                            Dreadnought IDS
                        </h1>
                        <p className="text-gray-400 mt-2">Real-time Network Intrusion Detection System</p>
                    </div>
                    <Link href="/reports" className="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 border border-gray-700 rounded-lg text-gray-300 transition-colors">
                        <FileText className="w-5 h-5" />
                        View Reports
                    </Link>
                </header>

                {/* Stats Row */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-gray-800/80 backdrop-blur-sm p-6 rounded-xl shadow-lg border border-gray-700 flex items-center justify-between hover:border-green-500/50 transition-colors group">
                        <div>
                            <p className="text-sm text-gray-400 uppercase font-semibold group-hover:text-green-400 transition-colors">System Status</p>
                            <p className="text-2xl font-bold text-green-500 mt-1">Active Monitoring</p>
                        </div>
                        <Activity className="w-10 h-10 text-green-500 opacity-20 group-hover:opacity-100 transition-opacity" />
                    </div>
                    <div className="bg-gray-800/80 backdrop-blur-sm p-6 rounded-xl shadow-lg border border-gray-700 flex items-center justify-between hover:border-red-500/50 transition-colors group">
                        <div>
                            <p className="text-sm text-gray-400 uppercase font-semibold group-hover:text-red-400 transition-colors">Threats Detected</p>
                            <p className="text-2xl font-bold text-red-500 mt-1">{stats.malicious}</p>
                        </div>
                        <AlertOctagon className="w-10 h-10 text-red-500 opacity-20 group-hover:opacity-100 transition-opacity" />
                    </div>
                    <div className="bg-gray-800/80 backdrop-blur-sm p-6 rounded-xl shadow-lg border border-gray-700 flex items-center justify-between hover:border-blue-500/50 transition-colors group">
                        <div>
                            <p className="text-sm text-gray-400 uppercase font-semibold group-hover:text-blue-400 transition-colors">Network Load</p>
                            <p className="text-2xl font-bold text-blue-500 mt-1">Normal</p>
                        </div>
                        <Shield className="w-10 h-10 text-blue-500 opacity-20 group-hover:opacity-100 transition-opacity" />
                    </div>
                </div>

                {/* Main Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Left Column: Chart */}
                    <div className="lg:col-span-2 bg-gray-800/80 backdrop-blur-sm p-6 rounded-xl shadow-lg border border-gray-700 hover:border-gray-600 transition-colors">
                        <h2 className="text-lg font-semibold text-white mb-4">Threat Activity (Real-time)</h2>
                        <div className="h-64 w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={chartData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.1} />
                                    <XAxis dataKey="name" stroke="#9CA3AF" fontSize={12} tickLine={false} axisLine={false} />
                                    <YAxis stroke="#9CA3AF" fontSize={12} tickLine={false} axisLine={false} />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#1F2937', border: 'none', borderRadius: '8px', color: '#fff' }}
                                        itemStyle={{ color: '#fff' }}
                                    />
                                    <Line type="monotone" dataKey="threats" stroke="#EF4444" strokeWidth={2} dot={false} activeDot={{ r: 8 }} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Right Column: Recent Alerts (Compact) */}
                    <div className="bg-gray-800/80 backdrop-blur-sm p-6 rounded-xl shadow-lg border border-gray-700 overflow-hidden hover:border-gray-600 transition-colors">
                        <h2 className="text-lg font-semibold text-white mb-4">Latest Incidents</h2>
                        <div className="space-y-4 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
                            {alerts.slice(0, 5).map((alert: any, idx) => (
                                <div key={idx} className="flex items-start gap-3 p-3 bg-red-900/20 rounded-lg border border-red-900/30 hover:bg-red-900/40 transition-colors cursor-pointer">
                                    <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                                    <div>
                                        <p className="text-sm font-bold text-gray-100">{alert.type}</p>
                                        <p className="text-xs text-gray-400">{alert.src_ip} → {alert.dst_ip}</p>
                                        <p className="text-xs text-gray-500 mt-1">{alert.time_str}</p>
                                    </div>
                                </div>
                            ))}
                            {alerts.length === 0 && <p className="text-sm text-gray-500 text-center py-4">No recent incidents</p>}
                        </div>
                    </div>
                </div>

                {/* Bottom: Full Table */}
                <div className="bg-gray-800/80 backdrop-blur-sm p-6 rounded-xl shadow-lg border border-gray-700 hover:border-gray-600 transition-colors">
                    <h2 className="text-lg font-semibold text-white mb-4">Detailed Incident Log</h2>
                    <AlertTable alerts={alerts} />
                </div>
            </div>
        </div>
    );
}
