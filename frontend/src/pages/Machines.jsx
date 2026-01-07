import React, { useEffect, useState } from 'react';
import { Server, Play, Pause, AlertTriangle } from 'lucide-react';
import { cn } from '../lib/utils';
import api from '../lib/api';

// Machine Card Component associated with this page
const MachineCard = ({ machine }) => {
    // Status Logic
    const isRunning = machine.status === 'ACTIVE' || machine.status === 'RUNNING'; // Handle variation
    const isError = machine.status === 'STOPPED' && machine.alarm; // Simplified logic

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 relative overflow-hidden group hover:border-slate-700 transition-all">
            {/* Status Bar */}
            <div className={cn(
                "absolute top-0 left-0 w-1 h-full",
                isRunning ? "bg-green-500" : isError ? "bg-red-500" : "bg-slate-700"
            )} />

            <div className="flex justify-between items-start mb-6 pl-4">
                <div>
                    <h3 className="text-xl font-bold text-white">{machine.name}</h3>
                    <p className="text-sm text-slate-500 mt-1">Fiber Laser 4kW</p>
                </div>
                <div className={cn(
                    "px-3 py-1 rounded-full text-xs font-bold flex items-center gap-2",
                    isRunning ? "bg-green-500/10 text-green-500" : "bg-slate-800 text-slate-400"
                )}>
                    {isRunning ? <Play size={12} /> : <Pause size={12} />}
                    {machine.status || 'IDLE'}
                </div>
            </div>

            {/* Current Run Details */}
            <div className="pl-4 space-y-4">
                <div className="bg-slate-950/50 rounded-lg p-4 border border-slate-800/50">
                    <div className="flex justify-between text-xs text-slate-500 mb-2">
                        <span>CURRENT PROGRAM</span>
                        <span>SHEET S-027</span>
                    </div>
                    <div className="font-mono text-blue-400 font-medium truncate">
                        {machine.current_run?.program || 'NO PROGRAM LOADED'}
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <span className="text-xs text-slate-500 block">Total Runtime today</span>
                        <span className="text-lg font-medium text-white">4h 12m</span>
                    </div>
                    <div>
                        <span className="text-xs text-slate-500 block">Utilization</span>
                        <span className="text-lg font-medium text-green-400">82%</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

const Machines = () => {
    const [machines, setMachines] = useState([]);

    useEffect(() => {
        const fetchMachines = async () => {
            try {
                const res = await api.get('/machines');
                setMachines(res.data);
            } catch (err) {
                // Mock data
                setMachines([
                    { id: 1, name: 'Laser 1', status: 'RUNNING', current_run: { program: 'L1-027.MIN' } },
                    { id: 2, name: 'Laser 2', status: 'IDLE', current_run: null },
                    { id: 3, name: 'Laser 3', status: 'STOPPED', current_run: null },
                ]);
            }
        };
        fetchMachines();
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-white">Machine Status</h2>
                <button className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-medium transition-colors">
                    View Schedule
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {machines.map((m) => (
                    <MachineCard key={m.id} machine={m} />
                ))}
            </div>

            <div className="mt-12 p-8 border border-slate-800 rounded-xl bg-slate-900/50 flex flex-col items-center justify-center text-center">
                <Server className="text-slate-700 w-16 h-16 mb-4" />
                <h3 className="text-lg font-medium text-white">MTConnect Stream Status</h3>
                <p className="text-slate-500 mt-2 max-w-md">
                    All adaptors are reporting healthy heartbeats. Latency is running at &lt;50ms.
                </p>
            </div>
        </div>
    );
};

export default Machines;
