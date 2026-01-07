// Mock API for static GitHub Pages deployment
// This replaces the axios backend calls with mock data
// Note: Only GET requests are supported as this is a read-only static site

const mockData = {
    '/dashboard/summary': {
        jobs_queued: 24,
        jobs_running: 3,
        jobs_done_today: 18,
        lasers_active: 2
    },
    '/dashboard/activity': [
        { time: "10:21", message: "Laser 1 completed Sheet S-027 (Jobs: 10452, 10453)" },
        { time: "10:15", message: "Job 10452 posted back to JobBOSS2 (1.8 hours billed)." },
        { time: "09:44", message: "Sheet S-027 started on Laser 1" },
    ],
    '/machines': [
        { id: 1, name: 'Laser 1', status: 'RUNNING', current_run: { program: 'L1-027.MIN' } },
        { id: 2, name: 'Laser 2', status: 'IDLE', current_run: null },
        { id: 3, name: 'Laser 3', status: 'STOPPED', current_run: null },
    ],
    '/jobs': [
        { job_id: 'uuid-1', erp_job: '10452', customer: 'ACME Parts', part: 'PART-AX123', status: 'RUNNING', qty: 250 },
        { job_id: 'uuid-2', erp_job: '10453', customer: 'Cyberdyne', part: 'SKY-NET-01', status: 'RUNNING', qty: 80 },
        { job_id: 'uuid-3', erp_job: '10460', customer: 'Wayne Ent', part: 'BAT-WING-07', status: 'NESTING', qty: 40 },
        { job_id: 'uuid-4', erp_job: '10461', customer: 'Stark Ind', part: 'MK3-CHEST', status: 'QUEUED', qty: 10 },
        { job_id: 'uuid-5', erp_job: '10422', customer: 'General Motors', part: 'BRACKET-L', status: 'DONE', qty: 5000 },
    ]
};

const api = {
    get: (url) => {
        return Promise.resolve({ data: mockData[url] || {} });
    },
    // These methods are not implemented for static site but included for API compatibility
    post: () => Promise.reject(new Error('POST not supported in static mode')),
    put: () => Promise.reject(new Error('PUT not supported in static mode')),
    delete: () => Promise.reject(new Error('DELETE not supported in static mode')),
    patch: () => Promise.reject(new Error('PATCH not supported in static mode'))
};

export default api;
