import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Server, ClipboardList, Settings, User } from 'lucide-react';
import { cn } from '../lib/utils';

const NavItem = ({ to, icon: Icon, label }) => {
    const location = useLocation();
    const isActive = location.pathname === to;

    return (
        <Link
            to={to}
            className={cn(
                "flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors",
                isActive
                    ? "bg-slate-800 text-blue-400 border-l-4 border-blue-500"
                    : "text-slate-400 hover:bg-slate-900 hover:text-white"
            )}
        >
            <Icon size={20} />
            <span className="font-medium">{label}</span>
        </Link>
    );
};

const Layout = ({ children }) => {
    return (
        <div className="flex h-screen bg-slate-950 text-white font-sans overflow-hidden">
            {/* Sidebar */}
            <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col">
                <div className="p-6 border-b border-slate-800">
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                        LaserFlow
                    </h1>
                    <p className="text-xs text-slate-500 mt-1">Shop Floor Automation v1.0</p>
                </div>

                <nav className="flex-1 p-4 space-y-2">
                    <NavItem to="/" icon={LayoutDashboard} label="Dashboard" />
                    <NavItem to="/machines" icon={Server} label="Machines" />
                    <NavItem to="/jobs" icon={ClipboardList} label="Jobs" />
                    <NavItem to="/admin" icon={Settings} label="Admin" />
                </nav>

                <div className="p-4 border-t border-slate-800">
                    <div className="flex items-center space-x-3 text-sm text-slate-400">
                        <User size={16} />
                        <span>John (Admin)</span>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col overflow-hidden">
                {/* Header */}
                <header className="h-16 bg-slate-900/50 backdrop-blur border-b border-slate-800 flex items-center justify-between px-8">
                    <div className="flex items-center space-x-4">
                        <span className="w-2.5 h-2.5 rounded-full bg-green-500 animate-pulse"></span>
                        <span className="text-slate-400 text-sm">MTConnect: Connected</span>
                        <span className="text-slate-600">|</span>
                        <span className="w-2.5 h-2.5 rounded-full bg-green-500"></span>
                        <span className="text-slate-400 text-sm">JB2: Sync OK</span>
                    </div>
                    <div className="text-slate-400 text-sm">
                        {new Date().toLocaleTimeString()}
                    </div>
                </header>

                <div className="flex-1 overflow-auto p-8">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default Layout;
