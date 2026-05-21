"use client";

import { useState } from "react";

export default function Home() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");

  return (
    <div className="flex-1 bg-[#09090b] flex flex-col items-center justify-center p-6 sm:p-12 relative overflow-hidden">
      {/* Background gradients */}
      <div className="absolute top-1/4 left-1/4 -translate-x-1/2 -translate-y-1/2 w-[300px] h-[300px] rounded-full bg-indigo-500/10 blur-[100px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 translate-x-1/2 translate-y-1/2 w-[300px] h-[300px] rounded-full bg-violet-500/10 blur-[100px] pointer-events-none" />
      
      <div className="w-full max-w-4xl z-10 space-y-8">
        <div className="text-center space-y-3">
          <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl bg-gradient-to-r from-zinc-100 via-zinc-200 to-zinc-400 bg-clip-text text-transparent">
            Automate Your Code Reviews
          </h1>
          <p className="text-zinc-400 max-w-xl mx-auto text-base sm:text-lg">
            Paste your source code or a unified git diff below, and our AI reviewer will scan it for bugs, issues, and style violations.
          </p>
        </div>

        {/* Input Panel with Glassmorphism */}
        <div className="bg-[#18181b]/50 border border-[#27272a] rounded-2xl p-6 backdrop-blur-xl shadow-2xl space-y-6 glow-card">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-zinc-200">Submit Code</h2>
          </div>
          
          <div className="w-full h-80 bg-zinc-950/40 border border-zinc-800 rounded-xl p-4">
            {/* Code placeholder for now */}
            <p className="text-zinc-500 text-sm">Editor scaffold ready...</p>
          </div>
        </div>
      </div>
    </div>
  );
}
