import React, { useMemo, useState } from "react";

function normalizeUsers(users) {
  if (!users) return [];
  // if it's a mapping: { "Name": hours, ... }
  if (!Array.isArray(users)) {
    return Object.entries(users).map(([name, hours]) => ({ name, hours }));
  }
  // already an array: [{ name, hours }]
  return users;
}

export default function ActivityItem({
  activity,
  hours,
  users,
  defaultOpen = false,
}) {
  const [open, setOpen] = useState(defaultOpen);
  const usersList = useMemo(() => normalizeUsers(users), [users]);

  // if hours not sent, derive from users
  const total = useMemo(
    () =>
      typeof hours === "number"
        ? hours
        : usersList.reduce((acc, u) => acc + Number(u.hours || 0), 0),
    [hours, usersList]
  );

  return (
    <div className="rounded-xl border border-gray-200 bg-white">
      {/* Header row */}
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        className="w-full flex items-center justify-between px-4 py-3"
      >
        <div className="flex items-center gap-3">
          {/* left blue icon (triangular play inside rounded box) */}
          <span className="inline-flex h-7 w-7 items-center justify-center rounded-md border border-blue-400">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#1D9BF0"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
          </span>

          <span className="text-[18px] font-semibold text-gray-800">
            {activity}
          </span>
        </div>

        <span className="text-[18px] font-extrabold text-gray-800">
          {total} H
        </span>
      </button>

      {/* Collapsible users */}
      {open && (
        <div className="px-4 pb-3">
          <hr className="border-gray-200 mb-3" />
          <ul className="space-y-20">
            {usersList.map((u, i) => (
              <li
                key={`${u.name}-${i}`}
                className="flex items-center justify-between text-[14px]"
              >
                <span className="text-[17px] text-gray-700">{u.name}</span>
                <span className="text-[17px] font-medium text-gray-900">
                  {u.hours} h
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
