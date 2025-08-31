// Filtr_Status.jsx
import React, { useEffect, useRef, useState } from "react";

export default function Status({ value = "all", onChange }) {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState(value);
  const ref = useRef(null);

  const options = [
    { label: "ALL", value: "all" },
    { label: "In progress", value: "in_progress" },
    { label: "Finished", value: "finished" },
  ];

  useEffect(() => setSelected(value), [value]);

  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setIsOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const handleSelect = (opt) => {
    setSelected(opt.value);
    onChange?.(opt.value);
    setIsOpen(false);
  };

  const currentLabel =
    options.find((o) => o.value === selected)?.label || "ALL";

  return (
    <div className="flex items-center gap-2" ref={ref}>
      <span className="text-[18px] font-medium text-gray-700">Status:</span>

      {/* Make container shrink to button width */}
      <div className="relative inline-block">
        <button
          type="button"
          className="w-[130px] select-none pl-0 pr-3 py-2 text-left bg-white border border-gray-300 rounded-low shadow-sm hover:bg-gray-50 focus:outline-none"
          onClick={() => setIsOpen((o) => !o)}
          aria-haspopup="listbox"
          aria-expanded={isOpen}
        >
          {currentLabel}
        </button>

        {isOpen && (
          <ul
            className="absolute left-0 mt-1 w-full z-10 max-h-60 overflow-auto rounded-md border border-gray-200 bg-white shadow-lg list-none p-0"
            role="listbox"
            tabIndex={-1}
          >
            {options.map((opt) => (
              <li
                key={opt.value}
                role="option"
                aria-selected={selected === opt.value}
                className={`cursor-pointer text-[16px] min-h-[37px] flex items-center hover:bg-gray-100 ${
                  selected === opt.value ? "bg-gray-50 font-medium" : ""
                }`}
                onClick={() => handleSelect(opt)}
              >
                <span className="block w-full pl-[10px] pr-3 py-2">
                  {opt.label}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
