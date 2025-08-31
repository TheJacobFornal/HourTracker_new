// Filtr_Leader.jsx
import React, { useEffect, useRef, useState } from "react";
import axios from "axios";

export default function LeaderDropdown({ value, onChange }) {
  const [isOpen, setIsOpen] = useState(false);
  const [leaders, setLeaders] = useState([]);
  const [selected, setSelected] = useState(value ?? "ALL");
  const ref = useRef(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/get/leaders").then((res) => {
      setLeaders(["ALL", ...(res.data || [])]);
    });
  }, []);

  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setIsOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const handleSelect = (leader) => {
    setSelected(leader);
    onChange?.(leader);
    setIsOpen(false);
  };

  return (
    <div className="flex items-center gap-2" ref={ref}>
      <span className="text-[18px] font-medium text-gray-700">Leader:</span>

      <div className="relative inline-block">
        <button
          type="button"
          className="w-[130px] select-none pl-0 pr-3 py-2 text-left text-[16px] bg-white border border-gray-300 rounded-low shadow-sm hover:bg-gray-50 focus:outline-none"
          onClick={() => setIsOpen((o) => !o)}
          aria-haspopup="listbox"
          aria-expanded={isOpen}
        >
          <span className="block truncate">{selected}</span>
        </button>

        {isOpen && (
          <ul
            className="absolute left-0 mt-1 w-full z-10 max-h-60 overflow-auto rounded-md border border-gray-200 bg-white shadow-lg list-none p-0"
            role="listbox"
            tabIndex={-1}
          >
            {leaders.map((leader) => (
              <li
                key={leader}
                role="option"
                aria-selected={selected === leader}
                className={`cursor-pointer text-[16px] min-h-[37px] flex items-center hover:bg-gray-100 ${
                  selected === leader ? "bg-gray-50 font-medium" : ""
                }`}
                onClick={() => handleSelect(leader)}
              >
                <span className="block w-full pl-[10px] pr-3 py-2 truncate">
                  {leader}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
