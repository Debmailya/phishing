import { useMemo, useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function App() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const statusColor = useMemo(() => {
    if (!result) return 'text-cyber-accent';
    return result.prediction === 1 ? 'text-cyber-danger' : 'text-cyber-safe';
  }, [result]);

  const handleScan = async () => {
    setError('');
    setResult(null);

    if (!url.trim()) {
      setError('Please enter a URL to scan.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });

      const data = await response.json();
      if (!response.ok) {
        setError(data.detail || 'Invalid URL or server error.');
      } else {
        setResult(data);
      }
    } catch (scanError) {
      setError('Cannot connect to the backend API.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-cyber-bg text-white px-6 py-10">
      <section className="mx-auto max-w-3xl rounded-2xl border border-cyan-500/30 bg-cyber-panel p-8 shadow-glow">
        <div className="mb-6">
          <p className="text-xs uppercase tracking-[0.3em] text-cyan-300">AI Cybersecurity Dashboard</p>
          <h1 className="text-3xl font-bold">PhishGuard URL Scanner</h1>
          <p className="mt-2 text-sm text-slate-300">
            Analyze suspicious links in real-time with machine learning.
          </p>
        </div>

        <div className="space-y-4">
          <label htmlFor="url-input" className="block text-sm text-slate-300">
            Website URL
          </label>
          <input
            id="url-input"
            type="text"
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            placeholder="https://example.com/login"
            className="w-full rounded-lg border border-cyan-700/60 bg-slate-950 px-4 py-3 text-sm outline-none ring-cyan-400/50 focus:ring"
          />

          <button
            type="button"
            onClick={handleScan}
            disabled={loading}
            className="w-full rounded-lg bg-cyan-500 px-4 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? 'Scanning...' : 'Scan URL'}
          </button>
        </div>

        {error && <p className="mt-4 rounded-md bg-red-500/10 px-4 py-3 text-sm text-red-300">{error}</p>}

        <div className="mt-8 rounded-xl border border-slate-700 bg-slate-900/60 p-5">
          <p className="text-xs uppercase tracking-wider text-slate-400">Scan Result</p>
          <p className={`mt-2 text-2xl font-bold ${statusColor}`}>
            {result ? result.result : 'Awaiting URL scan...'}
          </p>
          <p className="mt-2 text-sm text-slate-300">
            Confidence:{' '}
            <span className="font-semibold text-white">
              {result ? `${(result.confidence * 100).toFixed(2)}%` : '--'}
            </span>
          </p>
        </div>
      </section>
    </main>
  );
}