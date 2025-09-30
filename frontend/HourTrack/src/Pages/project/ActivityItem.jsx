import React, { useMemo, useState } from "react";
import "./Project_Style.css";
import triangle from "../../assets/triangle.png";

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
    <div className="activity-item">
      {/* Header row */}
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        className="w-full flex items-center justify-between px-4 py-3"
      >
        <div className="flex items-center gap-3">
          {/* left blue icon (triangular play inside rounded box) */}
          <span className="activity-icon">
            <img
              src={triangle}
              alt="triangle"
              style={{ width: 28, height: 28, transform: "rotate(90deg)" }}
            />
          </span>
          <span className="text-[21px] font-semibold text-black-800">
            {activity}
          </span>
        </div>

        <span className="text-[19px] font-bold text-gray-700">{total} H</span>
      </button>

      {/* Collapsible users */}
      {open && (
        <div className="user_List_acitivity">
          <hr className="border-gray-200 mb-3" />
          <ul className="space-y-500">
            {usersList.map((u, i) => (
              <li
                key={`${u.name}-${i}`}
                className="flex items-center justify-between text-[17px]"
              >
                <span className="text-[19px] font-medium text-gray-900">
                  {u.name}
                </span>
                <span className="text-[19px] font-medium text-gray-900">
                  {u.hours} H
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
