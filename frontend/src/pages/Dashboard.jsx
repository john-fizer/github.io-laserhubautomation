import React, { useEffect, useState } from 'react';
import { Package, Zap, CheckCircle, Clock, ArrowUpRight } from 'lucide-react';
import { cn } from '../lib/utils';
import api from '../lib/api';

const StatCard = ({ label, value, icon: Icon, color, subtext }) => (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl hover:bg-slate-800/50 transition-all">
        <div className="flex items-start justify-between">
            <div>
                <p className="text-slate-500 text-sm font-medium">{label}</p>
                <h3 className="text-3xl font-bold text-white mt-2">{value}</h3>
                {subtext && <p className="text-slate-500 text-xs mt-1">{subtext}</p>}
            </div>
            <div className={cn("p-3 rounded-lg bg-opacity-10", color)}>
                <Icon size={24} className={cn("text-white opacity-90")} />
            </div>
        </div>
    </div>
);

const ActivityItem = ({ time, message }) => (
    <div className="flex gap-4 items-start relative pb-6 border-l border-slate-800 ml-2 pl-6 last:border-0">
        <div className="absolute -left-[5px] top-1 w-2.5 h-2.5 rounded-full bg-slate-700 border border-slate-950"></div>
        <span className="text-xs font-mono text-slate-500 pt-0.5">{time}</span>
        <p className="text-slate-300 text-sm">{message}</p>
    </div>
);

const Dashboard = () => {
    const [stats, setStats] = useState(null);
    const [activity, setActivity] = useState([]);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const res = await api.get('/dashboard/summary');
                setStats(res.data);
            } catch (err) {
                console.error("Dashboard Stats Fail", err);
                // Fallback mock
                setStats({ jobs_queued: 24, jobs_running: 3, jobs_done_today: 18, lasers_active: 2 });
            }
        };

        const fetchActivity = async () => {
            try {
                const res = await api.get('/dashboard/activity');
                setActivity(res.data);
            } catch (err) {
                setActivity([
                    { time: "10:21", message: "Laser 1 completed Sheet S-027 (Jobs: 10452, 10453)" },
                    { time: "10:15", message: "Job 10452 posted back to JobBOSS2 (1.8 hours billed)." },
                    { time: "09:44", message: "Sheet S-027 started on Laser 1" },
                ]);
            }
        };

        fetchStats();
        fetchActivity();

        const interval = setInterval(() => { fetchStats(); fetchActivity(); }, 15000);
        return () => clearInterval(interval);
    }, []);

    if (!stats) return <div className="text-slate-500">Loading dashboard...</div>;

    return (
        <div className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    label="Queue Depth"
                    value={stats.jobs_queued}
                    icon={Package}
                    color="bg-blue-500"
                    subtext="Jobs waiting for nest"
                />
                <StatCard
                    label="Active Lasers"
                    value={`${stats.lasers_active} / 3`}
                    icon={Zap}
                    color="bg-purple-500"
                    subtext="Running efficiency: 85%"
                />
                <StatCard
                    label="Jobs Running"
                    value={stats.jobs_running}
                    icon={Clock}
                    color="bg-amber-500"
                    subtext="Currently on table"
                />
                <StatCard
                    label="Completed Today"
                    value={stats.jobs_done_today}
                    icon={CheckCircle}
                    color="bg-green-500"
                    subtext="+12% from yesterday"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Main Job Board Preview */}
                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-lg font-semibold text-white">Active Production</h2>
                        <button className="text-xs text-blue-400 hover:text-blue-300 flex items-center gap-1">
                            View all jobs <ArrowUpRight size={12} />
                        </button>
                    </div>

                    <div className="overflow-x-auto">
                        <table className="w-full text-left">
                            <thead className="text-xs text-slate-500 uppercase bg-slate-800/50 rounded">
                                <tr>
                                    <th className="px-4 py-3 rounded-l">Job #</th>
                                    <th className="px-4 py-3">Customer</th>
                                    <th className="px-4 py-3">Status</th>
                                    <th className="px-4 py-3 text-right rounded-r">Progress</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-800">
                                {[
                                    { id: '10452', cust: 'ACME Parts', status: 'RUNNING', progress: 45 },
                                    { id: '10453', cust: 'Cyberdyne', status: 'RUNNING', progress: 30 },
                                    { id: '10460', cust: 'Wayne Ent', status: 'NESTING', progress: 0 },
                                    { id: '10461', cust: 'Stark Ind', status: 'QUEUED', progress: 0 },
                                ].map((job) => (
                                    <tr key={job.id} className="hover:bg-slate-800/30 transition-colors">
                                        <td className="px-4 py-3 font-mono text-sm text-blue-400">{job.id}</td>
                                        <td className="px-4 py-3 text-sm text-slate-300">{job.cust}</td>
                                        <td className="px-4 py-3">
                                            <span className={cn(
                                                "text-xs px-2 py-1 rounded-full font-medium",
                                                job.status === 'RUNNING' ? "bg-amber-500/10 text-amber-500" :
                                                    job.status === 'NESTING' ? "bg-purple-500/10 text-purple-500" :
                                                        "bg-slate-700/50 text-slate-400"
                                            )}>
                                                {job.status}
                                            </span>
                                        </td>
                                        <td className="px-4 py-3 text-right">
                                            <div className="w-24 h-1.5 bg-slate-800 rounded-full ml-auto overflow-hidden">
                                                <div
                                                    className="h-full bg-blue-500 rounded-full"
                                                    style={{ width: `${job.progress}%` }}
                                                ></div>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Feed */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h2 className="text-lg font-semibold text-white mb-6">Live Feed</h2>
                    <div className="space-y-1">
                        {activity.map((item, idx) => (
                            <ActivityItem key={idx} time={item.time} message={item.message} />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
