import React, { useMemo, useState } from "react";
import "./Project_Style.css";
import triangle from "../../assets/triangle.png";

// ✅ Safe normalization for all data shapes
function normalizeUsers(users) {
  if (!users) return [];

  // handle both mapping and array formats
  if (!Array.isArray(users)) {
    return Object.entries(users).map(([name, value]) => {
      if (typeof value === "object" && value !== null) {
        return {
          name,
          hours: Number(value.hours) || 0,
          daily_hours: Number(value.daily_hours) || 0,
        };
      }
      return { name, hours: Number(value) || 0, daily_hours: 0 };
    });
  }

  return users.map((u) => ({
    name: u.name,
    hours: Number(u.hours) || 0,
    daily_hours: Number(u.daily_hours) || 0,
  }));
}

export default function ActivityItem({
  activity,
  hours,
  daily_hours,
  users,
  defaultOpen = false,
}) {
  const [open, setOpen] = useState(defaultOpen);
  const usersList = useMemo(() => normalizeUsers(users), [users]);

  // Calculate totals safely
  const totalHours = useMemo(
    () =>
      typeof hours === "number"
        ? hours
        : usersList.reduce((acc, u) => acc + (u.hours || 0), 0),
    [hours, usersList]
  );

  const totalDailyHours = useMemo(
    () =>
      typeof daily_hours === "number"
        ? daily_hours
        : usersList.reduce((acc, u) => acc + (u.daily_hours || 0), 0),
    [daily_hours, usersList]
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

        <span className="text-[19px] font-bold text-gray-700">
          {totalHours} H{totalDailyHours > 0 && ` + ${totalDailyHours} H`}
        </span>
      </button>

      {/* Collapsible user list */}
      {open && (
        <div className="user_List_acitivity">
          <hr className="border-gray-200 mb-3" />
          <ul className="space-y-2">
            {usersList.map((u, i) => (
              <li
                key={`${u.name}-${i}`}
                className="flex items-center justify-between text-[17px]"
              >
                <span className="text-[19px] font-medium text-gray-900">
                  {u.name}
                </span>
                <span className="text-[19px] font-medium text-gray-900">
                  {u.hours} H{u.daily_hours > 0 && ` + ${u.daily_hours} H`}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
