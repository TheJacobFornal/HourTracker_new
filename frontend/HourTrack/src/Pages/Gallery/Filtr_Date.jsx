// Filtr_Date.jsx
import React, { useEffect, useRef, useState } from "react";

export default function DateRange({ value, onChange }) {
  const [from, setFrom] = useState(value?.from ?? "");
  const [to, setTo] = useState(value?.to ?? "");
  const [error, setError] = useState("");
  const isFirst = useRef(true);

  useEffect(() => {
    setFrom(value?.from ?? "");
    setTo(value?.to ?? "");
  }, [value?.from, value?.to]);

  useEffect(() => {
    if (isFirst.current) {
      isFirst.current = false;
      return;
    }
    if (!from && !to) {
      setError("");
      onChange?.({ from: null, to: null });
      return;
    }
    if ((from && !to) || (!from && to)) {
      setError("");
      return;
    }
    if (from > to) {
      setError("Start must be before finish.");
      return;
    }
    setError("");
    onChange?.({ from, to });
  }, [from, to, onChange]);

  const clear = () => {
    setFrom("");
    setTo("");
    setError("");
    onChange?.({ from: null, to: null });
  };

  return (
    <div className="flex flex-col">
      <style>{`
        input[type="date"]::-webkit-calendar-picker-indicator {
          opacity: 0 !important;
          display: none !important;
          -webkit-appearance: none !important;
        }
        input[type="date"]::-moz-calendar-picker-indicator { display: none !important; }
        input[type="date"]::-ms-clear { display: none; }
        input[type="date"]::-ms-expand { display: none; }
      `}</style>

      <div className="flex items-center gap-2">
        <span className="text-[18px] font-medium text-gray-700">Date:</span>

        <div className="relative inline-flex items-center gap-2">
          <input
            type="date"
            value={from}
            onChange={(e) => setFrom(e.target.value)}
            max={to || undefined}
            placeholder="YYYY-MM-DD"
            className="w-[130px] text-[16px] bg-white border border-gray-300 rounded-low shadow-sm hover:bg-gray-50 focus:outline-none px-2 py-2"
          />
          <input
            type="date"
            value={to}
            onChange={(e) => setTo(e.target.value)}
            min={from || undefined}
            placeholder="YYYY-MM-DD"
            className="w-[130px] text-[16px] bg-white border border-gray-300 rounded-low shadow-sm hover:bg-gray-50 focus:outline-none px-2 py-2"
          />
          <button
            type="button"
            onClick={clear}
            className="h-fit text-[16px] rounded-low border border-gray-300 px-3 py-2 text-gray-700 bg-white shadow-sm hover:bg-gray-50"
          >
            Clear
          </button>
        </div>
      </div>

      {error && <p className="mt-1 text-xs text-red-600">{error}</p>}
    </div>
  );
}
