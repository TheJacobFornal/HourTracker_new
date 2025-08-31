import React from "react";
import ActivityItem from "./ActivityItem";

export default function ActivitiesList({ data = [] }) {
  if (!data.length) return <p>No activities found.</p>;

  return (
    <div className="flex flex-col gap-3">
      {data.map((row, idx) => (
        <ActivityItem
          key={`${row.activity}-${idx}`}
          activity={row.activity}
          hours={row.hours}
          users={row.users}
        />
      ))}
    </div>
  );
}
