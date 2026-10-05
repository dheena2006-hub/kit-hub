import React, { useEffect, useState } from "react";

const api = async (path, opts = {}) => {
  const t = localStorage.getItem("token");
  const res = await fetch("/api" + path, { ...opts,
    headers: { "Content-Type": "application/json", ...(t && { Authorization: "Bearer " + t }) },
    body: opts.body && JSON.stringify(opts.body) });
  if (opts.raw) return res;
  const data = res.status === 204 ? null : await res.json();
  if (!res.ok) throw new Error(data?.error || data?.detail || "Request failed");
  return data;
};
const useForm = (init) => { const [f, s] = useState(init); return [f, (k) => (e) => s({ ...f, [k]: e.target.value }), s]; };

function Auth({ onLogin }) {
  const [mode, setMode] = useState("login"); const [msg, setMsg] = useState(""); const [err, setErr] = useState("");
  const [f, set] = useForm({ name: "", email: "", password: "", roll_no: "", department: "", class_name: "", blood_group: "O+", phone: "", linkedin: "", portfolio: "" });
  const submit = async () => { setErr(""); setMsg("");
    try {
      if (mode === "login") { const d = await api("/login/", { method: "POST", body: { email: f.email, password: f.password } });
        localStorage.setItem("token", d.token); onLogin(d.user); }
      else { const d = await api("/register/", { method: "POST", body: f }); setMsg(d.message); setMode("login"); }
    } catch (e) { setErr(e.message); } };
  const fields = mode === "login" ? ["email", "password"] : Object.keys(f).filter((k) => k !== "blood_group");
  return <div className="wrap"><div className="card"><h2>KIT Hub — {mode === "login" ? "Login" : "Register"}</h2>
    {fields.map((k) => <input key={k} placeholder={k === "linkedin" ? "LinkedIn URL (required)" : k === "portfolio" ? "Portfolio URL (optional)" : k.replace("_", " ")} type={k === "password" ? "password" : "text"} value={f[k]} onChange={set(k)} />)}
    {mode === "register" && <select value={f.blood_group} onChange={set("blood_group")}>{["A+","A-","B+","B-","AB+","AB-","O+","O-"].map((b) => <option key={b}>{b}</option>)}</select>}
    <p className="err">{err}</p><p className="ok">{msg}</p>
    <button onClick={submit}>{mode === "login" ? "Login" : "Register"}</button>
    <button className="sec" onClick={() => setMode(mode === "login" ? "register" : "login")}>{mode === "login" ? "New student? Register" : "Back to login"}</button>
  </div></div>;
}

function Admin() {
  const [list, setList] = useState([]); const [st, setSt] = useState("pending");
  const load = () => api("/admin/users/?status=" + st).then(setList);
  useEffect(() => { load(); }, [st]);
  const act = (id, action) => api(`/admin/users/${id}/`, { method: "POST", body: { action } }).then(load);
  const del = (id) => confirm("Delete user?") && api(`/admin/users/${id}/`, { method: "DELETE" }).then(load);
  return <div><select value={st} onChange={(e) => setSt(e.target.value)}>{["pending","approved","rejected"].map((s) => <option key={s}>{s}</option>)}</select>
    {list.filter((u) => u.role === "student").map((u) => <div className="card" key={u.id}><b>{u.name}</b> · {u.roll_no} · {u.department}/{u.class_name} · {u.email}<br /><a href={u.linkedin} target="_blank" rel="noreferrer">LinkedIn</a>{u.portfolio && <> · <a href={u.portfolio} target="_blank" rel="noreferrer">Portfolio</a></>}<br />
      {st !== "approved" && <button onClick={() => act(u.id, "approve")}>Approve</button>}
      {st !== "rejected" && <button className="sec" onClick={() => act(u.id, "reject")}>Reject</button>}
      <button className="bad" onClick={() => del(u.id)}>Delete</button></div>)}
    {!list.length && <p>No {st} users.</p>}</div>;
}

function Announcements({ user }) {
  const [list, setList] = useState([]); const [f, set, setAll] = useForm({ title: "", description: "" });
  const load = () => api("/announcements/").then(setList); useEffect(() => { load(); }, []);
  const post = () => api("/announcements/", { method: "POST", body: f }).then(() => { setAll({ title: "", description: "" }); load(); });
  return <div>{user.role === "admin" && <div className="card"><input placeholder="Title" value={f.title} onChange={set("title")} />
    <textarea placeholder="Description" value={f.description} onChange={set("description")} /><button onClick={post}>Post</button></div>}
    {list.map((a) => <div className="card" key={a.id}><b>{a.title}</b><p>{a.description}</p><small>{a.author} · {new Date(a.created_at).toLocaleString()}</small></div>)}</div>;
}

function Chat() {
  const [contacts, setContacts] = useState([]); const [to, setTo] = useState(""); const [msgs, setMsgs] = useState([]); const [text, setText] = useState("");
  useEffect(() => { api("/contacts/").then(setContacts); }, []);
  const load = () => to && api("/messages/?with=" + to).then(setMsgs);
  useEffect(() => { load(); const i = setInterval(load, 4000); return () => clearInterval(i); }, [to]);
  const send = () => text && api("/messages/", { method: "POST", body: { to, content: text } }).then(() => { setText(""); load(); });
  return <div><select value={to} onChange={(e) => setTo(e.target.value)}><option value="">Select contact</option>{contacts.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}</select>
    {msgs.map((m) => <div key={m.id} className="card">{m.content}</div>)}
    {to && <><input value={text} onChange={(e) => setText(e.target.value)} placeholder="Message" /><button onClick={send}>Send</button></>}</div>;
}

function Blood() {
  const [g, setG] = useState(""); const [list, setList] = useState([]);
  useEffect(() => { api("/blood/?group=" + encodeURIComponent(g)).then(setList); }, [g]);
  return <div><select value={g} onChange={(e) => setG(e.target.value)}><option value="">All groups</option>{["A+","A-","B+","B-","AB+","AB-","O+","O-"].map((b) => <option key={b}>{b}</option>)}</select>
    {list.map((u, i) => <div className="card" key={i}><b>{u.name}</b> · {u.blood_group} · {u.department} · {u.phone}</div>)}</div>;
}

function Staff() {
  const [list, setList] = useState([]); useEffect(() => { api("/staff/").then(setList); }, []);
  return <div>{list.map((s) => <div className="card" key={s.id}><b>{s.name}</b> · {s.designation} · {s.department}</div>)}</div>;
}

function Profile({ user, setUser }) {
  const [f, setF] = useState({ linkedin: user.linkedin || "", portfolio: user.portfolio || "", phone: user.phone || "" }); const [msg, setMsg] = useState("");
  const save = async () => { setMsg(""); try { setUser(await api("/me/", { method: "PATCH", body: f })); setMsg("Saved"); } catch (e) { setMsg(e.message); } };
  const dl = async (fmt) => { const res = await api("/me/export/?format=" + fmt, { raw: true }); const url = URL.createObjectURL(await res.blob());
    Object.assign(document.createElement("a"), { href: url, download: "my_data." + fmt }).click(); };
  return <div className="card"><h3>{user.name}</h3><p>{user.email} · {user.role}</p>
    {user.role === "student" && <><input placeholder="LinkedIn URL (required)" value={f.linkedin} onChange={(e) => setF({ ...f, linkedin: e.target.value })} />
    <input placeholder="Portfolio URL (optional)" value={f.portfolio} onChange={(e) => setF({ ...f, portfolio: e.target.value })} />
    <input placeholder="Phone" value={f.phone} onChange={(e) => setF({ ...f, phone: e.target.value })} />
    <button onClick={save}>Save profile</button> <small>{msg}</small></>}
    <p>Download my data:</p>{["pdf", "json", "csv"].map((fm) => <button key={fm} onClick={() => dl(fm)}>{fm.toUpperCase()}</button>)}</div>;
}

export default function App() {
  const [user, setUser] = useState(null); const [tab, setTab] = useState("announcements"); const [ready, setReady] = useState(false);
  useEffect(() => { // persistent session until manual logout
    if (localStorage.getItem("token")) api("/me/").then(setUser).catch(() => localStorage.removeItem("token")).finally(() => setReady(true)); else setReady(true); }, []);
  if (!ready) return null;
  if (!user) return <Auth onLogin={setUser} />;
  const tabs = { announcements: <Announcements user={user} />, messages: <Chat />, blood: <Blood />, staff: <Staff />, profile: <Profile user={user} setUser={setUser} />,
    ...(user.role === "admin" && { admin: <Admin /> }) };
  return <div className="wrap"><nav>{Object.keys(tabs).map((t) => <button key={t} className={t === tab ? "" : "sec"} onClick={() => setTab(t)}>{t}</button>)}
    <button className="bad" onClick={() => { localStorage.removeItem("token"); setUser(null); }}>Logout</button></nav>{tabs[tab]}</div>;
}
