"use client";

import React, { useEffect, useState } from 'react';
import api from '@/lib/api';
import { FileText, Download, ArrowLeft, Shield } from 'lucide-react';
import Link from 'next/link';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import MatrixBackground from '@/components/MatrixBackground';

export default function ReportsPage() {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const res = await api.get('/history');
                setHistory(res.data);
            } catch (error) {
                console.error("Error fetching history:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchHistory();
    }, []);

    const generatePDF = () => {
        const doc = new jsPDF();

        // Header
        doc.setFontSize(20);
        doc.setTextColor(40, 167, 69); // Green
        doc.text("Dreadnought IDS - Incident Report", 14, 22);

        doc.setFontSize(10);
        doc.setTextColor(100);
        doc.text(`Generated on: ${new Date().toLocaleString()}`, 14, 30);

        // Table
        const tableColumn = ["Time", "Type", "Source IP", "Destination IP", "Details"];
        const tableRows = [];

        history.forEach((alert: any) => {
            const alertData = [
                alert.time_str,
                alert.type,
                alert.src_ip,
                alert.dst_ip,
                JSON.stringify(alert.details).substring(0, 50) + "..." // Truncate details
            ];
            tableRows.push(alertData);
        });

        autoTable(doc, {
            head: [tableColumn],
            body: tableRows,
            startY: 40,
            theme: 'grid',
            styles: { fontSize: 8 },
            headStyles: { fillColor: [22, 163, 74] } // Green header
        });

        doc.save(`dreadnought_report_${new Date().toISOString().slice(0, 10)}.pdf`);
    };

    return (
        <div className="relative min-h-screen bg-gray-900 text-gray-100 overflow-hidden">
            <MatrixBackground />

            <div className="relative z-10 p-6 max-w-7xl mx-auto">
                <header className="flex items-center justify-between mb-8">
                    <div className="flex items-center gap-4">
                        <Link href="/" className="p-2 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors">
                            <ArrowLeft className="w-6 h-6 text-gray-400" />
                        </Link>
                        <h1 className="text-3xl font-bold text-green-500 flex items-center gap-3">
                            <Shield className="w-8 h-8" />
                            Incident Reports
                        </h1>
                    </div>
                    <button
                        onClick={generatePDF}
                        className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg text-white font-semibold transition-colors shadow-lg shadow-green-900/20"
                    >
                        <Download className="w-5 h-5" />
                        Download PDF
                    </button>
                </header>

                <div className="bg-gray-800/80 backdrop-blur-sm rounded-xl border border-gray-700 shadow-xl overflow-hidden">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left">
                            <thead className="bg-gray-900/50 text-gray-400 uppercase text-xs font-semibold">
                                <tr>
                                    <th className="px-6 py-4">Time</th>
                                    <th className="px-6 py-4">Type</th>
                                    <th className="px-6 py-4">Source IP</th>
                                    <th className="px-6 py-4">Destination IP</th>
                                    <th className="px-6 py-4">Details</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-700">
                                {loading ? (
                                    <tr>
                                        <td colSpan={5} className="px-6 py-8 text-center text-gray-500">Loading history...</td>
                                    </tr>
                                ) : history.length === 0 ? (
                                    <tr>
                                        <td colSpan={5} className="px-6 py-8 text-center text-gray-500">No historical incidents found.</td>
                                    </tr>
                                ) : (
                                    history.map((alert: any, idx) => (
                                        <tr key={idx} className="hover:bg-gray-700/50 transition-colors">
                                            <td className="px-6 py-4 text-sm text-gray-300 whitespace-nowrap">{alert.time_str}</td>
                                            <td className="px-6 py-4">
                                                <span className={`px-2 py-1 rounded text-xs font-bold ${alert.type === 'BENIGN'
                                                        ? 'bg-green-900/30 text-green-400 border border-green-900/50'
                                                        : 'bg-red-900/30 text-red-400 border border-red-900/50'
                                                    }`}>
                                                    {alert.type}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-sm text-gray-300 font-mono">{alert.src_ip}</td>
                                            <td className="px-6 py-4 text-sm text-gray-300 font-mono">{alert.dst_ip}</td>
                                            <td className="px-6 py-4 text-xs text-gray-500 font-mono max-w-xs truncate">
                                                {JSON.stringify(alert.details)}
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
}
