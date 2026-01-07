import React, { useEffect, useState } from 'react';
import { Search, Filter } from 'lucide-react';
import api from '../lib/api';
import { cn } from '../lib/utils';

const Jobs = () => {
    const [jobs, setJobs] = useState([]);
    const [filter, setFilter] = useState('ALL');

    useEffect(() => {
        const fetchJobs = async () => {
            try {
                const res = await api.get('/jobs');
                setJobs(res.data);
            } catch (err) {
                setJobs([
                    { job_id: 'uuid-1', erp_job: '10452', customer: 'ACME Parts', part: 'PART-AX123', status: 'RUNNING', qty: 250 },
                    { job_id: 'uuid-2', erp_job: '10453', customer: 'Cyberdyne', part: 'SKY-NET-01', status: 'RUNNING', qty: 80 },
                    { job_id: 'uuid-3', erp_job: '10460', customer: 'Wayne Ent', part: 'BAT-WING-07', status: 'NESTING', qty: 40 },
                    { job_id: 'uuid-4', erp_job: '10461', customer: 'Stark Ind', part: 'MK3-CHEST', status: 'QUEUED', qty: 10 },
                    { job_id: 'uuid-5', erp_job: '10422', customer: 'General Motors', part: 'BRACKET-L', status: 'DONE', qty: 5000 },
                ]);
            }
        };
        fetchJobs();
    }, []);

    const filteredJobs = filter === 'ALL' ? jobs : jobs.filter(j => j.status === filter);

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <h2 className="text-2xl font-bold text-white">Job Queue</h2>
                <div className="flex gap-2">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
                        <input
                            type="text"
                            placeholder="Search jobs..."
                            className="bg-slate-900 border border-slate-700 rounded-lg pl-10 pr-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500 w-64"
                        />
                    </div>
                    <button className="p-2 bg-slate-800 text-slate-400 rounded-lg border border-slate-700 hover:text-white">
                        <Filter size={20} />
                    </button>
                </div>
            </div>

            {/* Filter Tabs */}
            <div className="flex border-b border-slate-800">
                {['ALL', 'QUEUED', 'NESTING', 'RUNNING', 'DONE'].map(status => (
                    <button
                        key={status}
                        onClick={() => setFilter(status)}
                        className={cn(
                            "px-4 py-3 text-sm font-medium border-b-2 transition-colors",
                            filter === status
                                ? "border-blue-500 text-blue-400"
                                : "border-transparent text-slate-500 hover:text-white hover:border-slate-700"
                        )}
                    >
                        {status}
                    </button>
                ))}
            </div>

            {/* Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="bg-slate-950 text-xs uppercase text-slate-500 font-medium">
                        <tr>
                            <th className="px-6 py-4">Job Number</th>
                            <th className="px-6 py-4">Customer</th>
                            <th className="px-6 py-4">Part Number</th>
                            <th className="px-6 py-4">Quantity</th>
                            <th className="px-6 py-4">Status</th>
                            <th className="px-6 py-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {filteredJobs.map((job) => (
                            <tr key={job.job_id} className="hover:bg-slate-800/50 transition-colors group">
                                <td className="px-6 py-4 font-mono text-sm text-blue-400 font-medium">{job.erp_job}</td>
                                <td className="px-6 py-4 text-sm text-slate-300">{job.customer}</td>
                                <td className="px-6 py-4 text-sm text-slate-400">{job.part}</td>
                                <td className="px-6 py-4 text-sm text-slate-400">{job.qty.toLocaleString()}</td>
                                <td className="px-6 py-4">
                                    <span className={cn(
                                        "text-xs px-2 py-1 rounded-full font-bold",
                                        job.status === 'RUNNING' ? "bg-amber-500/10 text-amber-500" :
                                            job.status === 'DONE' ? "bg-green-500/10 text-green-500" :
                                                job.status === 'QUEUED' ? "bg-blue-500/10 text-blue-500" :
                                                    "bg-slate-700/50 text-slate-400"
                                    )}>
                                        {job.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-right">
                                    <button className="text-sm text-slate-500 hover:text-white underline">
                                        Details
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Jobs;
