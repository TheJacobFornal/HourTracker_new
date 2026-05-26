import React, { useState, useEffect } from "react";
import { API_ENDPOINTS } from "../../config/api";
import confetti from "canvas-confetti";
import SkolimImg from "../../assets/skolim.png";

const THEMES = {
  light: {
    bg: "#f9f9fb",
    title: "#0f172a",
    subtitle: "#007aff",
    label: "#6b7280",
    selectBg: "#f9f9fb",
    selectBorder: "#e5e5ea",
    selectColor: "#222",
    selectOption: "#fff",
    divider: "#e5e5ea",
    activityChecked: "#9FA0A0",
    activityUnchecked: "#222",
    toggleText: "🌸 Pink",
    btnBg: "linear-gradient(135deg, #007aff, #0056d6)",
    btnColor: "#fff",
    btnDisabled: "#e5e5ea",
    btnDisabledColor: "#b0b0b0",
  },
  pink: {
    bg: "linear-gradient(160deg, #ff6eb4 0%, #ff1f8e 35%, #c2006b 70%, #7a003f 100%)",
    title: "#fff",
    subtitle: "rgba(255,255,255,0.8)",
    label: "rgba(255,255,255,0.75)",
    selectBg: "rgba(255,255,255,0.15)",
    selectBorder: "rgba(255,255,255,0.3)",
    selectColor: "#fff",
    selectOption: "#c2006b",
    divider: "rgba(255,255,255,0.2)",
    activityChecked: "#FFD9F8",
    activityUnchecked: "#fff",
    toggleText: "💙 Light",
    btnBg: "linear-gradient(135deg, #fff 0%, #ffd6ec 100%)",
    btnColor: "#c2006b",
    btnDisabled: "rgba(255,255,255,0.1)",
    btnDisabledColor: "rgba(255,255,255,0.3)",
  },
};

function fireConfetti(theme = "pink") {
  const duration = 3000;
  const end = Date.now() + duration;
  const colors = theme === "light"
    ? ["#007aff", "#0056d6", "#60a5fa", "#fff", "#e0f0ff"]
    : ["#ff2d78", "#ff6eb4", "#fff", "#ffd6ec", "#c2006b"];

  (function frame() {
    confetti({
      particleCount: 6,
      angle: 60,
      spread: 55,
      origin: { x: 0 },
      colors,
    });
    confetti({
      particleCount: 6,
      angle: 120,
      spread: 55,
      origin: { x: 1 },
      colors,
    });
    if (Date.now() < end) requestAnimationFrame(frame);
  })();
}

async function downloadExcel(month, year, activityIds) {
  const res = await fetch(API_ENDPOINTS.zestawienieExport, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ month, year, activity_ids: activityIds }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Zestawienie_${year}-${String(month).padStart(2, "0")}.xlsx`;
  a.click();
  URL.revokeObjectURL(url);
}

const MONTHS = [
  "Styczeń","Luty","Marzec","Kwiecień","Maj","Czerwiec",
  "Lipiec","Sierpień","Wrzesień","Październik","Listopad","Grudzień",
];
const currentYear = new Date().getFullYear();
const YEARS = Array.from({ length: 10 }, (_, i) => currentYear - i);

const makeLabelStyle = (t) => ({
  fontSize: "12px",
  fontWeight: "700",
  letterSpacing: "3px",
  textTransform: "uppercase",
  color: t.label,
  display: "block",
  marginBottom: "8px",
});

const makeSelectStyle = (t) => ({
  background: t.selectBg,
  border: `1px solid ${t.selectBorder}`,
  borderRadius: "10px",
  color: t.selectColor,
  padding: "11px 16px",
  fontSize: "16px",
  fontWeight: "600",
  outline: "none",
  cursor: "pointer",
  width: "100%",
  transition: "all 0.3s ease",
});

export default function Zestawienie() {
  const [month, setMonth] = useState(null);
  const [year, setYear] = useState(currentYear);
  const [activities, setActivities] = useState([]);
  const [checked, setChecked] = useState({});
  const [loading, setLoading] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [celebrate, setCelebrate] = useState(false);
  const [skolimHiding, setSkolimHiding] = useState(false);
  const [themeName, setThemeName] = useState("light");
  const t = THEMES[themeName];

  useEffect(() => {
    if (!month) { setActivities([]); return; }
    const ac = new AbortController();
    setLoading(true);
    fetch(API_ENDPOINTS.activitiesByMonth, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ month, year }),
      signal: ac.signal,
    })
      .then((r) => r.json())
      .then((data) => {
        const list = data.activities ?? [];
        setActivities(list);
        setChecked(Object.fromEntries(list.map((a) => [a.id, false])));
      })
      .catch((e) => { if (e.name !== "AbortError") console.error(e); })
      .finally(() => setLoading(false));
    return () => ac.abort();
  }, [month, year]);

  const hasActivities = activities.length > 0 && !loading;
  const allChecked = activities.length > 0 && activities.every((a) => checked[a.id]);
  const toggleAll = (val) => setChecked(Object.fromEntries(activities.map((a) => [a.id, val])));
  const toggle = (id) => setChecked((p) => ({ ...p, [id]: !p[id] }));
  const selectedIds = activities.filter((a) => checked[a.id]).map((a) => a.id);
  const canExport = selectedIds.length > 0 && !exporting;

  const handleExport = async () => {
    if (!canExport) return;
    setExporting(true);
    try {
      await downloadExcel(month, year, selectedIds);
      fireConfetti(themeName);
      setCelebrate(true);
      setSkolimHiding(false);
      setTimeout(() => setSkolimHiding(true), 4400);
      setTimeout(() => { setCelebrate(false); setSkolimHiding(false); }, 5000);
    }
    catch (e) { console.error(e); }
    finally { setExporting(false); }
  };

  // -30px compensates for the 60px sidebar to hit true screen center.
  // When activities are shown, shift content an additional 80px left.
  const monthChosen = month !== null;
  const screenCenter = "translateX(-30px)";
  const contentShift = hasActivities ? "translateX(-110px)" : "translateX(-30px)";

  return (
    <div style={{
      minHeight: "100vh",
      background: t.bg,
      transition: "background 0.5s ease",
      fontFamily: "'Segoe UI', sans-serif",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      padding: "48px 24px",
    }}>

      {/* Title — always screen-centered */}
      <div style={{ transform: screenCenter, textAlign: "center", marginBottom: "40px", width: "100%" }}>
        <p style={{
          margin: "0 0 6px 0",
          fontSize: "13px",
          letterSpacing: "4px",
          textTransform: "uppercase",
          color: "rgba(255,255,255,0.65)",
          fontWeight: "600",
        }}>
          Raport miesięczny
        </p>
        <h1 style={{
          fontSize: "42px",
          fontWeight: "900",
          textTransform: "uppercase",
          letterSpacing: "4px",
          color: t.title,
          textShadow: themeName === "light" ? "none" : "0 0 20px rgba(255,255,255,0.4)",
          margin: "0 0 6px 0",
          lineHeight: 1.15,
        }}>
          Generator
        </h1>
        <h2 style={{
          fontSize: "18px",
          fontWeight: "400",
          letterSpacing: "6px",
          textTransform: "uppercase",
          color: t.subtitle,
          margin: "0 0 14px 0",
          fontStyle: "italic",
        }}>
          zestawienia aktywności
        </h2>
        <div style={{
          height: "2px", width: "60px",
          background: "linear-gradient(90deg, rgba(255,255,255,0.7), transparent)",
          borderRadius: "2px", margin: "0 auto",
        }} />
      </div>

      {/* Content — centered when no activities, slightly left when loaded */}
      <div style={{
        transform: !monthChosen ? screenCenter : contentShift,
        transition: "transform 0.4s ease",
        display: "flex",
        gap: "60px",
        alignItems: "flex-start",
        maxWidth: "900px",
        width: "100%",
        justifyContent: !monthChosen ? "center" : "flex-start",
      }}>

        {/* LEFT — selectors */}
        <div style={{ flex: "0 0 200px" }}>
          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            <div>
              <label style={makeLabelStyle(t)}>Miesiąc</label>
              <select
                value={month ?? ""}
                onChange={(e) => setMonth(e.target.value ? Number(e.target.value) : null)}
                style={makeSelectStyle(t)}
              >
                <option value="" disabled style={{ background: t.selectOption }}>-- Wybierz miesiąc --</option>
                {MONTHS.map((n, i) => (
                  <option key={i + 1} value={i + 1} style={{ background: t.selectOption }}>{n}</option>
                ))}
              </select>
            </div>
            <div>
              <label style={makeLabelStyle(t)}>Rok</label>
              <select value={year} onChange={(e) => setYear(Number(e.target.value))} style={makeSelectStyle(t)}>
                {YEARS.map((y) => (
                  <option key={y} value={y} style={{ background: t.selectOption }}>{y}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Divider — only when activities present */}
        {hasActivities && (
          <div style={{ width: "1px", alignSelf: "stretch", background: t.divider, flexShrink: 0 }} />
        )}

        {/* RIGHT — activities */}
        {hasActivities && (
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
              <span style={makeLabelStyle(t)}>Wszystkie aktywności</span>
              <button onClick={() => toggleAll(!allChecked)} style={{
                background: "none", border: "none",
                color: "rgba(255,255,255,0.6)", fontSize: "11px",
                fontWeight: "600", cursor: "pointer", padding: 0,
                textDecoration: "underline", textUnderlineOffset: "3px",
                fontSize: "13px",
              }}>
                {allChecked ? "Odznacz wszystkie" : "Zaznacz wszystkie"}
              </button>
            </div>
            {(() => {
              const mid = Math.ceil(activities.length / 2);
              const left = activities.slice(0, mid);
              const right = activities.slice(mid);
              const renderItem = (a) => (
                <label key={a.id} style={{ display: "flex", alignItems: "center", gap: "10px", cursor: "pointer", marginBottom: "11px" }}>
                  <input
                    type="checkbox"
                    checked={!!checked[a.id]}
                    onChange={() => toggle(a.id)}
                    style={{ accentColor: "#fff", width: "16px", height: "16px", flexShrink: 0 }}
                  />
                  <span style={{
                    color: checked[a.id] ? t.activityChecked : t.activityUnchecked,
                    fontSize: "15px", fontWeight: "500",
                    transition: "color 0.2s",
                    whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis",
                  }}>
                    {a.name}
                  </span>
                </label>
              );
              return (
                <div style={{ display: "flex", gap: "28px" }}>
                  <div style={{ flex: 1 }}>{left.map(renderItem)}</div>
                  <div style={{ flex: 1 }}>{right.map(renderItem)}</div>
                </div>
              );
            })()}
          </div>
        )}

        {/* Loading / empty state — only show when month is chosen */}
        {!hasActivities && monthChosen && (
          <div style={{ display: "flex", alignItems: "center" }}>
            <p style={{ color: t.label, fontSize: "15px", fontStyle: "italic", margin: 0 }}>
              {loading ? "Ładowanie..." : "Brak aktywności w tym okresie."}
            </p>
          </div>
        )}
      </div>

      {/* Button — always screen-centered */}
      <div style={{ transform: screenCenter, marginTop: "48px" }}>
        <button
          onClick={handleExport}
          disabled={!canExport}
          style={{
            padding: "14px 56px",
            background: canExport ? t.btnBg : t.btnDisabled,
            border: "none",
            borderRadius: "50px",
            color: canExport ? t.btnColor : t.btnDisabledColor,
            fontSize: "15px",
            fontWeight: "800",
            letterSpacing: "3px",
            textTransform: "uppercase",
            cursor: canExport ? "pointer" : "not-allowed",
            boxShadow: canExport ? "0 8px 30px rgba(255,100,150,0.4)" : "none",
            transition: "all 0.3s",
          }}
        >
          {exporting ? "Generowanie..." : "Wygeneruj Excel"}
        </button>
      </div>

      {/* Theme toggle button */}
      <button
        onClick={() => setThemeName(n => n === "light" ? "pink" : "light")}
        style={{
          position: "fixed",
          bottom: "24px",
          right: "24px",
          padding: "8px 14px",
          borderRadius: "50px",
          border: "1px solid rgba(255,255,255,0.25)",
          background: themeName === "light" ? "#fff" : "rgba(0,0,0,0.25)",
          backdropFilter: "blur(10px)",
          boxShadow: themeName === "light" ? "0 1px 4px rgba(0,0,0,0.1)" : "none",
          color: themeName === "light" ? "#374151" : "#fff",
          border: themeName === "light" ? "1px solid #e5e5ea" : "1px solid rgba(255,255,255,0.25)",
          fontSize: "12px",
          fontWeight: "600",
          cursor: "pointer",
          zIndex: 1000,
          letterSpacing: "1px",
          transition: "all 0.2s ease",
        }}
      >
        {t.toggleText}
      </button>

      {celebrate && themeName === "pink" && (
        <div style={{
          position: "fixed",
          bottom: 0,
          left: 0,
          zIndex: 9999,
          pointerEvents: "none",
          animation: skolimHiding
            ? "skolimSlideOut 0.6s cubic-bezier(0.4,0,1,1) forwards"
            : "skolimSlideIn 0.7s cubic-bezier(0,0,0.2,1) forwards",
        }}>
          <img
            src={SkolimImg}
            alt="Skolim"
            style={{ height: "420px", display: "block" }}
          />
        </div>
      )}

      <style>{`
        @keyframes skolimSlideIn {
          from { transform: translateX(-120%) translateY(40px); opacity: 0; }
          to   { transform: translateX(0)     translateY(0);    opacity: 1; }
        }
        @keyframes skolimSlideOut {
          from { transform: translateX(0)     translateY(0);    opacity: 1; }
          to   { transform: translateX(-120%) translateY(40px); opacity: 0; }
        }
      `}</style>

    </div>
  );
}
