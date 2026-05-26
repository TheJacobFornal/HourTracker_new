import React from "react";
import "./Project_Style.css";

export default function Project_User_Sumarry({ data = [] }) {
  if (!data.length) return <p className="no-user">No user found.</p>;

  return (
    <div className="user-summary-container">
      <table className="user-summary-table">
        <thead>
          <tr>
            <th className="user-summary-header user-summary-header1">Osoba</th>
            <th className="user-summary-header">Godz. Archiwum</th>
            <th className="user-summary-header">Aktualny mies.</th>
          </tr>
        </thead>
        <tbody>
          {data.map((user, index) => (
            <tr key={index} className="user-summary-row">
              <td className="user-summary-cell name-cell">
                {user.Name_Surname}
              </td>
              <td className="user-summary-cell">{user.Logs_Hours} H</td>
              <td className="user-summary-cell">
                {user.Daily_Hours > 0 ? `${user.Daily_Hours} H` : "0 H"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
