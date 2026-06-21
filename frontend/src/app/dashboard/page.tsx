"use client";

import { useState, useEffect } from "react";
import Cookies from "js-cookie";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function Dashboard() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      const token = Cookies.get("token");
      try {
        const res = await fetch(`${API_BASE_URL}/analytics/metrics`, {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        });
        if (res.ok) {
          const data = await res.json();
          setMetrics(data);
        }
      } catch (err) {
        console.error("Failed to fetch metrics", err);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
  }, []);

  if (loading) {
    return (
      <div className="flex-1 bg-black flex items-center justify-center min-h-screen">
        <div className="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!metrics) {
    return (
      <div className="flex-1 bg-black flex items-center justify-center min-h-screen">
        <p className="text-zinc-500">Failed to load analytics.</p>
      </div>
    );
  }

  return (
    <div className="flex-1 bg-black flex flex-col p-6 sm:p-12 relative overflow-hidden min-h-screen">
      <div className="absolute top-0 right-0 w-[500px] h-[500px] rounded-full bg-blue-900/20 blur-[120px] pointer-events-none" />
      
      <div className="w-full max-w-6xl mx-auto z-10 space-y-8 animate-fade-in">
        <div>
          <h1 className="text-3xl font-extrabold text-white">Analytics Dashboard</h1>
          <p className="text-zinc-400 mt-2">Team velocity and code quality metrics.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-zinc-900 border border-zinc-800 p-6 rounded-2xl">
            <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider">Avg Review Time</h3>
            <p className="text-4xl font-black text-white mt-2">{metrics.velocity.avg_review_time_minutes} <span className="text-xl text-zinc-500 font-medium">min</span></p>
          </div>
          <div className="bg-zinc-900 border border-zinc-800 p-6 rounded-2xl">
            <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider">PRs Reviewed</h3>
            <p className="text-4xl font-black text-white mt-2">{metrics.velocity.prs_reviewed_this_week}</p>
          </div>
          <div className="bg-zinc-900 border border-zinc-800 p-6 rounded-2xl">
            <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider">AI Acceptance Rate</h3>
            <p className="text-4xl font-black text-blue-500 mt-2">{metrics.accuracy.acceptance_rate}</p>
          </div>
        </div>

        <div className="bg-zinc-900 border border-zinc-800 p-6 rounded-2xl h-[400px]">
          <h3 className="text-lg font-bold text-white mb-6">Developer Bug Heatmap</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={metrics.heatmap}>
              <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
              <XAxis dataKey="developer" stroke="#a1a1aa" tick={{fill: '#a1a1aa'}} />
              <YAxis stroke="#a1a1aa" tick={{fill: '#a1a1aa'}} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '8px', color: '#fff' }}
                itemStyle={{ color: '#e4e4e7' }}
              />
              <Bar dataKey="security" stackId="a" fill="#ef4444" name="Security" radius={[0, 0, 4, 4]} />
              <Bar dataKey="performance" stackId="a" fill="#f59e0b" name="Performance" />
              <Bar dataKey="style" stackId="a" fill="#3b82f6" name="Style" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
